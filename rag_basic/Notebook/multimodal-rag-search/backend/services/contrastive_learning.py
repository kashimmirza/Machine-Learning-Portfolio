# backend/services/contrastive_learning.py
"""
Contrastive Representation Learning Service
Implements continuous learning for multimodal embeddings inspired by human learning
"""

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import List, Dict, Tuple, Optional
import logging
from dataclasses import dataclass
from collections import deque
import time

logger = logging.getLogger(__name__)


@dataclass
class LearningExample:
    """Example for contrastive learning"""
    anchor: np.ndarray
    positive: np.ndarray
    negative: np.ndarray
    modality: str
    timestamp: float
    metadata: Dict


class ContrastiveLoss(nn.Module):
    """
    Contrastive loss function for multimodal learning
    Pulls positive examples closer and pushes negative examples apart
    """
    
    def __init__(self, temperature: float = 0.07):
        super().__init__()
        self.temperature = temperature
    
    def forward(
        self,
        anchor: torch.Tensor,
        positive: torch.Tensor,
        negatives: torch.Tensor
    ) -> torch.Tensor:
        """
        Calculate contrastive loss
        
        Args:
            anchor: Anchor embedding [batch_size, embed_dim]
            positive: Positive example embedding [batch_size, embed_dim]
            negatives: Negative examples [batch_size, num_negatives, embed_dim]
        """
        # Normalize embeddings
        anchor = F.normalize(anchor, dim=-1)
        positive = F.normalize(positive, dim=-1)
        negatives = F.normalize(negatives, dim=-1)
        
        # Positive similarity
        pos_sim = torch.sum(anchor * positive, dim=-1) / self.temperature
        
        # Negative similarities
        neg_sim = torch.matmul(negatives, anchor.unsqueeze(-1)).squeeze(-1)
        neg_sim = neg_sim / self.temperature
        
        # Contrastive loss (InfoNCE)
        numerator = torch.exp(pos_sim)
        denominator = numerator + torch.sum(torch.exp(neg_sim), dim=-1)
        
        loss = -torch.log(numerator / denominator)
        return loss.mean()


