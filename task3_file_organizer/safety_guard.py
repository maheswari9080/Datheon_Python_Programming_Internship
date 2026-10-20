"""Filesystem safety guard, path validation, and collision resolution."""

import os
import sys
from pathlib import Path
from typing import Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent


class SafetyError(Exception):
    """Raised when an operation violates filesystem safety constraints."""
    pass


def validate_target_directory(target_path: Path) -> Tuple[bool, str]:
    """Validate that target directory exists and is safe to organize.

    Safety rules:
    - Target must exist and be a directory.
    - Must NOT be a filesystem root (e.g. C:\, D:\, /).
    - Must NOT be a critical OS system directory.
    - Must NOT be the project repository directory itself.
    """
    try:
        resolved = target_path.resolve()
    except Exception as e:
        return False, f"Could not resolve target path: {e}"

    if not resolved.exists():
        return False, f"Target directory does not exist: {resolved}"

    if not resolved.is_dir():
        return False, f"Target path is a file, not a directory: {resolved}"

    # Check root filesystem
    if resolved == resolved.parent or str(resolved).rstrip("\\/") in ("/", "C:", "D:", "E:", "F:", "C:\\", "D:\\"):
        return False, f"Refusing to organize filesystem root: {resolved}"

    # Check protected system folders
    resolved_str = str(resolved).lower()
    system_patterns = ["windows", "system32", "program files", "program files (x86)", "/etc", "/bin", "/usr", "/sys", "/proc"]
    for pat in system_patterns:
        if resolved_str == pat or resolved_str.endswith(f"\\{pat}") or resolved_str.endswith(f"/{pat}"):
            return False, f"Refusing to organize protected system directory: {resolved}"

    # Check if target IS the project repository itself
    try:
        if resolved == PROJECT_ROOT.resolve():
            return False, f"Refusing to organize the internship project root repository: {resolved}"
    except Exception:
        pass

    return True, str(resolved)


def resolve_collision_path(destination_file: Path, policy: str = "rename") -> Tuple[bool, Path]:
    """Resolve file collision according to policy.

    Args:
        destination_file: Proposed destination file path.
        policy: 'rename' (append _1, _2), 'skip' (do not move), or 'overwrite'.

    Returns:
        Tuple of (should_move: bool, resolved_path: Path)
    """
    if not destination_file.exists():
        return True, destination_file

    if policy == "skip":
        return False, destination_file

    if policy == "overwrite":
        return True, destination_file

    # Default: rename policy
    parent = destination_file.parent
    stem = destination_file.stem
    suffix = destination_file.suffix

    counter = 1
    while True:
        candidate = parent / f"{stem}_{counter}{suffix}"
        if not candidate.exists():
            return True, candidate
        counter += 1
