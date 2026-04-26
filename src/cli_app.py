import typer
import uvicorn
import os

from api_server import app as fastapi_app
from runner import run_completion

app = typer.Typer(add_completion=False)


def _resolve_server_host_port(
    host: str | None,
    port: int | None,
) -> tuple[str, int]:
    resolved_host = host if host is not None else os.getenv("HOST", "0.0.0.0")
    resolved_port = (
        port if port is not None else int(os.getenv("PORT", "8000"))
    )
    return resolved_host, resolved_port


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    prompt: str | None = typer.Option(
        None,
        "--prompt",
        "-p",
        help="The prompt to send to the model.",
    ),
    serve_api: bool = typer.Option(
        False,
        "--serve-api",
        help="Start the FastAPI server.",
    ),
    host: str | None = typer.Option(
        None,
        "--host",
        help=(
            "Host for the FastAPI server "
            "(defaults to HOST env var or 0.0.0.0)."
        ),
    ),
    port: int | None = typer.Option(
        None,
        "--port",
        help="Port for the FastAPI server (defaults to PORT env var or 8000).",
    ),
) -> None:
    if ctx.invoked_subcommand is not None:
        return

    if serve_api:
        serve(host=host, port=port)
        return

    prompt_text = (
        prompt if prompt is not None else typer.prompt("Enter prompt")
    )
    typer.echo(run_completion(prompt_text))


@app.command("serve")
def serve(
    host: str | None = typer.Option(
        None,
        "--host",
        help=(
            "Host for the FastAPI server "
            "(defaults to HOST env var or 0.0.0.0)."
        ),
    ),
    port: int | None = typer.Option(
        None,
        "--port",
        help="Port for the FastAPI server (defaults to PORT env var or 8000).",
    ),
) -> None:
    """Launch the FastAPI server."""
    resolved_host, resolved_port = _resolve_server_host_port(host, port)
    uvicorn.run(fastapi_app, host=resolved_host, port=resolved_port)
