"""
Structured JSON logger for agentic workflows.
Every tool imports this for consistent, parseable, secret-masked logs.
"""

import logging
import json
import sys
from datetime import datetime, timezone


class JSONFormatter(logging.Formatter):
    """Outputs log records as single-line JSON with secret masking."""

    def format(self, record):
        # Import here to avoid circular imports
        from shared.secrets import mask_secrets, mask_dict

        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": mask_secrets(record.getMessage()),
        }

        # Include extra fields with secret masking
        if hasattr(record, "inputs"):
            log_entry["inputs"] = mask_dict(record.inputs) if isinstance(record.inputs, dict) else mask_secrets(str(record.inputs))
        if hasattr(record, "outputs"):
            log_entry["outputs"] = mask_dict(record.outputs) if isinstance(record.outputs, dict) else mask_secrets(str(record.outputs))
        if hasattr(record, "cost_usd"):
            log_entry["cost_usd"] = record.cost_usd
        if hasattr(record, "duration_ms"):
            log_entry["duration_ms"] = record.duration_ms

        # Include exception info (mask secrets in error messages)
        if record.exc_info and record.exc_info[0]:
            log_entry["error"] = {
                "type": record.exc_info[0].__name__,
                "message": mask_secrets(str(record.exc_info[1])),
            }

        return json.dumps(log_entry)


def get_logger(name: str, level: str = "INFO") -> logging.Logger:
    """Get a configured JSON logger.

    Args:
        name: Logger name (usually __name__)
        level: Log level (DEBUG, INFO, WARNING, ERROR)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)

    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    return logger
