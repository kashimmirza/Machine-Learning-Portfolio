import asyncio
import time
import httpx
import random
from typing import List

# Configuration
BASE_URL = "http://localhost:8000/api/v1"
CONCURRENT_USERS = 10
TOTAL_REQUESTS = 50

QUESTIONS = [
    "What are the top 5 products?",
    "Show me sales for last month.",
    "Who is the best customer?",
    "List all employees.",
    "What is the total revenue?"
]

async def simulate_user(client: httpx.AsyncClient, user_id: int):
    """
    Simulates a user logging in and asking a question.
    """
    # 1. Login (Auto-register flow)
    email = f"user{user_id}@test.com"
    password = "Password123!"
    
    try:
        # Try login
        login_res = await client.post(f"{BASE_URL}/auth/login", data={"username": email, "password": password, "grant_type": "password"})
        if login_res.status_code == 401:
            # Register if failed
            await client.post(f"{BASE_URL}/auth/register", json={"email": email, "password": password})
            login_res = await client.post(f"{BASE_URL}/auth/login", data={"username": email, "password": password, "grant_type": "password"})
            
        token = login_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. Create Session
        session_res = await client.post(f"{BASE_URL}/auth/session", headers=headers)
        session_id = session_res.json()["session_id"]
        
        # 3. Ask Question
        question = random.choice(QUESTIONS)
        start = time.time()
        chat_res = await client.post(
            f"{BASE_URL}/chatbot/chat", 
            headers=headers,
            json={"message": question, "session_id": session_id}
        )
        duration = time.time() - start
        
        status = "SUCCESS" if chat_res.status_code == 200 else "FAIL"
        print(f"User {user_id}: {status} in {duration:.2f}s")
        return {"duration": duration, "status": status}
        
    except Exception as e:
        print(f"User {user_id}: ERROR - {str(e)}")
        return {"duration": 0, "status": "ERROR"}

async def run_stress_test():
    print(f"Starting Stress Test: {CONCURRENT_USERS} users, {TOTAL_REQUESTS} total requests...")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        tasks = []
        for i in range(CONCURRENT_USERS):
            tasks.append(simulate_user(client, i))
        
        results = await asyncio.gather(*tasks)
        
    # Analysis
    success_count = sum(1 for r in results if r["status"] == "SUCCESS")
    avg_conf = sum(r["duration"] for r in results) / len(results)
    
    print("\n--- Results ---")
    print(f"Successful: {success_count}/{len(results)}")
    print(f"Avg Latency: {avg_conf:.2f}s")

if __name__ == "__main__":
    asyncio.run(run_stress_test())
