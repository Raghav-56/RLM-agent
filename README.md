# RLM agent

A general purpose connector to run LLMs in a RLM harness.

## Architecture

```mermaid
%%{init: {
  "theme": "base",
  "themeVariables": {
	"primaryColor": "#e8f5ff",
	"primaryTextColor": "#0b253a",
	"primaryBorderColor": "#1c6ea4",
	"lineColor": "#3a4a5a",
	"fontSize": "14px",
	"tertiaryColor": "#f6f9fc"
  },
  "flowchart": { "curve": "basis", "htmlLabels": true }
}}%%
flowchart LR
	subgraph EP[Entry Points]
		CLI["CLI\nsrc/rlm_agent/cli_app.py"]
		API["FastAPI\nsrc/rlm_agent/api_server.py"]
	end

	subgraph PR[Prompt Layer]
		SP["System Prompt\nsrc/rlm_agent/prompts/system_prompt.txt"]
		PU["Prompt Utils\nsrc/rlm_agent/prompt_utils.py"]
	end

	subgraph CORE[Execution Layer]
		RUN["Runner\nsrc/rlm_agent/runner.py"]
		RLM["RLM Instance\nfrom rlm package"]
	end

	subgraph WEB[Web Layer]
		ROUTER["Web Router\nsrc/rlm_agent/web/routes.py"]
		STATIC["Static Assets\nsrc/rlm_agent/web/static/"]
	end

	CLI -->|user_query| RUN
	API -->|CompletionRequest| RUN
	ROUTER -->|GET /| STATIC
	API -->|mount| STATIC
	RUN -->|compose| PU
	SP --> PU
	PU -->|final prompt| RUN
	RUN -->|RLM instance| RLM
	RLM -->|completion| RUN
	RUN -->|response| CLI
	RUN -->|CompletionResponse| API

	classDef entry fill:#d7ecff,stroke:#1c6ea4,stroke-width:2px,color:#0b253a;
	classDef prompt fill:#ffeecf,stroke:#d08c00,stroke-width:2px,color:#4a3300;
	classDef core fill:#dff7e8,stroke:#2c9a63,stroke-width:2px,color:#0d3b25;
	classDef web fill:#f1e4ff,stroke:#7b57c2,stroke-width:2px,color:#321a5e;

	class CLI,API entry;
	class SP,PU prompt;
	class RUN,RLM core;
	class ROUTER,STATIC web;
```

- CLI and API share the same runner (src/rlm_agent/runner.py).
- Prompt composition centralized in src/rlm_agent/prompt_utils.py.
- Runner orchestrates prompt building, RLM initialization, and response extraction.
- FastAPI accepts CompletionRequest with user_query and optional data payload.
- Data retrieval uses fetch_data_stub() placeholder (can be replaced with actual API integration).
- Website served at / through src/rlm_agent/web/routes.py with static assets in src/rlm_agent/web/static/.
- API errors from RLM calls are returned as HTTP 503 with exception details.

## Usage (user)

- CLI direct: `python -m rlm_agent --prompt "your question"`
- CLI interactive: `python -m rlm_agent`
- API mode: `python -m rlm_agent serve`
- Local development: `python -m rlm_agent serve --host localhost --port 8000`
- Render deploy: Server binds to HOST/PORT automatically (defaults: 0.0.0.0:8000)
- Deployment: `HOST=0.0.0.0 PORT=8000 python -m rlm_agent serve`
- Website: Open http://localhost:8000/ after starting API mode
- Interactive UI: Send user_query + optional data to POST /completion
- API docs: http://localhost:8000/docs

## Usage (developer)

- Core files:
- src/main.py
**Core files:**
- `src/rlm_agent/cli_app.py` — Typer CLI entry point
- `src/rlm_agent/api_server.py` — FastAPI server and routes
- `src/rlm_agent/runner.py` — Shared orchestrator
- `src/rlm_agent/prompt_utils.py` — Prompt composition logic
- `src/rlm_agent/prompts/system_prompt.txt` — Base system instructions
- `src/rlm_agent/web/routes.py` — Web UI router
- `src/rlm_agent/web/templates/index.html` — Web UI template
- `src/rlm_agent/web/static/site.css` — Web UI styles
- `src/rlm_agent/web/static/app.js` — Web UI client script

**Configuration (environment variables):**
- `MODEL` — LM backend (e.g., "gemini", "openai", "anthropic")
- `MODAL_NAME` — Model name passed to backend
- `VERBOSE_MODE` — Enable RLM verbose logging (default: "false")
- `HOST` — Server bind host (default: "0.0.0.0")
- `PORT` — Server bind port (default: "8000")

**Development:**
- Edit `src/rlm_agent/prompts/system_prompt.txt` to tune default behavior
- Keep prompt assembly changes in `src/rlm_agent/prompt_utils.py`
- Use `python -m rlm_agent --help` to view CLI commands
- See Architecture.md for detailed component diagram