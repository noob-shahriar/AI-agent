from dotenv import load_dotenv

from agent.core import Agent
from agent.llm import LLM
from agent.tools import CalculatorTool, WebSearchTool, WikipediaTool, FileNoteTool


def build_agent() -> Agent:
    load_dotenv()
    llm = LLM()
    tools = [WebSearchTool(), WikipediaTool(), CalculatorTool(), FileNoteTool()]
    return Agent(tools=tools, llm=llm, verbose=False)


def main():
    print("AI Research Agent — multi-purpose CLI agent. Type 'exit' to quit.\n")
    agent = build_agent()

    while True:
        try:
            question = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break
        if not question:
            continue

        answer = agent.run(question)
        print(f"\nAgent: {answer}\n")


if __name__ == "__main__":
    main()
