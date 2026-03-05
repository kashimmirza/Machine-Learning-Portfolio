# backend/services/openai_pinecone_service.py
"""
OpenAI + Pinecone Integration for Multimodal Search
Handles all modalities: Text, Image, Audio, Video
"""

import os
import logging
from typing import List, Dict, Any, Optional, Union
from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec
import base64
from io import BytesIO
from PIL import Image
import asyncio
from pathlib import Path

logger = logging.getLogger(__name__)


class OpenAIPineconeService:
    """
    Unified service for OpenAI + Pinecone multimodal operations
    
    GPT-4o-mini Capabilities:
    ✅ Text: Native support
    ✅ Images: Vision-capable (can analyze images)
    ✅ Audio: Via Whisper API (transcription)
    ⚠️ Video: Extract frames → analyze as images
    """
    
    def __init__(self):
        """Initialize OpenAI and Pinecone clients"""
        # OpenAI setup
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")
        
        self.client = OpenAI(api_key=self.openai_api_key)
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.embedding_model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
        
        # Pinecone setup
        self.pinecone_api_key = os.getenv("PINECONE_API_KEY")
        if not self.pinecone_api_key:
            raise ValueError("PINECONE_API_KEY not found in environment")
        
        self.pc = Pinecone(api_key=self.pinecone_api_key)
        self.index_name = os.getenv("PINECONE_INDEX_NAME", "multimodal-search-index")
        self.dimension = int(os.getenv("PINECONE_DIMENSION", "1536"))
        
        # Initialize index
        self._init_index()
        
        logger.info(f"OpenAI + Pinecone service initialized (Model: {self.model})")
    
    def _init_index(self):
        """Initialize Pinecone index if it doesn't exist"""
        try:
            # Check if index exists
            existing_indexes = self.pc.list_indexes()
            
            if self.index_name not in [idx.name for idx in existing_indexes]:
                # Create index
                self.pc.create_index(
                    name=self.index_name,
                    dimension=self.dimension,
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud=os.getenv("PINECONE_CLOUD", "aws"),
                        region=os.getenv("PINECONE_REGION", "us-east-1")
                    )
                )
                logger.info(f"Created Pinecone index: {self.index_name}")
            else:
                logger.info(f"Pinecone index exists: {self.index_name}")
            
            # Get index
            self.index = self.pc.Index(self.index_name)
            
        except Exception as e:
            logger.error(f"Error initializing Pinecone index: {e}")
            raise
    
    # ========================================================================
    # Text Embeddings (Using OpenAI)
    # ========================================================================
    
    async def generate_text_embedding(
        self,
        text: Union[str, List[str]],
        normalize: bool = True
    ) -> Union[List[float], List[List[float]]]:
        """
        Generate embeddings for text using OpenAI
        
        Args:
            text: Single text or list of texts
            normalize: Whether to normalize (handled by OpenAI)
            
        Returns:
            Embedding vector(s)
        """
        try:
            # Handle single text
            if isinstance(text, str):
                text = [text]
            
            # Generate embeddings
            response = self.client.embeddings.create(
                input=text,
                model=self.embedding_model
            )
            
            # Extract embeddings
            embeddings = [item.embedding for item in response.data]
            
            # Return single or multiple
            return embeddings[0] if len(embeddings) == 1 else embeddings
            
        except Exception as e:
            logger.error(f"Error generating text embedding: {e}")
            raise
    
    # ========================================================================
    # Image Analysis (GPT-4o-mini has vision)
    # ========================================================================
    
    async def analyze_image(
        self,
        image_data: bytes,
        prompt: str = "Describe this image in detail, including objects, scenes, colors, and mood."
    ) -> Dict[str, Any]:
        """
        Analyze image using GPT-4o-mini vision capabilities
        
        Args:
            image_data: Image bytes
            prompt: Analysis prompt
            
        Returns:
            Analysis results including description and embedding
        """
        try:
            # Convert to base64
            base64_image = base64.b64encode(image_data).decode('utf-8')
            
            # Call GPT-4o-mini with vision
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=500
            )
            
            description = response.choices[0].message.content
            
            # Generate embedding from description
            embedding = await self.generate_text_embedding(description)
            
            return {
                "description": description,
                "embedding": embedding,
                "model": self.model
            }
            
        except Exception as e:
            logger.error(f"Error analyzing image: {e}")
            raise
    
    async def generate_image_embedding(
        self,
        image_data: bytes
    ) -> List[float]:
        """
        Generate embedding for image
        Strategy: Analyze image → embed description
        
        Args:
            image_data: Image bytes
            
        Returns:
            Embedding vector
        """
        analysis = await self.analyze_image(image_data)
        return analysis["embedding"]
    
    # ========================================================================
    # Audio Processing (Whisper for transcription)
    # ========================================================================
    
    async def transcribe_audio(
        self,
        audio_data: bytes,
        format: str = "mp3"
    ) -> Dict[str, Any]:
        """
        Transcribe audio using Whisper
        
        Args:
            audio_data: Audio bytes
            format: Audio format (mp3, wav, etc.)
            
        Returns:
            Transcription and embedding
        """
        try:
            # Save temporarily (Whisper API needs file)
            temp_path = f"/tmp/audio_temp.{format}"
            with open(temp_path, "wb") as f:
                f.write(audio_data)
            
            # Transcribe
            with open(temp_path, "rb") as audio_file:
                transcription = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            
            # Clean up
            os.remove(temp_path)
            
            text = transcription.text
            
            # Generate embedding from transcription
            embedding = await self.generate_text_embedding(text)
            
            return {
                "transcription": text,
                "embedding": embedding,
                "model": "whisper-1"
            }
            
        except Exception as e:
            logger.error(f"Error transcribing audio: {e}")
            raise
    
    async def generate_audio_embedding(
        self,
        audio_data: bytes,
        format: str = "mp3"
    ) -> List[float]:
        """
        Generate embedding for audio
        Strategy: Transcribe → embed text
        
        Args:
            audio_data: Audio bytes
            format: Audio format
            
        Returns:
            Embedding vector
        """
        result = await self.transcribe_audio(audio_data, format)
        return result["embedding"]
    
    # ========================================================================
    # Video Processing (Extract frames → analyze)
    # ========================================================================
    
    async def analyze_video(
        self,
        video_path: str,
        max_frames: int = 10,
        fps: float = 1.0
    ) -> Dict[str, Any]:
        """
        Analyze video by extracting and analyzing frames
        
        ⚠️ Note: GPT-4o-mini doesn't natively support video
        Strategy: Extract key frames → analyze as images
        
        Args:
            video_path: Path to video file
            max_frames: Maximum frames to analyze
            fps: Frames per second to extract
            
        Returns:
            Video analysis with embeddings
        """
        try:
            import cv2
            
            # Open video
            video = cv2.VideoCapture(video_path)
            
            # Get video properties
            video_fps = video.get(cv2.CAP_PROP_FPS)
            frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = frame_count / video_fps
            
            # Calculate frame interval
            frame_interval = int(video_fps / fps)
            
            # Extract frames
            frames_analyzed = []
            frame_descriptions = []
            frame_num = 0
            extracted = 0
            
            while extracted < max_frames:
                ret, frame = video.read()
                if not ret:
                    break
                
                if frame_num % frame_interval == 0:
                    # Convert frame to bytes
                    _, buffer = cv2.imencode('.jpg', frame)
                    frame_bytes = buffer.tobytes()
                    
                    # Analyze frame
                    analysis = await self.analyze_image(
                        frame_bytes,
                        prompt="Describe what's happening in this video frame."
                    )
                    
                    frames_analyzed.append({
                        "frame_number": frame_num,
                        "timestamp": frame_num / video_fps,
                        "description": analysis["description"]
                    })
                    
                    frame_descriptions.append(analysis["description"])
                    extracted += 1
                
                frame_num += 1
            
            video.release()
            
            # Combine descriptions
            combined_description = " ".join(frame_descriptions)
            
            # Generate embedding from combined description
            embedding = await self.generate_text_embedding(combined_description)
            
            return {
                "duration": duration,
                "frames_analyzed": len(frames_analyzed),
                "frame_descriptions": frames_analyzed,
                "combined_description": combined_description,
                "embedding": embedding,
                "strategy": "frame_extraction_and_analysis"
            }
            
        except Exception as e:
            logger.error(f"Error analyzing video: {e}")
            raise
    
    async def generate_video_embedding(
        self,
        video_path: str,
        max_frames: int = 10
    ) -> List[float]:
        """
        Generate embedding for video
        Strategy: Extract frames → analyze → embed descriptions
        
        Args:
            video_path: Path to video file
            max_frames: Maximum frames to analyze
            
        Returns:
            Embedding vector
        """
        analysis = await self.analyze_video(video_path, max_frames)
        return analysis["embedding"]
    
    # ========================================================================
    # Unified Search (Pinecone)
    # ========================================================================
    
    async def search(
        self,
        query: str,
        modality: str = "all",
        top_k: int = 20,
        filters: Optional[Dict] = None
    ) -> List[Dict[str, Any]]:
        """
        Search across modalities using Pinecone
        
        Args:
            query: Search query
            modality: Modality filter (text, image, video, audio, all)
            top_k: Number of results
            filters: Additional metadata filters
            
        Returns:
            Search results
        """
        try:
            # Generate query embedding
            query_embedding = await self.generate_text_embedding(query)
            
            # Build filter
            metadata_filter = {}
            if modality != "all":
                metadata_filter["modality"] = modality
            
            if filters:
                metadata_filter.update(filters)
            
            # Search Pinecone
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True,
                filter=metadata_filter if metadata_filter else None
            )
            
            # Format results
            formatted_results = []
            for match in results.matches:
                formatted_results.append({
                    "id": match.id,
                    "score": float(match.score),
                    "metadata": match.metadata,
                    "modality": match.metadata.get("modality", "unknown")
                })
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error searching: {e}")
            raise
    
    # ========================================================================
    # Indexing (Add to Pinecone)
    # ========================================================================
    
    async def index_content(
        self,
        content_id: str,
        content_type: str,
        data: Any,
        metadata: Dict[str, Any]
    ) -> bool:
        """
        Index content in Pinecone
        
        Args:
            content_id: Unique content ID
            content_type: text, image, audio, video
            data: Content data (text string, bytes, or path)
            metadata: Additional metadata
            
        Returns:
            Success status
        """
        try:
            # Generate embedding based on type
            if content_type == "text":
                embedding = await self.generate_text_embedding(data)
            
            elif content_type == "image":
                embedding = await self.generate_image_embedding(data)
            
            elif content_type == "audio":
                embedding = await self.generate_audio_embedding(data)
            
            elif content_type == "video":
                embedding = await self.generate_video_embedding(data)
            
            else:
                raise ValueError(f"Unsupported content type: {content_type}")
            
            # Add modality to metadata
            metadata["modality"] = content_type
            
            # Upsert to Pinecone
            self.index.upsert(
                vectors=[
                    {
                        "id": content_id,
                        "values": embedding,
                        "metadata": metadata
                    }
                ]
            )
            
            logger.info(f"Indexed {content_type} content: {content_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error indexing content: {e}")
            return False
    
    async def batch_index(
        self,
        items: List[Dict[str, Any]],
        batch_size: int = 100
    ) -> Dict[str, Any]:
        """
        Batch index multiple items
        
        Args:
            items: List of items to index
            batch_size: Batch size for Pinecone
            
        Returns:
            Results summary
        """
        success_count = 0
        failed_count = 0
        
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            
            for item in batch:
                try:
                    success = await self.index_content(
                        content_id=item["id"],
                        content_type=item["type"],
                        data=item["data"],
                        metadata=item.get("metadata", {})
                    )
                    
                    if success:
                        success_count += 1
                    else:
                        failed_count += 1
                        
                except Exception as e:
                    logger.error(f"Error indexing item {item.get('id')}: {e}")
                    failed_count += 1
        
        return {
            "total": len(items),
            "success": success_count,
            "failed": failed_count
        }
    
    # ========================================================================
    # AI-Powered Features
    # ========================================================================
    
    async def generate_description(
        self,
        query: str,
        context: Optional[str] = None
    ) -> str:
        """
        Generate natural language description using GPT-4o-mini
        
        Args:
            query: Query to describe
            context: Optional context
            
        Returns:
            Generated description
        """
        try:
            messages = [
                {"role": "system", "content": "You are a helpful search assistant."}
            ]
            
            if context:
                messages.append({"role": "user", "content": f"Context: {context}"})
            
            messages.append({"role": "user", "content": query})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=200
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating description: {e}")
            return ""


# ============================================================================
# Singleton Instance
# ============================================================================

_service_instance = None


def get_openai_pinecone_service() -> OpenAIPineconeService:
    """Get or create service instance"""
    global _service_instance
    if _service_instance is None:
        _service_instance = OpenAIPineconeService()
    return _service_instance


# ============================================================================
# Example Usage
# ============================================================================

if __name__ == "__main__":
    import asyncio
    
    async def test_service():
        """Test the service"""
        service = get_openai_pinecone_service()
        
        # Test text embedding
        print("=== Testing Text Embedding ===")
        text_emb = await service.generate_text_embedding("lion in the wild")
        print(f"Embedding dimension: {len(text_emb)}")
        print(f"First 5 values: {text_emb[:5]}")
        print()
        
        # Test search
        print("=== Testing Search ===")
        results = await service.search("lion", top_k=5)
        print(f"Found {len(results)} results")
        print()
    
    asyncio.run(test_service())