# agent_runner.py
from langchain.agents import initialize_agent
from langchain_openai import ChatOpenAI
from langchain.agents.agent_types import AgentType
from langchain.memory import ConversationBufferMemory
from tools.all_tools import (
    semantic_query_tool,
    summarize_tool,
    note_stat_tool,
    export_tool,
    keyword_filter_tool,
    company_summary_tool,
    fetch_all_records_tool,
)

llm = ChatOpenAI(temperature=0)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

tools = [
    # semantic_query_tool,
    # summarize_tool,
    # note_stat_tool,
    # export_tool,
    # keyword_filter_tool,
    # company_summary_tool,
    fetch_all_records_tool,
]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True,
    memory=memory,
)

def run_agent_query(query: str) -> str:
    return agent.run(query)
