#!/bin/bash
echo "🌐 GTIS - Global Trend Intelligence System"
echo "=========================================="
echo ""

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo "📋 Checking prerequisites..."

if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed${NC}"
    exit 1
else
    echo -e "${GREEN}✓ Docker found${NC}"
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed${NC}"
    exit 1
else
    echo -e "${GREEN}✓ Docker Compose found${NC}"
fi

echo ""
echo "🔧 Setting up project..."

mkdir -p data models/cache logs
touch data/.gitkeep models/cache/.gitkeep logs/.gitkeep

if [ ! -f .env ]; then
    cp .env.example .env
    echo -e "${GREEN}✓ .env file created${NC}"
fi

echo ""
echo "🐳 Building Docker containers..."
docker-compose build

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Docker containers built successfully${NC}"
else
    echo -e "${RED}❌ Failed to build Docker containers${NC}"
    exit 1
fi

echo ""
echo "🚀 Starting services..."
docker-compose up -d

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Services started successfully${NC}"
else
    echo -e "${RED}❌ Failed to start services${NC}"
    exit 1
fi

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 15

echo ""
echo "=========================================="
echo -e "${GREEN}✅ GTIS is ready!${NC}"
echo "=========================================="
echo ""
echo "📊 Access your applications:"
echo "   • Frontend Dashboard: http://localhost:8501"
echo "   • Backend API: http://localhost:8000"
echo "   • API Documentation: http://localhost:8000/docs"
echo ""
echo "Happy analyzing! 🎉"
