# AI Experiments & Tools

This repository is a collection of various AI experiments, tools, and proof-of-concepts. It serves as a playground for exploring different AI technologies, frameworks, and integrations.

## 🧪 Current Experiments

### Ollama + Open WebUI Setup

A Docker Compose setup for running AI models locally with a web interface.

**Location**: `ollama-webui/` directory (`docker-compose.yml`, `Dockerfile.downloader`, `download.sh`)

**What it does**:

- Runs Ollama for local AI model inference
- Provides Open WebUI for easy model interaction
- Automatically downloads TinyLlama and llama3.2:1b models

## 🚀 Planned Experiments

- **LiteLLM**: Unified API for multiple LLM providers
- **n8n**: AI workflow automation
- **LangChain**: AI application development framework
- **Vector Databases**: Embedding storage and retrieval
- **Custom AI Agents**: Specialized AI automation tools
- **Multi-modal AI**: Vision, audio, and text processing
- **AI Fine-tuning**: Custom model training experiments

## 📋 General Prerequisites

- Docker and Docker Compose
- At least 8GB of RAM (more for larger models)
- (Optional) NVIDIA GPU with CUDA support for faster inference
- Various API keys depending on the experiment (Hugging Face, OpenAI, etc.)

## 🎯 Repository Structure

Each experiment will be organized in its own directory or clearly documented section. This keeps different AI tools and concepts separate while maintaining easy access to all experiments.

## 🛠️ Setup Instructions

### Ollama + Open WebUI Experiment

1. Navigate to the experiment directory:

   ```bash
   cd ollama-webui
   ```

2. Create a `.env` file (copy from the example):

   ```bash
   cp .env.example .env
   # Edit .env and add your Hugging Face token
   ```

3. Start the services:

   ```bash
   # Build and start all services
   docker-compose up -d --build
   ```

   This will:
   - Start Ollama and Open WebUI
   - Download TinyLlama from Hugging Face
   - Download llama3.2:1b from Ollama

4. Access the Web UI:

   - Open your browser and navigate to `http://localhost:3000`
   - Wait for the models to finish downloading (check progress in logs)

### Usage

**Web Interface**: Open `http://localhost:3000` to chat with the models through a web interface.

**Terminal Interface**:

```bash
# Interactive chat
docker exec -it ollama ollama run llama3.2:1b

# Single question
docker exec -it ollama ollama run llama3.2:1b "Your question here"
```

**API Access**:

```bash
curl -X POST http://localhost:11434/api/generate -d '{
  "model": "llama3.2:1b",
  "prompt": "Your question here"
}'
```

## 📝 Contributing

Feel free to contribute new AI experiments, improvements, or documentation! Each experiment should:

1. Be well-documented with setup instructions
2. Include any necessary configuration files
3. Have clear usage examples
4. Be organized in its own directory (for larger experiments)

## 📚 Resources & References

- [Ollama Documentation](https://ollama.ai/)
- [Open WebUI](https://github.com/open-webui/open-webui)
- [LiteLLM](https://docs.litellm.ai/)
- [n8n](https://n8n.io/)
- [LangChain](https://python.langchain.com/)

## 🤝 License

This repository is for educational and experimental purposes. Please respect the licenses of individual AI models and tools used within these experiments.
