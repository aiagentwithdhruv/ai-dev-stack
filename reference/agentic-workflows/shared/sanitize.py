"""
Input sanitization — prevents shell injection and limits input size.
All user inputs passed to tools should go through these functions.
"""

import re
import shlex

from shared.logger import get_logger

logger = get_logger(__name__)


def sanitize_input(value: str, max_length: int = 1000) -> str:
    """Remove shell metacharacters and limit input length.

    Args:
        value: Raw user input
        max_length: Maximum allowed characters (default 1000)

    Returns:
        Sanitized string safe for use in tool arguments
    """
    if not isinstance(value, str):
        return str(value)[:max_length]

    # Remove shell metacharacters that enable injection
    sanitized = re.sub(r'[;&|`$(){}\[\]!<>]', '', value)

    # Collapse multiple spaces
    sanitized = re.sub(r'\s+', ' ', sanitized).strip()

    # Enforce length limit
    sanitized = sanitized[:max_length]

    if sanitized != value.strip():
        logger.warning("Input sanitized: removed potentially dangerous characters")

    return sanitized


def quote_for_shell(value: str) -> str:
    """Safely quote a value for shell interpolation.

    Args:
        value: String to quote for shell use

    Returns:
        Shell-safe quoted string
    """
    return shlex.quote(value)


def validate_url(url: str) -> str:
    """Validate and sanitize a URL (SSRF guard).

    Args:
        url: URL string to validate

    Returns:
        Validated URL

    Raises:
        ValueError: If URL is malformed or uses a blocked scheme/host
    """
    url = url.strip()

    # Only allow http and https
    if not re.match(r'^https?://', url, re.IGNORECASE):
        raise ValueError(f"Invalid URL scheme. Only http:// and https:// allowed. Got: {url[:50]}")

    # Block internal/private IPs
    blocked_hosts = [
        r'localhost',
        r'127\.0\.0\.\d+',
        r'0\.0\.0\.0',
        r'10\.\d+\.\d+\.\d+',
        r'172\.(1[6-9]|2\d|3[01])\.\d+\.\d+',
        r'192\.168\.\d+\.\d+',
        r'\[::1\]',
    ]

    for pattern in blocked_hosts:
        if re.search(pattern, url):
            raise ValueError("URLs pointing to internal/private networks are blocked")

    return url


def validate_email(email: str) -> str:
    """Basic email format validation.

    Args:
        email: Email address to validate

    Returns:
        Validated email address

    Raises:
        ValueError: If email format is invalid
    """
    email = email.strip().lower()
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if not re.match(pattern, email):
        raise ValueError(f"Invalid email format: {email}")

    return email
