from rlm import RLM

from prompt_utils import build_user_prompt, load_system_prompt

from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_MODEL=os.getenv("GEMINI_MODEL")


def run_completion(user_query: str, data: str | None = None) -> str:
    final_user_prompt = build_user_prompt(user_query=user_query, data=data)
    rlm = RLM(
        backend="gemini",
        backend_kwargs={"model_name": GEMINI_MODEL},
        custom_system_prompt=load_system_prompt(),
        verbose=True,
    )
    return rlm.completion(final_user_prompt).response