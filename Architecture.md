# RLM Agent - Detailed Architecture

## System Lifecycle

How a request flows through the system from entry point to response:

```mermaid
%%{init: {
  "theme": "base",
  "themeVariables": {
	"primaryColor": "#e8f5ff",
	"primaryTextColor": "#0b253a",
	"primaryBorderColor": "#1c6ea4",
	"lineColor": "#3a5a7a",
	"fontSize": "12px",
	"tertiaryColor": "#f6f9fc"
  },
  "flowchart": { "curve": "basis", "htmlLabels": true }
}}%%
flowchart TD
	U1["User Input<br/>CLI or API Request"]
	EP["Entry Point<br/>CLI Handler or API Endpoint"]
	BUILDPROMPT["Build User Prompt<br/>Combine System + Query + Data"]
	SYSTEMPROMPT["Load System Prompt<br/>from system_prompt.txt"]
	RUNNER["Runner<br/>run_completion"]
	RLMINIT["RLM Instance<br/>Initialize with Prompt"]
	COMPLETION["RLM Completion<br/>Execute & Call Model"]
	RESPONSE["Return Response"]
	U2["User Output"]

	U1 --> EP
	EP --> RUNNER
	RUNNER --> SYSTEMPROMPT
	SYSTEMPROMPT --> BUILDPROMPT
	RUNNER --> BUILDPROMPT
	BUILDPROMPT --> RLMINIT
	RLMINIT --> COMPLETION
	COMPLETION --> RESPONSE
	RESPONSE --> U2

	classDef user fill:#fff3cd,stroke:#856404,stroke-width:2px,color:#856404;
	classDef entry fill:#d7ecff,stroke:#1c6ea4,stroke-width:2px,color:#0b253a;
	classDef prompt fill:#ffeecf,stroke:#d08c00,stroke-width:2px,color:#4a3300;
	classDef core fill:#dff7e8,stroke:#2c9a63,stroke-width:2px,color:#0d3b25;
	classDef ext fill:#f1e4ff,stroke:#7b57c2,stroke-width:2px,color:#321a5e;

	class U1,U2 user;
	class EP entry;
	class SYSTEMPROMPT,BUILDPROMPT prompt;
	class RUNNER,RLMINIT,COMPLETION core;
	class RESPONSE ext;
```

## Component Interaction

How the major components communicate with each other:

```mermaid
%%{init: {
  "theme": "base",
  "themeVariables": {
	"primaryColor": "#e8f5ff",
	"primaryTextColor": "#0b253a",
	"primaryBorderColor": "#1c6ea4",
	"lineColor": "#3a5a7a",
	"fontSize": "12px",
	"tertiaryColor": "#f6f9fc"
  },
  "flowchart": { "curve": "basis", "htmlLabels": true }
}}%%
graph TB
	CLI["CLI Handler<br/>src/rlm_agent/cli_app.py"]
	API["FastAPI Server<br/>src/rlm_agent/api_server.py"]
	RUNNER["Runner<br/>src/rlm_agent/runner.py"]
	PROMPTUTIL["Prompt Utils<br/>src/rlm_agent/prompt_utils.py"]
	SYSPROMPT["System Prompt<br/>src/rlm_agent/prompts/system_prompt.txt"]
	RLM["RLM Instance<br/>from rlm package"]
	RESPONSE["Response<br/>response.response"]

	CLI -->|user_query or prompt text| RUNNER
	API -->|CompletionRequest<br/>user_query + data| RUNNER
	RUNNER -->|build_user_prompt| PROMPTUTIL
	PROMPTUTIL -->|load_system_prompt| SYSPROMPT
	PROMPTUTIL -->|build final prompt| RUNNER
	RUNNER -->|create RLM instance<br/>with prompts| RLM
	RLM -->|completion method| RESPONSE
	RESPONSE -->|extract response| RUNNER
	RUNNER -->|return string| CLI
	RUNNER -->|return CompletionResponse| API

	classDef entry fill:#d7ecff,stroke:#1c6ea4,stroke-width:2px,color:#0b253a;
	classDef prompt fill:#ffeecf,stroke:#d08c00,stroke-width:2px,color:#4a3300;
	classDef core fill:#dff7e8,stroke:#2c9a63,stroke-width:2px,color:#0d3b25;
	classDef ext fill:#f1e4ff,stroke:#7b57c2,stroke-width:2px,color:#321a5e;

	class CLI,API entry;
	class PROMPTUTIL,SYSPROMPT prompt;
	class RUNNER,RLM core;
	class RESPONSE ext;
```

## Entry Points

How users interact with the RLM Agent:

```mermaid
%%{init: {
  "theme": "base",
  "themeVariables": {
	"primaryColor": "#e8f5ff",
	"primaryTextColor": "#0b253a",
	"primaryBorderColor": "#1c6ea4",
	"lineColor": "#3a5a7a",
	"fontSize": "12px",
	"tertiaryColor": "#f6f9fc"
  },
  "flowchart": { "curve": "basis", "htmlLabels": true }
}}%%
graph LR
	USER["User"]
	
	USER -->|Direct Command| MODE1["CLI Direct<br/>python -m rlm_agent --prompt"]
	USER -->|Interactive| MODE2["CLI Interactive<br/>python -m rlm_agent"]
	USER -->|HTTP Request| MODE3["API Server<br/>python -m rlm_agent serve"]
	USER -->|Browser| MODE4["Web UI<br/>http://localhost:8000"]

	MODE1 -->|invokes| RUNNER["run_completion"]
	MODE2 -->|invokes| RUNNER
	MODE3 -->|POST /completion| API["CompletionRequest<br/>user_query + data"]
	MODE3 -->|GET /| HOME["Home Route<br/>Serves HTML"]
	MODE4 -->|fetches| HOME
	
	API -->|calls| RUNNER
	RUNNER -->|returns| RESULT["String Response"]
	HOME -->|serves| STATIC["Static Assets"]

	classDef user fill:#fff3cd,stroke:#856404,stroke-width:2px,color:#856404;
	classDef entry fill:#d7ecff,stroke:#1c6ea4,stroke-width:2px,color:#0b253a;
	classDef web fill:#ffeecf,stroke:#d08c00,stroke-width:2px,color:#4a3300;
	classDef core fill:#dff7e8,stroke:#2c9a63,stroke-width:2px,color:#0d3b25;

	class USER user;
	class MODE1,MODE2,MODE3,MODE4 entry;
	class HOME,STATIC web;
	class RUNNER,API,RESULT core;
```

