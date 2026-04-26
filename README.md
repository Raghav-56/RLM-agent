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
		CLI[Typer CLI\nsrc/main.py -> src/cli_app.py]
		API[FastAPI Server\nsrc/api_server.py]
	end

	subgraph PR[Prompt Layer]
		SP[System Prompt Loader\nsrc/system_prompt.txt]
		PU[Prompt Utils\nsrc/prompt_utils.py]
		DS[(Data Source\nStub now, API later)]
	end

	subgraph CORE[Execution Layer]
		RUN[Runner\nsrc/runner.py]
		RLM[RLM Engine\nrlm package]
		ENV[Execution Environment\nlocal / docker / modal / etc]
	end

	subgraph EXT[External Integrations]
		GEM[Gemini Backend]
		FUT[Future API Producer\nSends data + user_query]
	end

	CLI -->|prompt| PU
	API -->|user_query + optional data| RUN
	SP --> PU
	DS --> PU
	PU -->|composed prompt| RUN
	RUN --> RLM
	RLM --> ENV
	RLM --> GEM
	FUT -. planned input .-> API
	RUN -->|model response| CLI
	RUN -->|JSON response| API

	classDef entry fill:#d7ecff,stroke:#1c6ea4,stroke-width:2px,color:#0b253a;
	classDef prompt fill:#ffeecf,stroke:#d08c00,stroke-width:2px,color:#4a3300;
	classDef core fill:#dff7e8,stroke:#2c9a63,stroke-width:2px,color:#0d3b25;
	classDef ext fill:#f1e4ff,stroke:#7b57c2,stroke-width:2px,color:#321a5e;
	classDef store fill:#ffdfe4,stroke:#c04864,stroke-width:2px,color:#4f1421;

	class CLI,API entry;
	class SP,PU prompt;
	class RUN,RLM,ENV core;
	class GEM,FUT ext;
	class DS store;
```

- CLI and API share the same runner.
- Prompt composition is centralized in src/prompt_utils.py.
- The runner is the only place that configures and calls RLM.
- FastAPI accepts user_query plus optional data payload.
- Data retrieval is stubbed now and can be replaced by producer API.
- Website is served at / through src/web/routes.py with static assets in src/web/static/.
- API errors from model/backend calls are returned as HTTP 503 with details.

## Usage (user)

- CLI direct: python src/main.py --prompt "your question"
- CLI interactive: python src/main.py
- API mode (preferred): python src/main.py serve
- API mode (legacy flag): python src/main.py --serve-api
- Render deploys: the server binds to HOST/PORT automatically (defaults: 0.0.0.0:8000).
- Local override example: python src/main.py serve --host 127.0.0.1 --port 8000
- Website: open http://127.0.0.1:8000/ after starting API mode.
- Interactive UI can send user_query + optional data directly to POST /completion.
- API docs: http://127.0.0.1:8000/docs
- TODO: add curl examples

## Usage (developer)

- Core files:
- src/main.py
- src/cli_app.py
- src/api_server.py
- src/runner.py
- src/prompt_utils.py
- src/web/routes.py
- src/web/templates/index.html
- src/web/static/site.css
- src/web/static/app.js
- Edit src/system_prompt.txt to tune default behavior.
- Keep prompt assembly changes inside src/prompt_utils.py.
- Use python src/main.py --help to view CLI commands/options.
- TODO: add setup, test, and contribution details
