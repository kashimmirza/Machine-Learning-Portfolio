from fastapi.testclient import TestClient
from api.main import app
import uuid

client = TestClient(app)

def test_create_user():
    wallet = f"0x{uuid.uuid4().hex}"
    response = client.post("/users", json={"wallet_address": wallet, "role": "requester"})
    assert response.status_code == 200
    data = response.json()
    assert data["wallet_address"] == wallet
    assert data["role"] == "requester"
    assert "id" in data
    return data

def test_create_task_flow():
    # 1. Create Requester
    requester = test_create_user()
    
    # 2. Create Task
    task_data = {
        "description": "Test Task",
        "price_mnee": 10.0,
        "creator_id": requester["id"]
    }
    response = client.post("/tasks", json=task_data)
    assert response.status_code == 200
    task = response.json()
    assert task["description"] == "Test Task"
    assert task["creator_id"] == requester["id"]
    assert task["status"] == "pending"
    
    # 3. Complete Task (Simulate Worker)
    worker_wallet = f"0x{uuid.uuid4().hex}"
    worker_response = client.post("/users", json={"wallet_address": worker_wallet, "role": "worker"})
    worker = worker_response.json()
    
    complete_data = {
        "status": "completed",
        "result_data": "Task result",
        "worker_id": worker["id"]
    }
    response = client.post(f"/tasks/{task['id']}/complete", json=complete_data)
    assert response.status_code == 200
    updated_task = response.json()
    assert updated_task["status"] == "completed"
    assert updated_task["worker_id"] == worker["id"]
    assert updated_task["result_data"] == "Task result"
    
    # 4. Validate Task (Simulate Creator)
    response = client.post(f"/tasks/{task['id']}/validate")
    assert response.status_code == 200
    validated_task = response.json()
    assert validated_task["status"] == "validated"

def test_content_flow():
    # 1. Create Creator
    creator_wallet = f"0x{uuid.uuid4().hex}"
    creator_response = client.post("/users", json={"wallet_address": creator_wallet, "role": "creator"})
    creator = creator_response.json()
    
    # 2. Create Content
    content_data = {
        "title": "Premium Content",
        "price_mnee": 5.0,
        "content_data": "http://example.com/secret",
        "creator_id": creator["id"]
    }
    response = client.post("/content", json=content_data)
    assert response.status_code == 200
    content = response.json()
    
    # 3. Access Content as Creator (Should succeed)
    response = client.get(f"/content/{content['id']}?user_id={creator['id']}")
    assert response.status_code == 200
    assert response.json()["content_data"] == "http://example.com/secret"
    
    # 4. Access Content as Other User (Should fail)
    other_wallet = f"0x{uuid.uuid4().hex}"
    other_response = client.post("/users", json={"wallet_address": other_wallet, "role": "requester"})
    other = other_response.json()
    
    response = client.get(f"/content/{content['id']}?user_id={other['id']}")
    assert response.status_code == 403
