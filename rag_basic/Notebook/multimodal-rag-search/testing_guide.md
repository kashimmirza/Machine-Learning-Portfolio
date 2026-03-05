<!-- @format -->

# 🧪 Testing Guide - Multimodal RAG Search System

## Quick Test Execution

### 1. Install Test Dependencies

```bash
pip install requests colorama
```

### 2. Start the System

```bash
# Using Docker Compose (recommended)
chmod +x setup.sh
./setup.sh
# Select option 1

# Wait for services to start (1-2 minutes)
```

### 3. Run Tests

```bash
# Run all tests
python test_all_endpoints.py

# Or with custom URL
python test_all_endpoints.py --url http://your-server:8000
```

## Test Suite Coverage

### Health & System Tests (2 tests)

- ✅ Health check endpoint
- ✅ Root endpoint

### Multimodal Search Tests (4 tests)

- ✅ Basic search (all modalities)
- ✅ Filtered search (specific modalities)
- ✅ Search with metadata filters
- ✅ Pagination

### Modality-Specific Tests (4 tests)

- ✅ Text-only search
- ✅ Image-only search
- ✅ Video-only search
- ✅ Audio-only search

### Data Ingestion Tests (3 tests)

- ✅ Bulk text ingestion
- ✅ Bulk image ingestion
- ✅ Empty items validation

### Validation Tests (3 tests)

- ✅ Empty query rejection
- ✅ Invalid limit rejection
- ✅ Invalid modality handling

### Performance Tests (2 tests)

- ✅ Response time check (<500ms)
- ✅ Concurrent request handling

### Result Quality Tests (3 tests)

- ✅ Schema validation
- ✅ Score ordering
- ✅ Aggregations

### Learning Tests (1 test)

- ✅ Continuous learning simulation

### Edge Case Tests (3 tests)

- ✅ Very long query
- ✅ Special characters
- ✅ Unicode support

## Expected Output

```
================================================================================
         MULTIMODAL RAG SEARCH SYSTEM - COMPREHENSIVE TEST SUITE
================================================================================

HEALTH & SYSTEM TESTS
✓ PASS | Health Check | 45ms
✓ PASS | Root Endpoint | 12ms

MULTIMODAL SEARCH TESTS
✓ PASS | Basic Multimodal Search | 156ms
✓ PASS | Filtered Multimodal Search | 142ms
✓ PASS | Search with Filters | 138ms
✓ PASS | Search Pagination | 267ms

MODALITY-SPECIFIC SEARCH TESTS
✓ PASS | Text-Only Search | 134ms
✓ PASS | Image-Only Search | 145ms
✓ PASS | Video-Only Search | 139ms
✓ PASS | Audio-Only Search | 141ms

DATA INGESTION TESTS
✓ PASS | Bulk Text Ingestion | 89ms
✓ PASS | Bulk Image Ingestion | 87ms
✓ PASS | Empty Items Validation | 23ms

INPUT VALIDATION TESTS
✓ PASS | Empty Query Validation | 18ms
✓ PASS | Invalid Limit Validation | 42ms
✓ PASS | Invalid Modality Handling | 156ms

PERFORMANCE TESTS
✓ PASS | Response Time Check | 723ms
✓ PASS | Concurrent Search Handling | 445ms

RESULT QUALITY TESTS
✓ PASS | Result Schema Validation | 134ms
✓ PASS | Score Ordering | 142ms
✓ PASS | Aggregations | 138ms

LEARNING & ADAPTATION TESTS
✓ PASS | Continuous Learning Simulation | 589ms

EDGE CASE TESTS
✓ PASS | Very Long Query | 145ms
✓ PASS | Special Characters | 567ms
✓ PASS | Unicode Query | 598ms

================================================================================
                              TEST SUMMARY
================================================================================
Total Tests: 30
Passed: 30
Failed: 0
Success Rate: 100.0%
```

## Manual Testing

### Test Health Endpoint

```bash
curl http://localhost:8000/api/v1/health
```

### Test Search

```bash
curl -X POST http://localhost:8000/api/v1/search/multimodal \
  -H "Content-Type: application/json" \
  -d '{
    "query": "lion",
    "modalities": ["all"],
    "limit": 10
  }'
```

### Test Image Search

```bash
curl -X POST "http://localhost:8000/api/v1/search/image?query=lion&limit=5"
```

### Test Bulk Ingestion

```bash
curl -X POST http://localhost:8000/api/v1/ingest/bulk \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {
        "id": "test_1",
        "title": "Test Item",
        "url": "https://example.com/test"
      }
    ],
    "modality": "text",
    "batch_size": 10
  }'
```

## Interactive API Testing

### Using Swagger UI

1. Open http://localhost:8000/api/docs
2. Try the endpoints interactively
3. See request/response schemas
4. Test with different parameters

### Using curl with jq

