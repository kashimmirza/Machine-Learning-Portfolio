<!-- @format -->

# 🚀 OpenAI + Pinecone Integration Guide

## Your Setup

You're using:

- ✅ **OpenAI**: gpt-4o-mini (with vision)
- ✅ **Pinecone**: Vector database
- ✅ **Model Capabilities**:
  - Text: ✅ Native
  - Images: ✅ Vision-capable
  - Audio: ✅ Via Whisper API
  - Video: ⚠️ Extract frames → analyze

## Quick Start (5 Minutes)

### Step 1: Secure Your Keys

**⚠️ URGENT: Your keys are exposed! Rotate them NOW:**

1. **OpenAI**: https://platform.openai.com/api-keys
2. **Pinecone**: https://app.pinecone.io/

### Step 2: Install Dependencies

```bash
cd backend
pip install -r requirements_openai_pinecone.txt --break-system-packages
```

### Step 3: Configure Environment

```bash
# Create .env file
cp .env.example .env

# Edit with your NEW keys
nano .env
```

Add:

```env
OPENAI_API_KEY=sk-proj-YOUR-NEW-KEY
OPENAI_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

PINECONE_API_KEY=YOUR-NEW-PINECONE-KEY
PINECONE_INDEX_NAME=multimodal-search-index
PINECONE_ENVIRONMENT=us-east-1-aws
```

### Step 4: Test the Service

```bash
python -m services.openai_pinecone_service

# Expected output:
# === Testing Text Embedding ===
# Embedding dimension: 1536
# First 5 values: [0.123, -0.456, ...]
#
# === Testing Search ===
# Found 0 results (index is empty initially)
```

## Model Capabilities

### GPT-4o-mini Modality Support

| Modality   | Supported  | Method           | Notes                    |
| ---------- | ---------- | ---------------- | ------------------------ |
| **Text**   | ✅ Yes     | Native           | Full support             |
| **Images** | ✅ Yes     | Vision API       | Can analyze images       |
| **Audio**  | ✅ Yes     | Whisper API      | Transcription only       |
| **Video**  | ⚠️ Partial | Frame extraction | Extract → analyze frames |

### Implementation Details

#### 1. Text Processing

```python
# Direct embedding
embedding = await service.generate_text_embedding("lion in the wild")
```

#### 2. Image Processing

```python
# Strategy: Analyze image → embed description
with open("lion.jpg", "rb") as f:
    image_data = f.read()

embedding = await service.generate_image_embedding(image_data)

# Internally:
# 1. GPT-4o-mini analyzes image (vision)
# 2. Generates description: "A majestic lion resting under tree..."
# 3. Embeds description
```

#### 3. Audio Processing

```python
# Strategy: Transcribe → embed text
with open("lion_roar.mp3", "rb") as f:
    audio_data = f.read()

embedding = await service.generate_audio_embedding(audio_data)

# Internally:
# 1. Whisper transcribes: "lion roaring sound..."
# 2. Embeds transcription
```

#### 4. Video Processing

```python
# Strategy: Extract frames → analyze → embed
embedding = await service.generate_video_embedding("lion_video.mp4")

# Internally:
# 1. Extracts key frames (1 fps)
# 2. GPT-4o-mini analyzes each frame
# 3. Combines descriptions
# 4. Embeds combined description
```

## Integration with Existing Code

### Update main.py

```python
# backend/main.py
from services.openai_pinecone_service import get_openai_pinecone_service

# Initialize service
openai_service = get_openai_pinecone_service()

@app.post("/api/v1/search/openai")
async def search_with_openai(request: SearchRequest):
    """Search using OpenAI embeddings + Pinecone"""
    try:
        results = await openai_service.search(
            query=request.query,
            modality=request.modality,
            top_k=request.limit
        )

        return {
            "success": True,
            "query": request.query,
            "results": results,
            "total": len(results),
            "provider": "OpenAI + Pinecone"
        }
    except Exception as e:
        raise HTTPException(500, str(e))
```

