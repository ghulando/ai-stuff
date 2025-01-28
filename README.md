# AI Models with Ollama and Open WebUI

This repository contains a Docker Compose setup for running AI models using Ollama with Open WebUI interface.

## Prerequisites

- Docker and Docker Compose
- At least 8GB of RAM for running models
- (Optional) NVIDIA GPU with CUDA support for faster inference
- Hugging Face account and access token (for TinyLlama model)

## Features

- Easy-to-use web interface with Open WebUI
- Automatic model downloading (TinyLlama and llama2:1b)
- Support for multiple models
- Docker-based setup for easy deployment

## Setup Instructions

1. Create a `.env` file with your configuration:
   ```bash
   OLLAMA_PORT=11434
   HF_TOKEN=your_huggingface_token  # Replace with your Hugging Face token
   ```

2. Start the services:
   ```bash
   docker-compose up -d
   ```
   This will:
   - Start Ollama and Open WebUI
   - Download TinyLlama from Hugging Face
   - Download llama2:1b from Ollama

3. Access the Web UI:
   Open your browser and navigate to `http://localhost:3000`

## Components

- **Ollama**: Handles model serving and inference
- **Open WebUI**: Provides the user interface for interacting with models
- **Model Downloader**: Downloads TinyLlama and llama2:1b models automatically

## Directory Structure

- `docker-compose.yml`: Service orchestration
- `.env`: Environment configuration
- `Dockerfile.downloader`: Model downloader configuration
- `download.sh`: Model download script
- `models/`: Directory for downloaded models

## Usage

1. Open the Web UI at `http://localhost:3000`
2. The following models will be available:
   - TinyLlama (downloaded from Hugging Face)
   - llama2:1b (downloaded from Ollama)
3. Start chatting with your preferred model
4. You can:
   - Switch between models
   - Adjust model parameters
   - View model information

## Notes

- Models are downloaded automatically during startup
- Models are persisted in Docker volumes and the models directory
- The Web UI runs on port 3000
- Ollama API is available on port 11434
