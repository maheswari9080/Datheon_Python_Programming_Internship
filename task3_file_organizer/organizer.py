#!/usr/bin/env python3
"""Automated File Organizer and Cleanup Utility.

Datheon Python Internship - Task 03.
Executable via:
    python task3_file_organizer/organizer.py --target "path/to/folder" --dry-run
"""

import argparse
import logging
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR.parent) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR.parent))

from task3_file_organizer.categories import CategoryMapper
from task3_file_organizer.safety_guard import (
    resolve_collision_path,
    validate_target_directory,
)

DEFAULT_LOG_DIR = SCRIPT_DIR / "logs"

BANNER = r"""
================================================================================
                    AUTOMATED FILE ORGANIZER & CLEANUP                          
                    Datheon Python Internship Project 03                        
================================================================================
"""


def setup_logger(log_dir: Path) -> logging.Logger:
    """Configure file and console logger."""
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "organizer_audit.log"

    logger = logging.getLogger("FileOrganizer")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger


class OrganizeResult:
    """Tracks execution counts and outcomes."""

    def __init__(self) -> None:
        self.scanned: int = 0
        self.moved: int = 0
        self.skipped: int = 0
        self.collisions_resolved: int = 0
        self.errors: int = 0
        self.details: List[str] = []


def organize_directory(
    target_path: Path,
    dry_run: bool = False,
    collision_policy: str = "rename",
    logger: Optional[logging.Logger] = None,
) -> Tuple[int, OrganizeResult]:
    """Execute organization on target directory.

    Returns:
        Tuple of (exit_code: int, result: OrganizeResult)
        Exit codes: 0 = success, 1 = partial failure, 2 = fatal/unsafe.
    """
    res = OrganizeResult()

    # Step 1: Validate target safety
    is_safe, msg = validate_target_directory(target_path)
    if not is_safe:
        if logger:
            logger.error(f"Unsafe target directory rejected: {msg}")
        return 2, res

    target_dir = Path(msg)
    mapper = CategoryMapper()
    known_categories = set(mapper.all_category_names)

    if logger:
        logger.info(
            f"Starting file organization on '{target_dir}'. Dry-Run={dry_run}, "
            f"Collision Policy={collision_policy}"
        )

    # Step 2: Scan files in target directory (non-recursive to avoid category loops)
    try:
        entries = list(os.scandir(target_dir))
    except Exception as e:
        if logger:
            logger.error(f"Failed to scan directory {target_dir}: {e}")
        return 2, res

    for entry in entries:
        try:
            # Skip subdirectories (including existing category folders)
            if entry.is_dir(follow_symlinks=False):
                res.skipped += 1
                continue

            # Skip symlinks and special files
            if entry.is_symlink():
                res.skipped += 1
                if logger:
                    logger.info(f"Skipping symlink: {entry.name}")
                continue

            # Skip hidden files (starting with dot)
            if entry.name.startswith("."):
                res.skipped += 1
                continue

            source_file = Path(entry.path)
            res.scanned += 1

            # Determine category
            category = mapper.get_category(entry.name)
            dest_folder = target_dir / category
            proposed_dest = dest_folder / entry.name

            # Resolve collisions
            should_move, final_dest = resolve_collision_path(
                proposed_dest, policy=collision_policy
            )

            if not should_move:
                res.skipped += 1
                msg_skip = f"Skipped (collision policy: {collision_policy}): {entry.name}"
                res.details.append(msg_skip)
                if logger:
                    logger.info(msg_skip)
                continue

            if final_dest != proposed_dest:
                res.collisions_resolved += 1
                msg_col = f"Collision resolved: '{entry.name}' -> '{final_dest.name}'"
                res.details.append(msg_col)
                if logger:
                    logger.info(msg_col)

            # Move or preview
            if dry_run:
                res.moved += 1
                preview_msg = f"[DRY-RUN PREVIEW] Would move: '{entry.name}' -> '{category}/{final_dest.name}'"
                res.details.append(preview_msg)
                if logger:
                    logger.info(preview_msg)
            else:
                dest_folder.mkdir(parents=True, exist_ok=True)
                shutil.move(str(source_file), str(final_dest))
                res.moved += 1
                move_msg = f"[MOVED] '{entry.name}' -> '{category}/{final_dest.name}'"
                res.details.append(move_msg)
                if logger:
                    logger.info(move_msg)

        except Exception as file_err:
            res.errors += 1
            err_msg = f"[ERROR] Failed processing '{entry.name}': {file_err}"
            res.details.append(err_msg)
            if logger:
                logger.error(err_msg)

    exit_code = 1 if res.errors > 0 else 0
    if logger:
        logger.info(
            f"Finished run: Scanned={res.scanned}, Moved={res.moved}, "
            f"Skipped={res.skipped}, Collisions={res.collisions_resolved}, Errors={res.errors}"
        )

    return exit_code, res


