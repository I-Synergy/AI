"""Shared fixtures for the Claude template test suite."""

import sys
import io
from pathlib import Path

import pytest

# Fix UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

TESTS_DIR = Path(__file__).parent
TEMPLATE_ROOT = TESTS_DIR.parent.parent


@pytest.fixture(scope="session")
def template_root() -> Path:
    return TEMPLATE_ROOT


@pytest.fixture(scope="session")
def skills_dir(template_root) -> Path:
    return template_root / ".ai" / "skills"
