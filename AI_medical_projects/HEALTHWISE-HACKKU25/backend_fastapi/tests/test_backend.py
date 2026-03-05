import requests
import json

BASE_URL = "http://localhost:8000"

def test_root():
    """Verify backend is reachable"""
    try:
        resp = requests.get(f"{BASE_URL}/")
        print(f"[ROOT] Status: {resp.status_code}, Response: {resp.json()}")
        assert resp.status_code == 200
    except Exception as e:
        print(f"[ROOT] FAILED: {e}")

def test_vitals_agent():
    """Verify Vitals Agent Logic"""
    payload = {
        "agent_type": "vitals",
        "data": {"heart_rate": 110}
    }
    # Note: Authorization header omitted for basic dev test (or add dummy token)
    try:
        resp = requests.post(f"{BASE_URL}/api/agents/chat", json=payload)
        print(f"[VITALS] Status: {resp.status_code}, Response: {resp.json()}")
        assert resp.status_code == 200
        assert resp.json().get("alert") is True
    except Exception as e:
        print(f"[VITALS] FAILED: {e}")

if __name__ == "__main__":
    print("--- Starting Backend Tests ---")
    test_root()
    test_vitals_agent()
    print("--- Tests Finished ---")
