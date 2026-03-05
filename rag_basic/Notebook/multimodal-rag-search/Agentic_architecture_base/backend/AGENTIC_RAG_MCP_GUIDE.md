# 🤖 AURORA HEALTH - AGENTIC RAG WITH MCP INTEGRATION
## Complete Multimodal Search System

---

## 🎯 WHAT THIS IS

An **intelligent medical information retrieval system** that combines:

✅ **Agentic RAG** - AI decides which data source to use  
✅ **MCP Server** - Standardized tool integration protocol  
✅ **Multi-source Search** - Hospital DB + Web + Medical Knowledge  
✅ **LLM Tool Calling** - GPT decides which tools to invoke  
✅ **Real-time Data** - Live bed availability, emergency routing  

---

## 🏗️ ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────┐
│                    USER QUERY                               │
│              "I have chest pain in Dhaka"                   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              RAG ORCHESTRATOR                               │
│  • Receives query                                           │
│  • Asks LLM: "Which tools do you need?"                    │
│  • LLM analyzes and chooses tools                          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  LLM (GPT-4)                                │
│  Decides: "This is emergency + location-based"             │
│  Chooses: get_emergency_hospitals tool                     │
│  Arguments: {lat: 23.76, lon: 90.36, condition: "chest"}  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  MCP AGENT                                  │
│  • Formats request as JSON-RPC 2.0                         │
│  • Calls MCP server                                        │
│  • Returns structured result                               │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  MCP SERVER                                 │
│  ┌──────────────────────────────────────────────────┐     │
│  │  AVAILABLE TOOLS:                                │     │
│  │                                                   │     │
│  │  1. search_hospitals                             │     │
│  │     → PostgreSQL query                           │     │
│  │     → Returns hospitals by disease/location      │     │
│  │                                                   │     │
│  │  2. check_bed_availability                       │     │
│  │     → Real-time bed status                       │     │
│  │     → ICU/Cabin/Ward availability                │     │
│  │                                                   │     │
│  │  3. get_emergency_hospitals                      │     │
│  │     → Haversine distance calculation             │     │
│  │     → Returns nearest 24/7 hospitals             │     │
│  │                                                   │     │
│  │  4. search_medical_web                           │     │
│  │     → SerpAPI integration                        │     │
│  │     → Latest medical research/news               │     │
│  │                                                   │     │
│  │  5. search_medical_knowledge                     │     │
│  │     → Internal knowledge base                    │     │
│  │     → Symptoms, treatments, prevention           │     │
│  │                                                   │     │
│  │  6. get_patient_info                             │     │
│  │     → Patient medical history                    │     │
│  │     → Medications, allergies, records            │     │
│  └──────────────────────────────────────────────────┘     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│               DATA SOURCES                                  │
│  • PostgreSQL (Aurora Health DB)                           │
│  • Medical Knowledge Base                                   │
│  • SerpAPI (Web Search)                                    │
│  • Real-time Bed Tracking                                  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              RESULT BACK TO USER                            │
│                                                             │
│  "🚨 EMERGENCY - Nearest hospitals:                        │
│   1. NICVD - 5.2 km (Emergency: 02-9015951)                │
│   2. Square Hospital - 6.8 km                              │
│   3. DMCH - 7.1 km                                         │
│                                                             │
│   IMMEDIATE ACTION:                                        │
│   • Call ambulance: 999                                    │
│   • Take aspirin if available                              │
│   • Go to NICVD immediately"                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 KEY FEATURES

### **1. Intelligent Routing**
- LLM decides which data source to use
- No hardcoded rules
- Context-aware decisions

### **2. Multi-Tool Support**
```
Emergency Query → get_emergency_hospitals
Hospital Search → search_hospitals  
Medical Info → search_medical_knowledge OR search_medical_web
Bed Check → check_bed_availability
Patient Data → get_patient_info
```

### **3. JSON-RPC 2.0 Protocol**
- Standardized communication
- Compatible with any MCP client
- Error handling built-in

### **4. Real-time Data**
- Live bed availability
- Current hospital status
- Latest medical research (via web)

---

## 🚀 QUICK START

### **Step 1: Set Environment Variables**

```bash
# Create .env file
cat > .env << 'EOF'
# OpenAI API Key (required)
export OPENAI_API_KEY=your-openai-key-here

# SerpAPI Key (optional - for web search)
export SERPAPI_KEY=your-serpapi-key-here

# Database Configuration
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=aurora_health
export DB_USER=aurora
export DB_PASSWORD=aurora_secure_password_2026
EOF

# Load environment variables
source .env
```

### **Step 2: Install Dependencies**

```bash
# Install required packages
pip install fastapi uvicorn httpx psycopg2-binary openai requests --break-system-packages
```

### **Step 3: Start MCP Server**

