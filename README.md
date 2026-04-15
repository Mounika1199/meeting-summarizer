# Meeting Summarizer

A real-time meeting transcript summarization tool powered by a local LLM via [Ollama](https://ollama.com). Paste a meeting transcript and receive a structured, speaker-wise summary streamed live to your browser — no data leaves your infrastructure.

## Features

- **Real-time streaming** — summary is streamed token-by-token over WebSockets
- **Hierarchical summarization** — automatically splits long transcripts into chunks and merges the results
- **Multi-language support** — request summaries in any language
- **Fully local** — runs on-premise using Ollama; no external API calls for inference
- **Dockerized** — single `docker-compose up` to run everything

## Architecture

```
Browser (WebSocket)
    │
    ▼
FastAPI app  ──►  Ollama (local LLM)
    │
    ▼
Hierarchical summarization pipeline
  1. Tokenize & chunk transcript
  2. Summarize each chunk
  3. Merge into a final structured summary
```

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) with GPU support (NVIDIA)
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)
- A [Hugging Face](https://huggingface.co/settings/tokens) account and access token (used to download the tokenizer)

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/meeting-summarizer.git
cd meeting-summarizer
```

### 2. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and fill in your values:

```env
HF_TOKEN=hf_your_huggingface_token_here
OLLAMA_HOST=http://ollama:11434
```

### 3. Pull the LLM model

Before starting the app, pull your chosen model into Ollama. The default is `gemma3:12b-20k`:

```bash
ollama pull gemma3:12b-20k
```

Or update `DEFAULT_MODEL` in [app/config.py](app/config.py) to use a different model.

### 4. Start the services

```bash
docker-compose up --build
```

This starts two containers:
- `ollama_container` — Ollama LLM server (GPU-enabled)
- `fastapi_container` — FastAPI application on port `8009`

### 5. Open the app

Navigate to [http://localhost:8009/static/index.html](http://localhost:8009/static/index.html) in your browser.

## Usage

1. Paste your meeting transcript into the text area
2. Select the output language
3. Click **Summarize**
4. The summary streams live to the page, structured as:
   - **Speaker-wise summaries** — bullet points per speaker
   - **Overall meeting summary** — key decisions and action items

## Project Structure

```
meeting_summarizer/
├── app/
│   ├── config.py                  # Environment config, tokenizer setup
│   ├── main.py                    # FastAPI app entry point
│   ├── routes/
│   │   └── websocket_routes.py    # WebSocket endpoint
│   ├── services/
│   │   ├── ollama_client.py       # Streaming calls to Ollama API
│   │   └── summarization_pipeline.py  # Hierarchical summarization logic
│   └── utils/
│       ├── prompt_builder.py      # Prompt templates
│       └── tokenizer_utils.py     # Text chunking by token count
├── static/                        # Frontend HTML/CSS/JS
├── Dockerfile                     # FastAPI app image
├── Dockerfile.ollama              # Ollama image with non-root user
├── docker-compose.yml             # Orchestrates both services
├── requirements.txt
├── .env.example                   # Environment variable template
└── Modelfile                      # Custom Ollama model config (optional)
```

## Configuration

| Variable | Default | Description |
|---|---|---|
| `HF_TOKEN` | — | Hugging Face token for tokenizer download |
| `OLLAMA_HOST` | `http://ollama:11434` | Ollama API base URL |
| `DEFAULT_MODEL` | `gemma3:12b-20k` | Ollama model used for summarization |
| `MAX_CONTEXT_TOKENS` | `6000` | Max tokens per chunk before splitting |

## GPU Configuration

The `docker-compose.yml` is configured for NVIDIA GPUs. Edit the `NVIDIA_VISIBLE_DEVICES` environment variable to match your setup:

```yaml
environment:
  - NVIDIA_VISIBLE_DEVICES=0  # use GPU 0
```

## License

MIT
