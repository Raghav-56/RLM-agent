from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
import logging

from runner import run_completion
from web.routes import router as web_router

app = FastAPI(title="RLM Agent API", version="0.1.0")
logger = logging.getLogger(__name__)

_STATIC_DIR = Path(__file__).resolve().parent / "web" / "static"
app.mount("/static", StaticFiles(directory=_STATIC_DIR), name="static")
app.include_router(web_router)


class CompletionRequest(BaseModel):
    user_query: str
    data: str | None = None


class CompletionResponse(BaseModel):
    response: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/completion", response_model=CompletionResponse)
def completion(request: CompletionRequest) -> CompletionResponse:
    try:
        result = run_completion(
            user_query=request.user_query,
            data=request.data,
        )
    except Exception as exc:
        logger.exception("Completion request failed")
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    return CompletionResponse(response=result)
