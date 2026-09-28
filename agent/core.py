import re

from .llm import LLM

REACT_SYSTEM_PROMPT = """You are a helpful, careful multi-purpose AI research agent.
Prefer using tools to verify facts instead of guessing.

You have access to the following tools:
{tool_descriptions}

Use exactly this format:

Question: the question you must answer
Thought: reason about what to do next
Action: the tool to use, must be exactly one of [{tool_names}]
Action Input: the input to that tool
Observation: the result of the tool (you will not write this yourself)
... (this Thought/Action/Action Input/Observation cycle can repeat)
Thought: I now know the final answer
Final Answer: the final answer to the original question

Rules:
- Output only ONE Thought/Action/Action Input block, then stop and wait.
- Never invent an Observation yourself; it will be provided to you.
- If no tool is needed, skip straight to "Thought: I now know the final answer"
  followed by "Final Answer: ...".
"""

ACTION_RE = re.compile(r"Action:\s*(.+?)\nAction Input:\s*(.+)", re.IGNORECASE | re.DOTALL)
FINAL_RE = re.compile(r"Final Answer:\s*(.*)", re.IGNORECASE | re.DOTALL)


class Agent:
    def __init__(self, tools, llm: LLM = None, max_steps: int = 6, verbose: bool = True):
        self.tools = {t.name: t for t in tools}
        self.llm = llm or LLM()
        self.max_steps = max_steps
        self.verbose = verbose

    def _system_prompt(self) -> str:
        descriptions = "\n".join(f"- {t.name}: {t.description}" for t in self.tools.values())
        names = ", ".join(self.tools.keys())
        return REACT_SYSTEM_PROMPT.format(tool_descriptions=descriptions, tool_names=names)

    def run(self, question: str, on_step=None) -> str:
        messages = [
            {"role": "system", "content": self._system_prompt()},
            {"role": "user", "content": f"Question: {question}"},
        ]

        for step in range(self.max_steps):
            reply = self.llm.chat(messages)
            if self.verbose:
                print(f"\n--- Step {step + 1} ---\n{reply}")

            final_match = FINAL_RE.search(reply)
            action_match = ACTION_RE.search(reply)

            # If both patterns match, trust whichever comes first in the text.
            if final_match and (not action_match or final_match.start() < action_match.start()):
                return final_match.group(1).strip()

            if not action_match:
                messages.append({"role": "assistant", "content": reply})
                messages.append({
                    "role": "user",
                    "content": (
                        "Please follow the exact Thought/Action/Action Input format, "
                        "or give a Final Answer."
                    ),
                })
                continue

            tool_name = action_match.group(1).strip()
            tool_input = action_match.group(2).strip().split("\n")[0]
            tool = self.tools.get(tool_name)

            if tool is None:
                observation = f"Unknown tool '{tool_name}'. Available tools: {list(self.tools)}"
            else:
                observation = tool.run(tool_input)

            if self.verbose:
                print(f"Observation: {observation}")
            if self.verbose:
                print(f"Observation: {observation}")

            if on_step:
                on_step(tool_name, tool_input, observation)

            messages.append({"role": "assistant", "content": reply})
            messages.append({"role": "user", "content": f"Observation: {observation}"})

        return "I couldn't reach a final answer within the step limit. Try rephrasing your question."
