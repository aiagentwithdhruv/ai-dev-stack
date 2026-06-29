"""
Sandbox — restricts where tools can read/write and validates output paths.
Prevents tools from accessing sensitive system locations.
"""

from pathlib import Path

from shared.logger import get_logger

logger = get_logger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent.resolve()

# Tools can ONLY write to these directories
ALLOWED_OUTPUT_DIRS = [
    PROJECT_ROOT / ".tmp",
    PROJECT_ROOT / "runs",
    PROJECT_ROOT / "output",
]

# Tools can NEVER read/write these paths
BLOCKED_PATHS = [
    Path.home() / ".ssh",
    Path.home() / ".aws",
    Path.home() / ".config",
    Path("/etc"),
    Path("/var"),
    Path("/usr"),
    Path("/System"),
]

# Files tools must never touch
PROTECTED_FILES = [
    PROJECT_ROOT / ".env",
    PROJECT_ROOT / "shared" / "env_loader.py",
    PROJECT_ROOT / "shared" / "logger.py",
    PROJECT_ROOT / "shared" / "tool_validator.py",
    PROJECT_ROOT / "shared" / "sandbox.py",
    PROJECT_ROOT / "shared" / "secrets.py",
    PROJECT_ROOT / "AGENT-CONTRACT.md",
]


class SandboxError(Exception):
    """Raised when a tool tries to escape the sandbox."""
    pass


def validate_output_path(path_str: str) -> Path:
    """Validate that an output path is within allowed directories.

    Args:
        path_str: The output path to validate

    Returns:
        Resolved Path object if valid

    Raises:
        SandboxError: If path is outside allowed directories
    """
    path = Path(path_str).resolve()

    # Check against blocked paths
    for blocked in BLOCKED_PATHS:
        if path.is_relative_to(blocked.resolve()):
            raise SandboxError(f"Output path '{path}' is in a blocked location: {blocked}")

    # Check against protected files
    for protected in PROTECTED_FILES:
        if path == protected.resolve():
            raise SandboxError(f"Cannot write to protected file: {protected.name}")

    # Check it's within an allowed directory
    for allowed in ALLOWED_OUTPUT_DIRS:
        allowed_resolved = allowed.resolve()
        if path.is_relative_to(allowed_resolved):
            # Ensure the parent directory exists
            path.parent.mkdir(parents=True, exist_ok=True)
            logger.info(f"Output path validated: {path}")
            return path

    allowed_names = [str(d.relative_to(PROJECT_ROOT)) for d in ALLOWED_OUTPUT_DIRS]
    raise SandboxError(
        f"Output path '{path}' is outside allowed directories.\n"
        f"Allowed: {', '.join(allowed_names)}\n"
        f"Hint: Use .tmp/ for intermediate files or runs/ for logs."
    )


def validate_input_path(path_str: str) -> Path:
    """Validate that an input path is safe to read.

    Args:
        path_str: The input path to validate

    Returns:
        Resolved Path object if valid

    Raises:
        SandboxError: If path points to a sensitive location
    """
    path = Path(path_str).resolve()

    for blocked in BLOCKED_PATHS:
        if path.is_relative_to(blocked.resolve()):
            raise SandboxError(f"Cannot read from blocked location: {blocked}")

    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    logger.info(f"Input path validated: {path}")
    return path
