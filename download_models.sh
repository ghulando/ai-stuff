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

# Download models
download_model "deepseek-coder" "deepseek-ai/deepseek-coder-1.3b-base"
download_model "llama2" "meta-llama/Llama-2-7b-chat-hf"

echo "All models downloaded successfully!"
