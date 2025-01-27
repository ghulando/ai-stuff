# AI Models Docker Setup

This repository contains a Dockerized setup for running multiple open-source AI models with a local UI interface.

## Prerequisites

- Docker and Docker Compose
- NVIDIA GPU with CUDA support
- NVIDIA Container Toolkit installed

## Models Included

- Deepseek Coder (1.3B base model)
- LLaMA 2 (7B chat model)

## Setup Instructions

1. Make the download script executable:
   ```bash
   chmod +x download_models.sh
   ```

2. Download the models:
   ```bash
   ./download_models.sh
   ```
   Note: You'll need Hugging Face authentication for some models. Use `huggingface-cli login` with your access token.

3. Build and start the Docker container:
   ```bash
   docker-compose up --build
   ```

4. Access the UI:
   Open your browser and navigate to `http://localhost:7860`

## Usage

1. Select a model from the dropdown menu
2. Click "Load Model" to initialize it
3. Enter your prompt in the input box
4. Click "Generate" to get the model's response

## Directory Structure

- `app.py`: Main application file with the Gradio UI
- `Dockerfile`: Container configuration
- `docker-compose.yml`: Service orchestration
- `requirements.txt`: Python dependencies
- `download_models.sh`: Script to download models
- `models/`: Directory for downloaded models
- `cache/`: Cache directory for model weights

## Notes

- Models are downloaded to the `models` directory and mounted into the container
- The UI runs on port 7860
- GPU acceleration is enabled by default
- Model weights are cached for faster loading
