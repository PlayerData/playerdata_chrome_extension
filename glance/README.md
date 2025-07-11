# Glance Dashboard with Extensions

A customizable dashboard with merge freeze monitoring and GitHub PR integration.

## Features

- 🔒 Shows merge freeze status for all repositories
- 📋 Displays your open GitHub pull requests via RSS feed
- 📊 PagerDuty incident monitoring
- ⚡ Fast async API calls
- 🏥 Health check endpoints
- 🐳 Full Docker support with Docker Compose

## Quick Start

1. **Set up environment variables**:

   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

2. **Start the services**:

   ```bash
   ./start.sh
   ```

3. **Access the dashboard**:
   - Glance Dashboard: http://localhost:8085
   - Extension API: http://localhost:8081
   - GitHub RSS Feed: http://localhost:8086/my-open-prs.xml
   - Health Check: http://localhost:8081/health

## Configuration

Edit `config/home.yml` to configure your Glance dashboard. Both extensions are configured:

```yaml
- type: extension
  url: http://merge-freeze-extension:8081
  cache: 2m
  allow-potentially-dangerous-html: true

- type: rss
  title: My Open Pull Requests
  limit: 10
  cache: 1m
  feeds:
    - url: http://github-pr-scraper:8086/my-open-prs.xml
      title: My PRs
```

## Environment Variables

- `MERGE_APP_KEY`: Your MergeFreeze API key
- `GITHUB_KEY`: Your GitHub token
- `GITHUB_USERNAME`: Your GitHub username
- `PAGER_KEY`: Your PagerDuty API key
- `AQI_KEY`: Your Air Quality API key

## Structure

- `config/` - Glance configuration files
- `assets/` - Static assets (logos, etc.)
- `github-pr-scraper.py` - GitHub PR scraper and RSS server
- `app.py` - Merge freeze extension
- `docker-compose.yml` - Runs Glance + both extensions
- `start.sh` - Easy startup script

## Manual Commands

```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down

# Rebuild and restart
docker compose up --build -d

# Restart individual services
docker-compose restart glance
docker-compose restart github-pr-scraper
docker-compose restart merge-freeze-extension
```

## Architecture

- **Glance**: Main dashboard application
- **Merge Freeze Extension**: Python HTTP service for repository status
- **GitHub PR Scraper**: Python HTTP service generating RSS feed of open PRs
- **Docker**: Containerized deployment for all services

## Services

### Merge Freeze Extension (Port 8081)
- `GET /` - Main widget endpoint (returns HTML)
- `GET /health` - Health check endpoint (returns JSON)

### GitHub PR Scraper (Port 8086)
- `GET /my-open-prs.xml` - RSS feed of open pull requests
- `GET /health` - Health check endpoint (returns JSON)
- Generates RSS feed on-demand from GitHub API
- Filters by author and PlayerData organization

## Repositories Monitored

- PlayerData/app
- PlayerData/playerdata-core
- PlayerData/api
- PlayerData/web
- PlayerData/analysis-services

## Troubleshooting

1. **Extension not loading**: Check that services are healthy:

   ```bash
   curl http://localhost:8081/health
   curl http://localhost:8086/my-open-prs.xml
   ```

2. **API errors**: Check the logs:

   ```bash
   docker compose logs merge-freeze-extension
   docker compose logs github-pr-scraper
   ```

3. **Port conflicts**: Change ports in `docker-compose.yml` if needed

## Development

To run locally without Docker:

```bash
# Merge Freeze Extension
pip install -r requirements.txt
export MERGE_APP_KEY=your_key_here
python app.py

# GitHub PR Scraper
python github-pr-scraper.py
```