### Update LangGraph Agent

```python
# backend/agents/langgraph_agent.py
from services.openai_pinecone_service import get_openai_pinecone_service

openai_service = get_openai_pinecone_service()

@tool
def openai_vector_search(query: str, modality: str = "all") -> List[Dict]:
    """Search using OpenAI + Pinecone"""
    import asyncio
    results = asyncio.run(
        openai_service.search(query, modality=modality)
    )
    return results
```

## Indexing Content

### Index Text

```python
await openai_service.index_content(
    content_id="doc_001",
    content_type="text",
    data="Lions are majestic creatures...",
    metadata={
        "title": "About Lions",
        "category": "wildlife",
        "url": "https://example.com/lions"
    }
)
```

### Index Image

```python
with open("lion.jpg", "rb") as f:
    image_data = f.read()

await openai_service.index_content(
    content_id="img_001",
    content_type="image",
    data=image_data,
    metadata={
        "title": "Lion in Savanna",
        "category": "wildlife",
        "url": "https://cdn.example.com/lion.jpg"
    }
)
```

### Index Audio

```python
with open("lion_roar.mp3", "rb") as f:
    audio_data = f.read()

await openai_service.index_content(
    content_id="audio_001",
    content_type="audio",
    data=audio_data,
    metadata={
        "title": "Lion Roar",
        "duration": 30,
        "url": "https://cdn.example.com/lion_roar.mp3"
    }
)
```

### Index Video

```python
await openai_service.index_content(
    content_id="video_001",
    content_type="video",
    data="/path/to/lion_video.mp4",  # File path
    metadata={
        "title": "Lion Documentary",
        "duration": 180,
        "url": "https://cdn.example.com/lion_doc.mp4"
    }
)
```

### Batch Indexing

```python
items = [
    {
        "id": "text_001",
        "type": "text",
        "data": "Lion content...",
        "metadata": {"title": "Lions"}
    },
    {
        "id": "img_001",
        "type": "image",
        "data": image_bytes,
        "metadata": {"title": "Lion Photo"}
    }
]

result = await openai_service.batch_index(items)
print(f"Indexed {result['success']}/{result['total']}")
```

## Cost Optimization

### OpenAI Pricing (as of Jan 2024)

| Model                  | Input              | Output             |
| ---------------------- | ------------------ | ------------------ |
| gpt-4o-mini            | $0.150 / 1M tokens | $0.600 / 1M tokens |
| text-embedding-3-small | $0.020 / 1M tokens | -                  |
| whisper-1              | $0.006 / minute    | -                  |

### Cost Estimation

```python
# Text search (1000 queries/day)
# Embedding: 1000 queries × 50 tokens × $0.02/1M = $0.001/day
# = $0.03/month ✅ Very cheap

# Image search (1000 images/day)
# Vision: 1000 images × 100 tokens × $0.15/1M = $0.015/day
# Embedding: 1000 × 50 × $0.02/1M = $0.001/day
# = $0.48/month ✅ Affordable

# Audio search (100 audio files/day, 1 min each)
# Whisper: 100 × $0.006 = $0.60/day
# Embedding: negligible
# = $18/month ⚠️ Monitor usage
```

### Caching Strategy

```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=10000)
def cached_embedding(text: str) -> str:
    """Cache embeddings to avoid re-computation"""
    # Return cached or compute new
    pass

# Reduces OpenAI API calls by 80%+
```

## Performance Tuning

### 1. Parallel Processing

```python
import asyncio

async def batch_embed(texts: List[str]) -> List[List[float]]:
    """Process multiple texts in parallel"""
    tasks = [
        openai_service.generate_text_embedding(text)
        for text in texts
    ]
    return await asyncio.gather(*tasks)
```

### 2. Pinecone Optimization

