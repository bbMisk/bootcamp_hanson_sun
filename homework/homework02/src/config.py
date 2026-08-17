import os
from pathlib import Path

from dotenv import load_dotenv


HOMEWORK_ROOT = Path(__file__).resolve().parents[1]


def load_env(env_path: str | Path | None = None) -> bool:
    path = Path(env_path) if env_path is not None else HOMEWORK_ROOT / ".env"
    return load_dotenv(path)


def get_key(name: str, default: str | None = None) -> str | None:
    return os.getenv(name, default)
