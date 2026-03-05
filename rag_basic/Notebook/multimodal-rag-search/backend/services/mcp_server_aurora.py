#!/usr/bin/env python3
"""
🏥 Aurora Health - MCP Server for Multimodal Medical Search
Implements Model Context Protocol (MCP) for:
- Medical knowledge search
- Hospital database search
- Patient record search
- Real-time web search for latest medical information
- Medical image analysis
"""

import os
import json
import logging
from typing import List, Dict, Any
import httpx
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
import psycopg2
from psycopg2.extras import RealDictCursor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(title="Aurora Health MCP Server", version="1.0.0")

# Server configuration
HTTP_HOST = "0.0.0.0"
HTTP_PORT = 8001
SERPAPI_KEY = os.environ.get("SERPAPI_KEY", "")

# Database configuration
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': int(os.environ.get('DB_PORT', 5432)),
    'database': os.environ.get('DB_NAME', 'aurora_health'),
    'user': os.environ.get('DB_USER', 'aurora'),
    'password': os.environ.get('DB_PASSWORD', 'aurora_secure_password_2026')
}


# ============================================================================
# DATABASE CONNECTION
# ============================================================================

def get_db_connection():
    """Get PostgreSQL database connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return None


# ============================================================================
# TOOL DEFINITIONS
# ============================================================================

async def list_tools() -> Dict[str, Any]:
    """Return all available tools for Aurora Health MCP server"""
    return {
        "tools": [
            {
                "name": "search_hospitals",
                "description": "Search for hospitals in Bangladesh by disease expertise, location, or facilities",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "disease": {
                            "type": "string",
                            "description": "Disease or medical condition (e.g., 'heart attack', 'diabetes')"
                        },
                        "location": {
                            "type": "string",
                            "description": "District or division in Bangladesh (e.g., 'Dhaka', 'Chittagong')"
                        },
                        "bed_type": {
                            "type": "string",
                            "description": "Type of bed needed (icu, cabin, ward)",
                            "enum": ["icu", "cabin", "ward", "ccu", "nicu"]
                        },
                        "max_distance_km": {
                            "type": "number",
                            "description": "Maximum distance in kilometers",
                            "default": 50
                        }
                    },
                    "required": []
                }
            },
            {
                "name": "check_bed_availability",
                "description": "Check real-time bed availability at hospitals",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "hospital_name": {
                            "type": "string",
                            "description": "Name of the hospital"
                        },
                        "bed_type": {
                            "type": "string",
                            "description": "Type of bed (icu, cabin, ward)",
                            "enum": ["icu", "cabin", "ward", "ccu", "nicu"]
                        },
                        "district": {
                            "type": "string",
                            "description": "District name"
                        }
                    },
                    "required": []
                }
            },
            {
                "name": "search_medical_web",
                "description": "Search the web for latest medical information, research, or health news",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Medical search query"
                        },
                        "max_results": {
                            "type": "integer",
                            "description": "Maximum number of results",
                            "default": 5
                        }
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "get_emergency_hospitals",
                "description": "Get nearest hospitals for emergency cases with critical care facilities",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "latitude": {
                            "type": "number",
                            "description": "Patient's latitude"
                        },
                        "longitude": {
                            "type": "number",
                            "description": "Patient's longitude"
                        },
                        "condition": {
                            "type": "string",
                            "description": "Medical emergency (e.g., 'heart attack', 'stroke')"
                        },
                        "max_results": {
                            "type": "integer",
                            "description": "Number of hospitals to return",
                            "default": 3
                        }
                    },
                    "required": ["latitude", "longitude", "condition"]
                }
            },
            {
                "name": "search_medical_knowledge",
                "description": "Search Aurora Health's medical knowledge base for diseases, symptoms, treatments",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Medical query (disease, symptom, treatment)"
                        },
                        "category": {
                            "type": "string",
                            "description": "Category to search",
                            "enum": ["disease", "symptom", "treatment", "medication", "all"]
                        }
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "get_patient_info",
                "description": "Retrieve patient medical history and records (requires authorization)",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "patient_id": {
                            "type": "string",
                            "description": "Patient ID"
                        },
                        "info_type": {
                            "type": "string",
                            "description": "Type of information",
                            "enum": ["medical_history", "medications", "allergies", "lab_results", "all"]
                        }
                    },
                    "required": ["patient_id"]
                }
            }
        ]
    }


# ============================================================================
# TOOL IMPLEMENTATIONS
# ============================================================================

async def search_hospitals(disease: str = "", location: str = "", 
                          bed_type: str = "", max_distance_km: float = 50) -> str:
    """Search hospitals based on criteria"""
    
    conn = get_db_connection()
    if not conn:
        return "Database connection failed. Unable to search hospitals."
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Build dynamic query
        query = """
            SELECT h.name, h.name_bengali, h.district, h.division,
                   h.address, h.phone_emergency, h.total_beds,
                   h.quality_rating, h.emergency_24x7
            FROM hospitals h
            WHERE 1=1
        """
        params = []
        
        if location:
            query += " AND (h.district ILIKE %s OR h.division ILIKE %s)"
            params.extend([f"%{location}%", f"%{location}%"])
        
        if disease:
            # Map disease to departments (simplified)
            disease_dept_map = {
                'heart': 'Cardiology',
                'brain': 'Neurology',
                'cancer': 'Oncology',
                'bone': 'Orthopedics',
                'diabetes': 'Endocrinology'
            }
            for key, dept in disease_dept_map.items():
                if key in disease.lower():
                    query += " AND h.departments::text ILIKE %s"
                    params.append(f"%{dept}%")
                    break
        
        query += " ORDER BY h.quality_rating DESC, h.total_beds DESC LIMIT 5"
        
        cursor.execute(query, params)
        hospitals = cursor.fetchall()
        
        if not hospitals:
            return f"No hospitals found matching criteria: disease={disease}, location={location}"
        
        # Format results
        results = []
        for i, h in enumerate(hospitals, 1):
            result = f"{i}. {h['name']} ({h['name_bengali']})\n"
            result += f"   Location: {h['district']}, {h['division']}\n"
            result += f"   Address: {h['address']}\n"
            result += f"   Emergency: {h['phone_emergency']}\n"
            result += f"   Beds: {h['total_beds']}\n"
            result += f"   Rating: {h['quality_rating']}/5.0\n"
            result += f"   24/7 Emergency: {'Yes' if h['emergency_24x7'] else 'No'}\n"
            results.append(result)
        
        cursor.close()
        conn.close()
        
        return "\n".join(results)
        
    except Exception as e:
        logger.error(f"Hospital search error: {e}")
        return f"Error searching hospitals: {str(e)}"


async def check_bed_availability(hospital_name: str = "", bed_type: str = "", 
                                 district: str = "") -> str:
    """Check bed availability at hospitals"""
    
    conn = get_db_connection()
    if not conn:
        return "Database connection failed."
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        query = """
            SELECT h.name, h.district, ba.bed_type, 
                   ba.total_beds, ba.occupied_beds, ba.available_beds,
                   ba.last_updated
            FROM hospitals h
            JOIN bed_availability ba ON h.hospital_id = ba.hospital_id
            WHERE 1=1
        """
        params = []
        
        if hospital_name:
            query += " AND h.name ILIKE %s"
            params.append(f"%{hospital_name}%")
        
        if district:
            query += " AND h.district ILIKE %s"
            params.append(f"%{district}%")
        
        if bed_type:
            query += " AND ba.bed_type = %s"
            params.append(bed_type.lower())
        
        query += " ORDER BY ba.available_beds DESC"
        
        cursor.execute(query, params)
        beds = cursor.fetchall()
        
        if not beds:
            return "No bed availability information found."
        
        # Format results
        results = []
        for bed in beds:
            result = f"{bed['name']} - {bed['district']}\n"
            result += f"  {bed['bed_type'].upper()}: {bed['available_beds']}/{bed['total_beds']} available\n"
            result += f"  Last updated: {bed['last_updated']}\n"
            results.append(result)
        
        cursor.close()
        conn.close()
        
        return "\n".join(results)
        
    except Exception as e:
        logger.error(f"Bed availability error: {e}")
        return f"Error checking bed availability: {str(e)}"


async def search_medical_web(query: str, max_results: int = 5) -> str:
    """Search web for medical information using SerpAPI"""
    
    if not SERPAPI_KEY:
        return "Web search not available. SERPAPI_KEY not configured."
    
    try:
        async with httpx.AsyncClient() as client:
            params = {
                "api_key": SERPAPI_KEY,
                "engine": "google",
                "q": f"medical {query}",  # Add medical context
                "num": max_results
            }
            
            response = await client.get("https://serpapi.com/search", params=params)
            response.raise_for_status()
            data = response.json()
            
            organic_results = data.get("organic_results", [])
            
            if not organic_results:
                return f"No web results found for '{query}'"
            
            # Format results
            results = []
            for i, item in enumerate(organic_results[:max_results], 1):
                result = f"{i}. {item.get('title')}\n"
                result += f"   {item.get('link')}\n"
                result += f"   {item.get('snippet', '')}\n"
                results.append(result)
            
            return "\n".join(results)
            
    except Exception as e:
        logger.error(f"Web search error: {e}")
        return f"Error searching web: {str(e)}"


async def get_emergency_hospitals(latitude: float, longitude: float, 
                                  condition: str, max_results: int = 3) -> str:
    """Get nearest emergency hospitals for critical condition"""
    
    conn = get_db_connection()
    if not conn:
        return "Database connection failed."
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Calculate distance using Haversine formula (simplified)
        # Map condition to required departments
        dept_map = {
            'heart': 'Cardiology',
            'stroke': 'Neurology',
            'trauma': 'Emergency',
            'accident': 'Orthopedics'
        }
        
        required_dept = None
        for key, dept in dept_map.items():
            if key in condition.lower():
                required_dept = dept
                break
        
        query = """
            SELECT h.name, h.name_bengali, h.district, h.phone_emergency,
                   h.address, h.quality_rating,
                   (
                       6371 * acos(
                           cos(radians(%s)) * cos(radians(h.latitude)) *
                           cos(radians(h.longitude) - radians(%s)) +
                           sin(radians(%s)) * sin(radians(h.latitude))
                       )
                   ) AS distance_km
            FROM hospitals h
            WHERE h.emergency_24x7 = TRUE
        """
        params = [latitude, longitude, latitude]
        
        if required_dept:
            query += " AND h.departments::text ILIKE %s"
            params.append(f"%{required_dept}%")
        
        query += " ORDER BY distance_km ASC, h.quality_rating DESC LIMIT %s"
        params.append(max_results)
        
        cursor.execute(query, params)
        hospitals = cursor.fetchall()
        
        if not hospitals:
            return "No emergency hospitals found nearby."
        
        # Format results
        results = []
        results.append(f"🚨 EMERGENCY HOSPITALS FOR: {condition.upper()}\n")
        
        for i, h in enumerate(hospitals, 1):
            result = f"{i}. {h['name']} ({h['name_bengali']})\n"
            result += f"   Distance: {h['distance_km']:.1f} km\n"
            result += f"   Emergency: {h['phone_emergency']}\n"
            result += f"   Location: {h['address']}, {h['district']}\n"
            result += f"   Rating: {h['quality_rating']}/5.0\n"
            results.append(result)
        
        cursor.close()
        conn.close()
        
        return "\n".join(results)
        
    except Exception as e:
        logger.error(f"Emergency hospital search error: {e}")
        return f"Error finding emergency hospitals: {str(e)}"


async def search_medical_knowledge(query: str, category: str = "all") -> str:
    """Search Aurora Health medical knowledge base"""
    
    # This would connect to your medical knowledge base
    # For now, returning structured medical information
    
    knowledge = {
        "heart attack": {
            "disease": "Myocardial Infarction (Heart Attack)",
            "symptoms": [
                "Severe chest pain",
                "Sweating",
                "Shortness of breath",
                "Nausea",
                "Arm/jaw pain"
            ],
            "urgency": "IMMEDIATE - Call 999",
            "specialist": "Cardiologist",
            "facilities_needed": ["Cath Lab", "ICU", "ECG"],
            "treatment": "Immediate angioplasty or thrombolysis",
            "prevention": "Control blood pressure, cholesterol, quit smoking, exercise"
        },
        "diabetes": {
            "disease": "Diabetes Mellitus",
            "symptoms": [
                "Increased thirst",
                "Frequent urination",
                "Extreme hunger",
                "Unexplained weight loss",
                "Fatigue",
                "Blurred vision"
            ],
            "urgency": "Schedule appointment",
            "specialist": "Endocrinologist",
            "treatment": "Insulin therapy, oral medications, lifestyle changes",
            "prevention": "Healthy diet, regular exercise, maintain healthy weight"
        }
    }
    
    # Search knowledge base
    query_lower = query.lower()
    for key, info in knowledge.items():
        if key in query_lower:
            result = f"📋 MEDICAL INFORMATION: {info['disease']}\n\n"
            result += f"SYMPTOMS:\n"
            for symptom in info['symptoms']:
                result += f"  • {symptom}\n"
            result += f"\nURGENCY: {info['urgency']}\n"
            result += f"SPECIALIST: {info['specialist']}\n"
            if 'facilities_needed' in info:
                result += f"FACILITIES NEEDED: {', '.join(info['facilities_needed'])}\n"
            result += f"\nTREATMENT: {info['treatment']}\n"
            result += f"PREVENTION: {info['prevention']}\n"
            return result
    
    return f"Medical information for '{query}' not found in knowledge base. Try web search for latest information."


async def get_patient_info(patient_id: str, info_type: str = "all") -> str:
    """Get patient information (with authorization check)"""
    
    # In production, implement proper authorization
    # For demo, returning sample data
    
    conn = get_db_connection()
    if not conn:
        return "Database connection failed."
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Get patient data
        query = """
            SELECT p.patient_id, u.full_name, u.email, u.phone,
                   p.date_of_birth, p.gender, p.blood_type,
                   p.address_city, p.address_district,
                   p.emergency_contact_name, p.emergency_contact_phone
            FROM patients p
            JOIN users u ON p.user_id = u.user_id
            WHERE p.patient_id::text LIKE %s
            LIMIT 1
        """
        
        cursor.execute(query, [f"%{patient_id}%"])
        patient = cursor.fetchone()
        
        if not patient:
            return f"Patient {patient_id} not found."
        
        result = f"👤 PATIENT INFORMATION\n\n"
        result += f"Name: {patient['full_name']}\n"
        result += f"DOB: {patient['date_of_birth']}\n"
        result += f"Gender: {patient['gender']}\n"
        result += f"Blood Type: {patient['blood_type']}\n"
        result += f"Location: {patient['address_city']}, {patient['address_district']}\n"
        result += f"Phone: {patient['phone']}\n"
        result += f"Emergency Contact: {patient['emergency_contact_name']} ({patient['emergency_contact_phone']})\n"
        
        cursor.close()
        conn.close()
        
        return result
        
    except Exception as e:
        logger.error(f"Patient info error: {e}")
        return f"Error retrieving patient information: {str(e)}"


# ============================================================================
# JSON-RPC ENDPOINT
# ============================================================================

@app.post("/")
async def mcp_entrypoint(request: Request):
    """Main MCP JSON-RPC 2.0 endpoint"""
    
    # Parse request
    body = await request.body()
    try:
        rpc = json.loads(body)
    except Exception:
        return {
            "jsonrpc": "2.0",
            "error": {"code": -32700, "message": "Parse error"}
        }
    
    method = rpc.get("method", "")
    response = {"jsonrpc": "2.0", "id": rpc.get("id")}
    
    logger.info(f"Received method: {method}")
    
    # Route to appropriate handler
    if method == "initialize":
        response["result"] = {
            "server": "aurora-health-mcp",
            "version": "1.0.0",
            "capabilities": ["tools", "streaming"]
        }
        logger.info("Initialization received")
        
    elif method == "list_tools":
        response["result"] = await list_tools()
        logger.info("Tool list served")
        
    elif method == "call_tool":
        params = rpc.get("params", {})
        tool_name = params.get("name", "")
        tool_args = params.get("arguments", {})
        
        logger.info(f"Calling tool: {tool_name} with args: {tool_args}")
        
        # Route to specific tool
        if tool_name == "search_hospitals":
            result = await search_hospitals(**tool_args)
        elif tool_name == "check_bed_availability":
            result = await check_bed_availability(**tool_args)
        elif tool_name == "search_medical_web":
            result = await search_medical_web(**tool_args)
        elif tool_name == "get_emergency_hospitals":
            result = await get_emergency_hospitals(**tool_args)
        elif tool_name == "search_medical_knowledge":
            result = await search_medical_knowledge(**tool_args)
        elif tool_name == "get_patient_info":
            result = await get_patient_info(**tool_args)
        else:
            response["error"] = {
                "code": -32601,
                "message": f"Unknown tool: {tool_name}"
            }
            return response
        
        response["result"] = {"content": result}
        logger.info(f"Tool result: {result[:200]}...")
        
    elif method == "shutdown":
        response["result"] = "Server shutdown acknowledged"
        logger.info("Shutdown requested")
        
    else:
        response["error"] = {
            "code": -32601,
            "message": f"Method '{method}' not found"
        }
        logger.warning(f"Unknown method: {method}")
    
    return response


# ============================================================================
# STREAMING ENDPOINT (SSE)
# ============================================================================

@app.get("/stream")
async def mcp_stream(tool: str, **kwargs):
    """Server-Sent Events endpoint for streaming results"""
    
    async def generate():
        try:
            if tool == "search_hospitals":
                result = await search_hospitals(**kwargs)
            elif tool == "search_medical_web":
                result = await search_medical_web(**kwargs)
            else:
                result = f"Unknown tool: {tool}"
            
            # Stream result
            yield f"data: {json.dumps({'result': result})}\n\n"
            
        except Exception as e:
            logger.error(f"Streaming error: {e}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")


# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    
    # Check database
    conn = get_db_connection()
    db_status = "connected" if conn else "disconnected"
    if conn:
        conn.close()
    
    return {
        "status": "healthy",
        "server": "aurora-health-mcp",
        "version": "1.0.0",
        "database": db_status,
        "tools_available": 6
    }


# ============================================================================
# STARTUP EVENT
# ============================================================================

@app.on_event("startup")
async def startup_event():
    logger.info("🏥 Starting Aurora Health MCP Server...")
    logger.info(f"   Listening at http://{HTTP_HOST}:{HTTP_PORT}/")
    logger.info(f"   Health check: http://localhost:{HTTP_PORT}/health")
    logger.info(f"   Database: {DB_CONFIG['database']}@{DB_CONFIG['host']}")
    print(f"\n✅ Aurora Health MCP Server running on http://localhost:{HTTP_PORT}/\n")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    uvicorn.run(app, host=HTTP_HOST, port=HTTP_PORT)
