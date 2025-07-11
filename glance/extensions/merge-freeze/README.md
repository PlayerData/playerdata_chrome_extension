# Merge Freeze Extension

A Glance extension that monitors merge freeze status across multiple PlayerData repositories.

## Overview

This extension provides a web server that fetches merge freeze status from multiple repositories and displays them in a Glance dashboard widget. It shows:

- Overall summary of frozen/unfrozen repositories
- Individual repository status (frozen, unfrozen, or error)
- Who froze each repository
- Last update timestamp

## Files

- `merge-freeze-server.py` - Main server application
- `requirements.txt` - Python dependencies
- `Dockerfile.extension` - Docker configuration
- `README.md` - This documentation

## Configuration

The extension requires the following environment variable:

- `MERGE_APP_KEY` - Access token for the MergeFreeze API

## Repositories Monitored

- app (master branch)
- api (master branch)
- web (master branch)
- analysis-services (master branch)
- actions (main branch)

## API Endpoints

- `/` - Returns HTML widget content for Glance
- `/health` - Health check endpoint

## Usage

The extension is automatically started via Docker Compose when running the main Glance application. It serves on port 8081 and provides data to the Glance dashboard.
