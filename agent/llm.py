import os

from openai import OpenAI


class LLM:
    """
    Thin wrapper around an OpenAI-compatible chat completions API.

    Works with OpenAI directly, or with any OpenAI-compatible provider
    (e.g. Groq, Together AI, OpenRouter) by pointing BASE_URL at it.
    This keeps the agent's reasoning code independent of which provider
    you're paying for.
    """

    def __init__(self, api_key: str = None, base_url: str = None, model: str = None):
        self.api_key = api_key or os.getenv("API_KEY")
        self.base_url = base_url or os.getenv("BASE_URL", "https://api.openai.com/v1")
        self.model = model or os.getenv("MODEL", "gpt-4o-mini")

        if not self.api_key:
            raise ValueError(
                "No API key found. Copy .env.example to .env and set API_KEY."
            )

        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def chat(self, messages, temperature: float = 0.2, stop=None) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            stop=stop,
        )
        return response.choices[0].message.content
