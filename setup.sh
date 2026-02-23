#!/bin/bash

# AI Portfolio Copilot Setup Script

set -e

echo "🚀 Setting up AI Portfolio Copilot..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.10+ first."
    exit 1
fi

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

echo "✅ Python and Node.js found"

# Setup Python environment
echo "📦 Setting up Python environment..."
cd backend/python
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip
pip install -r ../../requirements.txt
echo "✅ Python dependencies installed"

# Setup Node.js
echo "📦 Setting up Node.js environment..."
cd ../nodejs
npm install
echo "✅ Node.js dependencies installed"

# Check for .env file
cd ../..
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your API keys before running the application"
else
    echo "✅ .env file exists"
fi

echo ""
echo "✨ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys (OPENAI_API_KEY, PINECONE_API_KEY)"
echo "2. Initialize knowledge base: cd backend/python && python -m scripts.initialize_knowledge_base"
echo "3. Start Python backend: cd backend/python && python -m api.server"
echo "4. Start Node.js gateway: cd backend/nodejs && npm start"
echo "5. Open frontend/example.html in your browser"
echo ""
echo "For more details, see QUICKSTART.md"
