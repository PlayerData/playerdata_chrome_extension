#!/bin/bash

# Start Glance + GitHub PR Scraper
cd "$(dirname "$0")"

echo "🐳 Starting Glance + GitHub PR Scraper..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found"
    echo "Please create a .env file with:"
    echo "GITHUB_KEY=your_github_token"
    echo "GITHUB_USERNAME=your_github_username"
    exit 1
fi

# Build and start containers
echo "🔨 Building and starting containers..."
docker-compose up --build -d

echo "✅ Setup complete!"
echo "🌐 Glance: http://localhost:8085"
echo "📡 RSS Feed: http://localhost:8086/my-open-prs.xml"