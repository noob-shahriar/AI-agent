import requests

from .base import Tool


class WikipediaTool(Tool):
    name = "wikipedia"
    description = (
        "Looks up a short, reliable summary of a topic on Wikipedia. Input should be a "
        "topic or name, e.g. 'Alan Turing' or 'Transformer (deep learning)'."
    )

    def run(self, tool_input: str) -> str:
        topic = tool_input.strip()
        try:
            url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + requests.utils.quote(topic)
            resp = requests.get(url, timeout=8, headers={"User-Agent": "ai-research-agent/1.0"})
            if resp.status_code != 200:
                return f"No Wikipedia page found for '{topic}'."
            data = resp.json()
            extract = data.get("extract")
            return extract or f"No summary available for '{topic}'."
        except Exception as e:
            return f"Wikipedia lookup failed: {e}"