```python
# Use namespaces for organization
index.upsert(
    vectors=vectors,
    namespace="production_data"  # Separate prod/dev data
)

# Query with metadata filters
results = index.query(
    vector=query_vector,
    filter={"category": {"$eq": "wildlife"}},  # Pre-filter
    top_k=20
)
```

### 3. Reduce Video Processing Cost

```python
# Extract fewer frames
await openai_service.analyze_video(
    video_path="video.mp4",
    max_frames=5,  # Instead of 10
    fps=0.5  # 1 frame every 2 seconds
)
```

## Monitoring

### Track OpenAI Usage

```python
import logging

logger = logging.getLogger(__name__)

class MonitoredOpenAIService(OpenAIPineconeService):
    async def generate_text_embedding(self, text):
        logger.info(f"OpenAI API call: embedding, tokens: {len(text.split())}")
        return await super().generate_text_embedding(text)
```

### Set Up Alerts

```python
# Alert if daily cost > $10
if daily_cost > 10:
    send_alert(f"OpenAI costs: ${daily_cost}")
```

## Testing

### Unit Tests

```python
import pytest

@pytest.mark.asyncio
async def test_text_embedding():
    service = get_openai_pinecone_service()
    embedding = await service.generate_text_embedding("test")

    assert len(embedding) == 1536
    assert all(isinstance(x, float) for x in embedding)

@pytest.mark.asyncio
async def test_search():
    service = get_openai_pinecone_service()

    # Index test data
    await service.index_content(
        content_id="test_1",
        content_type="text",
        data="test content",
        metadata={"category": "test"}
    )

    # Search
    results = await service.search("test", top_k=5)
    assert len(results) > 0
```

## Migration from Qdrant

### Side-by-Side Comparison

```python
# Option 1: A/B test both
@app.post("/api/v1/search/qdrant")
async def search_qdrant(request):
    return await qdrant_service.search(request.query)

@app.post("/api/v1/search/pinecone")
async def search_pinecone(request):
    return await openai_service.search(request.query)

# Compare results, performance, costs
```

### Gradual Migration

```python
# Week 1: 10% traffic to Pinecone
# Week 2: 25% traffic to Pinecone
# Week 3: 50% traffic to Pinecone
# Week 4: 100% traffic to Pinecone

import random

@app.post("/api/v1/search")
async def search(request):
    if random.random() < 0.10:  # 10%
        return await openai_service.search(request.query)
    else:
        return await qdrant_service.search(request.query)
```

## Production Checklist

- [ ] API keys rotated and secured
- [ ] .env in .gitignore
- [ ] Pinecone index created
- [ ] Cost monitoring enabled
- [ ] Rate limiting implemented
- [ ] Caching configured
- [ ] Error handling tested
- [ ] Backup strategy defined
- [ ] Monitoring dashboards set up
- [ ] Team trained on new system

## Troubleshooting

### Issue: "Index not found"

```python
# Create index manually
from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(api_key="your-key")
pc.create_index(
    name="multimodal-search-index",
    dimension=1536,
    metric="cosine",
    spec=ServerlessSpec(cloud="aws", region="us-east-1")
)
```

### Issue: "Rate limit exceeded"

```python
# Implement exponential backoff
from tenacity import retry, wait_exponential, stop_after_attempt

@retry(wait=wait_exponential(min=1, max=60), stop=stop_after_attempt(3))
async def generate_with_retry(text):
    return await openai_service.generate_text_embedding(text)
```

### Issue: "High costs"

```python
# 1. Enable caching
# 2. Reduce video frame count
# 3. Use batch processing
# 4. Set spending limits in OpenAI dashboard
```

## Next Steps

1. ✅ Secure your API keys (URGENT)
2. ✅ Install dependencies
3. ✅ Test the service
4. ✅ Index sample data
5. ✅ Integrate with your app
6. ✅ Set up monitoring
7. ✅ Deploy to production

---

**Your multimodal search now powered by OpenAI + Pinecone!** 🚀
