# backend/services/vector_db.py
"""
Vector Database Service - Qdrant Integration
Handles all vector similarity search operations
"""

from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
    SearchRequest,
)
import logging
import os

logger = logging.getLogger(__name__)


class VectorDBService:
    """Service for managing vector database operations"""
    
    def __init__(self, host: str = "localhost", port: int = 6333):
        """Initialize Qdrant client"""
        self.client = QdrantClient(host=host, port=port)
        self.collections = {
            "text": "text_embeddings",
            "image": "image_embeddings",
            "video": "video_embeddings",
            "audio": "audio_embeddings",
        }
        
    async def initialize_collections(self):
        """Create collections if they don't exist"""
        for modality, collection_name in self.collections.items():
            try:
                # Check if collection exists
                collections = self.client.get_collections().collections
                exists = any(c.name == collection_name for c in collections)
                
                if not exists:
                    # Determine vector size based on modality
                    vector_size = {
                        "text": 384,  # sentence-transformers
                        "image": 512,  # CLIP
                        "video": 512,  # CLIP video frames
                        "audio": 768,  # Wav2Vec2
                    }[modality]
                    
                    self.client.create_collection(
                        collection_name=collection_name,
                        vectors_config=VectorParams(
                            size=vector_size,
                            distance=Distance.COSINE,
                        ),
                    )
                    logger.info(f"Created collection: {collection_name}")
                else:
                    logger.info(f"Collection already exists: {collection_name}")
                    
            except Exception as e:
                logger.error(f"Error initializing collection {collection_name}: {e}")
                raise
    
    async def insert_vectors(
        self,
        collection_name: str,
        vectors: List[List[float]],
        payloads: List[Dict[str, Any]],
        ids: Optional[List[str]] = None,
    ) -> bool:
        """Insert vectors into collection"""
        try:
            points = [
                PointStruct(
                    id=ids[i] if ids else i,
                    vector=vectors[i],
                    payload=payloads[i],
                )
                for i in range(len(vectors))
            ]
            
            self.client.upsert(
                collection_name=collection_name,
                points=points,
            )
            
            logger.info(f"Inserted {len(vectors)} vectors into {collection_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error inserting vectors: {e}")
            return False
    
    async def search(
        self,
        collection_name: str,
        query_vector: List[float],
        limit: int = 10,
        score_threshold: float = 0.0,
        filter_conditions: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Search for similar vectors"""
        try:
            # Build filter if provided
            query_filter = None
            if filter_conditions:
                conditions = []
                for key, value in filter_conditions.items():
                    conditions.append(
                        FieldCondition(
                            key=key,
                            match=MatchValue(value=value),
                        )
                    )
                query_filter = Filter(must=conditions)
            
            # Perform search
            results = self.client.search(
                collection_name=collection_name,
                query_vector=query_vector,
                limit=limit,
                score_threshold=score_threshold,
                query_filter=query_filter,
            )
            
            # Format results
            formatted_results = [
                {
                    "id": str(result.id),
                    "score": result.score,
                    "payload": result.payload,
                }
                for result in results
            ]
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error searching vectors: {e}")
            return []
    
    async def batch_search(
        self,
        searches: List[Dict[str, Any]],
    ) -> List[List[Dict[str, Any]]]:
        """Perform batch search across multiple collections"""
        try:
            requests = [
                SearchRequest(
                    vector=search["query_vector"],
                    limit=search.get("limit", 10),
                    score_threshold=search.get("score_threshold", 0.0),
                )
                for search in searches
            ]
            
            # Execute batch search
            all_results = []
            for search in searches:
                results = await self.search(
                    collection_name=search["collection_name"],
                    query_vector=search["query_vector"],
                    limit=search.get("limit", 10),
                    score_threshold=search.get("score_threshold", 0.0),
                    filter_conditions=search.get("filter_conditions"),
                )
                all_results.append(results)
            
            return all_results
            
        except Exception as e:
            logger.error(f"Error in batch search: {e}")
            return []
    
    async def delete_vectors(
        self,
        collection_name: str,
        ids: List[str],
    ) -> bool:
        """Delete vectors by IDs"""
        try:
            self.client.delete(
                collection_name=collection_name,
                points_selector=ids,
            )
            logger.info(f"Deleted {len(ids)} vectors from {collection_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting vectors: {e}")
            return False
    
    async def get_collection_info(self, collection_name: str) -> Dict[str, Any]:
        """Get information about a collection"""
        try:
            info = self.client.get_collection(collection_name=collection_name)
            return {
                "name": collection_name,
                "vectors_count": info.vectors_count,
                "points_count": info.points_count,
                "status": info.status,
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {e}")
            return {}
    
    async def close(self):
        """Close database connection"""
        try:
            self.client.close()
            logger.info("Vector DB connection closed")
        except Exception as e:
            logger.error(f"Error closing connection: {e}")


# Singleton instance
_vector_db_instance = None


def get_vector_db() -> VectorDBService:
    """Get or create vector database instance"""
    global _vector_db_instance
    if _vector_db_instance is None:
        host = os.getenv("QDRANT_HOST", "localhost")
        port = int(os.getenv("QDRANT_PORT", 6333))
        _vector_db_instance = VectorDBService(host=host, port=port)
    return _vector_db_instance