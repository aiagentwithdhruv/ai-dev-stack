"""
Tool Validator — scans Python tool files for dangerous patterns before execution.
Blocks unsafe imports, eval/exec, and shell commands. Run this on any newly created or
modified tool BEFORE executing it; block on failure.
"""

import ast
import re
from pathlib import Path

from shared.logger import get_logger

logger = get_logger(__name__)

# Imports that tools must NEVER use
BLOCKED_IMPORTS = {
    "subprocess",
    "shutil",
    "ctypes",
    "multiprocessing",
    "socket",
    "http.server",
    "xmlrpc",
    "pickle",
    "shelve",
    "code",
    "codeop",
    "compileall",
    "importlib",
}

# Function calls that are never safe in dynamically created tools
BLOCKED_CALLS = {
    "exec",
    "eval",
    "compile",
    "__import__",
    "globals",
    "locals",
    "getattr",
    "setattr",
    "delattr",
}

# os module functions that are dangerous
BLOCKED_OS_CALLS = {
    "os.system",
    "os.popen",
    "os.exec",
    "os.execl",
    "os.execle",
    "os.execlp",
    "os.execlpe",
    "os.execv",
    "os.execve",
    "os.execvp",
    "os.execvpe",
    "os.spawn",
    "os.spawnl",
    "os.spawnle",
    "os.remove",
    "os.rmdir",
    "os.removedirs",
    "os.unlink",
}

# Regex patterns for dangerous code that AST might miss
DANGEROUS_PATTERNS = [
    r"os\.system\s*\(",
    r"os\.popen\s*\(",
    r"subprocess\.",
    r"shutil\.rmtree\s*\(",
    r"__import__\s*\(",
    r"\bexec\s*\(",
    r"\beval\s*\(",
    r"open\s*\(.*/etc/",
    r"open\s*\(.*~/.ssh",
    r"requests\..*\.send\(",  # raw socket-level sends
]


class ToolValidationError(Exception):
    """Raised when a tool file fails security validation."""
    pass


def validate_tool_file(tool_path: str) -> dict:
    """Validate a Python tool file for dangerous patterns.

    Args:
        tool_path: Path to the .py file to validate

    Returns:
        {"safe": True/False, "issues": [...], "file": "..."}

    Raises:
        ToolValidationError: If critical safety violations found
    """
    path = Path(tool_path)
    if not path.exists():
        raise FileNotFoundError(f"Tool file not found: {tool_path}")
    if not path.suffix == ".py":
        raise ToolValidationError(f"Not a Python file: {tool_path}")

    source = path.read_text()
    issues = []

    # 1. AST-based analysis (catches structured code)
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise ToolValidationError(f"Syntax error in {tool_path}: {e}")

    for node in ast.walk(tree):
        # Check imports
        if isinstance(node, ast.Import):
            for alias in node.names:
                module_root = alias.name.split(".")[0]
                if alias.name in BLOCKED_IMPORTS or module_root in BLOCKED_IMPORTS:
                    issues.append(f"Blocked import: '{alias.name}' (line {node.lineno})")

        elif isinstance(node, ast.ImportFrom):
            if node.module:
                module_root = node.module.split(".")[0]
                if node.module in BLOCKED_IMPORTS or module_root in BLOCKED_IMPORTS:
                    issues.append(f"Blocked import: 'from {node.module}' (line {node.lineno})")

        # Check dangerous function calls
        elif isinstance(node, ast.Call):
            func_name = _get_call_name(node)
            if func_name in BLOCKED_CALLS:
                issues.append(f"Blocked call: '{func_name}()' (line {node.lineno})")
            elif func_name in BLOCKED_OS_CALLS:
                issues.append(f"Blocked OS call: '{func_name}()' (line {node.lineno})")

    # 2. Regex-based analysis (catches string-constructed attacks)
    for pattern in DANGEROUS_PATTERNS:
        for match in re.finditer(pattern, source):
            line_num = source[:match.start()].count("\n") + 1
            issues.append(f"Dangerous pattern: '{match.group()}' (line {line_num})")

    # Deduplicate issues
    issues = list(dict.fromkeys(issues))

    result = {"safe": len(issues) == 0, "issues": issues, "file": str(path)}

    if issues:
        logger.warning(
            f"Tool validation FAILED for {path.name}: {len(issues)} issue(s) found",
            extra={"inputs": {"file": str(path), "issues": issues}},
        )
        raise ToolValidationError(
            f"Tool '{path.name}' failed security validation:\n"
            + "\n".join(f"  - {issue}" for issue in issues)
        )

    logger.info(f"Tool validation PASSED for {path.name}")
    return result


def _get_call_name(node: ast.Call) -> str:
    """Extract the full dotted function name from a Call node."""
    if isinstance(node.func, ast.Name):
        return node.func.id
    elif isinstance(node.func, ast.Attribute):
        parts = []
        current = node.func
        while isinstance(current, ast.Attribute):
            parts.append(current.attr)
            current = current.value
        if isinstance(current, ast.Name):
            parts.append(current.id)
        return ".".join(reversed(parts))
    return ""
