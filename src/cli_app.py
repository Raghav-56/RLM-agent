import typer
import uvicorn

from api_server import app as fastapi_app
from runner import run_completion

app = typer.Typer(add_completion=False)


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
    host: str = typer.Option(
        "127.0.0.1",
        "--host",
        help="Host for the FastAPI server.",
    ),
    port: int = typer.Option(
        8000,
        "--port",
        help="Port for the FastAPI server.",
    ),
) -> None:
    if ctx.invoked_subcommand is not None:
        return

    if serve_api:
        serve(host=host, port=port)
        return

    if prompt is None:
        prompt = typer.prompt("Enter prompt")

    typer.echo(run_completion(prompt))


@app.command("serve")
def serve(
    host: str = typer.Option(
        "127.0.0.1",
        "--host",
        help="Host for the FastAPI server.",
    ),
    port: int = typer.Option(
        8000,
        "--port",
        help="Port for the FastAPI server.",
    ),
) -> None:
    """Launch the FastAPI server."""
    uvicorn.run(fastapi_app, host=host, port=port)
