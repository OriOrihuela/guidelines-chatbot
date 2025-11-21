# Guidelines Chatbot

Guidelines Chatbot is a lightweight reference implementation that shows how to
wire up `google-adk` agents with a Storyblok content space. The repository is
structured as a reusable Python package (`storyblok_agent`) plus a tiny CLI
entry point (`main.py`) you can extend for your own workflows or demos.

---

## Requirements

- Python 3.11+ (managed through [`uv`](https://github.com/astral-sh/uv))
- A Storyblok space with a valid API access token
- Internet connectivity (the client performs live Storyblok HTTP requests)

---

## Project Structure

```
.
├── main.py                     # Simple CLI entry point
├── storyblok_agent/
│   ├── agent.py                # Root ADK agent definition
│   ├── tools/tools.py          # Tool wrappers that call Storyblok
│   └── clients/storyblok.py    # Thin Storyblok CDN client
├── pyproject.toml              # Tooling + dependency metadata
└── uv.lock                     # Resolved dependency versions
```

---

## Setup

1. **Clone & install**

   ```bash
   git clone https://github.com/OriOrihuela/guidelines-chatbot.git
   cd guidelines-chatbot
   uv sync
   ```

   `uv` will create `.venv/` and install both runtime and dev dependencies.

2. **Activate the environment**

   ```bash
   source .venv/bin/activate
   ```

3. **Provide Storyblok credentials**

   Add an `.env` file (or export environment variables another way) with
   your published-space token:

   ```
   STORYBLOK_API_TOKEN=your-token-here
   ```

   The client loads environment variables via `python-dotenv`.

4. **Configure `google-adk` defaults**

   The ADK looks for its runtime config in `~/.config/google-adk/config.toml`
   (or in the path pointed to by `GOOGLE_ADK_CONFIG`). Make sure that file
   exists and defines the Gemini model and credential settings you want to
   reuse—for example, pointing at `gemini-2.5-flash` so it matches
   `storyblok_agent.agent.root_agent`. See the
   [google-adk docs](https://google.github.io/adk-docs/) for the complete list
   of supported keys.

---

## Usage

### Run the demo CLI

```bash
uv run python main.py
```

At the moment the CLI prints a placeholder message. You can replace it with an
interactive loop that instantiates `root_agent` or triggers specific tools.

### Import the agent in your own code

```python
from storyblok_agent.agent import root_agent

response = root_agent.run("Summarize the landing page content")
print(response.text)
```

`root_agent` is an ADK `Agent` pre-wired with Storyblok-aware tools and a
Gemini 2.5 Flash model configuration.

---

## Storyblok Tool Reference

| Tool | Purpose | Typical Prompt |
| ---- | ------- | -------------- |
| `get_story(slug)` | Fetch a single story and all fields | "Open `/home` and summarize hero text." |
| `list_stories(prefix=None)` | List stories or folders | "List everything under `blog/`." |
| `search_stories(term)` | Full-text search across stories | "Find content mentioning `SEO`." |
| `filter_stories(field, value)` | Filter by component or metadata | "Show stories where `category` is `case-study`." |
| `get_links()` | Retrieve the Storyblok link tree | "What is the navigation hierarchy?" |
| `get_tags()` | List available tags | "Which tags do we use for editorial content?" |
| `extract_story_text(slug)` | Convert rich text blocks into plain text | "Give me the readable copy for `/about`." |

The tools are defined in `storyblok_agent/tools/tools.py` and rely on the
`StoryblokClient` in `storyblok_agent/clients/storyblok.py`. Each tool returns
raw JSON suitable for post-processing inside your agent instructions.

---

## Development Tips

- **Formatting & linting**: rely on the defaults provided by `uv` and the
  linters configured in `pyproject.toml`. Run `uv run ruff check` (if enabled)
  or `uv run pytest` to exercise any future tests you add.
- **Extending the CLI**: update `main.py` to parse arguments, launch a REPL,
  or expose FastAPI/Flask endpoints; everything is already import-safe.
- **Adding tools**: create new helper functions in `storyblok_agent/tools`
  (wrapping `StoryblokClient`) and register them with `FunctionTool` inside
  `storyblok_agent/agent.py`.
- **Regenerating locks**: when dependencies change, run `uv lock` to refresh
  `uv.lock` so collaborators reproduce the same environment.

---

## Troubleshooting

- _`ValueError: Missing STORYBLOK_API_TOKEN in environment`_: confirm your
  `.env` file exists or the variable is exported before running the app.
- _Unexpected HTTP responses_: the Storyblok CDN returns error payloads when
  tokens are invalid or slugs do not exist. Inspect the `error`, `status`,
  and `message` fields returned by the tools to diagnose.

Feel free to open issues or PRs if you build on top of this starter kit!
