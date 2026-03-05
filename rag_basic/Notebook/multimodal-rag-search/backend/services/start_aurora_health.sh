#!/bin/bash
# Aurora Health AI - Quick Start Script

echo "🏥 =========================================="
echo "   AURORA HEALTH AI - QUICK START"
echo "   Medical-Grade AI Healthcare Platform"
echo "=========================================="
echo ""

# Check Python version
echo "✓ Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "  Python $python_version detected"
echo ""

# Check if .env exists
if [ ! -f "backend/.env" ]; then
    echo "⚠️  Creating .env file..."
    cat > backend/.env << 'EOF'
# Aurora Health AI Configuration

# OpenAI API Key (REQUIRED)
OPENAI_API_KEY=your-openai-key-here
OPENAI_MODEL=gpt-4o
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

# Pinecone (Optional - for vector search)
PINECONE_API_KEY=your-pinecone-key-here
PINECONE_INDEX_NAME=aurora-health-ai

# Application
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO

# Security (Change in production!)
SECRET_KEY=change-this-in-production-use-random-string
EOF
    echo "  ✓ Created backend/.env"
    echo "  ⚠️  IMPORTANT: Edit backend/.env and add your OpenAI API key!"
    echo ""
fi

# Install dependencies
echo "📦 Installing dependencies..."
cd backend
pip install --break-system-packages -r requirements_health.txt -q
cd ..
echo "  ✓ Dependencies installed"
echo ""

# Create data directory
echo "📁 Creating data directory..."
mkdir -p /mnt/user-data/outputs/data
echo "  ✓ Data directory created"
echo ""

# Initialize database
echo "🗄️  Initializing medical database..."
python3 -c "
import sys
sys.path.insert(0, 'backend')
from databases.medical_knowledge_base import get_medical_kb
kb = get_medical_kb()
print('  ✓ Medical knowledge base initialized')
print(f'  ✓ Database location: {kb.db_path}')
"
echo ""

# Test services
echo "🧪 Testing medical services..."
python3 << 'PYTHON'
import sys
import asyncio
sys.path.insert(0, 'backend')

async def test_services():
    try:
        from services.openai_pinecone_service import get_openai_pinecone_service
        from databases.medical_knowledge_base import get_medical_kb
        
        # Test medical KB
        kb = get_medical_kb()
        diseases = kb.query_diseases(['fever', 'cough'])
        print(f"  ✓ Medical KB working ({len(diseases)} diseases found)")
        
        # Test OpenAI service
        openai_service = get_openai_pinecone_service()
        print("  ✓ OpenAI service initialized")
        
        print("\n✅ All services operational!")
        
    except Exception as e:
        print(f"\n❌ Service test failed: {e}")
        print("\n💡 Make sure you've added your OpenAI API key to backend/.env")

asyncio.run(test_services())
PYTHON
echo ""

echo "🚀 =========================================="
echo "   READY TO LAUNCH!"
echo "=========================================="
echo ""
echo "To start Aurora Health AI:"
echo ""
echo "  cd backend"
echo "  python3 main_health.py"
echo ""
echo "Then open: http://localhost:8000/api/docs"
echo ""
echo "📚 API Documentation will be available at:"
echo "   http://localhost:8000/api/docs"
echo ""
echo "🔐 SECURITY REMINDER:"
echo "   1. Keep your .env file secure"
echo "   2. Never commit API keys to git"
echo "   3. Use different keys for production"
echo ""
echo "💡 NEXT STEPS:"
echo "   1. Test the API endpoints in /api/docs"
echo "   2. Try the AI doctor consultation"
echo "   3. Upload a medical image for analysis"
echo "   4. Check medication interactions"
echo ""
echo "Need help? Check AURORA_HEALTH_AI.md for documentation"
echo ""