def main() -> None:
    """CLI Entry point for File Organizer."""
    parser = argparse.ArgumentParser(
        description="Automated File Organizer (Datheon Python Internship Task 3)",
    )
    parser.add_argument(
        "--target",
        type=str,
        default=None,
        help="Target folder path to organize.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate file moves without altering files on disk (Recommended first).",
    )
    parser.add_argument(
        "--collision",
        choices=["rename", "skip", "overwrite"],
        default="rename",
        help="Collision handling policy when destination file already exists.",
    )
    parser.add_argument(
        "--log-dir",
        type=str,
        default=str(DEFAULT_LOG_DIR),
        help="Directory to save execution audit logs.",
    )
    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="Execute immediately without interactive confirmation.",
    )
    args = parser.parse_args()

    print(BANNER)

    target_input = args.target
    if not target_input:
        try:
            target_input = input("Enter the directory path to organize: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nOperation cancelled by user.")
            sys.exit(0)

    if not target_input:
        print("Error: Target directory cannot be empty.")
        sys.exit(2)

    target_path = Path(target_input)
    is_safe, msg = validate_target_directory(target_path)
    if not is_safe:
        print(f"\n[X] SAFETY ERROR: {msg}")
        sys.exit(2)

    resolved_path = Path(msg)
    print(f"Target Directory: {resolved_path}")
    print(f"Execution Mode:   {'DRY-RUN (SIMULATION ONLY)' if args.dry_run else 'LIVE MOVE'}")
    print(f"Collision Policy: {args.collision}")

    if not args.dry_run and not args.non_interactive:
        print("\nWARNING: You are about to move files in this folder!")
        confirm = input("Are you sure you want to proceed? (yes/no): ").strip().lower()
        if confirm not in ("y", "yes"):
            print("Operation aborted by user.")
            sys.exit(0)

    logger = setup_logger(Path(args.log_dir))
    code, result = organize_directory(
        resolved_path,
        dry_run=args.dry_run,
        collision_policy=args.collision,
        logger=logger,
    )

    print("\n" + "=" * 60)
    print("                 EXECUTION SUMMARY                      ")
    print("=" * 60)
    print(f"  Files Scanned:        {result.scanned}")
    print(f"  Files Moved/Planned:  {result.moved}")
    print(f"  Items Skipped:        {result.skipped}")
    print(f"  Collisions Resolved:  {result.collisions_resolved}")
    print(f"  Errors Encountered:   {result.errors}")
    print(f"  Audit Log Saved To:   {args.log_dir}/organizer_audit.log")
    print("=" * 60)

    if result.details:
        print("\nActivity Details (First 10 operations):")
        for detail in result.details[:10]:
            print(f"  {detail}")
        if len(result.details) > 10:
            print(f"  ... and {len(result.details) - 10} more in the log file.")

    sys.exit(code)


if __name__ == "__main__":
    main()
