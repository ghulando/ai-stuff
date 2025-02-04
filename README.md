# AI Models with Ollama and Open WebUI

This repository contains a Docker Compose setup for running AI models using Ollama with Open WebUI interface.

## Prerequisites

- Docker and Docker Compose
- At least 8GB of RAM for running models
- (Optional) NVIDIA GPU with CUDA support for faster inference
- Hugging Face account and access token (for TinyLlama model)

## Features

- Easy-to-use web interface with Open WebUI
- Automatic model downloading (TinyLlama and llama3.2:1b)
- Support for multiple models
- Docker-based setup for easy deployment
- Terminal-based interaction options

## Setup Instructions

1. Clone this repository:

   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Create a `.env` file with your configuration:

   ```bash
   # Hugging Face API Token (Get it from https://huggingface.co/settings/tokens)
   HF_TOKEN=your_huggingface_token

   # Ollama Configuration
   OLLAMA_HOST=ollama
   OLLAMA_PORT=11434

   # Models to download from Hugging Face (comma-separated)
   HF_MODELS=TinyLlama/TinyLlama-1.1B-Chat-v1.0

   # Models to download from Ollama (comma-separated)
   OLLAMA_MODELS=llama3.2:1b
   ```

3. Start the services:

   ```bash
   # Build and start all services
   docker-compose up -d --build

   # Check the status of the services
   docker-compose ps
   ```

   This will:
   - Start Ollama and Open WebUI
   - Download TinyLlama from Hugging Face
   - Download llama3.2:1b from Ollama

4. Access the Web UI:
   - Open your browser and navigate to `http://localhost:3000`
   - Wait for the models to finish downloading (check progress in logs)

## Components

- **Ollama**: Handles model serving and inference (runs on port 11434)
- **Open WebUI**: Provides the user interface for interacting with models (runs on port 3000)
- **Model Downloader**: Downloads and manages TinyLlama and llama3.2:1b models automatically

## Directory Structure

- `docker-compose.yml`: Service orchestration and container configuration
- `.env`: Environment variables and model configuration
- `Dockerfile.downloader`: Model downloader service configuration
- `download.sh`: Script for downloading and setting up models
- `models/`: Directory where downloaded models are stored
- `.gitignore`: Specifies which files Git should ignore

## Usage

### Web Interface

1. Open the Web UI at `http://localhost:3000`
2. Available models:
   - TinyLlama (downloaded from Hugging Face)
   - llama3.2:1b (downloaded from Ollama)
3. Features:
   - Chat with models
   - Switch between models
   - Adjust model parameters
   - View model information

### Terminal Interface

1. Single question/response:

   ```bash
   # Ask a single question
   docker exec -it ollama ollama run llama3.2:1b "Your question here"
   ```

2. Interactive chat session:

   ```bash
   # Start an interactive chat session
   docker exec -it ollama ollama run llama3.2:1b
   ```

3. API calls using curl:

   ```bash
   # Generate a response using the API
   curl -X POST http://localhost:11434/api/generate -d '{
     "model": "llama3.2:1b",
     "prompt": "Your question here"
   }'
   ```

### Model Management

```bash
# List all available models
docker exec -it ollama ollama list

# Remove a model
docker exec -it ollama ollama rm llama3.2:1b

# Pull a specific model
docker exec -it ollama ollama pull llama3.2:1b
```

## Troubleshooting

1. If models fail to download:

   ```bash
   # Check model downloader logs
   docker-compose logs model-downloader
   
   # Check Ollama logs
   docker-compose logs ollama
   ```

2. If services aren't starting:

   ```bash
   # Restart all services
   docker-compose down
   docker-compose up -d --build
   ```

## Notes

- Models are downloaded automatically during startup
- Models are persisted in Docker volumes and the models directory
- The Web UI runs on port 3000
- Ollama API is available on port 11434
- Both web interface and terminal commands can be used to interact with the models
- First startup might take longer due to model downloads
