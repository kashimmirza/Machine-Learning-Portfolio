from typing import TypedDict, Annotated, Sequence, Literal
from langchain_core.messages import BaseMessage, FunctionMessage, ToolMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor, ToolInvocation
from langchain_core.utils.function_calling import convert_to_openai_function
from langgraph.graph.message import add_messages

from app.services.llm import llm_service
from app.core.agent.tools import tools

# Define the Agent State
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

# Create the tool executor
tool_executor = ToolExecutor(tools)

# Bind tools to the LLM
model = llm_service.get_llm().bind_tools(tools)

# Define the nodes
def call_model(state: AgentState):
    messages = state['messages']
    response = model.invoke(messages)
    return {"messages": [response]}

def call_tool(state: AgentState):
    messages = state['messages']
    last_message = messages[-1]
    
    # We construct an ToolInvocation for each tool call
    tool_calls = last_message.tool_calls
    
    results = []
    for tool_call in tool_calls:
        action = ToolInvocation(
            tool=tool_call["name"],
            tool_input=tool_call["args"],
        )
        # Execute the tool
        response = tool_executor.invoke(action)
        
        # Create a ToolMessage
        tool_message = ToolMessage(
            tool_call_id=tool_call["id"],
            content=str(response),
            name=tool_call["name"]
        )
        results.append(tool_message)
        
    return {"messages": results}

# Define the edge logic
def should_continue(state: AgentState) -> Literal["continue", "end"]:
    messages = state['messages']
    last_message = messages[-1]
    # If there is a function call, then we continue
    if last_message.tool_calls:
        return "continue"
    # Otherwise we end
    return "end"

# Build the graph
workflow = StateGraph(AgentState)

workflow.add_node("agent", call_model)
workflow.add_node("action", call_tool)

workflow.set_entry_point("agent")

workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "action",
        "end": END
    }
)

workflow.add_edge("action", "agent")

app_graph = workflow.compile()
