#!/usr/bin/env python3
"""
Ensure folder-level junctions exist from .ai/skills/ and .ai/agents/ to:
  - .claude/skills/  (junction -> .ai/skills/)
  - .github/skills/  (junction -> .ai/skills/)
  - .reasonix/skills/  (junction -> .ai/skills/)
  - .claude/agents/  (junction -> .ai/agents/)
  - .github/agents/  (junction -> .ai/agents/)

All platforms read the same canonical source via junctions — no copies or wrappers.

Usage:
    python sync-skills.py              # ensure junctions exist
    python sync-skills.py --dry-run    # show what would change without writing
"""

import argparse
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.parent.parent  # .ai/scripts/ -> .ai/ -> repo root

# Source → [target junctions]
JUNCTIONS = {
    ".ai/skills": [".claude/skills", ".github/skills", ".reasonix/skills", ".pi/skills"],
    ".ai/agents": [".claude/agents", ".github/agents", ".reasonix/agents", ".pi/agents"],
    ".ai/chains": [".pi/chains"],
}


def _is_junction(path: Path) -> bool:
    """Check if a directory is a Windows junction (reparse point)."""
    if sys.platform != "win32":
        return path.is_symlink()
    try:
        import ctypes
        FILE_ATTRIBUTE_REPARSE_POINT = 0x400
        attrs = ctypes.windll.kernel32.GetFileAttributesW(str(path))
        return attrs != -1 and bool(attrs & FILE_ATTRIBUTE_REPARSE_POINT)
    except Exception:
        return False


def _rmdir(path: Path):
    """Remove a directory or junction safely."""
    if _is_junction(path):
        subprocess.run(["cmd", "/c", "rmdir", str(path)], capture_output=True)
    elif path.is_dir():
        import shutil
        shutil.rmtree(str(path), ignore_errors=True)


def sync_junction(source_rel: str, target_rel: str, dry_run: bool) -> str:
    """Ensure target_rel is a junction pointing to source_rel. Returns status."""
    root = SCRIPT_DIR
    target = root / target_rel
    source = (root / source_rel).resolve()

    if target.exists():
        if _is_junction(target):
            # Junction exists — verify it points correctly by checking a known file
            test_file = target / (".gitkeep" if "skills" in source_rel else "architect.md")
            if test_file.exists():
                return "OK"
            # Wrong target or broken — remove and recreate
            action = "RECREATE"
        else:
            action = "RECREATE"
    else:
        action = "CREATE"

    if not dry_run:
        if target.exists():
            _rmdir(target)
        target.parent.mkdir(parents=True, exist_ok=True)
        result = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(target), str(source)],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            return f"FAIL — {result.stderr.strip()}"

    return action


def sync_all(dry_run: bool = False) -> int:
    prefix = "[DRY RUN] " if dry_run else ""
    print(f"{prefix}Ensuring folder-level junctions...")

    changed = 0
    for source_rel, targets in JUNCTIONS.items():
        for target_rel in targets:
            result = sync_junction(source_rel, target_rel, dry_run)
            if result == "OK":
                print(f"  OK   {target_rel} -> {source_rel}")
            else:
                label = f"WOULD {result}" if dry_run else result
                print(f"  {label} {target_rel} -> {source_rel}")
                changed += 1

    print(f"\n{changed} junction(s) {'would be ' if dry_run else ''}changed.")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Ensure junctions from .ai/skills/ and .ai/agents/ to all platform targets"
    )
    parser.add_argument("--dry-run", action="store_true", help="Show changes without writing")
    args = parser.parse_args()
    sys.exit(sync_all(dry_run=args.dry_run))


if __name__ == "__main__":
    main()
