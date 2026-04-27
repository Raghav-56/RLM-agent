from rlm import RLM

from rlm_agent.prompt_utils import build_user_prompt, load_system_prompt

from dotenv import load_dotenv
import os

load_dotenv()

MODEL = os.getenv("MODEL")
MODAL_NAME = os.getenv("MODAL_NAME")
VERBROSE_MODE = os.getenv("VERBOSE_MODE", "false").lower() == "true"


def run_completion(user_query: str, data: str | None = None) -> str:
    final_user_prompt = build_user_prompt(user_query=user_query, data=data)
    rlm = RLM(
        backend=MODEL,
        backend_kwargs={"model_name": MODAL_NAME},
        custom_system_prompt=load_system_prompt(),
        verbose=VERBROSE_MODE,
    )
    return rlm.completion(final_user_prompt).response