## Data Flow

How data moves from input to output:

```mermaid
%%{init: {
  "theme": "base",
  "themeVariables": {
	"primaryColor": "#e8f5ff",
	"primaryTextColor": "#0b253a",
	"primaryBorderColor": "#1c6ea4",
	"lineColor": "#3a5a7a",
	"fontSize": "12px",
	"tertiaryColor": "#f6f9fc"
  },
  "flowchart": { "curve": "basis", "htmlLabels": true }
}}%%
flowchart LR
	subgraph INPUT["Input"]
		QUERY["user_query: str"]
		DATA["data: str | None"]
	end

	subgraph COMPOSE["Prompt Composition"]
		LOAD["load_system_prompt"]
		FETCH["fetch_data_stub<br/>or use provided data"]
		BUILD["build_user_prompt"]
	end

	subgraph RLM_EXEC["RLM Execution"]
		RLMINIT["RLM instance"]
		COMPLETE["completion method"]
	end

	subgraph OUTPUT["Output"]
		EXTRACT["response.response"]
		RETURN["Return to caller"]
	end

	QUERY --> BUILD
	DATA --> FETCH
	FETCH --> BUILD
	LOAD --> BUILD
	BUILD --> RLMINIT
	RLMINIT --> COMPLETE
	COMPLETE --> EXTRACT
	EXTRACT --> RETURN

	classDef input fill:#fff3cd,stroke:#856404,stroke-width:2px,color:#856404;
	classDef compose fill:#ffeecf,stroke:#d08c00,stroke-width:2px,color:#4a3300;
	classDef rlm fill:#dff7e8,stroke:#2c9a63,stroke-width:2px,color:#0d3b25;
	classDef output fill:#d7ecff,stroke:#1c6ea4,stroke-width:2px,color:#0b253a;

	class INPUT input;
	class COMPOSE compose;
	class RLM_EXEC rlm;
	class OUTPUT output;
```

## Component Glossary

### Entry Points (src/rlm_agent/)
- **cli_app.py** — Typer CLI with three modes: direct prompt (`--prompt`), interactive prompt, or serve command. Handles host/port configuration.
- **api_server.py** — FastAPI application with `/health` and `/completion` endpoints. Mounts static files and web router. Returns HTTP 503 on errors.
- **runner.py** — Shared orchestrator called by both CLI and API. Coordinates prompt building, RLM initialization, and response extraction.

### Prompt Layer (src/rlm_agent/)
- **prompt_utils.py** — Core functions: `load_system_prompt()` reads from file, `build_user_prompt()` combines system prompt, data, and user query.
- **prompts/system_prompt.txt** — Base instruction template for the model.
- **Data retrieval** — Currently stubbed with `fetch_data_stub()` placeholder. Optional data can be passed via API or CLI.

### Web Layer (src/rlm_agent/web/)
- **routes.py** — FastAPI router serving GET `/` endpoint that returns HTML response.
- **templates/index.html** — Web UI template for browser interaction.
- **static/site.css** — Web UI styles.
- **static/app.js** — Web UI client-side JavaScript.

### RLM Integration
- **RLM class** — External package imported in runner.py. Initialized with backend (LM provider), model name, system prompt, and verbose flag.
- **backend** — LM provider selection (Anthropic, OpenAI, Gemini, etc.). Set via MODEL environment variable.
- **backend_kwargs** — Additional config like `model_name` passed to RLM.
- **Execution environments** — Managed internally by RLM package (Local, Docker, Modal, E2B, Daytona, Prime).

### Request/Response Models
- **CompletionRequest** — Pydantic model with `user_query: str` and `data: str | None`.
- **CompletionResponse** — Pydantic model with `response: str`.

### Configuration (environment variables)
- **MODEL** — LM backend provider (e.g., "gemini", "openai").
- **MODAL_NAME** — Model name passed to backend (e.g., "gpt-4", "claude-3-opus").
- **VERBOSE_MODE** — Enable verbose logging (default: "false").
- **HOST** — Server bind address (default: "0.0.0.0").
- **PORT** — Server port (default: "8000").

### Core Types (rlm/core/types.py)
- **Message** — Individual message in conversation history
- **Response** — Structured response containing code, output, and metadata
- **CompactionMetadata** — Information about session compaction/history management
- **DepthMetadata** — Metadata tracking execution depth and complexity

### Utilities
- **Token Utils** — Manages token counting and rate limiting
- **Parsing** — Extracts code blocks and structured content from model responses
- **RLM Utils** — Helper functions for session management and data handling
- **Exceptions** — Custom exception types for error handling
- **Logger** — Verbose and structured logging for debugging and monitoring
