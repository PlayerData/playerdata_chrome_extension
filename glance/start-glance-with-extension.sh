#!/bin/bash

echo "🚀 Starting Glance with Merge Freeze Extension..."

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found. Creating template..."
    cat > .env << EOF
MERGE_APP_KEY=your_merge_freeze_api_key_here
EOF
    echo "📝 Please edit .env file with your API key before continuing."
    echo "Press Enter to continue or Ctrl+C to stop and edit the file..."
    read
fi

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Create config directory if it doesn't exist
mkdir -p config

# Check if home.yml exists
if [ ! -f "config/home.yml" ]; then
    echo "⚠️  Warning: config/home.yml not found. Please ensure Glance configuration exists."
fi

# Use docker compose (try both v2 and v1 syntax)
if command -v "docker" >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
    echo "🐳 Using Docker Compose v2..."
    docker compose up -d
elif command -v "docker-compose" >/dev/null 2>&1; then
    echo "🐳 Using Docker Compose v1..."
    docker-compose up -d
else
    echo "❌ Docker Compose not found. Please install Docker Compose."
    exit 1
fi

# Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 5

# Check if services are running
if docker ps --format "table {{.Names}}\t{{.Status}}" | grep -E "(glance|merge-freeze)"; then
    echo "✅ Services are running!"
    echo ""
    echo "📊 Glance Dashboard: http://localhost:8080"
    echo "🔒 Extension Status: http://localhost:8081"
    echo "🏥 Extension Health: http://localhost:8081/health"
    echo ""
    echo "To stop the services, run: docker compose down"
else
    echo "❌ Services failed to start. Check logs with: docker compose logs"
    exit 1
fi
