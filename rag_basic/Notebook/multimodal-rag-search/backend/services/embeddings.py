# backend/services/embeddings.py
"""
Embedding Generation Service
Handles generation of embeddings for different modalities
"""

from typing import List, Optional, Union
import logging
import numpy as np
from sentence_transformers import SentenceTransformer
import torch
from PIL import Image
import io

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Service for generating embeddings across modalities"""
    
    def __init__(self):
        """Initialize embedding models"""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Using device: {self.device}")
        
        # Text embedding model
        self.text_model = None
        
        # Image/Video embedding model (CLIP)
        self.clip_model = None
        self.clip_processor = None
        
        # Audio embedding model
        self.audio_model = None
        
        self._load_models()
    
    def _load_models(self):
        """Load all embedding models"""
        try:
            # Load text model
            logger.info("Loading text embedding model...")
            self.text_model = SentenceTransformer(
                'sentence-transformers/all-MiniLM-L6-v2',
                device=self.device
            )
            
            # Load CLIP for images/videos
            logger.info("Loading CLIP model...")
            try:
                from transformers import CLIPProcessor, CLIPModel
                self.clip_model = CLIPModel.from_pretrained(
                    "openai/clip-vit-base-patch32"
                ).to(self.device)
                self.clip_processor = CLIPProcessor.from_pretrained(
                    "openai/clip-vit-base-patch32"
                )
            except Exception as e:
                logger.warning(f"CLIP model not available: {e}")
            
            # Load audio model (optional)
            logger.info("Audio model loading skipped (optional)")
            
            logger.info("All models loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            raise
    
    async def generate_text_embedding(
        self,
        text: Union[str, List[str]],
        normalize: bool = True
    ) -> Union[List[float], List[List[float]]]:
        """Generate embedding for text"""
        try:
            if isinstance(text, str):
                text = [text]
            
            embeddings = self.text_model.encode(
                text,
                normalize_embeddings=normalize,
                show_progress_bar=False,
            )
            
            if len(text) == 1:
                return embeddings[0].tolist()
            return embeddings.tolist()
            
        except Exception as e:
            logger.error(f"Error generating text embedding: {e}")
            raise
    
    async def generate_image_embedding(
        self,
        image_data: bytes,
        normalize: bool = True
    ) -> List[float]:
        """Generate embedding for image using CLIP"""
        try:
            if self.clip_model is None:
                raise ValueError("CLIP model not loaded")
            
            # Load image
            image = Image.open(io.BytesIO(image_data)).convert('RGB')
            
            # Process image
            inputs = self.clip_processor(
                images=image,
                return_tensors="pt"
            ).to(self.device)
            
            # Generate embedding
            with torch.no_grad():
                image_features = self.clip_model.get_image_features(**inputs)
            
            embedding = image_features.cpu().numpy()[0]
            
            if normalize:
                embedding = embedding / np.linalg.norm(embedding)
            
            return embedding.tolist()
            
        except Exception as e:
            logger.error(f"Error generating image embedding: {e}")
            raise
    
    async def generate_text_image_embedding(
        self,
        text: str,
        normalize: bool = True
    ) -> List[float]:
        """Generate CLIP embedding from text (for image search)"""
        try:
            if self.clip_model is None:
                raise ValueError("CLIP model not loaded")
            
            # Process text
            inputs = self.clip_processor(
                text=[text],
                return_tensors="pt",
                padding=True
            ).to(self.device)
            
            # Generate embedding
            with torch.no_grad():
                text_features = self.clip_model.get_text_features(**inputs)
            
            embedding = text_features.cpu().numpy()[0]
            
            if normalize:
                embedding = embedding / np.linalg.norm(embedding)
            
            return embedding.tolist()
            
        except Exception as e:
            logger.error(f"Error generating text-image embedding: {e}")
            raise
    
    async def generate_video_embedding(
        self,
        frames: List[bytes],
        aggregate: str = "mean",
        normalize: bool = True
    ) -> List[float]:
        """
        Generate embedding for video by processing frames
        
        Args:
            frames: List of frame images as bytes
            aggregate: How to combine frame embeddings ('mean', 'max', 'first', 'last')
            normalize: Whether to normalize the final embedding
        """
        try:
            if not frames:
                raise ValueError("No frames provided")
            
            # Generate embeddings for each frame
            frame_embeddings = []
            for frame_data in frames[:16]:  # Limit to 16 frames
                embedding = await self.generate_image_embedding(
                    frame_data,
                    normalize=False
                )
                frame_embeddings.append(embedding)
            
            # Aggregate frame embeddings
            frame_array = np.array(frame_embeddings)
            
            if aggregate == "mean":
                video_embedding = np.mean(frame_array, axis=0)
            elif aggregate == "max":
                video_embedding = np.max(frame_array, axis=0)
            elif aggregate == "first":
                video_embedding = frame_array[0]
            elif aggregate == "last":
                video_embedding = frame_array[-1]
            else:
                video_embedding = np.mean(frame_array, axis=0)
            
            if normalize:
                video_embedding = video_embedding / np.linalg.norm(video_embedding)
            
            return video_embedding.tolist()
            
        except Exception as e:
            logger.error(f"Error generating video embedding: {e}")
            raise
    
    async def generate_audio_embedding(
        self,
        audio_data: bytes,
        normalize: bool = True
    ) -> List[float]:
        """
        Generate embedding for audio
        
        Note: This is a placeholder. Implement with Wav2Vec2 or similar model
        """
        try:
            # Placeholder implementation
            # TODO: Implement with actual audio model (Wav2Vec2, Whisper, etc.)
            logger.warning("Audio embedding generation not implemented, using dummy")
            
            # Return dummy embedding for now
            embedding = np.random.randn(768).astype(np.float32)
            
            if normalize:
                embedding = embedding / np.linalg.norm(embedding)
            
            return embedding.tolist()
            
        except Exception as e:
            logger.error(f"Error generating audio embedding: {e}")
            raise
    
    async def generate_multimodal_embedding(
        self,
        text: Optional[str] = None,
        image_data: Optional[bytes] = None,
        combine_method: str = "concat",
        normalize: bool = True
    ) -> List[float]:
        """
        Generate combined multimodal embedding
        
        Args:
            text: Text input
            image_data: Image input as bytes
            combine_method: How to combine embeddings ('concat', 'mean', 'weighted')
            normalize: Whether to normalize final embedding
        """
        try:
            embeddings = []
            
            if text:
                text_emb = await self.generate_text_embedding(text, normalize=False)
                embeddings.append(np.array(text_emb))
            
            if image_data:
                image_emb = await self.generate_image_embedding(image_data, normalize=False)
                embeddings.append(np.array(image_emb))
            
            if not embeddings:
                raise ValueError("At least one modality must be provided")
            
            # Combine embeddings
            if combine_method == "concat":
                combined = np.concatenate(embeddings)
            elif combine_method == "mean":
                # Pad to same size if needed
                max_size = max(emb.shape[0] for emb in embeddings)
                padded = [
                    np.pad(emb, (0, max_size - emb.shape[0]), mode='constant')
                    for emb in embeddings
                ]
                combined = np.mean(padded, axis=0)
            elif combine_method == "weighted":
                # Simple weighted average (can be customized)
                weights = [0.6, 0.4][:len(embeddings)]  # Prefer text
                max_size = max(emb.shape[0] for emb in embeddings)
                padded = [
                    np.pad(emb, (0, max_size - emb.shape[0]), mode='constant')
                    for emb in embeddings
                ]
                combined = np.average(padded, axis=0, weights=weights)
            else:
                combined = np.concatenate(embeddings)
            
            if normalize:
                combined = combined / np.linalg.norm(combined)
            
            return combined.tolist()
            
        except Exception as e:
            logger.error(f"Error generating multimodal embedding: {e}")
            raise
    
    def get_embedding_dimensions(self) -> dict:
        """Get dimensions for each modality"""
        return {
            "text": 384,  # MiniLM
            "image": 512,  # CLIP
            "video": 512,  # CLIP (same as image)
            "audio": 768,  # Wav2Vec2 (placeholder)
        }


# Singleton instance
_embedding_service_instance = None


def get_embedding_service() -> EmbeddingService:
    """Get or create embedding service instance"""
    global _embedding_service_instance
    if _embedding_service_instance is None:
        _embedding_service_instance = EmbeddingService()
    return _embedding_service_instance