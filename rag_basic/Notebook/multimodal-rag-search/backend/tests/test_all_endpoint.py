#!/usr/bin/env python3
"""
Comprehensive Test Script for Multimodal RAG Search System
Tests all endpoints and functionalities with simulated mock data
"""

import requests
import json
import time
import numpy as np
from typing import Dict, List
from dataclasses import dataclass
import logging
from colorama import Fore, Style, init

# Initialize colorama for colored output
init(autoreset=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class TestResult:
    """Test result container"""
    test_name: str
    passed: bool
    duration_ms: float
    message: str
    response_data: Dict = None


class MultimodalSearchTester:
    """Comprehensive test suite for multimodal search system"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results: List[TestResult] = []
        self.session = requests.Session()
    
    def print_header(self, text: str):
        """Print formatted header"""
        print(f"\n{Fore.CYAN}{'='*80}")
        print(f"{Fore.CYAN}{text.center(80)}")
        print(f"{Fore.CYAN}{'='*80}\n")
    
    def print_test_result(self, result: TestResult):
        """Print formatted test result"""
        status = f"{Fore.GREEN}✓ PASS" if result.passed else f"{Fore.RED}✗ FAIL"
        print(f"{status} | {result.test_name} | {result.duration_ms:.0f}ms")
        if not result.passed:
            print(f"  {Fore.YELLOW}└─ {result.message}")
    
    def print_summary(self):
        """Print test summary"""
        self.print_header("TEST SUMMARY")
        
        passed = sum(1 for r in self.results if r.passed)
        failed = sum(1 for r in self.results if not r.passed)
        total = len(self.results)
        
        print(f"Total Tests: {total}")
        print(f"{Fore.GREEN}Passed: {passed}")
        print(f"{Fore.RED}Failed: {failed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if failed > 0:
            print(f"\n{Fore.RED}Failed Tests:")
            for result in self.results:
                if not result.passed:
                    print(f"  - {result.test_name}: {result.message}")
    
    def run_test(self, test_func, test_name: str):
        """Run a single test"""
        logger.info(f"Running: {test_name}")
        start_time = time.time()
        
        try:
            test_func()
            duration = (time.time() - start_time) * 1000
            result = TestResult(
                test_name=test_name,
                passed=True,
                duration_ms=duration,
                message="Success"
            )
        except AssertionError as e:
            duration = (time.time() - start_time) * 1000
            result = TestResult(
                test_name=test_name,
                passed=False,
                duration_ms=duration,
                message=str(e)
            )
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            result = TestResult(
                test_name=test_name,
                passed=False,
                duration_ms=duration,
                message=f"Error: {str(e)}"
            )
        
        self.results.append(result)
        self.print_test_result(result)
        return result
    
    # ========================================================================
    # Health & System Tests
    # ========================================================================
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.session.get(f"{self.base_url}/api/v1/health")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert data['status'] == 'healthy', f"System not healthy: {data}"
        assert 'services' in data, "Missing services status"
        assert 'version' in data, "Missing version info"
        
        logger.info(f"System health: {json.dumps(data, indent=2)}")
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = self.session.get(f"{self.base_url}/")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert 'name' in data, "Missing API name"
        assert 'version' in data, "Missing version"
    
    # ========================================================================
    # Multimodal Search Tests
    # ========================================================================
    
    def test_multimodal_search_basic(self):
        """Test basic multimodal search with lion query"""
        payload = {
            "query": "lion",
            "modalities": ["all"],
            "limit": 20,
            "offset": 0
        }
        
        response = self.session.post(
            f"{self.base_url}/api/v1/search/multimodal",
            json=payload
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert 'results' in data, "Missing results"
        assert 'total_results' in data, "Missing total count"
        assert 'execution_time_ms' in data, "Missing execution time"
        assert data['query'] == 'lion', "Query mismatch"
        
        # Validate execution time
        assert data['execution_time_ms'] < 500, "Search too slow"
        
        logger.info(f"Found {data['total_results']} results in {data['execution_time_ms']:.2f}ms")
    
    def test_multimodal_search_filtered(self):
        """Test filtered multimodal search (images and videos only)"""
        payload = {
            "query": "lion",
            "modalities": ["image", "video"],
            "limit": 15,
            "offset": 0
        }
        
        response = self.session.post(
            f"{self.base_url}/api/v1/search/multimodal",
            json=payload
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        
        # Verify only requested modalities returned
        for result in data['results']:
            assert result['modality'] in ['image', 'video'], \
                f"Unexpected modality: {result['modality']}"
    
    def test_multimodal_search_with_filters(self):
        """Test search with metadata filters"""
        payload = {
            "query": "lion",
            "modalities": ["all"],
            "limit": 10,
            "filters": {
                "category": "wildlife",
                "min_score": 0.8
            }
        }
        
        response = self.session.post(
            f"{self.base_url}/api/v1/search/multimodal",
            json=payload
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    def test_multimodal_search_pagination(self):
        """Test search pagination"""
        # First page
        payload1 = {"query": "lion", "limit": 5, "offset": 0}
        response1 = self.session.post(
            f"{self.base_url}/api/v1/search/multimodal",
            json=payload1
        )
        
        # Second page
        payload2 = {"query": "lion", "limit": 5, "offset": 5}
        response2 = self.session.post(
            f"{self.base_url}/api/v1/search/multimodal",
            json=payload2
        )
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        results1 = response1.json()['results']
        results2 = response2.json()['results']
        
        # Verify different results
        if results1 and results2:
            assert results1[0]['id'] != results2[0]['id'], "Pagination not working"
    
    # ========================================================================
    # Modality-Specific Search Tests
    # ========================================================================
    
    def test_text_search(self):
        """Test text-only search"""
        response = self.session.post(
            f"{self.base_url}/api/v1/search/text",
            params={"query": "lion conservation", "limit": 10}
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        
        # Verify all results are text modality
        for result in data['results']:
            assert result['modality'] == 'text', \
                f"Expected text, got {result['modality']}"
    
    def test_image_search(self):
        """Test image-only search"""
        response = self.session.post(
            f"{self.base_url}/api/v1/search/image",
            params={"query": "lion in savanna", "limit": 10}
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        
        # Verify all results are images
        for result in data['results']:
            assert result['modality'] == 'image'
            assert 'url' in result
            assert 'thumbnail_url' in result
    
    def test_video_search(self):
        """Test video-only search"""
        response = self.session.post(
            f"{self.base_url}/api/v1/search/video",
            params={"query": "lion documentary", "limit": 10}
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        
        # Verify all results are videos
        for result in data['results']:
            assert result['modality'] == 'video'
            assert 'duration' in result
    
    def test_audio_search(self):
        """Test audio-only search"""
        response = self.session.post(
            f"{self.base_url}/api/v1/search/audio",
            params={"query": "lion roar", "limit": 10}
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        
        # Verify all results are audio
        for result in data['results']:
            assert result['modality'] == 'audio'
    
    # ========================================================================
    # Data Ingestion Tests
    # ========================================================================
    
    def test_bulk_ingestion_text(self):
        """Test bulk text data ingestion"""
        items = [
            {
                "id": f"test_text_{i}",
                "title": f"Test Article {i}",
                "description": "Test article about lions",
                "url": f"https://example.com/article-{i}",
                "content": "Lions are majestic creatures..."
            }
            for i in range(5)
        ]
        
        payload = {
            "items": items,
            "modality": "text",
            "batch_size": 10
        }
        
        response = self.session.post(
            f"{self.base_url}/api/v1/ingest/bulk",
            json=payload
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert data['status'] == 'accepted'
        assert 'estimated_time_seconds' in data
    
    def test_bulk_ingestion_images(self):
        """Test bulk image data ingestion"""
        items = [
            {
                "id": f"test_img_{i}",
                "title": f"Lion Image {i}",
                "url": f"https://cdn.example.com/lion-{i}.jpg",
                "thumbnail_url": f"https://cdn.example.com/thumb-{i}.jpg",
                "metadata": {"category": "wildlife"}
            }
            for i in range(5)
        ]
        
        payload = {
            "items": items,
            "modality": "image",
            "batch_size": 10
        }
        
        response = self.session.post(
            f"{self.base_url}/api/v1/ingest/bulk",
            json=payload
        )
        assert response.status_code == 200
    
    def test_bulk_ingestion_empty(self):
        """Test bulk ingestion with empty items"""
        payload = {
            "items": [],
            "modality": "text",
            "batch_size": 10
        }
        
        response = self.session.post(
            f"{self.base_url}/api/v1/ingest/bulk",
            json=payload
        )
        assert response.status_code == 400, "Should reject empty items"
    
    # ========================================================================
    # Validation Tests
    # ========================================================================
    
    def test_search_empty_query(self):
        """Test search with empty query"""
        payload = {
            "query": "",
            "modalities": ["all"],
            "limit": 10
        }
        
        response = self.session.post(
            f"{self.base_url}/api/v1/search/multimodal",
            json=payload
        )
        assert response.status_code == 422, "Should reject empty query"
    
    def test_search_invalid_limit(self):
        """Test search with invalid limit"""
        # Exceed max limit
        payload = {"query": "lion", "limit": 150}
        response = self.session.post(
            f"{self.base_url}/api/v1/search/multimodal",
            json=payload
        )
        assert response.status_code == 422, "Should reject limit > 100"
        
        # Below minimum
        payload = {"query": "lion", "limit": 0}
        response = self.session.post(
            f"{self.base_url}/api/v1/search/multimodal",
            json=payload
        )
        assert response.status_code == 422, "Should reject limit < 1"
    
    def test_search_invalid_modality(self):
        """Test search with invalid modality"""
        payload = {
            "query": "lion",
            "modalities": ["invalid_modality"],
            "limit": 10
        }
        
        response = self.session.post(
            f"{self.base_url}/api/v1/search/multimodal",
            json=payload
        )
        # Should either reject or ignore invalid modality
        assert response.status_code in [200, 422]
    
    # ========================================================================
    # Performance Tests
    # ========================================================================
    
    def test_search_response_time(self):
        """Test that search responds within acceptable time"""
        queries = ["lion", "technology", "nature", "music", "sports"]
        
        for query in queries:
            start = time.time()
            response = self.session.post(
                f"{self.base_url}/api/v1/search/multimodal",
                json={"query": query, "limit": 20}
            )
            duration = (time.time() - start) * 1000
            
            assert response.status_code == 200
            assert duration < 500, f"Query '{query}' took {duration:.0f}ms (>500ms)"
    
    def test_concurrent_searches(self):
        """Test handling concurrent search requests"""
        import concurrent.futures
        
        def perform_search(query):
            response = self.session.post(
                f"{self.base_url}/api/v1/search/multimodal",
                json={"query": query, "limit": 10}
            )
            return response.status_code == 200
        
        queries = ["lion", "tiger", "bear", "elephant", "giraffe"]
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(perform_search, queries))
        
        assert all(results), "Some concurrent searches failed"
    
    # ========================================================================
    # Result Quality Tests
    # ========================================================================
    
    def test_result_schema(self):
        """Test that results follow expected schema"""
        response = self.session.post(
            f"{self.base_url}/api/v1/search/multimodal",
            json={"query": "lion", "limit": 1}
        )
        assert response.status_code == 200
        
        data = response.json()
        
        # Verify response structure
        required_fields = ['query', 'total_results', 'returned_results', 
                          'modalities', 'results', 'execution_time_ms']
        for field in required_fields:
            assert field in data, f"Missing field: {field}"
        
        # Verify result item structure
        if data['results']:
            result = data['results'][0]
            result_fields = ['id', 'modality', 'title', 'url', 'score', 'created_at']
            for field in result_fields:
                assert field in result, f"Result missing field: {field}"
            
            # Validate score range
            assert 0 <= result['score'] <= 1, f"Invalid score: {result['score']}"
    
    def test_score_ordering(self):
        """Test that results are ordered by relevance score"""
        response = self.session.post(
            f"{self.base_url}/api/v1/search/multimodal",
            json={"query": "lion", "limit": 10}
        )
        assert response.status_code == 200
        
        results = response.json()['results']
        
        if len(results) > 1:
            scores = [r['score'] for r in results]
            assert scores == sorted(scores, reverse=True), \
                "Results not ordered by score"
    
    def test_aggregations(self):
        """Test that aggregations are provided"""
        response = self.session.post(
            f"{self.base_url}/api/v1/search/multimodal",
            json={"query": "lion", "limit": 20}
        )
        assert response.status_code == 200
        
        data = response.json()
        
        if 'aggregations' in data:
            assert 'by_modality' in data['aggregations']
            
            modality_counts = data['aggregations']['by_modality']
            total_count = sum(modality_counts.values())
            assert total_count <= 20, "Aggregation counts incorrect"
    
    # ========================================================================
    # Learning & Adaptation Tests
    # ========================================================================
    
    def test_continuous_learning_simulation(self):
        """Simulate continuous learning from user interactions"""
        # Simulate multiple searches
        queries = ["lion", "lion king", "african wildlife", "big cats"]
        
        for query in queries:
            response = self.session.post(
                f"{self.base_url}/api/v1/search/multimodal",
                json={"query": query, "limit": 5}
            )
            assert response.status_code == 200
            
            # In a real system, user interactions would be recorded here
            # and used for continuous learning
    
    # ========================================================================
    # Edge Case Tests
    # ========================================================================
    
    def test_very_long_query(self):
        """Test search with very long query"""
        long_query = " ".join(["lion"] * 50)  # 50 words
        
        payload = {"query": long_query, "limit": 10}
        response = self.session.post(
            f"{self.base_url}/api/v1/search/multimodal",
            json=payload
        )
        
        # Should either truncate or reject
        assert response.status_code in [200, 422]
    
    def test_special_characters_query(self):
        """Test search with special characters"""
        queries = ["lion's roar", "lion & tiger", "lion/tiger", "lion@safari"]
        
        for query in queries:
            response = self.session.post(
                f"{self.base_url}/api/v1/search/multimodal",
                json={"query": query, "limit": 5}
            )
            assert response.status_code == 200, f"Failed on query: {query}"
    
    def test_unicode_query(self):
        """Test search with Unicode characters"""
        queries = ["狮子", "león", "лев", "🦁"]
        
        for query in queries:
            response = self.session.post(
                f"{self.base_url}/api/v1/search/multimodal",
                json={"query": query, "limit": 5}
            )
            assert response.status_code == 200, f"Failed on query: {query}"
    
    # ========================================================================
    # Run All Tests
    # ========================================================================
    
    def run_all_tests(self):
        """Run complete test suite"""
        self.print_header("MULTIMODAL RAG SEARCH SYSTEM - COMPREHENSIVE TEST SUITE")
        
        # Health & System Tests
        self.print_header("HEALTH & SYSTEM TESTS")
        self.run_test(self.test_health_check, "Health Check")
        self.run_test(self.test_root_endpoint, "Root Endpoint")
        
        # Multimodal Search Tests
        self.print_header("MULTIMODAL SEARCH TESTS")
        self.run_test(self.test_multimodal_search_basic, "Basic Multimodal Search")
        self.run_test(self.test_multimodal_search_filtered, "Filtered Multimodal Search")
        self.run_test(self.test_multimodal_search_with_filters, "Search with Filters")
        self.run_test(self.test_multimodal_search_pagination, "Search Pagination")
        
        # Modality-Specific Tests
        self.print_header("MODALITY-SPECIFIC SEARCH TESTS")
        self.run_test(self.test_text_search, "Text-Only Search")
        self.run_test(self.test_image_search, "Image-Only Search")
        self.run_test(self.test_video_search, "Video-Only Search")
        self.run_test(self.test_audio_search, "Audio-Only Search")
        
        # Data Ingestion Tests
        self.print_header("DATA INGESTION TESTS")
        self.run_test(self.test_bulk_ingestion_text, "Bulk Text Ingestion")
        self.run_test(self.test_bulk_ingestion_images, "Bulk Image Ingestion")
        self.run_test(self.test_bulk_ingestion_empty, "Empty Items Validation")
        
        # Validation Tests
        self.print_header("INPUT VALIDATION TESTS")
        self.run_test(self.test_search_empty_query, "Empty Query Validation")
        self.run_test(self.test_search_invalid_limit, "Invalid Limit Validation")
        self.run_test(self.test_search_invalid_modality, "Invalid Modality Handling")
        
        # Performance Tests
        self.print_header("PERFORMANCE TESTS")
        self.run_test(self.test_search_response_time, "Response Time Check")
        self.run_test(self.test_concurrent_searches, "Concurrent Search Handling")
        
        # Result Quality Tests
        self.print_header("RESULT QUALITY TESTS")
        self.run_test(self.test_result_schema, "Result Schema Validation")
        self.run_test(self.test_score_ordering, "Score Ordering")
        self.run_test(self.test_aggregations, "Aggregations")
        
        # Learning Tests
        self.print_header("LEARNING & ADAPTATION TESTS")
        self.run_test(self.test_continuous_learning_simulation, "Continuous Learning Simulation")
        
        # Edge Case Tests
        self.print_header("EDGE CASE TESTS")
        self.run_test(self.test_very_long_query, "Very Long Query")
        self.run_test(self.test_special_characters_query, "Special Characters")
        self.run_test(self.test_unicode_query, "Unicode Query")
        
        # Print summary
        self.print_summary()
        
        return sum(1 for r in self.results if not r.passed) == 0


def main():
    """Main test execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Test Multimodal RAG Search System')
    parser.add_argument(
        '--url',
        default='http://localhost:8000',
        help='Base URL of the API (default: http://localhost:8000)'
    )
    args = parser.parse_args()
    
    print(f"{Fore.CYAN}Starting test suite...")
    print(f"{Fore.CYAN}API URL: {args.url}\n")
    
    tester = MultimodalSearchTester(base_url=args.url)
    success = tester.run_all_tests()
    
    exit_code = 0 if success else 1
    exit(exit_code)


if __name__ == "__main__":
    main()