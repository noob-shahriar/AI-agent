import streamlit as st
from dotenv import load_dotenv

from agent.core import Agent
from agent.llm import LLM
from agent.tools import CalculatorTool, WebSearchTool, WikipediaTool, FileNoteTool

load_dotenv()

st.set_page_config(page_title="AI Research Agent", page_icon="🤖", layout="centered")


@st.cache_resource
def get_agent() -> Agent:
    tools = [WebSearchTool(), WikipediaTool(), CalculatorTool(), FileNoteTool()]
    return Agent(tools=tools, llm=LLM(), verbose=False)


agent = get_agent()

# ---------- Sidebar ----------
with st.sidebar:
    st.header("🛠️ Tools")
    st.markdown(
        "- 🌐 **web_search** – live web results\n"
        "- 📚 **wikipedia** – topic summaries\n"
        "- 🧮 **calculator** – safe math\n"
        "- 📝 **save_note** – save to notes.txt"
    )
    st.divider()
    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.caption("Built with Python · ReAct agent · Streamlit")

# ---------- Header ----------
st.title("🤖 AI Research Agent")
st.caption("Ask me anything. I'll decide which tools to use and show my work.")

# ---------- Chat history ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("steps"):
            with st.expander("🔍 How I got this answer"):
                for tool, tool_input, obs in msg["steps"]:
                    st.markdown(f"**🛠️ {tool}** ← `{tool_input}`")
                    st.caption(obs[:500])

# ---------- New question ----------
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        steps = []
        status = st.status("Thinking...", expanded=True)

        def on_step(tool, tool_input, observation):
            steps.append((tool, tool_input, observation))
            status.write(f"🛠️ Using **{tool}** ← `{tool_input}`")

        try:
            answer = agent.run(
                prompt,
                on_step=on_step,
                history=st.session_state.messages[:-1],
            )
            status.update(label="Done", state="complete", expanded=False)
        except Exception as e:
            answer = f"Something went wrong: `{e}`"
            status.update(label="Error", state="error")

        st.markdown(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "steps": steps}
    )