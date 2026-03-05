import asyncio
import sys
import os

# Ensure backend path is in sys.path
sys.path.append(os.path.join(os.getcwd()))

from app.agents.orchestrator import agent_orchestrator

async def test_agents():
    print("--- Starting Agentic Backend Verification ---")
    
    # Test 1: Vitals Agent (High Heart Rate)
    print("\n[Test 1] Testing Vitals Agent (Elevated Heart Rate)...")
    vitals_data = {"heart_rate": 110, "blood_pressure": "120/80"}
    result_vitals = await agent_orchestrator.route_request("vitals", vitals_data)
    print(f"Result: {result_vitals}")
    assert result_vitals["success"] is True
    assert result_vitals["result"]["status"] == "Elevated Heart Rate"
    
    # Test 2: Nutrition Agent
    print("\n[Test 2] Testing Nutrition Agent (High Calorie)...")
    nutrition_data = {"meal": "Pizza", "calories": 900}
    result_nutrition = await agent_orchestrator.route_request("nutrition", nutrition_data)
    print(f"Result: {result_nutrition}")
    assert result_nutrition["success"] is True
    assert result_nutrition["result"]["nutritional_assessment"] == "High calorie meal detected."
    
    # Test 3: Broadcast
    print("\n[Test 3] Testing Broadcast...")
    broadcast_data = {"heart_rate": 70, "calories": 500}
    result_broadcast = await agent_orchestrator.broadcast(broadcast_data)
    print(f"Result: {result_broadcast}")
    assert result_broadcast["type"] == "comprehensive_report"
    
    print("\n--- Verification Complete: ALL TESTS PASSED ---")

if __name__ == "__main__":
    asyncio.run(test_agents())
