from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

_INDEX_PATH = Path(__file__).resolve().parent / "templates" / "index.html"


@router.get("/", response_class=HTMLResponse)
def home() -> HTMLResponse:
    html = _INDEX_PATH.read_text(encoding="utf-8")
    return HTMLResponse(content=html)
