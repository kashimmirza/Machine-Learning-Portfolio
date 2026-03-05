# backend/tests/test_search.py
"""
Test cases for search endpoints
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestSearchEndpoints:
    """Test search functionality"""
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "services" in data
    
    def test_multimodal_search_basic(self):
        """Test basic multimodal search"""
        payload = {
            "query": "lion",
            "modalities": ["all"],
            "limit": 10,
            "offset": 0
        }
        
        response = client.post("/api/v1/search/multimodal", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert "results" in data
        assert "total_results" in data
        assert "execution_time_ms" in data
        assert data["query"] == "lion"
    
    def test_multimodal_search_filtered(self):
        """Test filtered multimodal search"""
        payload = {
            "query": "lion",
            "modalities": ["image", "video"],
            "limit": 20,
            "offset": 0,
            "filters": {
                "category": "wildlife"
            }
        }
        
        response = client.post("/api/v1/search/multimodal", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["results"]) <= 20
        
        # Check that only requested modalities are returned
        for result in data["results"]:
            assert result["modality"] in ["image", "video"]
    
    def test_text_search(self):
        """Test text-specific search"""
        response = client.post(
            "/api/v1/search/text",
            params={"query": "lion conservation", "limit": 10}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify all results are text modality
        for result in data["results"]:
            assert result["modality"] == "text"
    
    def test_image_search(self):
        """Test image-specific search"""
        response = client.post(
            "/api/v1/search/image",
            params={"query": "lion", "limit": 10}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify all results are image modality
        for result in data["results"]:
            assert result["modality"] == "image"
            assert "url" in result
            assert "thumbnail_url" in result
    
    def test_video_search(self):
        """Test video-specific search"""
        response = client.post(
            "/api/v1/search/video",
            params={"query": "lion documentary", "limit": 10}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify all results are video modality
        for result in data["results"]:
            assert result["modality"] == "video"
            assert "duration" in result
    
    def test_audio_search(self):
        """Test audio-specific search"""
        response = client.post(
            "/api/v1/search/audio",
            params={"query": "lion roar", "limit": 10}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify all results are audio modality
        for result in data["results"]:
            assert result["modality"] == "audio"
    
    def test_search_empty_query(self):
        """Test search with empty query"""
        payload = {
            "query": "",
            "modalities": ["all"],
            "limit": 10
        }
        
        response = client.post("/api/v1/search/multimodal", json=payload)
        assert response.status_code == 422  # Validation error
    
    def test_search_pagination(self):
        """Test search pagination"""
        # First page
        response1 = client.post(
            "/api/v1/search/multimodal",
            json={"query": "lion", "limit": 5, "offset": 0}
        )
        
        # Second page
        response2 = client.post(
            "/api/v1/search/multimodal",
            json={"query": "lion", "limit": 5, "offset": 5}
        )
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        results1 = response1.json()["results"]
        results2 = response2.json()["results"]
        
        # Verify different results (if enough data exists)
        if results1 and results2:
            assert results1[0]["id"] != results2[0]["id"]
    
    def test_search_limit_bounds(self):
        """Test search limit boundaries"""
        # Test max limit
        response = client.post(
            "/api/v1/search/multimodal",
            json={"query": "lion", "limit": 150}
        )
        assert response.status_code == 422  # Exceeds max limit of 100
        
        # Test minimum limit
        response = client.post(
            "/api/v1/search/multimodal",
            json={"query": "lion", "limit": 0}
        )
        assert response.status_code == 422  # Below minimum limit of 1
    
    def test_search_result_schema(self):
        """Test search result schema compliance"""
        response = client.post(
            "/api/v1/search/multimodal",
            json={"query": "lion", "limit": 1}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "query" in data
        assert "total_results" in data
        assert "returned_results" in data
        assert "modalities" in data
        assert "results" in data
        assert "execution_time_ms" in data
        
        # Verify result item structure
        if data["results"]:
            result = data["results"][0]
            assert "id" in result
            assert "modality" in result
            assert "title" in result
            assert "url" in result
            assert "score" in result
            assert 0 <= result["score"] <= 1
            assert "created_at" in result
    
    def test_bulk_ingest_validation(self):
        """Test bulk ingestion validation"""
        payload = {
            "items": [],
            "modality": "text",
            "batch_size": 100
        }
        
        response = client.post("/api/v1/ingest/bulk", json=payload)
        assert response.status_code == 400  # No items provided


class TestPerformance:
    """Test performance requirements"""
    
    def test_search_response_time(self):
        """Test that search responds within acceptable time"""
        import time
        
        start = time.time()
        response = client.post(
            "/api/v1/search/multimodal",
            json={"query": "lion", "limit": 20}
        )
        end = time.time()
        
        assert response.status_code == 200
        response_time = (end - start) * 1000  # Convert to ms
        
        # Should respond within 500ms (including network)
        assert response_time < 500


if __name__ == "__main__":
    pytest.main([__file__, "-v"])