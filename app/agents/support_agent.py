from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_aws import ChatBedrock
from app.core.config import get_settings
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
from app.core.logging import get_logger
from app.tools.order_tools import ALL_TOOLS

logger = get_logger(__name__)

settings = get_settings()

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    session_id: str
    customer_id: str

SYSTEM_PROMPT = """You are a helpful customer support agent for VoiceIQ.

Your job:
- Help customers with orders, refunds, and account questions
- Use the available tools to get real information
- Never make up order details or account information
- If you can't resolve something, transfer to a human agent

Rules:
1. Always use tools to get real information before answering
2. Transfer to human if customer is upset after 2 failed attempts
3. Be concise and friendly
"""

llm = ChatBedrock(
    model_id=settings.bedrock_model_id,
    region_name=settings.aws_region,
    model_kwargs={
        "max_tokens": 512,
        "temperature": 0.0,
    },
)

def agent_node(state: AgentState) -> AgentState:
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    llm_with_tools = llm.bind_tools(ALL_TOOLS)
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}
 

def create_agent():
    tool_node = ToolNode(ALL_TOOLS)

    graph = StateGraph(AgentState)

    graph.add_node("agent", agent_node)
    graph.add_node("tools", tool_node)

    graph.set_entry_point("agent")

    graph.add_conditional_edges("agent", tools_condition)
    graph.add_edge("tools", "agent")

    return graph.compile()

agent = create_agent()

async def process_message(message, session_id, customer_id=""):
    result = await agent.ainvoke({
        "messages": [HumanMessage(content=message)],
        "session_id": session_id,
        "customer_id": customer_id,
    })
    final_response = result["messages"][-1].content
    tools_used = []
    for msg in result["messages"]:
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            for tc in msg.tool_calls:
                tools_used.append(tc["name"])
    return {
        "response": final_response,
        "session_id": session_id,
        "tools_used": tools_used,
    }

