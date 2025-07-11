# Glance Merge Freeze Extension

A simple FastAPI-based extension for Glance that displays merge freeze status across multiple repositories.

## Features

- 🔒 Shows merge freeze status for all repositories
- 📊 Clean, modern UI using Glance's built-in CSS classes
- ⚡ Fast async API calls
- 🏥 Health check endpoint
- 🐳 Docker support with Docker Compose

## Quick Start

1. **Set up environment variables**:

   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

2. **Start the services**:

   ```bash
   ./start-glance-with-extension.sh
   ```

3. **Access the dashboard**:
   - Glance Dashboard: http://localhost:8080
   - Extension API: http://localhost:8081
   - Health Check: http://localhost:8081/health

## Configuration

Edit `config/home.yml` to configure your Glance dashboard. The extension widget is already configured:

```yaml
- type: extension
  url: http://merge-freeze-extension:8081
  cache: 2m
  allow-potentially-dangerous-html: true
```

## Environment Variables

- `MERGE_APP_KEY`: Your MergeFreeze API key
- `GITHUB_KEY`: Your GitHub token
- `PAGER_KEY`: Your PagerDuty API key
- `AQI_KEY`: Your Air Quality API key

## Manual Commands

```bash
# Start services
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down

# Rebuild and restart
docker compose up --build -d
```

## Architecture

- **FastAPI**: Modern Python web framework
- **Async/Await**: Concurrent API calls for better performance
- **Docker**: Containerized deployment
- **Glance Extensions**: Native integration with Glance dashboard

## API Endpoints

- `GET /` - Main widget endpoint (returns HTML)
- `GET /health` - Health check endpoint (returns JSON)

## Repositories Monitored

- PlayerData/app
- PlayerData/playerdata-core
- PlayerData/api
- PlayerData/web
- PlayerData/analysis-services

## Troubleshooting

1. **Extension not loading**: Check that the extension service is healthy:

   ```bash
   curl http://localhost:8081/health
   ```

2. **API errors**: Check the logs:

   ```bash
   docker compose logs merge-freeze-extension
   ```

3. **Port conflicts**: Change ports in `docker-compose.yml` if needed

## Development

To run locally without Docker:

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export MERGE_APP_KEY=your_key_here

# Run the app
python app.py
```
