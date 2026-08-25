"""Tests for rlm_agent.runner configuration resolution (pure logic only)."""

import pytest

from rlm_agent.runner import RunnerConfigError, resolve_model_config


@pytest.fixture(autouse=True)
def _clean_env(monkeypatch):
    for var in ("MODEL", "MODAL_NAME", "VERBOSE_MODE"):
        monkeypatch.delenv(var, raising=False)


def test_env_vars_used(monkeypatch):
    monkeypatch.setenv("MODEL", "openai")
    monkeypatch.setenv("MODAL_NAME", "gpt-5")
    assert resolve_model_config() == ("openai", "gpt-5")


def test_missing_model_raises(monkeypatch):
    monkeypatch.delenv("MODEL", raising=False)
    with pytest.raises(RunnerConfigError, match="MODEL"):
        resolve_model_config()


def test_explicit_args_win_over_env(monkeypatch):
    monkeypatch.setenv("MODEL", "openai")
    monkeypatch.setenv("MODAL_NAME", "gpt-5")
    assert resolve_model_config(model="anthropic", backend_model="claude") == (
        "anthropic",
        "claude",
    )


def test_partial_override_falls_back_to_env(monkeypatch):
    monkeypatch.setenv("MODEL", "openai")
    monkeypatch.setenv("MODAL_NAME", "gpt-5")
    assert resolve_model_config(model="anthropic") == ("anthropic", "gpt-5")
    assert resolve_model_config(backend_model="o4-mini") == ("openai", "o4-mini")


def test_unset_backend_model_resolves_to_none():
    assert resolve_model_config(model="openai") == ("openai", None)


def test_empty_model_env_raises(monkeypatch):
    monkeypatch.setenv("MODEL", "")
    with pytest.raises(RunnerConfigError):
        resolve_model_config()


def test_empty_backend_name_becomes_none(monkeypatch):
    monkeypatch.setenv("MODEL", "openai")
    monkeypatch.setenv("MODAL_NAME", "")
    assert resolve_model_config() == ("openai", None)


def test_verbose_resolution(monkeypatch):
    from rlm_agent.runner import _resolve_verbose

    assert _resolve_verbose() is False
    monkeypatch.setenv("VERBOSE_MODE", "true")
    assert _resolve_verbose() is True
    monkeypatch.setenv("VERBOSE_MODE", "TRUE")
    assert _resolve_verbose() is True
