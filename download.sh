#!/bin/bash

echo "Starting model downloads..."

# Download from Hugging Face
echo "Downloading TinyLlama from Hugging Face..."
python3 -c '
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    local_dir="/models/TinyLlama-1.1B-Chat-v1.0",
    token="'$HF_TOKEN'",
    ignore_patterns=["*.md", "*.txt"]
)
'

# Wait for Ollama to be ready
echo "Waiting for Ollama service..."
sleep 10

# Download from Ollama
echo "Downloading llama2:1b from Ollama..."
curl -X POST http://ollama:11434/api/pull -d '{"name": "llama2:1b"}'

echo "Downloads completed!" 