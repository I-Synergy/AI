#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate the release-versioning job in .github/workflows/ci.yml.

In the template repository, checks:
  1. ci.yml, the inline version step and CHANGELOG.md exist; the old scripts are gone
  2. ci.yml triggers on push to main only
  3. ci.yml requests contents: write and wires changelog, tag and release steps
  4. the tag is the plain build number (no `v` prefix)
  5. the inline version step derives the documented values for merge and PR builds

In an implementing repository, the template's release layout does not apply.
The same test then checks the project's own release contract instead:
  * a workflow that tags or publishes a release,
  * every `scripts/...` path that workflow references exists,
  * the releasing workflow names a version/build source it uses.
A repository with no release workflow is reported as not applicable, not failed.
"""

import io
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

SCRIPT_DIR = Path(__file__).parent
TEMPLATE_ROOT = SCRIPT_DIR.parent.parent
WORKFLOW = TEMPLATE_ROOT / ".github" / "workflows" / "ci.yml"
OLD_WORKFLOW = TEMPLATE_ROOT / ".github" / "workflows" / "release.yml"
OLD_SCRIPTS = TEMPLATE_ROOT / "scripts"

BUILD_NUMBER = "2026.11028.11435"
MERGE_VERSION = {
    "VersionNumber": "2026.11028.11435.0",
    "VersionInformational": "2026.11028.11435",
    "VersionPackage": "2026.11028.11435",
}


def ok(message: str) -> None:
    print(f"  PASS: {message}")


def fail(message: str) -> None:
    print(f"  FAIL: {message}")


def read(path: Path) -> str:
    """Read a file the host may have written as UTF-16 (Windows PowerShell's default)."""
    raw = path.read_bytes()
    if raw.startswith((b"\xff\xfe", b"\xfe\xff")):
        return raw.decode("utf-16")
    return raw.decode("utf-8")


def load_workflow() -> dict:
    import yaml

    return yaml.safe_load(read(WORKFLOW))


def version_step(doc: dict) -> dict:
    for step in doc.get("jobs", {}).get("release", {}).get("steps", []):
        if step.get("id") == "version":
            return step
    return {}


def test_files_exist() -> bool:
    print("TEST 1: release assets exist")
    print("-" * 40)
    valid = True
    if not WORKFLOW.exists():
        fail(f"{WORKFLOW.relative_to(TEMPLATE_ROOT)} not found")
        valid = False
    else:
        ok("ci.yml")
    if OLD_WORKFLOW.exists():
        fail("release.yml still exists; the release job belongs in ci.yml")
        valid = False
    else:
        ok("release.yml removed")
    if OLD_SCRIPTS.exists():
        fail("scripts/ still exists; the versioning logic is inline in ci.yml")
        valid = False
    else:
        ok("scripts/ removed")
    return valid


def test_workflow_trigger(doc: dict) -> bool:
    print("\nTEST 2: workflow triggers on push to main only")
    print("-" * 40)
    # PyYAML resolves the bare `on` key to the boolean True.
    triggers = doc.get("on", doc.get(True))
    if not isinstance(triggers, dict):
        fail("workflow has no trigger map")
        return False
    push = triggers.get("push")
    if not isinstance(push, dict) or push.get("branches") != ["main"]:
        fail(f"push trigger must target [main], found {push!r}")
        return False
    if "workflow_dispatch" not in triggers:
        fail("workflow_dispatch trigger is missing")
        return False
    ok("push: [main] and workflow_dispatch")
    return True


def test_workflow_wiring(doc: dict, text: str) -> bool:
    print("\nTEST 3: workflow permissions and release steps")
    print("-" * 40)
    valid = True
    permissions = doc.get("permissions") or {}
    if permissions.get("contents") != "write":
        fail(f"permissions.contents must be 'write', found {permissions.get('contents')!r}")
        valid = False
    else:
        ok("permissions.contents: write")

    required = {
        "inline version derivation": "VersionNumber=",
        "release notes": "--notes-file",
        "annotated tag": "git tag -a",
        "gh release create": "gh release create",
    }
    for label, needle in required.items():
        if needle not in text:
            fail(f"workflow does not contain {label}")
            valid = False
    if valid:
        ok("inline version, release notes, tag and release steps present")

    forbidden = {
        "a commit to main": "git push origin HEAD:main",
        "a changelog commit": "git commit",
        "a CHANGELOG.md dependency": "CHANGELOG.md",
        "an external script": "scripts/",
    }
    for label, needle in forbidden.items():
        if needle in text:
            fail(f"workflow must not contain {label}")
            valid = False
    if valid:
        ok("main is not modified and no external scripts are used")

    if not re.search(r"steps\.build\.outputs\.BuildNumber", text):
        fail("workflow does not pass the resolved BuildNumber through")
        valid = False
    return valid


def test_tag_format(text: str) -> bool:
    print("\nTEST 4: tag is the plain build number")
    print("-" * 40)
    if re.search(r'git tag -a\s+"v\$BUILD_NUMBER"', text):
        fail('the tag step still prefixes the tag with "v"')
        return False
    if not re.search(r'git tag -a\s+"\$BUILD_NUMBER"', text):
        fail('the tag step must run: git tag -a "$BUILD_NUMBER"')
        return False
    ok('git tag -a "$BUILD_NUMBER"')
    return True


def find_powershell() -> tuple[str, bool] | None:
    """Locate a PowerShell host and say whether it is a Windows binary.

    The suite is often run with WSL's python3, whose PATH holds no Windows binaries.
    WSL still exposes the Windows filesystem under /mnt/c, so the hosts are found
    there when `which` cannot see them. A Windows host cannot read WSL paths such as
    /tmp/..., so every path handed to it has to be translated first.
    """
    for name in ("pwsh", "powershell"):
        found = shutil.which(name)
        if found:
            return found, sys.platform == "win32"

    candidates = [
        # PowerShell 7+ on Windows (WSL interop path).
        "/mnt/c/Program Files/PowerShell/7/pwsh.exe",
        "/mnt/c/Program Files/PowerShell/7-preview/pwsh.exe",
        # Windows PowerShell 5.1, present on every supported Windows install.
        "/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return candidate, True
    return None


def to_host_path(path: Path, windows_host: bool) -> str:
    """Translate a WSL path into a Windows path when the host binary needs one."""
    if not windows_host:
        return str(path)
    try:
        translated = subprocess.run(
            ["wslpath", "-w", str(path)],
            capture_output=True,
            text=True,
            timeout=30,
            check=True,
        )
        return translated.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return str(path)


# Passing values as arguments is the only transport that survives WSL interop: the
# layer that launches a Windows binary from Linux drops the environment it was given.
# The runner therefore prepends a preamble that restores the variables the step reads.
PREAMBLE = """param(
    [string]$BuildNumber,
    [string]$BuildReason,
    [string]$OutputPath
)
$env:BUILD_NUMBER = $BuildNumber
$env:INPUT_BUILD_NUMBER = $BuildNumber
$env:BUILD_REASON = $BuildReason
$env:GITHUB_OUTPUT = $OutputPath
$env:GITHUB_ACTIONS = 'true'
"""


def run_version_step(script: str, build_reason: str) -> dict:
    host = find_powershell()
    if not host:
        raise RuntimeError(
            "PowerShell (pwsh or powershell) is required to validate the inline "
            "version step; install PowerShell 7 or run the suite from Windows"
        )

    pwsh, windows_host = host
    with tempfile.TemporaryDirectory() as tmp:
        script_path = Path(tmp) / "version-step.ps1"
        output_path = Path(tmp) / "github-output.txt"
        script_path.write_text(PREAMBLE + script, encoding="utf-8")
        output_path.write_text("", encoding="utf-8")

        host_output = to_host_path(output_path, windows_host)
        env = {
            **os.environ,
            "GITHUB_OUTPUT": host_output,
            # The version step reads the build number the resolve step published, so the
            # test supplies it under the name the workflow actually uses. BUILD_NUMBER is
            # kept for the tag/check steps, which read it directly.
            "BUILD_NUMBER": BUILD_NUMBER,
            "INPUT_BUILD_NUMBER": BUILD_NUMBER,
            "BUILD_REASON": build_reason,
        }
        process = subprocess.run(
            [
                pwsh,
                "-NoProfile",
                "-NonInteractive",
                # The script is a throwaway written into a temp directory; the host's
                # execution policy (Restricted by default on Windows PowerShell 5.1)
                # would otherwise refuse to run it.
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                to_host_path(script_path, windows_host),
                "-BuildNumber",
                BUILD_NUMBER,
                "-BuildReason",
                build_reason,
                "-OutputPath",
                host_output,
            ],
            capture_output=True,
            text=True,
            env=env,
            timeout=120,
        )
        if process.returncode != 0:
            raise RuntimeError(
                f"inline version step failed ({build_reason}):\n"
                f"{process.stdout}\n{process.stderr}"
            )

        values = {}
        for line in read(output_path).splitlines():
            if "=" in line:
                name, value = line.split("=", 1)
                values[name.strip()] = value.strip()
        return values


def test_version_outputs(doc: dict) -> bool:
    print("\nTEST 5: inline version derivation")
    print("-" * 40)
    script = version_step(doc).get("run")
    if not script:
        fail("ci.yml has no step with id 'version' and a run block")
        return False

    try:
        merge = run_version_step(script, "Merge")
        pull_request = run_version_step(script, "PullRequest")
    except (RuntimeError, OSError, subprocess.SubprocessError) as exc:
        fail(str(exc))
        return False

    valid = True
    for name, expected in MERGE_VERSION.items():
        if merge.get(name) != expected:
            fail(f"merge build {name}: expected {expected!r}, found {merge.get(name)!r}")
            valid = False
    if valid:
        ok(f"merge build → {MERGE_VERSION['VersionInformational']}")

    if not re.fullmatch(r"\d{4}\.1\d{4}\.1\d{4}\.\d{2}", pull_request.get("VersionNumber", "")):
        fail(f"PR VersionNumber malformed: {pull_request.get('VersionNumber')!r}")
        valid = False
    if not pull_request.get("VersionPackage", "").endswith("-preview"):
        fail(f"PR VersionPackage must end with -preview: {pull_request.get('VersionPackage')!r}")
        valid = False
    if valid:
        ok("PR build → four-part version and -preview package")
    return valid


WORKFLOWS = TEMPLATE_ROOT / ".github" / "workflows"
SCRIPT_REF = re.compile(
    r"(?:\./)?scripts/[A-Za-z0-9._/-]+\.(?:ps1|sh|py|js|mjs|ts)")
RELEASE_MARKERS = ("gh release create", "action-gh-release", "git tag ")
VERSION_MARKERS = (
    "VersionNumber",
    "BuildNumber",
    "Set-VersionVariables",
    "steps.version.outputs",
    "require('./package.json').version",
    'require("./package.json").version',
    "git describe",
    "run_number",
    "GITHUB_RUN_NUMBER",
)


def workflow_texts() -> dict:
    """Every GitHub workflow body in this repository, by filename."""
    if not WORKFLOWS.is_dir():
        return {}
    files = sorted([*WORKFLOWS.glob("*.yml"), *WORKFLOWS.glob("*.yaml")])
    return {path.name: read(path) for path in files}


def validate_project_release() -> bool:
    """Check a derived project's own release contract.

    The template's release policy (inline version step, no root `scripts/`)
    does not apply here. What does apply is that a project which tags or
    publishes a release has a version source and that every script its
    workflows invoke exists.
    """
    print("TEST 1: project release assets")
    print("-" * 40)

    texts = workflow_texts()
    if not texts:
        print("  SKIP: no GitHub workflows in this repository")
        return True

    releasing = {name: text for name, text in texts.items()
                 if any(marker in text for marker in RELEASE_MARKERS)}
    if not releasing:
        print("  SKIP: no workflow tags or publishes a release")
        return True

    valid = True
    references = set()
    for text in texts.values():
        references.update(SCRIPT_REF.findall(text))
    missing = sorted(rel for rel in references
                     if not (TEMPLATE_ROOT / rel).is_file())
    if missing:
        fail("workflow references missing script(s): " + ", ".join(missing))
        valid = False
    else:
        ok(f"{len(references)} referenced script(s) present")

    for name, text in sorted(releasing.items()):
        if not any(marker in text for marker in VERSION_MARKERS):
            fail(f"{name} tags or publishes without a visible version/build source")
            valid = False
        else:
            ok(f"{name} derives or reads a version before releasing")

    # An unrelated `scripts/` directory is not an error: only referenced files
    # matter, so a project is free to organise its own tooling.
    return valid


def uses_template_release() -> bool:
    """Whether this repository uses the template's inline release workflow.

    Implementing repositories copy `.ai/tests` but keep their own CI. A project
    may legitimately version releases in `scripts/` or a separate workflow, so
    this template-only check must not fail there.
    """
    if not WORKFLOW.exists():
        return False
    text = read(WORKFLOW)
    return "VersionNumber=" in text and "gh release create" in text


def main() -> int:
    print("=" * 45)
    print("Release Versioning Validation")
    print("=" * 45)
    print()

    if not uses_template_release():
        print("This repository does not use the template's inline release workflow;")
        print("validating its own release contract instead.")
        print()
        valid = validate_project_release()
        print()
        if valid:
            print("✅ PROJECT RELEASE TESTS PASSED")
        else:
            print("\n❌ PROJECT RELEASE VALIDATION FAILED")
        return 0 if valid else 1

    if not test_files_exist():
        print("\n❌ RELEASE VALIDATION FAILED")
        return 1

    try:
        doc = load_workflow()
        text = read(WORKFLOW)
    except Exception as exc:
        fail(f"ci.yml is not valid YAML: {exc}")
        print("\n❌ RELEASE VALIDATION FAILED")
        return 1

    results = [
        test_workflow_trigger(doc),
        test_workflow_wiring(doc, text),
        test_tag_format(text),
        test_version_outputs(doc),
    ]

    print()
    print("=" * 45)
    if all(results):
        print("✅ ALL RELEASE TESTS PASSED")
        return 0
    print("❌ SOME RELEASE TESTS FAILED")
    return 1


if __name__ == "__main__":
    sys.exit(main())
