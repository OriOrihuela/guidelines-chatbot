import os

import requests
from dotenv import load_dotenv
from requests import RequestException

load_dotenv()


class StoryblokClient:

    def __init__(self):
        self.api_token = os.getenv("STORYBLOK_API_TOKEN")
        self.base_url = "https://api.storyblok.com/v2/cdn"
        self.timeout = 30

        if not self.api_token:
            raise ValueError("Missing STORYBLOK_API_TOKEN in environment")

    def _request(self, endpoint: str, params: dict = None):
        if params is None:
            params = {}

        params["token"] = self.api_token
        params["version"] = "published"

        url = f"{self.base_url}/{endpoint}"

        try:
            res = requests.get(url, params=params, timeout=self.timeout)
            res.raise_for_status()
        except RequestException as exc:
            status = getattr(getattr(exc, "response", None), "status_code", None)
            return {"error": True, "status": status, "message": str(exc)}

        try:
            return res.json()
        except ValueError:
            return {
                "error": True,
                "status": res.status_code,
                "message": "Invalid JSON response from Storyblok",
                "body": res.text,
            }

    def get_story(self, slug: str):
        return self._request(f"stories/{slug}")

    def list_stories(self, starts_with: str = None):
        params = {}
        if starts_with:
            params["starts_with"] = starts_with
        return self._request("stories", params)

    def search_stories(self, term: str):
        params = {"search_term": term}
        return self._request("stories", params)

    def filter_by_field(self, field: str, value: str):
        params = {f"filter_query[{field}][in]": value}
        return self._request("stories", params)

    def get_links(self):
        return self._request("links")

    def get_tags(self):
        return self._request("tags")

    def extract_text(self, story_json: dict):
        def traverse(node):
            if isinstance(node, dict):
                text = node.get("text", "")

                for key, val in node.items():
                    if isinstance(val, (dict, list)):
                        text += " " + traverse(val)

                return text

            elif isinstance(node, list):
                return " ".join(traverse(item) for item in node)

            return ""

        content = story_json.get("story", {}).get("content", {})
        return traverse(content)