```bash
# Terminal 1: Start MCP Server
cd /mnt/user-data/outputs/backend
python3 mcp_server_aurora.py

# Output:
# ✅ Aurora Health MCP Server running on http://localhost:8001/
```

### **Step 4: Test MCP Server**

```bash
# Test health check
curl http://localhost:8001/health

# Test tool listing
curl -X POST http://localhost:8001/ \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "list_tools"
  }'
```

### **Step 5: Run RAG Orchestrator**

```bash
# Terminal 2: Run RAG Orchestrator
cd /mnt/user-data/outputs/backend
python3 rag_orchestrator_mcp.py

# This will run demo queries automatically
```

---

## 💡 EXAMPLE QUERIES

### **Query 1: Emergency Situation**

```
Question: "I'm having severe chest pain and sweating. I'm in Manikganj. Where should I go?"

What Happens:
1. RAG Orchestrator sends to LLM
2. LLM recognizes: EMERGENCY + LOCATION
3. LLM chooses tool: get_emergency_hospitals
4. Arguments: {latitude: 23.86, longitude: 90.00, condition: "chest pain"}
5. MCP Server executes:
   - Calculates distances from patient location
   - Filters 24/7 emergency hospitals
   - Filters by cardiology expertise
   - Returns top 3 nearest
6. LLM formats final answer with:
   - Hospital names + distances
   - Emergency phone numbers
   - Immediate action steps

Response:
🚨 EMERGENCY HOSPITALS FOR: CHEST PAIN

1. National Institute of Cardiovascular Diseases (NICVD)
   Distance: 38.8 km
   Emergency: 02-9015951
   Location: Sher-e-Bangla Nagar, Dhaka
   Rating: 4.3/5.0

2. Square Hospitals Ltd
   Distance: 41.4 km
   Emergency: +880-2-8159457
   Rating: 4.7/5.0

IMMEDIATE ACTIONS:
• Call 999 NOW
• Take aspirin if available (not allergic)
• Do not drive yourself
• Ambulance ETA: 12 minutes
```

---

### **Query 2: Hospital Search**

```
Question: "Find hospitals in Dhaka with good cardiology departments"

What Happens:
1. LLM chooses: search_hospitals
2. Arguments: {disease: "heart", location: "Dhaka"}
3. MCP Server queries PostgreSQL
4. Returns hospitals with Cardiology dept in Dhaka

Response:
1. National Institute of Cardiovascular Diseases (NICVD)
   Location: Dhaka, Dhaka
   Beds: 550
   Rating: 4.3/5.0
   Emergency: 02-9015951

2. Square Hospitals Ltd
   Location: Dhaka, Dhaka
   Beds: 400
   Rating: 4.7/5.0
   Emergency: +880-2-8159457
```

---

### **Query 3: Medical Knowledge**

```
Question: "What are the symptoms of diabetes?"

What Happens:
1. LLM chooses: search_medical_knowledge
2. Arguments: {query: "diabetes", category: "disease"}
3. MCP Server returns structured medical info

Response:
📋 MEDICAL INFORMATION: Diabetes Mellitus

SYMPTOMS:
• Increased thirst
• Frequent urination
• Extreme hunger
• Unexplained weight loss
• Fatigue
• Blurred vision

URGENCY: Schedule appointment
SPECIALIST: Endocrinologist
TREATMENT: Insulin therapy, oral medications, lifestyle changes
PREVENTION: Healthy diet, regular exercise, maintain healthy weight
```

---

### **Query 4: Bed Availability**

```
Question: "Check ICU bed availability at NICVD"

What Happens:
1. LLM chooses: check_bed_availability
2. Arguments: {hospital_name: "NICVD", bed_type: "icu"}
3. MCP Server queries bed_availability table

Response:
National Institute of Cardiovascular Diseases - Dhaka
  ICU: 2/80 available
  Last updated: 2026-01-31 14:30:00
```

---

### **Query 5: Latest Medical Research**

```
Question: "What is the latest treatment for heart disease?"

What Happens:
1. LLM recognizes: "latest" = need web search
2. LLM chooses: search_medical_web
3. Arguments: {query: "latest heart disease treatment"}
4. MCP Server calls SerpAPI
5. Returns recent web results

Response:
1. New breakthrough in heart disease treatment - Mayo Clinic
   https://mayoclinic.org/...
   Researchers have developed a new...

2. Latest guidelines for cardiovascular disease - American Heart Association
   https://heart.org/...
   Updated 2025 guidelines recommend...
```

---

## 🔧 HOW IT WORKS

### **JSON-RPC 2.0 Communication**

```json
// Client → MCP Server
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "call_tool",
  "params": {
    "name": "search_hospitals",
    "arguments": {
      "disease": "heart",
      "location": "Dhaka"
    }
  }
}

// MCP Server → Client
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": "1. NICVD (জাতীয় হৃদরোগ ইনস্টিটিউট)\n   Location: Dhaka..."
  }
}
```