class MultiModalLearner:
    """
    Continuous learning system for multimodal embeddings
    Learns from interactions similar to how children learn
    """
    
    def __init__(
        self,
        embed_dim: int = 512,
        learning_rate: float = 0.001,
        memory_size: int = 10000,
        batch_size: int = 32
    ):
        self.embed_dim = embed_dim
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        
        # Experience replay memory (like human memory)
        self.memory = deque(maxlen=memory_size)
        
        # Projection networks for each modality
        self.projectors = {
            'text': self._create_projector(384, embed_dim),
            'image': self._create_projector(512, embed_dim),
            'video': self._create_projector(512, embed_dim),
            'audio': self._create_projector(768, embed_dim),
        }
        
        # Contrastive loss
        self.criterion = ContrastiveLoss()
        
        # Optimizers for each modality
        self.optimizers = {
            modality: torch.optim.Adam(
                projector.parameters(),
                lr=learning_rate
            )
            for modality, projector in self.projectors.items()
        }
        
        # Learning statistics
        self.stats = {
            'total_examples': 0,
            'losses': deque(maxlen=1000),
            'modality_counts': {},
            'learning_rate_history': [],
        }
        
        logger.info("MultiModalLearner initialized")
    
    def _create_projector(
        self,
        input_dim: int,
        output_dim: int
    ) -> nn.Module:
        """Create projection network to unified space"""
        return nn.Sequential(
            nn.Linear(input_dim, 1024),
            nn.ReLU(),
            nn.BatchNorm1d(1024),
            nn.Dropout(0.2),
            nn.Linear(1024, 512),
            nn.ReLU(),
            nn.BatchNorm1d(512),
            nn.Dropout(0.1),
            nn.Linear(512, output_dim)
        )
    
    def observe(
        self,
        anchor: np.ndarray,
        positive: np.ndarray,
        negative: np.ndarray,
        modality: str,
        metadata: Optional[Dict] = None
    ):
        """
        Observe a new example (like a child observing the world)
        
        Args:
            anchor: Anchor embedding
            positive: Positive example (similar concept)
            negative: Negative example (different concept)
            modality: Content type
            metadata: Additional information
        """
        example = LearningExample(
            anchor=anchor,
            positive=positive,
            negative=negative,
            modality=modality,
            timestamp=time.time(),
            metadata=metadata or {}
        )
        
        self.memory.append(example)
        self.stats['total_examples'] += 1
        self.stats['modality_counts'][modality] = \
            self.stats['modality_counts'].get(modality, 0) + 1
        
        logger.debug(f"Observed {modality} example. Memory size: {len(self.memory)}")
    
    def learn_batch(self) -> Optional[float]:
        """
        Learn from a batch of experiences (consolidate learning)
        Similar to how humans consolidate learning during sleep
        """
        if len(self.memory) < self.batch_size:
            return None
        
        # Sample batch from memory
        indices = np.random.choice(
            len(self.memory),
            size=self.batch_size,
            replace=False
        )
        batch = [self.memory[i] for i in indices]
        
        # Group by modality
        modality_batches = {}
        for example in batch:
            if example.modality not in modality_batches:
                modality_batches[example.modality] = []
            modality_batches[example.modality].append(example)
        
        # Train each modality
        total_loss = 0.0
        for modality, examples in modality_batches.items():
            if modality not in self.projectors:
                continue
            
            # Prepare tensors
            anchors = torch.FloatTensor([e.anchor for e in examples])
            positives = torch.FloatTensor([e.positive for e in examples])
            negatives = torch.FloatTensor([e.negative for e in examples])
            negatives = negatives.unsqueeze(1)  # Add negative dimension
            
            # Project to unified space
            projector = self.projectors[modality]
            projector.train()
            
            anchor_proj = projector(anchors)
            positive_proj = projector(positives)
            negative_proj = projector(negatives.squeeze(1))
            negative_proj = negative_proj.unsqueeze(1)
            
            # Calculate loss
            loss = self.criterion(anchor_proj, positive_proj, negative_proj)
            
            # Backpropagation
            optimizer = self.optimizers[modality]
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
        
        avg_loss = total_loss / len(modality_batches)
        self.stats['losses'].append(avg_loss)
        
        logger.info(f"Learned from batch. Loss: {avg_loss:.4f}")
        return avg_loss
    
    def continuous_learning_loop(
        self,
        num_iterations: int = 100,
        learn_every: int = 10
    ) -> Dict:
        """
        Continuous learning loop
        Periodically consolidates learning from memory
        """
        results = {
            'iterations': num_iterations,
            'losses': [],
            'final_loss': None,
        }
        
        for i in range(num_iterations):
            if i % learn_every == 0 and len(self.memory) >= self.batch_size:
                loss = self.learn_batch()
                if loss is not None:
                    results['losses'].append(loss)
                    
                    # Adaptive learning rate
                    if len(results['losses']) > 10:
                        recent_losses = results['losses'][-10:]
                        if np.std(recent_losses) < 0.01:  # Plateau
                            self._adjust_learning_rate(0.9)
        
        if results['losses']:
            results['final_loss'] = results['losses'][-1]
        
        return results
    
    def _adjust_learning_rate(self, factor: float):
        """Adjust learning rate for all optimizers"""
        for modality, optimizer in self.optimizers.items():
            for param_group in optimizer.param_groups:
                old_lr = param_group['lr']
                param_group['lr'] *= factor
                new_lr = param_group['lr']
                logger.info(f"{modality} LR: {old_lr:.6f} -> {new_lr:.6f}")
    
    def project_to_unified_space(
        self,
        embedding: np.ndarray,
        modality: str
    ) -> np.ndarray:
        """
        Project embedding from modality-specific space to unified space
        
        Args:
            embedding: Modality-specific embedding
            modality: Content type
            
        Returns:
            Unified space embedding
        """
        if modality not in self.projectors:
            logger.warning(f"Unknown modality: {modality}")
            return embedding
        
        projector = self.projectors[modality]
        projector.eval()
        
        with torch.no_grad():
            embedding_tensor = torch.FloatTensor(embedding).unsqueeze(0)
            projected = projector(embedding_tensor)
            return projected.squeeze(0).numpy()
    
    def cross_modal_similarity(
        self,
        embedding1: np.ndarray,
        modality1: str,
        embedding2: np.ndarray,
        modality2: str
    ) -> float:
        """
        Calculate similarity between embeddings from different modalities
        
        Args:
            embedding1: First embedding
            modality1: First modality
            embedding2: Second embedding
            modality2: Second modality
            
        Returns:
            Cosine similarity in unified space
        """
        # Project both to unified space
        unified1 = self.project_to_unified_space(embedding1, modality1)
        unified2 = self.project_to_unified_space(embedding2, modality2)
        
        # Calculate cosine similarity
        similarity = np.dot(unified1, unified2) / (
            np.linalg.norm(unified1) * np.linalg.norm(unified2)
        )
        
        return float(similarity)
    
    def get_learning_stats(self) -> Dict:
        """Get learning statistics"""
        stats = self.stats.copy()
        stats['memory_size'] = len(self.memory)
        
        if stats['losses']:
            stats['avg_loss'] = np.mean(stats['losses'])
            stats['recent_loss'] = stats['losses'][-1]
        
        return stats
    
    def save_checkpoint(self, path: str):
        """Save learning checkpoint"""
        checkpoint = {
            'projectors': {
                modality: projector.state_dict()
                for modality, projector in self.projectors.items()
            },
            'optimizers': {
                modality: optimizer.state_dict()
                for modality, optimizer in self.optimizers.items()
            },
            'stats': self.stats,
        }
        torch.save(checkpoint, path)
        logger.info(f"Checkpoint saved to {path}")
    
    def load_checkpoint(self, path: str):
        """Load learning checkpoint"""
        checkpoint = torch.load(path)
        
        for modality, state_dict in checkpoint['projectors'].items():
            if modality in self.projectors:
                self.projectors[modality].load_state_dict(state_dict)
        
        for modality, state_dict in checkpoint['optimizers'].items():
            if modality in self.optimizers:
                self.optimizers[modality].load_state_dict(state_dict)
        
        self.stats = checkpoint['stats']
        logger.info(f"Checkpoint loaded from {path}")


