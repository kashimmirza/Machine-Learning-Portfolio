import asyncio
from typing import AsyncGenerator, Optional
from urllib.parse import quote_plus
from psycopg_pool import AsyncConnectionPool

from langchain_core.messages import ToolMessage, convert_to_openai_messages
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.graph import END, StateGraph
from langgraph.graph.state import Command, CompiledStateGraph
from langgraph.types import RunnableConfig

from mem0 import AsyncMemory

from app.core.config import settings
from app.core.langgraph.tools import tools
from app.core.logging import logger
from app.core.prompts import load_system_prompt
from app.schemas.graph import GraphState
from app.schemas.chat import Message
from app.services.llm import llm_service
from app.utils.llm_utils import dump_messages, prepare_messages

class LangGraphAgent:
    def __init__(self):
        self.llm_service = llm_service.bind_tools(tools)
        self.tools_by_name = {tool.name: tool for tool in tools}
        
        self._connection_pool: Optional[AsyncConnectionPool] = None
        self._graph: Optional[CompiledStateGraph] = None
        self.memory: Optional[AsyncMemory] = None

    async def _long_term_memory(self) -> AsyncMemory:
        if self.memory is None:
            self.memory = await AsyncMemory.from_config(
                config_dict={
                    "vector_store": {
                        "provider": "pgvector",
                        "config": {
                            "collection_name": "agent_memory",
                            "dbname": settings.POSTGRES_DB,
                            "user": settings.POSTGRES_USER,
                            "password": settings.POSTGRES_PASSWORD,
                            "host": settings.POSTGRES_HOST,
                            "port": settings.POSTGRES_PORT,
                        },
                    },
                    "llm": {
                        "provider": "openai",
                        "config": {"model": settings.DEFAULT_LLM_MODEL},
                    },
                     "embedder": {
                        "provider": "openai", 
                        "config": {"model": "text-embedding-3-small"}
                    },
                }
            )
        return self.memory

    async def _get_connection_pool(self) -> AsyncConnectionPool:
        if self._connection_pool is None:
            connection_url = (
                "postgresql://"
                f"{quote_plus(settings.POSTGRES_USER)}:{quote_plus(settings.POSTGRES_PASSWORD)}"
                f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
            )
            self._connection_pool = AsyncConnectionPool(
                connection_url,
                open=False,
                max_size=settings.POSTGRES_POOL_SIZE,
                kwargs={"autocommit": True}
            )
            await self._connection_pool.open()
        return self._connection_pool

    async def _chat(self, state: GraphState, config: RunnableConfig) -> Command:
        try:
            SYSTEM_PROMPT = load_system_prompt(long_term_memory=state.long_term_memory)
            
            # prepare messages
            # Note: prepare_messages returns a list of Pydantic models (or dicts if adapted)
            # We need to make sure we are compatible with what llm_service expects
            
            # Using raw messages for now, relying on LangChain's ability to handle them
            # Ideally we adapt prepare_messages to return BaseMessages or dicts
            
            messages = [Message(role="system", content=SYSTEM_PROMPT)] + [
                 Message(role=m.type if hasattr(m, "type") else m.get("role", "user"), content=m.content if hasattr(m, "content") else(m.get("content", ""))) for m in state.messages
            ]
            
            # Convert to internal format for LLM service if needed, but llm_service uses langchain invoker
            # which expects BaseMessages or dicts.
            
            input_msgs = dump_messages(messages) # Convert to dicts
            
            response_message = await self.llm_service.call(input_msgs)
            
            if response_message.tool_calls:
                goto = "tool_call"
            else:
                goto = END
                
            return Command(update={"messages": [response_message]}, goto=goto)
            
        except Exception as e:
            logger.error(f"Error in chat node: {e}")
            raise

    async def _tool_call(self, state: GraphState) -> Command:
        outputs = []
        for tool_call in state.messages[-1].tool_calls:
            try:
                tool_result = await self.tools_by_name[tool_call["name"]].ainvoke(tool_call["args"])
                outputs.append(
                    ToolMessage(
                        content=str(tool_result),
                        name=tool_call["name"],
                        tool_call_id=tool_call["id"],
                    )
                )
            except Exception as e:
                logger.error(f"Tool execution failed: {e}")
                outputs.append(
                     ToolMessage(
                        content=f"Error executing tool: {e}",
                        name=tool_call["name"],
                        tool_call_id=tool_call["id"],
                    )
                )
        return Command(update={"messages": outputs}, goto="chat")

    async def create_graph(self) -> CompiledStateGraph:
         if self._graph is not None:
            return self._graph

         graph_builder = StateGraph(GraphState)
         graph_builder.add_node("chat", self._chat)
         graph_builder.add_node("tool_call", self._tool_call)
         
         graph_builder.set_entry_point("chat")
         
         connection_pool = await self._get_connection_pool()
         checkpointer = AsyncPostgresSaver(connection_pool)
         await checkpointer.setup()
         
         self._graph = graph_builder.compile(checkpointer=checkpointer)
         return self._graph

    async def get_response(self, messages: list[Message], session_id: str, user_id: str) -> list[dict]:
        if self._graph is None:
            await self.create_graph()
            
        memory_client = await self._long_term_memory()
        relevant_memory = await memory_client.search(user_id=user_id, query=messages[-1].content)
        memory_context = "\n".join([f"* {res['memory']}" for res in relevant_memory.get("results", [])])

        config = {"configurable": {"thread_id": session_id}}
        
        # Convert pydantic messages to list of BaseMessages or dicts for graph
        # StateGraph expects a "messages" key which is a list.
        # Our GraphState defines messages as annotated list.
        
        # We need to pass the INITIAL input. LangGraph will append.
        
        # For simplicity in this method, let's assume we pass all messages.
        # In a real app, we might only pass the new ones if the graph is maintaining history statefully.
        # But since we use persistent checkpointing, we only need to pass the NEW message(s).
        
        new_messages = dump_messages(messages) # PASS ALL? No, only new ones typically.
        # But for this MVP let's just pass the last user message if we assume state is preserved.
        # However, the user might be sending the whole history from frontend.
        # Let's assume frontend sends whole history, but we should only process the last one if the graph has state.
        # For SAFETY: Let's pass the whole history but let LangGraph dedupe via checkpointing if possible?
        # Actually, LangGraph's add_messages reducer handles appending. So if we pass whole history every time, it duplicates.
        # We should only pass the *new* messages.
        
        # Assuming `messages` contains the full conversation from frontend:
        # We should ideally find the diff. But simpler approach: Frontend sends only new message?
        # Let's assume frontend sends full history (common in stateless frontends).
        # We'll take the LAST message.
        
        input_state = {
            "messages": [dump_messages([messages[-1]])[0]], # Only the last one
            "long_term_memory": memory_context or "No relevant memory found."
        }
        
        final_state = await self._graph.ainvoke(input_state, config=config)
        
        # Background memory update
        await self._update_long_term_memory(user_id, final_state["messages"])
        
        return dump_messages(final_state["messages"]) # Return all messages or just new ones? Return all for now.

    async def _update_long_term_memory(self, user_id: str, messages: list) -> None:
        try:
            memory_client = await self._long_term_memory()
            await memory_client.add(messages, user_id=user_id)
        except Exception as e:
            logger.error(f"Memory update failed: {e}")

    async def get_stream_response(self, messages: list[Message], session_id: str, user_id: str):
        if self._graph is None:
            await self.create_graph()
            
        memory_client = await self._long_term_memory()
        relevant_memory = await memory_client.search(user_id=user_id, query=messages[-1].content)
        memory_context = "\n".join([f"* {res['memory']}" for res in relevant_memory.get("results", [])])

        config = {"configurable": {"thread_id": session_id}}
        input_state = {
             "messages": [dump_messages([messages[-1]])[0]], 
             "long_term_memory": memory_context or "No relevant memory found."
        }
        
        async for event in self._graph.astream_events(input_state, config=config, version="v1"):
             kind = event["event"]
             if kind == "on_chat_model_stream":
                 content = event["data"]["chunk"].content
                 if content:
                     yield content

