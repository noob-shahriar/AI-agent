from abc import ABC, abstractmethod


class Tool(ABC):
    """
    Base class every tool must implement.

    name        -> short identifier the LLM uses to call this tool
    description -> tells the LLM what the tool does and how to use it
                    (this text is shown directly to the model, so make it clear)
    """

    name: str = "tool"
    description: str = "A base tool. Override this."

    @abstractmethod
    def run(self, tool_input: str) -> str:
        """Execute the tool on the given input and return a string result."""
        raise NotImplementedError
