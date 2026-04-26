from pathlib import Path


def load_system_prompt() -> str:
    prompt_path = Path(__file__).with_name("system_prompt.txt")
    return prompt_path.read_text(encoding="utf-8").strip()


def fetch_data_stub() -> str:
    """Temporary placeholder for external data retrieval."""
    return "STUB_DATA: replace with API-fetched data"


def build_user_prompt(user_query: str, data: str | None = None) -> str:
    """Build the final user message sent after the system prompt."""
    resolved_data = data if data is not None else fetch_data_stub()
    clean_query = user_query.strip()
    return (
        "Context data:\n"
        f"{resolved_data}\n\n"
        "User query:\n"
        f"{clean_query}"
    )
