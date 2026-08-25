from rlm import RLM

from rlm_agent.prompt_utils import build_user_prompt, load_system_prompt

from dotenv import load_dotenv
import os

load_dotenv()

_MODEL_ENV_VAR = "MODEL"
_BACKEND_MODEL_ENV_VAR = "MODAL_NAME"
_VERBOSE_ENV_VAR = "VERBOSE_MODE"


class RunnerConfigError(RuntimeError):
    """Raised when required RLM configuration is missing or invalid."""


def _resolve_verbose() -> bool:
    """Resolve the verbose flag from the environment at call time."""
    return os.getenv(_VERBOSE_ENV_VAR, "false").lower() == "true"


def resolve_model_config(
    model: str | None = None,
    backend_model: str | None = None,
) -> tuple[str, str | None]:
    """Resolve the RLM backend configuration.

    Values are read from the environment at call time (not import time) so
    tests and callers can reconfigure without reloading the module.

    Args:
        model: Explicit backend name; overrides the ``MODEL`` env var.
        backend_model: Explicit backend model name; overrides ``MODAL_NAME``.

    Returns:
        ``(backend, backend_model_name)`` tuple.

    Raises:
        RunnerConfigError: If no backend is configured.
    """
    resolved_model = (
        model
        or os.getenv(_MODEL_ENV_VAR)
    )
    if not resolved_model:
        raise RunnerConfigError(
            f"No LLM backend configured. Set {_MODEL_ENV_VAR} or pass "
            "'model' explicitly."
        )
    resolved_backend_model = (
        backend_model
        if backend_model is not None
        else os.getenv(_BACKEND_MODEL_ENV_VAR)
    ) or None
    return resolved_model, resolved_backend_model


def run_completion(
    user_query: str,
    data: str | None = None,
    model: str | None = None,
    backend_model: str | None = None,
) -> str:
    final_user_prompt = build_user_prompt(user_query=user_query, data=data)
    resolved_model, resolved_backend_model = resolve_model_config(
        model=model,
        backend_model=backend_model,
    )
    rlm = RLM(
        backend=resolved_model,
        backend_kwargs={"model_name": resolved_backend_model},
        custom_system_prompt=load_system_prompt(),
        verbose=_resolve_verbose(),
    )
    return rlm.completion(final_user_prompt).response
