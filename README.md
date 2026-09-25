# AI Research Agent

A multi-purpose AI agent built **from scratch in Python**, using the **ReAct
(Reason + Act) pattern** — the same core idea behind tools like LangChain
agents and AutoGPT. No agent framework is used; the reasoning loop, tool
routing, and prompt design are all hand-written, so every part of how it
works is transparent and easy to explain in an interview.

The agent can hold a conversation and decide, on its own, when it needs to:
- **search the live web** for current information,
- **look up a topic on Wikipedia** for a reliable summary,
- **do math** safely and accurately, or
- **save a note** to disk for later.

## Why this project

Most "AI agent" tutorials just glue together a framework. This one builds
the agent loop itself, which demonstrates:
- Understanding of **LLM prompting and reasoning patterns** (ReAct), not
  just calling an API.
- **Tool-use / function-calling design** — a clean `Tool` interface any
  new capability can plug into.
- **Provider-agnostic API integration** (works with OpenAI or any
  OpenAI-compatible endpoint such as Groq or Together AI).
- Basic **software engineering practice**: modular structure, tests,
  environment-based config, and documentation.

## How it works

```
User question
     │
     ▼
┌─────────────────────────────┐
│  Agent (ReAct loop)         │
│  Thought → Action → ...     │◄──── Observation (tool result)
└─────────────────────────────┘
     │        │
     │        ▼
     │   ┌─────────────┐
     │   │   Tools      │  web_search · wikipedia · calculator · save_note
     │   └─────────────┘
     ▼
Final Answer
```

On each turn, the language model outputs a `Thought`, then either an
`Action` (a tool name) + `Action Input`, or a `Final Answer`. If it picked
a tool, the agent runs it and feeds the result back in as an `Observation`,
and the loop continues until the model is confident enough to answer.

## Project structure

```
AI-research-agent/
├── agent/
│   ├── core.py           # the ReAct loop (the "brain")
│   ├── llm.py             # provider-agnostic LLM API wrapper
│   └── tools/
│       ├── base.py        # Tool interface every tool implements
│       ├── web_search.py  # DuckDuckGo web search (no API key needed)
│       ├── wikipedia_tool.py
│       ├── calculator.py  # safe AST-based expression evaluator
│       └── file_tool.py   # saves notes to notes.txt
├── tests/
│   └── test_tools.py
├── main.py                 # command-line chat interface
├── requirements.txt
├── .env.example
└── README.md
```

## Setup

1. **Clone and enter the project**
   ```bash
   git clone https://github.com/noob-shahriar/AI-research-agent.git
   cd AI-research-agent
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your API key**
   ```bash
   cp .env.example .env
   ```
   Then open `.env` and set `API_KEY`. You have two easy options if you
   don't already have an OpenAI key:
   - **OpenAI**: keep `BASE_URL=https://api.openai.com/v1`, use a key from
     https://platform.openai.com
   - **Groq (free tier available)**: set
     `BASE_URL=https://api.groq.com/openai/v1` and
     `MODEL=llama-3.1-70b-versatile`, use a key from https://console.groq.com

5. **Run it**
   ```bash
   python main.py
   ```

## Example session

```
You: What's 234 * 18, and who invented the transformer architecture in deep learning?

Agent: 234 * 18 = 4212. The Transformer architecture was introduced in the
2017 paper "Attention Is All You Need" by Vaswani et al. at Google.
```

Behind the scenes the agent called `calculator` for the first part and
`wikipedia` (falling back to `web_search` if needed) for the second —
automatically, without being told which tool to use.

## Running tests

```bash
pytest
```

## Extending it

Adding a new capability is just a new `Tool` subclass:

```python
from agent.tools.base import Tool

class MyTool(Tool):
    name = "my_tool"
    description = "Explain clearly what this does and what input it expects."

    def run(self, tool_input: str) -> str:
        return "result"
```

Register it in `main.py`'s tool list and the agent can start using it —
no other code changes needed. Ideas to extend this project further:
- A tool that reads/summarizes a PDF or webpage
- A short-term memory / vector-search tool for long conversations
- A simple web UI (Streamlit or Flask) on top of the same `Agent` class
- Swapping the hand-written ReAct loop for native function-calling
  (OpenAI's `tools` parameter) as a v2

## License

MIT — see [LICENSE](LICENSE).
