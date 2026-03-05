#!/usr/bin/env python3
"""
🤖 Aurora Health - Agentic RAG Orchestrator with MCP Integration
Intelligent information retrieval combining:
- Medical document RAG
- Hospital database search
- Real-time web search via MCP
- LLM-driven decision making
"""

import os
import json
import requests
from typing import List, Dict, Any, Optional
import openai
from openai import OpenAI

# Configuration
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
CHAT_MODEL = "gpt-4o-mini"  # or "gpt-3.5-turbo"
MCP_SERVER_URL = "http://localhost:8001/"

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)


class MCPAgent:
    """Agent to communicate with MCP server for Aurora Health"""
    
    def __init__(self, endpoint: str = MCP_SERVER_URL):
        self.endpoint = endpoint
        self.tools_cache = None
    
    def initialize(self) -> bool:
        """Initialize connection with MCP server"""
        try:
            request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize"
            }
            
            response = requests.post(self.endpoint, json=request)
            response.raise_for_status()
            data = response.json()
            
            print(f"[MCPAgent] Connected to: {data.get('result', {}).get('server')}")
            return True
            
        except Exception as e:
            print(f"[MCPAgent] Initialization failed: {e}")
            return False
    
    def list_tools(self) -> List[Dict]:
        """Get available tools from MCP server"""
        try:
            request = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "list_tools"
            }
            
            response = requests.post(self.endpoint, json=request)
            response.raise_for_status()
            data = response.json()
            
            self.tools_cache = data.get('result', {}).get('tools', [])
            print(f"[MCPAgent] Available tools: {len(self.tools_cache)}")
            
            return self.tools_cache
            
        except Exception as e:
            print(f"[MCPAgent] Failed to list tools: {e}")
            return []
    
    def call_tool(self, tool_name: str, arguments: Dict) -> str:
        """Call a specific tool on MCP server"""
        try:
            request = {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "call_tool",
                "params": {
                    "name": tool_name,
                    "arguments": arguments
                }
            }
            
            print(f"[MCPAgent] Calling tool: {tool_name}")
            print(f"[MCPAgent] Arguments: {arguments}")
            
            response = requests.post(self.endpoint, json=request, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if 'error' in data:
                error_msg = data['error'].get('message', 'Unknown error')
                print(f"[MCPAgent] Tool error: {error_msg}")
                return f"Error: {error_msg}"
            
            result = data.get('result', {}).get('content', '')
            print(f"[MCPAgent] Tool result (first 200 chars): {result[:200]}...")
            
            return result
            
        except Exception as e:
            print(f"[MCPAgent] Tool call failed: {e}")
            return f"Tool call failed: {str(e)}"


class AuroraRAGOrchestrator:
    """
    Intelligent orchestrator that decides which information source to use:
    - Hospital database (via MCP)
    - Medical knowledge base (via MCP)
    - Real-time web search (via MCP)
    - Patient records (via MCP)
    """
    
    def __init__(self):
        self.mcp_agent = MCPAgent()
        self.initialized = False
    
    def initialize(self) -> bool:
        """Initialize the orchestrator"""
        print("[RAGOrchestrator] Initializing...")
        
        # Connect to MCP server
        if not self.mcp_agent.initialize():
            print("[RAGOrchestrator] Failed to connect to MCP server")
            return False
        
        # Get available tools
        tools = self.mcp_agent.list_tools()
        if not tools:
            print("[RAGOrchestrator] No tools available")
            return False
        
        self.initialized = True
        print(f"[RAGOrchestrator] Initialized with {len(tools)} tools")
        return True
    
    def _convert_mcp_tools_to_openai_format(self, mcp_tools: List[Dict]) -> List[Dict]:
        """Convert MCP tool format to OpenAI function calling format"""
        
        openai_tools = []
        
        for tool in mcp_tools:
            openai_tool = {
                "type": "function",
                "function": {
                    "name": tool['name'],
                    "description": tool['description'],
                    "parameters": tool['input_schema']
                }
            }
            openai_tools.append(openai_tool)
        
        return openai_tools
    
    def query(self, question: str, context: Optional[Dict] = None) -> str:
        """
        Main query method - uses LLM to decide which tools to use
        
        Args:
            question: User's medical question
            context: Optional context (patient_id, location, etc.)
        """
        
        if not self.initialized:
            if not self.initialize():
                return "Error: Could not initialize RAG orchestrator"
        
        print(f"\n{'='*80}")
        print(f"[RAGOrchestrator] Processing query: {question}")
        print(f"{'='*80}\n")
        
        # Get available tools from MCP
        mcp_tools = self.mcp_agent.tools_cache or self.mcp_agent.list_tools()
        
        # Convert to OpenAI format
        openai_tools = self._convert_mcp_tools_to_openai_format(mcp_tools)
        
        # Build system message with context
        system_message = """You are Aurora Health AI Assistant - an intelligent medical information system.

You have access to several tools to help answer questions:
- search_hospitals: Find hospitals by disease, location, or facilities
- check_bed_availability: Check real-time bed availability
- search_medical_web: Search latest medical information online
- get_emergency_hospitals: Find nearest emergency hospitals
- search_medical_knowledge: Search Aurora's medical knowledge base
- get_patient_info: Retrieve patient medical records

IMPORTANT GUIDELINES:
1. For emergency situations (heart attack, stroke, severe trauma):
   - Use get_emergency_hospitals with patient location
   - Provide immediate action steps
   - List hospital emergency numbers

2. For hospital search queries:
   - Use search_hospitals with disease/location
   - Check bed availability if admission needed

3. For medical information queries:
   - Try search_medical_knowledge first
   - Use search_medical_web for latest research/news

4. For patient-specific queries:
   - Use get_patient_info (requires patient ID)

5. Always prioritize patient safety and provide clear, actionable information.
"""
        
        # Add context to system message
        if context:
            system_message += f"\n\nCurrent context: {json.dumps(context)}"
        
        # Build messages
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": question}
        ]
        
        try:
            # First LLM call - decide which tools to use
            print("[RAGOrchestrator] Asking LLM to choose appropriate tools...")
            
            response = client.chat.completions.create(
                model=CHAT_MODEL,
                messages=messages,
                tools=openai_tools,
                tool_choice="auto",
                temperature=0.2,
                max_tokens=500
            )
            
            message = response.choices[0].message
            
            # Check if LLM wants to use tools
            if message.tool_calls:
                print(f"[RAGOrchestrator] LLM requested {len(message.tool_calls)} tool(s)")
                return self._handle_tool_calls(message, messages, openai_tools)
            else:
                # LLM can answer directly
                print("[RAGOrchestrator] LLM answering directly from knowledge")
                return message.content.strip()
        
        except Exception as e:
            print(f"[RAGOrchestrator] Error in query processing: {e}")
            return f"Error processing query: {str(e)}"
    
    def _handle_tool_calls(self, message, messages: List[Dict], 
                          tools: List[Dict]) -> str:
        """Handle tool calls from LLM"""
        
        # Add LLM's message with tool calls to conversation
        messages.append({
            "role": "assistant",
            "content": message.content,
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": tc.type,
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                }
                for tc in message.tool_calls
            ]
        })
        
        # Execute each tool call
        for tool_call in message.tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            
            print(f"\n[RAGOrchestrator] Executing tool: {function_name}")
            print(f"[RAGOrchestrator] Arguments: {arguments}")
            
            # Call MCP server tool
            tool_result = self.mcp_agent.call_tool(function_name, arguments)
            
            print(f"[RAGOrchestrator] Tool result (first 300 chars):")
            print(f"{tool_result[:300]}...")
            
            # Add tool result to conversation
            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": tool_result
            })
        
        # Final LLM call with tool results
        print("\n[RAGOrchestrator] Getting final answer from LLM...")
        
        try:
            final_response = client.chat.completions.create(
                model=CHAT_MODEL,
                messages=messages,
                temperature=0.2,
                max_tokens=1000
            )
            
            final_answer = final_response.choices[0].message.content.strip()
            
            print(f"\n[RAGOrchestrator] Final answer generated ({len(final_answer)} chars)")
            
            return final_answer
            
        except Exception as e:
            print(f"[RAGOrchestrator] Error getting final answer: {e}")
            
            # Return raw tool results if final LLM call fails
            tool_results = [msg['content'] for msg in messages if msg.get('role') == 'tool']
            return "\n\n".join(tool_results)


