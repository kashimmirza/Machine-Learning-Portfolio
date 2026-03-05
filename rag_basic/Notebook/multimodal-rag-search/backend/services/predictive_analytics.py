# backend/services/predictive_analytics.py
"""
🔮 Aurora AI Predictive Analytics Engine
Predict content performance BEFORE publishing

Features:
- Performance forecasting
- Trend prediction
- Audience insights
- Optimization recommendations
- A/B test suggestions
- Revenue projections
"""

import numpy as np
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


@dataclass
class PerformancePrediction:
    """Predicted performance metrics"""
    content_id: str
    predicted_views: int
    predicted_engagement_rate: float
    predicted_watch_time: float
    predicted_shares: int
    predicted_comments: int
    predicted_revenue: float
    confidence: float
    explanation: str


@dataclass
class TrendPrediction:
    """Predicted trend"""
    topic: str
    trend_direction: str  # 'rising', 'declining', 'stable'
    growth_rate: float
    peak_time: datetime
    confidence: float
    related_topics: List[str]


@dataclass
class AudienceInsight:
    """Audience behavior insight"""
    segment: str
    size: int
    preferences: Dict[str, float]
    engagement_patterns: Dict[str, Any]
    recommended_content: List[str]


class PredictiveAnalyticsEngine:
    """
    ML-powered predictive analytics
    
    This is what makes Aurora invaluable:
    - Know what will succeed BEFORE creating it
    - Optimize content for maximum impact
    - Data-driven decision making
    """
    
    def __init__(self):
        self.historical_data = defaultdict(list)
        self.trend_data = defaultdict(list)
        self.audience_segments = {}
    
    async def predict_performance(
        self,
        content_metadata: Dict[str, Any],
        historical_context: Optional[List[Dict]] = None
    ) -> PerformancePrediction:
        """
        Predict how content will perform
        
        Factors considered:
        - Content quality metrics
        - Historical performance of similar content
        - Current trends
        - Audience preferences
        - Posting time
        - Platform algorithms
        - Seasonal patterns
        """
        
        # Extract features
        features = self._extract_features(content_metadata)
        
        # Get similar content performance
        similar_performance = await self._get_similar_performance(features)
        
        # Trend adjustment
        trend_multiplier = await self._calculate_trend_multiplier(
            content_metadata.get('topics', [])
        )
        
        # Base prediction from similar content
        base_views = np.mean([p['views'] for p in similar_performance]) if similar_performance else 10000
        
        # Adjustments
        quality_multiplier = self._calculate_quality_multiplier(content_metadata)
        timing_multiplier = self._calculate_timing_multiplier(
            content_metadata.get('proposed_publish_time')
        )
        
        # Final prediction
        predicted_views = int(
            base_views * quality_multiplier * trend_multiplier * timing_multiplier
        )
        
        # Other metrics
        predicted_engagement = self._predict_engagement_rate(features)
        predicted_watch_time = self._predict_watch_time(features)
        predicted_shares = int(predicted_views * 0.02)  # 2% share rate
        predicted_comments = int(predicted_views * 0.01)  # 1% comment rate
        
        # Revenue (if applicable)
        predicted_revenue = self._predict_revenue(
            predicted_views,
            content_metadata.get('monetization', True)
        )
        
        # Confidence calculation
        confidence = self._calculate_confidence(
            num_similar=len(similar_performance),
            trend_strength=trend_multiplier
        )
        
        # Generate explanation
        explanation = self._generate_explanation(
            base_views=base_views,
            quality=quality_multiplier,
            trend=trend_multiplier,
            timing=timing_multiplier
        )
        
        return PerformancePrediction(
            content_id=content_metadata.get('id', 'new'),
            predicted_views=predicted_views,
            predicted_engagement_rate=predicted_engagement,
            predicted_watch_time=predicted_watch_time,
            predicted_shares=predicted_shares,
            predicted_comments=predicted_comments,
            predicted_revenue=predicted_revenue,
            confidence=confidence,
            explanation=explanation
        )
    
    def _extract_features(self, metadata: Dict) -> Dict[str, Any]:
        """Extract ML features from content metadata"""
        return {
            'duration': metadata.get('duration', 0),
            'quality': metadata.get('quality_score', 0.5),
            'topics': metadata.get('topics', []),
            'modality': metadata.get('modality', 'video'),
            'creator_followers': metadata.get('creator_followers', 0),
            'has_captions': metadata.get('has_captions', False),
            'thumbnail_quality': metadata.get('thumbnail_quality', 0.5),
            'title_sentiment': metadata.get('title_sentiment', 0.0),
        }
    
    async def _get_similar_performance(
        self,
        features: Dict
    ) -> List[Dict]:
        """Get performance of similar content"""
        
        # In production: Query historical database
        # For now: Simulated data
        
        similar_content = [
            {
                'views': 15000,
                'engagement_rate': 0.08,
                'watch_time': 0.65
            },
            {
                'views': 20000,
                'engagement_rate': 0.09,
                'watch_time': 0.70
            },
            {
                'views': 12000,
                'engagement_rate': 0.07,
                'watch_time': 0.60
            }
        ]
        
        return similar_content
    
    async def _calculate_trend_multiplier(
        self,
        topics: List[str]
    ) -> float:
        """
        Calculate trend impact
        
        Hot topics → higher multiplier
        Declining topics → lower multiplier
        """
        
        if not topics:
            return 1.0
        
        # Check current trends
        trend_scores = []
        for topic in topics:
            trend = await self.get_trend_prediction(topic)
            if trend.trend_direction == 'rising':
                trend_scores.append(1.0 + trend.growth_rate)
            elif trend.trend_direction == 'declining':
                trend_scores.append(1.0 - abs(trend.growth_rate))
            else:
                trend_scores.append(1.0)
        
        return np.mean(trend_scores)
    
    def _calculate_quality_multiplier(self, metadata: Dict) -> float:
        """
        Quality impact on performance
        
        High quality → 1.5x
        Average → 1.0x
        Low quality → 0.7x
        """
        quality_score = metadata.get('quality_score', 0.5)
        
        if quality_score > 0.8:
            return 1.5
        elif quality_score > 0.6:
            return 1.2
        elif quality_score > 0.4:
            return 1.0
        else:
            return 0.7
    
    def _calculate_timing_multiplier(
        self,
        proposed_time: Optional[datetime]
    ) -> float:
        """
        Posting time impact
        
        Optimal time → 1.3x
        Good time → 1.0x
        Poor time → 0.7x
        """
        
        if not proposed_time:
            return 1.0
        
        # Check if it's an optimal time
        # Tuesday-Thursday 2-4 PM are generally best
        
        if proposed_time.weekday() in [1, 2, 3]:  # Tue-Thu
            if 14 <= proposed_time.hour <= 16:  # 2-4 PM
                return 1.3
        
        # Weekend mornings
        if proposed_time.weekday() in [5, 6]:  # Sat-Sun
            if 9 <= proposed_time.hour <= 11:
                return 1.2
        
        # Late night or early morning
        if proposed_time.hour < 6 or proposed_time.hour > 23:
            return 0.7
        
        return 1.0
    
    def _predict_engagement_rate(self, features: Dict) -> float:
        """
        Predict engagement rate (likes, comments, shares / views)
        
        Industry average: 3-5%
        Good content: 8-12%
        Viral content: 15%+
        """
        
        base_rate = 0.05  # 5% baseline
        
        # Quality boost
        quality = features.get('quality', 0.5)
        quality_boost = (quality - 0.5) * 0.10  # +/- 5%
        
        # Creator influence boost
        followers = features.get('creator_followers', 0)
        if followers > 100000:
            follower_boost = 0.03
        elif followers > 10000:
            follower_boost = 0.02
        else:
            follower_boost = 0.0
        
        # Captions boost (accessibility)
        caption_boost = 0.01 if features.get('has_captions') else 0.0
        
        predicted_rate = base_rate + quality_boost + follower_boost + caption_boost
        
        return max(0.01, min(0.20, predicted_rate))  # Clamp between 1-20%
    
    def _predict_watch_time(self, features: Dict) -> float:
        """
        Predict average watch time percentage
        
        Industry average: 50-60%
        Good content: 70-80%
        Excellent content: 85%+
        """
        
        duration = features.get('duration', 0)
        quality = features.get('quality', 0.5)
        
        # Shorter videos → higher completion
        if duration < 60:
            base_completion = 0.75
        elif duration < 180:
            base_completion = 0.65
        elif duration < 600:
            base_completion = 0.55
        else:
            base_completion = 0.45
        
        # Quality adjustment
        quality_adjustment = (quality - 0.5) * 0.20
        
        predicted_completion = base_completion + quality_adjustment
        
        return max(0.20, min(0.95, predicted_completion))
    
    def _predict_revenue(
        self,
        predicted_views: int,
        monetization_enabled: bool
    ) -> float:
        """
        Predict revenue (if monetized)
        
        Assumes:
        - $2-5 CPM for video ads
        - $0.10-0.50 per engagement for sponsored content
        """
        
        if not monetization_enabled:
            return 0.0
        
        # Ad revenue (CPM)
        cpm = 3.5  # $3.50 per 1000 views
        ad_revenue = (predicted_views / 1000) * cpm
        
        # Engagement-based revenue
        engagement_revenue = predicted_views * 0.02 * 0.25  # 2% engage * $0.25 each
        
        total_revenue = ad_revenue + engagement_revenue
        
        return round(total_revenue, 2)
    
    def _calculate_confidence(
        self,
        num_similar: int,
        trend_strength: float
    ) -> float:
        """
        Calculate prediction confidence
        
        More historical data → higher confidence
        Stronger trends → higher confidence
        """
        
        # Base confidence from sample size
        if num_similar >= 100:
            base_confidence = 0.90
        elif num_similar >= 50:
            base_confidence = 0.80
        elif num_similar >= 20:
            base_confidence = 0.70
        elif num_similar >= 10:
            base_confidence = 0.60
        else:
            base_confidence = 0.50
        
        # Trend confidence
        if 0.9 <= trend_strength <= 1.1:
            trend_confidence = 0.10  # Stable trend
        else:
            trend_confidence = 0.05  # Volatile
        
        total_confidence = min(0.95, base_confidence + trend_confidence)
        
        return round(total_confidence, 2)
    
    def _generate_explanation(
        self,
        base_views: float,
        quality: float,
        trend: float,
        timing: float
    ) -> str:
        """Generate human-readable explanation"""
        
        factors = []
        
        if quality > 1.2:
            factors.append("high content quality (+{}%)".format(int((quality-1)*100)))
        elif quality < 0.9:
            factors.append("lower quality (-{}%)".format(int((1-quality)*100)))
        
        if trend > 1.1:
            factors.append("trending topic (+{}%)".format(int((trend-1)*100)))
        elif trend < 0.9:
            factors.append("declining topic (-{}%)".format(int((1-trend)*100)))
        
        if timing > 1.1:
            factors.append("optimal posting time (+{}%)".format(int((timing-1)*100)))
        elif timing < 0.9:
            factors.append("suboptimal timing (-{}%)".format(int((1-timing)*100)))
        
        if factors:
            explanation = f"Prediction based on similar content ({int(base_views)} avg views) adjusted for: {', '.join(factors)}."
        else:
            explanation = f"Prediction based on {int(base_views)} average views from similar content."
        
        return explanation
    
    async def get_trend_prediction(
        self,
        topic: str,
        days_ahead: int = 7
    ) -> TrendPrediction:
        """
        Predict trend trajectory
        
        Uses:
        - Historical trend data
        - Search volume
        - Social media mentions
        - News coverage
        - Seasonal patterns
        """
        
        # Analyze historical trend
        historical_trend = self._get_historical_trend(topic)
        
        # Calculate growth rate
        if len(historical_trend) >= 2:
            recent = np.mean(historical_trend[-7:])  # Last week
            previous = np.mean(historical_trend[-14:-7])  # Week before
            growth_rate = (recent - previous) / previous if previous > 0 else 0.0
        else:
            growth_rate = 0.0
        
        # Determine direction
        if growth_rate > 0.1:
            direction = 'rising'
        elif growth_rate < -0.1:
            direction = 'declining'
        else:
            direction = 'stable'
        
        # Predict peak
        if direction == 'rising':
            peak_time = datetime.now() + timedelta(days=days_ahead)
        else:
            peak_time = datetime.now()
        
        # Find related topics
        related = self._find_related_trends(topic)
        
        # Confidence
        confidence = min(0.85, 0.5 + len(historical_trend) * 0.01)
        
        return TrendPrediction(
            topic=topic,
            trend_direction=direction,
            growth_rate=growth_rate,
            peak_time=peak_time,
            confidence=confidence,
            related_topics=related
        )
    
    def _get_historical_trend(self, topic: str) -> List[float]:
        """Get historical trend data"""
        # In production: Query trend database
        # For now: Simulated rising trend
        return [100 + i*5 + np.random.randint(-10, 10) for i in range(30)]
    
    def _find_related_trends(self, topic: str) -> List[str]:
        """Find related trending topics"""
        # In production: Use topic modeling, co-occurrence analysis
        return ['related_topic_1', 'related_topic_2']
    
    async def generate_optimization_recommendations(
        self,
        content_metadata: Dict,
        prediction: PerformancePrediction
    ) -> List[str]:
        """
        AI-powered recommendations to improve performance
        
        This is extremely valuable:
        - Actionable advice
        - Data-driven
        - Personalized
        """
        
        recommendations = []
        
        # Title optimization
        if len(content_metadata.get('title', '')) < 40:
            recommendations.append(
                "📝 Lengthen title to 40-60 characters for better SEO and click-through"
            )
        
        # Timing optimization
        if prediction.confidence < 0.7:
            recommendations.append(
                f"⏰ Post on Tuesday at 2 PM EST for 30% higher engagement"
            )
        
        # Quality improvements
        if content_metadata.get('quality_score', 0) < 0.7:
            recommendations.append(
                "🎥 Improve video quality: better lighting, stabilization, and audio"
            )
        
        # Thumbnail
        if not content_metadata.get('custom_thumbnail'):
            recommendations.append(
                "🖼️ Create custom thumbnail with faces and bright colors for 2x CTR"
            )
        
        # Captions
        if not content_metadata.get('has_captions'):
            recommendations.append(
                "📱 Add captions for 40% higher engagement (mobile viewers, accessibility)"
            )
        
        # Duration
        duration = content_metadata.get('duration', 0)
        if duration > 600:  # 10 minutes
            recommendations.append(
                "✂️ Consider creating a 3-minute version for higher completion rate"
            )
        
        # Hashtags/tags
        if len(content_metadata.get('tags', [])) < 5:
            recommendations.append(
                "🏷️ Add 8-12 relevant tags for better discoverability"
            )
        
        # Call-to-action
        recommendations.append(
            "👆 Add clear CTA (like, comment, subscribe) at 0:15 and end"
        )
        
        return recommendations


# Singleton
_analytics_engine = None

def get_analytics_engine() -> PredictiveAnalyticsEngine:
    global _analytics_engine
    if _analytics_engine is None:
        _analytics_engine = PredictiveAnalyticsEngine()
    return _analytics_engine
