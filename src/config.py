import os
from pathlib import Path

from dotenv import load_dotenv


DEFAULT_ENV_PATH = Path(__file__).resolve().parents[1] / ".env"


def load_env(env_path: str | Path | None = None, *, override: bool = False) -> bool:
    path = Path(env_path) if env_path is not None else DEFAULT_ENV_PATH
    return load_dotenv(dotenv_path=path, override=override)


def get_key(name: str = "API_KEY") -> str | None:
    return os.getenv(name)