```bash
# Pretty print JSON response
curl -s http://localhost:8000/api/v1/health | jq .

# Extract specific field
curl -s -X POST http://localhost:8000/api/v1/search/multimodal \
  -H "Content-Type: application/json" \
  -d '{"query": "lion", "limit": 5}' | \
  jq '.results[] | {title, modality, score}'
```

## Load Testing

### Using Apache Bench

```bash
# 1000 requests, 10 concurrent
ab -n 1000 -c 10 -T 'application/json' \
  -p search_payload.json \
  http://localhost:8000/api/v1/search/multimodal
```

### Using Locust

```bash
# Install locust
pip install locust

# Create locustfile.py
cat > locustfile.py << 'EOF'
from locust import HttpUser, task, between

class SearchUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def search_lion(self):
        self.client.post("/api/v1/search/multimodal", json={
            "query": "lion",
            "limit": 10
        })

    @task(2)
    def search_image(self):
        self.client.post("/api/v1/search/image", params={
            "query": "lion",
            "limit": 5
        })
EOF

# Run load test
locust -f locustfile.py --host=http://localhost:8000
# Open http://localhost:8089
```

## Troubleshooting Tests

### Test Failures

If tests fail:

1. **Check if services are running**:

   ```bash
   docker ps
   # Should see: backend, frontend, qdrant, postgres, redis
   ```

2. **Check backend logs**:

   ```bash
   docker logs multimodal-backend
   ```

3. **Verify API is accessible**:

   ```bash
   curl http://localhost:8000/api/v1/health
   ```

4. **Check Qdrant**:
   ```bash
   curl http://localhost:6333/collections
   ```

### Connection Issues

```bash
# Test network connectivity
ping localhost

# Check port availability
netstat -an | grep 8000
lsof -i :8000

# Test with different URL
python test_all_endpoints.py --url http://127.0.0.1:8000
```

### Timeout Issues

If tests timeout:

1. Increase timeout in test script
2. Check system resources (CPU, Memory)
3. Verify no other heavy processes running
4. Check Docker resource limits

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Test

on: [push, pull_request]

jobs:
 test:
  runs-on: ubuntu-latest

  steps:
   - uses: actions/checkout@v2

   - name: Start services
     run: |
      docker-compose up -d
      sleep 60  # Wait for services

   - name: Install test dependencies
     run: pip install requests colorama

   - name: Run tests
     run: python test_all_endpoints.py

   - name: Stop services
     run: docker-compose down
```

## Performance Benchmarking

### Measure Search Performance

```python
import requests
import time
import statistics

def benchmark_search(query, iterations=100):
    times = []
    for _ in range(iterations):
        start = time.time()
        response = requests.post(
            "http://localhost:8000/api/v1/search/multimodal",
            json={"query": query, "limit": 20}
        )
        times.append((time.time() - start) * 1000)

    print(f"Query: '{query}'")
    print(f"Mean: {statistics.mean(times):.2f}ms")
    print(f"Median: {statistics.median(times):.2f}ms")
    print(f"P95: {statistics.quantiles(times, n=20)[18]:.2f}ms")
    print(f"P99: {statistics.quantiles(times, n=100)[98]:.2f}ms")

benchmark_search("lion")
```

## Custom Test Scenarios

### Create Your Own Test

```python
import requests

def test_custom_scenario():
    """Test specific business logic"""
    base_url = "http://localhost:8000"

    # 1. Search for content
    search_response = requests.post(
        f"{base_url}/api/v1/search/multimodal",
        json={"query": "your query", "limit": 10}
    )

    assert search_response.status_code == 200
    results = search_response.json()

    # 2. Verify specific conditions
    assert results['total_results'] > 0
    assert results['execution_time_ms'] < 200

    # 3. Check result quality
    for result in results['results']:
        assert result['score'] >= 0.5  # High relevance
        assert result['modality'] in ['text', 'image', 'video', 'audio']

    print("✓ Custom test passed!")

if __name__ == "__main__":
    test_custom_scenario()
```

## Test Data Generation

### Generate Mock Data

```python
import random
import string

def generate_test_items(count=100):
    """Generate mock test data"""
    modalities = ['text', 'image', 'video', 'audio']
    items = []

    for i in range(count):
        item = {
            "id": f"test_{i}",
            "title": f"Test Item {i}",
            "description": ''.join(random.choices(string.ascii_letters, k=50)),
            "url": f"https://example.com/item-{i}",
            "modality": random.choice(modalities),
            "metadata": {
                "category": random.choice(['wildlife', 'nature', 'technology']),
                "score": random.random()
            }
        }
        items.append(item)

    return items

# Use for bulk ingestion tests
items = generate_test_items(1000)
```

## Continuous Testing

### Watch Mode

```bash
# Install watchdog
pip install watchdog

# Auto-run tests on file changes
watchmedo auto-restart --patterns="*.py" --recursive \
  python test_all_endpoints.py
```

---

**Test Coverage: 30+ test cases across all functionalities**

_Ensuring production-ready quality_ ✅
