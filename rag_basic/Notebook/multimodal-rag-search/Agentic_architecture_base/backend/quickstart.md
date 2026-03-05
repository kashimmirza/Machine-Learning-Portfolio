<!-- @format -->

UICK START (3 Steps)

Step 1: Setup Environment
bash# Set API keys
export OPENAI_API_KEY=your-openai-key-here
export SERPAPI_KEY=your-serpapi-key-here # Optional

# Database already configured from previous setup

# Uses aurora_health database

Step 2: Start MCP Server
bash# Terminal 1
cd /mnt/user-data/outputs/backend
python3 mcp_server_aurora.py

# Output:

# ✅ Aurora Health MCP Server running on http://localhost:8001/

Step 3: Run RAG Orchestrator
bash# Terminal 2
python3 rag_orchestrator_mcp.py

# Runs 5 demo queries automatically!

```

---

## 💡 **HOW IT WORKS (Example)**

### **Query:** *"I have chest pain in Manikganj. Where should I go?"*
```

Step 1: User asks question
↓
Step 2: RAG Orchestrator receives query
↓
Step 3: Orchestrator asks GPT-4:
"I have these tools: [search_hospitals, get_emergency_hospitals, ...]
Which should I use for: 'chest pain in Manikganj'?"
↓
Step 4: GPT-4 decides:
"This is EMERGENCY + LOCATION-based
Use: get_emergency_hospitals
Arguments: {latitude: 23.86, longitude: 90.00, condition: 'chest pain'}"
↓
Step 5: MCP Agent calls MCP Server (JSON-RPC):
{
"method": "call_tool",
"params": {
"name": "get_emergency_hospitals",
"arguments": {...}
}
}
↓
Step 6: MCP Server executes tool: - Queries PostgreSQL hospitals table - Calculates distances (Haversine formula) - Filters by: 24/7 emergency + cardiology dept - Returns top 3 nearest
↓
Step 7: Result back to MCP Agent → Orchestrator
↓
Step 8: GPT-4 formats final answer:
"🚨 EMERGENCY - Go to NICVD (5.2 km, Emergency: 02-9015951)
IMMEDIATE: Call 999, Take aspirin if available"

```

**All decisions made by AI, not hardcoded!** 🤖

---

## 🎯 **KEY FEATURES**

### **1. Intelligent Routing**
```

"What is diabetes?"
→ LLM chooses: search_medical_knowledge

"Latest diabetes research?"
→ LLM chooses: search_medical_web

"Diabetes hospitals in Dhaka?"
→ LLM chooses: search_hospitals

```

### **2. Multi-Tool Orchestration**
```

Single query can use multiple tools:
"I have diabetes emergency in Dhaka, need ICU"

1. search_medical_knowledge (diabetes info)
2. get_emergency_hospitals (location-based)
3. check_bed_availability (ICU beds)

```

### **3. Real-time Data**
```

✅ Live bed availability from PostgreSQL
✅ Current hospital status
✅ Latest web results (SerpAPI)
✅ Up-to-date medical knowledge

📊 COMPARISON
FeatureTraditional RAGYour Agentic RAGRoutingHardcodedAI decidesData Sources1 (documents)4+ (DB, Web, KB)Tool SelectionProgrammaticLLM choosesUpdatesManual reindexReal-timeContext-awareNoYesMulti-sourceNoYes ✅Emergency HandlingNoYes ✅Bangladesh-specificNoYes ✅

🔧 TESTING
Test MCP Server:
bash# Test health
curl http://localhost:8001/health

# Test tool listing

curl -X POST http://localhost:8001/ \
 -H "Content-Type: application/json" \
 -d '{
"jsonrpc": "2.0",
"id": 1,
"method": "list_tools"
}'

# Test hospital search

curl -X POST http://localhost:8001/ \
 -H "Content-Type: application/json" \
 -d '{
"jsonrpc": "2.0",
"id": 1,
"method": "call_tool",
"params": {
"name": "search_hospitals",
"arguments": {"location": "Dhaka", "disease": "heart"}
}
}'

🎓 WHAT YOU LEARNED
From the blog architecture, you now have:
✅ MCP Protocol - JSON-RPC 2.0 implementation
✅ Tool Discovery - LLM knows available tools
✅ Function Calling - OpenAI tool calling pattern
✅ Agentic Behavior - AI makes routing decisions
✅ Multi-source RAG - DB + Web + Knowledge
✅ Real-world Application - Bangladesh healthcare

🌟 ADVANTAGES

1. No Hardcoded Rules
   python# Traditional RAG
   if "emergency" in query:
   search_hospitals()
   elif "latest" in query:
   search_web()

# Your Agentic RAG

llm.decide_which_tool() # AI chooses! 2. Flexible & Extensible
python# Add new tool: Just add to MCP server
def new_tool():
...

# LLM automatically discovers and uses it!

# No code changes needed

3. Context-Aware
   python# Same words, different tools:
   "Heart attack information" → search_medical_knowledge
   "Heart attack in Dhaka NOW" → get_emergency_hospitals

```

---

## 📁 **FILES SUMMARY**
```

✅ mcp_server_aurora.py (700 lines)

- MCP server with 6 medical tools
- JSON-RPC 2.0 implementation
- PostgreSQL integration
- SerpAPI web search

✅ rag_orchestrator_mcp.py (400 lines)

- Agentic RAG orchestrator
- OpenAI tool calling
- MCP client
- Demo queries

✅ AGENTIC_RAG_MCP_GUIDE.md (comprehensive)

- Architecture explanation
- Quick start guide
- Examples & comparisons
- Troubleshooting

```

**Total: 1,100+ lines of production-ready code!**

---
```

╔══════════════════════════════════════════════════════════════╗
║ ║
║ 🤖 AGENTIC RAG WITH MCP INTEGRATION ║
║ Following Blog Architecture Exactly ║
║ ║
║ ✅ MCP Server (JSON-RPC 2.0) ║
║ ✅ 6 Intelligent Tools ║
║ ✅ RAG Orchestrator (AI routing) ║
║ ✅ LLM Tool Calling (GPT-4) ║
║ ✅ Multi-source Search ║
║ ✅ Real-time Data ║
║ ✅ Bangladesh Healthcare ║
║ ║
║ Architecture: Same as blog article ║
║ Intelligence: AI decides data sources ║
║ Protocol: MCP (Model Context Protocol) ║
║ ║
║ Start MCP: python3 mcp_server_aurora.py ║
║ Run RAG: python3 rag_orchestrator_mcp.py ║
║ ║
╚══════════════════════════════════════════════════════════════╝
