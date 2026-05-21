# multi-input-agent
Python script to set the foundation for our multi-input AI executive assistant

## Setup

### Linux

Ollama (AI model inference)

```bash
# install, run again to update
curl -fsSL https://ollama.com/install.sh | sh

ollama pull gemma4:e4b
```

uv (python package manager and virtual environment)
```bash
# install, run again to update
curl -LsSf https://astral.sh/uv/install.sh | sh

# run in project directory
uv sync
```

## Environment Variables

Create an `.env` file and fill in your secrets:

```
DISCORD_WH_TOKEN=...
```

## Run

```bash
# run in project directory
uv run --env-file .env run.py
```