# ============================================================================
# DEMO USAGE
# ============================================================================

def demo_queries():
    """Demonstrate various query types"""
    
    print("\n" + "="*80)
    print("  🏥 AURORA HEALTH - AGENTIC RAG DEMO")
    print("="*80 + "\n")
    
    # Initialize orchestrator
    orchestrator = AuroraRAGOrchestrator()
    
    if not orchestrator.initialize():
        print("❌ Failed to initialize orchestrator")
        return
    
    print("✅ Orchestrator initialized successfully!\n")
    
    # Test queries
    queries = [
        {
            "question": "I'm having severe chest pain and sweating. I'm in Manikganj. Where should I go?",
            "context": {"latitude": 23.8617, "longitude": 90.0003, "urgency": "emergency"}
        },
        {
            "question": "Find hospitals in Dhaka with good cardiology departments",
            "context": {}
        },
        {
            "question": "What are the symptoms of diabetes?",
            "context": {}
        },
        {
            "question": "Check ICU bed availability at NICVD",
            "context": {}
        },
        {
            "question": "What is the latest treatment for heart disease?",
            "context": {}
        }
    ]
    
    for i, query_data in enumerate(queries, 1):
        print(f"\n{'='*80}")
        print(f"QUERY {i}/{len(queries)}")
        print(f"{'='*80}")
        
        question = query_data["question"]
        context = query_data["context"]
        
        print(f"\n❓ Question: {question}")
        if context:
            print(f"📋 Context: {context}")
        
        print("\n" + "-"*80)
        
        # Get answer
        answer = orchestrator.query(question, context)
        
        print(f"\n💡 ANSWER:")
        print("-"*80)
        print(answer)
        print("-"*80)
        
        # Pause between queries
        if i < len(queries):
            input("\nPress Enter to continue to next query...\n")


if __name__ == "__main__":
    # Check environment variables
    if not OPENAI_API_KEY:
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        print("   Set it with: export OPENAI_API_KEY=your-key-here")
        exit(1)
    
    # Run demo
    try:
        demo_queries()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
