from .base import Tool


class WebSearchTool(Tool):
    name = "web_search"
    description = (
        "Searches the live web for current information and returns a handful of short "
        "results (title, snippet, link). Input should be a search query, e.g. "
        "'latest release of Python'. Use this for anything recent or fact-based that you "
        "are not fully sure about."
    )

    def __init__(self, max_results: int = 4):
        self.max_results = max_results

    def run(self, tool_input: str) -> str:
        try:
            from ddgs import DDGS
        except ImportError:
            return (
                "web_search is unavailable: run 'pip install ddgs' first."
            )
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(tool_input, max_results=self.max_results))
            if not results:
                return "No results found."
            lines = []
            for r in results:
                title = r.get("title", "").strip()
                body = r.get("body", "").strip()
                href = r.get("href", "").strip()
                lines.append(f"- {title}: {body} ({href})")
            return "\n".join(lines)
        except Exception as e:
            return f"Search failed: {e}"
