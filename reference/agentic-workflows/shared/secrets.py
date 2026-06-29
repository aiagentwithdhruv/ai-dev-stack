"""
Secret masking — prevents API keys and sensitive values from leaking into logs.
Reads known secret env var names and redacts their values in any string or dict.
"""

import os
import re

# Env var names that contain secrets (add your own as you wire up tools)
SECRET_ENV_VARS = [
    "LLM_API_KEY",
    "OPENROUTER_API_KEY",
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "TAVILY_API_KEY",
    "EXA_API_KEY",
    "SMTP_PASSWORD",
    "GMAIL_TOKEN",
    "GOOGLE_SHEETS_CREDENTIALS",
    "SENDGRID_API_KEY",
    "NOTION_API_KEY",
    "SLACK_TOKEN",
]

REDACTED = "***REDACTED***"


def get_secret_values() -> list:
    """Get all current secret values from environment.

    Returns:
        List of secret values that should be masked (non-empty only)
    """
    values = []
    for var in SECRET_ENV_VARS:
        val = os.environ.get(var, "")
        if val and len(val) > 3:  # Skip very short values to avoid false matches
            values.append(val)
    return values


def mask_secrets(text: str) -> str:
    """Replace any secret values found in text with REDACTED.

    Args:
        text: String that may contain secret values

    Returns:
        String with all secret values replaced
    """
    if not isinstance(text, str):
        return text

    masked = text
    for secret_val in get_secret_values():
        if secret_val in masked:
            masked = masked.replace(secret_val, REDACTED)

    # Also catch common key patterns that might slip through
    # Matches patterns like: sk-xxx, key_xxx, token_xxx (12+ chars)
    masked = re.sub(
        r'(?:sk-|key_|token_|api[_-]?key[=:]\s*)[A-Za-z0-9_\-]{12,}',
        REDACTED,
        masked,
    )

    return masked


def mask_dict(data: dict) -> dict:
    """Recursively mask secrets in a dictionary.

    Args:
        data: Dictionary that may contain secret values

    Returns:
        New dictionary with all secret values masked
    """
    if not isinstance(data, dict):
        return data

    masked = {}
    for key, value in data.items():
        # Mask keys that look like they hold secrets
        key_lower = key.lower()
        if any(s in key_lower for s in ["key", "token", "secret", "password", "credential"]):
            masked[key] = REDACTED
        elif isinstance(value, str):
            masked[key] = mask_secrets(value)
        elif isinstance(value, dict):
            masked[key] = mask_dict(value)
        elif isinstance(value, list):
            masked[key] = [mask_secrets(v) if isinstance(v, str) else v for v in value]
        else:
            masked[key] = value

    return masked
