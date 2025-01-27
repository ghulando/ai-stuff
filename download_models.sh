#!/bin/bash

# Create models directory if it doesn't exist
mkdir -p models

# Function to download model
download_model() {
    MODEL_NAME=$1
    MODEL_ID=$2
    
    echo "Downloading $MODEL_NAME..."
    python3 -c "
from huggingface_hub import snapshot_download
import os

model_id = '$MODEL_ID'
local_dir = os.path.join('models', '$MODEL_NAME')

snapshot_download(
    repo_id=model_id,
    local_dir=local_dir,
    ignore_patterns=['*.md', '*.txt'],
    local_dir_use_symlinks=False
)
"
    echo "Finished downloading $MODEL_NAME"
}

# Download TinyLlama model
download_model "tiny-llama" "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

echo "Model downloaded successfully!"
