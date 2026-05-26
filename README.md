# multi-input-agent
Python script to set the foundation for our multi-input AI executive assistant

## Setup

Ollama (AI model inference)
```bash
# install, run again to update
curl -fsSL https://ollama.com/install.sh | sh # Linux or MacOS?
irm https://ollama.com/install.ps1 | iex # Windows Powershell or download at https://ollama.com/download/windows

ollama --version # check installed
ollama pull gemma4:e2b # download model
ollama list # check model downloaded
ollama run gemma4:e2b --verbose # test model
```

uv (python package manager and virtual environment)
```bash
# install, run again to update
curl -LsSf https://astral.sh/uv/install.sh | sh # Linux or MacOS?
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex" # Windows Powershell

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