---

### **OpenAI Tool Calling**

```python
# Define tools for LLM
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_hospitals",
            "description": "Search hospitals by disease, location, facilities",
            "parameters": {
                "type": "object",
                "properties": {
                    "disease": {"type": "string"},
                    "location": {"type": "string"}
                }
            }
        }
    }
]

# LLM decides which tool to use
response = openai.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": question}],
    tools=tools,
    tool_choice="auto"  # Let LLM decide
)

# LLM responds with tool call
if response.choices[0].message.tool_calls:
    # Execute the tool
    tool_name = response.choices[0].message.tool_calls[0].function.name
    arguments = response.choices[0].message.tool_calls[0].function.arguments
```

---

## 🎯 BENEFITS OF THIS ARCHITECTURE

### **1. Intelligent Decision Making**
```
Traditional RAG: Always searches same data source
Agentic RAG: LLM chooses best source for each query

Example:
"What is diabetes?" → Medical knowledge base
"Latest diabetes research?" → Web search
"Diabetes hospitals in Dhaka?" → Hospital database
```

### **2. Flexible & Extensible**
```
Add new tools easily:
1. Implement tool function in MCP server
2. Add to tool list
3. LLM automatically starts using it

No code changes in orchestrator needed!
```

### **3. Multi-source Integration**
```
Single query can use multiple sources:
"I have diabetes and need ICU in Dhaka"
  → search_medical_knowledge (diabetes info)
  → search_hospitals (diabetes specialists)
  → check_bed_availability (ICU beds)
```

### **4. Real-time & Accurate**
```
Database: Real-time bed status
Web: Latest medical research
Knowledge: Curated medical info
```

---

## 📊 COMPARISON

### **Traditional RAG vs Agentic RAG**

| Feature | Traditional RAG | Agentic RAG (Ours) |
|---------|----------------|-------------------|
| Data Source | Single (documents) | Multiple (DB + Web + Knowledge) |
| Routing | Hardcoded rules | LLM decides |
| Updates | Manual reindex | Real-time |
| Tool Selection | Programmatic | AI-driven |
| Flexibility | Low | High |
| Accuracy | Good | Better |
| Context-aware | No | Yes |

---

## 🛠️ TROUBLESHOOTING

### **Issue: MCP Server won't start**

```bash
# Check if port 8001 is free
lsof -i :8001

# If occupied, kill process
kill -9 <PID>

# Or use different port
# Edit mcp_server_aurora.py: HTTP_PORT = 8002
```

---

### **Issue: Database connection failed**

```bash
# Check PostgreSQL running
sudo systemctl status postgresql

# Test connection
psql -U aurora -d aurora_health -h localhost

# Check credentials in .env
echo $DB_PASSWORD
```

---

### **Issue: OpenAI API errors**

```bash
# Verify API key
echo $OPENAI_API_KEY

# Test API key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# Check quota/credits
# Visit: https://platform.openai.com/account/usage
```

---

### **Issue: Tool calls not working**

```bash
# Check MCP server logs
# Terminal 1 should show incoming requests

# Test tool manually
curl -X POST http://localhost:8001/ \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "call_tool",
    "params": {
      "name": "search_hospitals",
      "arguments": {"location": "Dhaka"}
    }
  }'
```

---

## 📚 FILES CREATED

```
backend/
├── mcp_server_aurora.py (700 lines)
│   └── MCP Server with 6 tools
│       • Hospital search
│       • Bed availability
│       • Emergency routing
│       • Web search
│       • Medical knowledge
│       • Patient records
│
└── rag_orchestrator_mcp.py (400 lines)
    └── Agentic RAG Orchestrator
        • LLM tool calling
        • MCP integration
        • Multi-source routing
        • Demo queries
```

---

## 🎉 SUMMARY

```
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║  🤖 AGENTIC RAG WITH MCP - COMPLETE!                    ║
║                                                          ║
║  ✅ MCP Server (6 tools)                                ║
║  ✅ RAG Orchestrator (AI routing)                       ║
║  ✅ Multi-source search                                 ║
║  ✅ Real-time data                                      ║
║  ✅ LLM tool calling                                    ║
║  ✅ Bangladesh healthcare focus                         ║
║                                                          ║
║  Architecture: Agentic RAG + MCP Protocol               ║
║  Intelligence: GPT-4 decides which tools to use         ║
║  Data: Hospital DB + Web + Medical Knowledge            ║
║                                                          ║
║  Start: python3 mcp_server_aurora.py                    ║
║  Test: python3 rag_orchestrator_mcp.py                  ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
```

**Your intelligent multimodal medical search system is ready!** 🚀

**Run it and see AI make smart decisions about data sources!** 🤖
