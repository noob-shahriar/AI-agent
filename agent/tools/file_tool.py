from .base import Tool


class FileNoteTool(Tool):
    name = "save_note"
    description = (
        "Saves a piece of text to a local research notes file (notes.txt) for later "
        "review. Input should be the exact text you want saved."
    )

    def __init__(self, path: str = "notes.txt"):
        self.path = path

    def run(self, tool_input: str) -> str:
        try:
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(tool_input.strip() + "\n---\n")
            return f"Saved note to {self.path}."
        except Exception as e:
            return f"Failed to save note: {e}"
