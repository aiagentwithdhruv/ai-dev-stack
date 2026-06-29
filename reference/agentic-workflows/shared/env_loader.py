"""
Environment loader — validates required env vars before tool execution.
Loads from .env file and checks against config/credentials.yaml.
"""

import os
from pathlib import Path

from shared.logger import get_logger

logger = get_logger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent
ENV_PATH = PROJECT_ROOT / ".env"


def load_env(env_path: str = None):
    """Load environment variables from .env file.

    Args:
        env_path: Optional custom path to .env file
    """
    path = Path(env_path) if env_path else ENV_PATH

    if not path.exists():
        logger.warning(f".env file not found at {path}. Using system environment only.")
        return

    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key and key not in os.environ:
                    os.environ[key] = value

    logger.info("Environment loaded from .env")


def require_env(*keys: str) -> dict:
    """Validate that required environment variables are set.

    Args:
        *keys: Environment variable names to check

    Returns:
        Dict of key → value for all required keys

    Raises:
        EnvironmentError: If any required key is missing
    """
    values = {}
    missing = []

    for key in keys:
        val = os.environ.get(key)
        if val:
            values[key] = val
        else:
            missing.append(key)

    if missing:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing)}. "
            f"Add them to {ENV_PATH}"
        )

    return values
