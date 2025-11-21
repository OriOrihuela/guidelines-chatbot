from ..clients.storyblok import StoryblokClient

client = StoryblokClient()


def get_story(slug: str):
    data = client.get_story(slug)
    return data


def list_stories(prefix: str = None):
    data = client.list_stories(starts_with=prefix)
    return data


def search_stories(term: str):
    data = client.search_stories(term)
    return data


def filter_stories(field: str, value: str):
    data = client.filter_by_field(field, value)
    return data


def get_links():
    return client.get_links()


def get_tags():
    return client.get_tags()


def extract_story_text(slug: str):
    story = client.get_story(slug)
    if "story" not in story:
        return "Story not found"
    return client.extract_text(story)
