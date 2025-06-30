# Ollama WebUI - Simple Setup

This is the simplest possible setup with just 2 services:

- **Ollama**: AI model server
- **Open WebUI**: Web interface for chatting with models

## Quick Start

1. Start the services:

   ```bash
   docker compose up -d
   ```

2. Download the smallest Llama 3 model:

   ```bash
   docker exec ollama ollama pull llama3.2:1b
   ```

3. Access the WebUI at: <http://localhost:3000>

4. Create an account and start chatting!

## What's Included

- **Minimal setup**: Only 2 containers
- **Manual model download**: You control when to download models
- **Open WebUI**: Modern chat interface

## Managing Models

- List downloaded models: `docker exec ollama ollama list`
- Download other models: `docker exec ollama ollama pull <model-name>`
- Remove models: `docker exec ollama ollama rm <model-name>`

## Stop Services

```bash
docker compose down
```