class InteractionLearner:
    """
    Learn from user interactions (click-through, dwell time, etc.)
    Similar to how children learn from feedback
    """
    
    def __init__(self):
        self.interaction_history = deque(maxlen=100000)
        self.concept_associations = {}  # Track concept relationships
        
    def record_interaction(
        self,
        query: str,
        result_id: str,
        modality: str,
        interaction_type: str,  # 'click', 'view', 'skip'
        dwell_time: float = 0.0,
        relevance_score: float = 0.0
    ):
        """Record user interaction for learning"""
        interaction = {
            'query': query,
            'result_id': result_id,
            'modality': modality,
            'interaction_type': interaction_type,
            'dwell_time': dwell_time,
            'relevance_score': relevance_score,
            'timestamp': time.time(),
        }
        
        self.interaction_history.append(interaction)
        
        # Update concept associations
        if query not in self.concept_associations:
            self.concept_associations[query] = {
                'clicked_results': [],
                'skipped_results': [],
                'preferred_modalities': {},
            }
        
        if interaction_type == 'click':
            self.concept_associations[query]['clicked_results'].append(result_id)
        elif interaction_type == 'skip':
            self.concept_associations[query]['skipped_results'].append(result_id)
        
        # Track modality preferences
        modality_prefs = self.concept_associations[query]['preferred_modalities']
        modality_prefs[modality] = modality_prefs.get(modality, 0) + relevance_score
    
    def get_learned_preferences(self, query: str) -> Dict:
        """Get learned preferences for a query"""
        if query not in self.concept_associations:
            return {}
        
        associations = self.concept_associations[query]
        
        # Calculate preferred modalities
        modality_prefs = associations['preferred_modalities']
        if modality_prefs:
            total = sum(modality_prefs.values())
            normalized_prefs = {
                mod: score / total
                for mod, score in modality_prefs.items()
            }
        else:
            normalized_prefs = {}
        
        return {
            'preferred_modalities': normalized_prefs,
            'interaction_count': len(associations['clicked_results']) + 
                               len(associations['skipped_results']),
            'click_through_rate': len(associations['clicked_results']) / 
                                 max(1, len(associations['clicked_results']) + 
                                     len(associations['skipped_results']))
        }
    
    def suggest_result_reranking(
        self,
        query: str,
        results: List[Dict]
    ) -> List[Dict]:
        """
        Rerank results based on learned preferences
        Similar to how humans develop preferences over time
        """
        preferences = self.get_learned_preferences(query)
        
        if not preferences.get('preferred_modalities'):
            return results  # No learned preferences yet
        
        # Boost results from preferred modalities
        modality_prefs = preferences['preferred_modalities']
        
        for result in results:
            modality = result.get('modality', 'unknown')
            boost = modality_prefs.get(modality, 0.5)
            result['score'] = result.get('score', 0.5) * (1 + boost)
        
        # Re-sort by boosted scores
        results.sort(key=lambda x: x.get('score', 0), reverse=True)
        
        return results


# Singleton instances
_multimodal_learner = None
_interaction_learner = None


def get_multimodal_learner() -> MultiModalLearner:
    """Get or create multimodal learner instance"""
    global _multimodal_learner
    if _multimodal_learner is None:
        _multimodal_learner = MultiModalLearner()
    return _multimodal_learner


def get_interaction_learner() -> InteractionLearner:
    """Get or create interaction learner instance"""
    global _interaction_learner
    if _interaction_learner is None:
        _interaction_learner = InteractionLearner()
    return _interaction_learner