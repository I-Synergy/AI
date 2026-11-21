#!/usr/bin/env python3
"""
scaffold-solution.py - Render a .NET solution from the template set.

The templates live in .ai/reference/templates/solution/: files/ holds one
template per output file (the output path plus ".txt"), manifest.json says which
output each template produces and under which flags, and package-versions.json
holds the central package versions with their groups.

The script asks for the application name, company, first sample entity, database
provider and optional projects, then writes the rendered files to an output
directory. It never overwrites an existing file.

Rendering order for every file the manifest selects:
  1. Conditional blocks. Marker lines {{#if flag}}, {{#if !flag}} and {{/if}} are
     removed; the lines between a false marker pair are removed too. A marker may
     sit inside a comment (// {{#if flag}}, <!-- {{#if flag}} -->). Blocks nest.
  2. Package versions. A line that holds only {PackageVersions} expands to one
     PackageVersion item per package of the selected groups (Directory.Packages.props).
  3. Tokens. The documented token names are replaced. Any other {Name} text is C#
     or JSON syntax (log placeholders, interpolation, generic arguments) and is left
     alone.
  4. Residual check. A documented token that is still present fails the run before
     anything is written.

Usage:
    python scaffold-solution.py                       # prompts for everything
    python scaffold-solution.py --name Acme --company "Acme Corp" --entity Item \\
        --entities Items --database sqlserver --with apphost --output ./Acme --yes
    python scaffold-solution.py --name Acme --company "Acme Corp" --yes --dry-run
    python scaffold-solution.py --check-templates

Exit codes: 0 success, 1 template check failed, 2 invalid input or render error.
"""

from __future__ import annotations

import argparse
import codecs
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Callable, Iterable, Optional

DEFAULT_TEMPLATE_ROOT = Path(__file__).resolve().parents[1] / "reference" / "templates" / "solution"

DATABASES = ("sqlserver", "postgres")
DATABASE_PROVIDER = {"sqlserver": "SqlServer", "postgres": "Postgres"}

# Optional flags, offered in the prompts. Each flag is a manifest "when" entry and a package group.
FLAG_HELP = {
    "apphost": "Aspire AppHost that runs the API and the database locally",
    "maui": "MAUI app head",
    "web": "Blazor web head",
    "sqlite-device": "SQLite store for the device app",
    "worker": "background worker host",
    "tests-acceptance": "Reqnroll acceptance tests",
    "tests-ui": "Playwright UI tests",
}

# Packages in the "core" and "tests" groups are always emitted. Every other group follows its flag.
ALWAYS_GROUPS = ("core", "tests")

# The only tokens the renderer replaces. The names are the contract in the templates README.
DOCUMENTED_TOKENS = (
    "ApplicationName",
    "applicationname",
    "ApplicationId",
    "Company",
    "Entity",
    "Entities",
    "entity",
    "entities",
    "Provider",
    "Year",
    "Version",
    "AppHostHttpsPort",
    "ApiHttpsPort",
    "WebHttpsPort",
    "PackageVersions",
)

# Overridable with --force-token (reproducible renders). Names are never overridable.
OVERRIDABLE_TOKENS = ("Version", "Year", "AppHostHttpsPort", "ApiHttpsPort", "WebHttpsPort")
DEFAULT_PORTS = {"AppHostHttpsPort": "44400", "ApiHttpsPort": "44401", "WebHttpsPort": "44402"}
PORT_TOKENS = ("AppHostHttpsPort", "ApiHttpsPort", "WebHttpsPort")

# Brace names that appear in templates as C# or JSON syntax, not as tokens. The template check
# reports any other {Name} so that a misspelt token is caught. Add a name here only after
# confirming that it is C# or JSON syntax.
CSHARP_BRACE_NAMES = frozenset({
    "Count",         # structured log placeholder
    "EntityId",      # structured log placeholder
    "T",             # generic type parameter in XML doc cref
    "SkipVariable",  # interpolated string in test infrastructure
    "apiServiceName",  # interpolated host name in Program.cs
    "createBody",    # interpolated assertion message
    "getBody",       # interpolated assertion message
    "listBody",      # interpolated assertion message
    "id",            # route parameter in endpoint tests
    "name",          # interpolated identifier in test infrastructure
    "skipRequested", # interpolated string in test infrastructure
})

CSHARP_KEYWORDS = frozenset({
    "abstract", "as", "base", "bool", "break", "byte", "case", "catch", "char", "checked", "class",
    "const", "continue", "decimal", "default", "delegate", "do", "double", "else", "enum", "event",
    "explicit", "extern", "false", "finally", "fixed", "float", "for", "foreach", "goto", "if",
    "implicit", "in", "int", "interface", "internal", "is", "lock", "long", "namespace", "new", "null",
    "object", "operator", "out", "override", "params", "private", "protected", "public", "readonly",
    "ref", "return", "sbyte", "sealed", "short", "sizeof", "stackalloc", "static", "string", "struct",
    "switch", "this", "throw", "true", "try", "typeof", "uint", "ulong", "unchecked", "unsafe",
    "ushort", "using", "virtual", "void", "volatile", "while",
})

# Namespace roots a generated solution must not take.
RESERVED_APPLICATION_NAMES = frozenset({
    "System", "Microsoft", "ISynergy", "Aspire", "Windows", "Azure", "Npgsql", "Asp",
})

NAME_PATTERN = re.compile(r"^[A-Z][A-Za-z0-9]{1,59}$")
COMPANY_FORBIDDEN = re.compile(r"[<>&\"{}\x00-\x1f]")
MARKER_OPEN = re.compile(r"^\s*(?://|#|<!--|/\*)?\s*\{\{#if\s+(!?)([a-z][a-z0-9-]*(?:\|[a-z][a-z0-9-]*)*)\s*\}\}\s*(?:-->|\*/)?\s*$")
MARKER_CLOSE = re.compile(r"^\s*(?://|#|<!--|/\*)?\s*\{\{/if\}\}\s*(?:-->|\*/)?\s*$")
PACKAGE_LINE = re.compile(r"^(\s*)\{PackageVersions\}\s*$")
RESIDUAL_TOKEN = re.compile(r"\{(" + "|".join(DOCUMENTED_TOKENS) + r")\}")
BRACE_NAME = re.compile(r"\{([A-Za-z][A-Za-z0-9]*)\}")
README_TOKEN_ROW = re.compile(r"^\|\s*`\{([A-Za-z]+)\}`\s*\|")


class ScaffoldError(Exception):
    """A user-facing error. The message is printed without a traceback."""


@dataclass(frozen=True)
class ManifestEntry:
    """One template file and the output it produces. `when` needs every flag; `when_any` needs one of them."""

    template: str
    output: str
    when: tuple[str, ...]
    when_any: tuple[str, ...] = ()


@dataclass(frozen=True)
class Package:
    """One central package version and the groups that emit it."""

    id: str
    version: str
    groups: tuple[str, ...]


@dataclass
class Options:
    """Resolved answers, from flags or prompts."""

    name: str
    company: str
    entity: str
    entities: str
    database: str
    application_id: str
    flags: set[str] = field(default_factory=set)
    output: Optional[Path] = None
    dry_run: bool = False
    overrides: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class PlannedFile:
    """A rendered file, ready to write."""

    rel: str
    data: bytes
    template: str


# ─── Loading ─────────────────────────────────────────────────────────────────


def load_manifest(root: Path) -> list[ManifestEntry]:
    """Read manifest.json. Every entry needs template, output and when."""
    path = root / "manifest.json"
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ScaffoldError(f"cannot read {path}: {exc}") from exc
    if not isinstance(raw, list):
        raise ScaffoldError(f"{path} must be a JSON array")
    entries = []
    for index, item in enumerate(raw):
        if not isinstance(item, dict) or not {"template", "output", "when"} <= item.keys():
            raise ScaffoldError(f"{path} entry {index} needs template, output and when")
        when = item["when"]
        if not isinstance(when, list) or not all(isinstance(flag, str) for flag in when):
            raise ScaffoldError(f"{path} entry {index}: when must be a list of flag names")
        when_any = item.get("whenAny", [])
        if not isinstance(when_any, list) or not all(isinstance(flag, str) for flag in when_any):
            raise ScaffoldError(f"{path} entry {index}: whenAny must be a list of flag names")
        entries.append(ManifestEntry(item["template"], item["output"], tuple(when), tuple(when_any)))
    return entries


def load_packages(root: Path) -> list[Package]:
    """Read package-versions.json. Every entry needs id, version and groups."""
    path = root / "package-versions.json"
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ScaffoldError(f"cannot read {path}: {exc}") from exc
    packages = []
    for index, item in enumerate(raw):
        if not isinstance(item, dict) or not {"id", "version", "groups"} <= item.keys():
            raise ScaffoldError(f"{path} entry {index} needs id, version and groups")
        packages.append(Package(item["id"], item["version"], tuple(item["groups"])))
    return packages


def available_flags(entries: Iterable[ManifestEntry]) -> set[str]:
    """Flags that have at least one template in the manifest."""
    return {flag for entry in entries for flag in entry.when}


def selected_groups(flags: Iterable[str]) -> set[str]:
    """Package groups that are emitted for the given flags."""
    return set(ALWAYS_GROUPS) | set(flags)


# ─── Validation and derived values ───────────────────────────────────────────


def validate_name(value: str, label: str) -> str:
    """Require a PascalCase identifier that is safe as a C# namespace segment."""
    if not NAME_PATTERN.match(value):
        raise ScaffoldError(
            f"{label} '{value}' must be PascalCase letters and digits, start with an upper-case letter, "
            "and be 2 to 60 characters long (for example Acme or Item)")
    return value


def validate_entity_name(value: str, label: str) -> str:
    """Require a PascalCase identifier that is not a C# keyword once lower-cased."""
    validate_name(value, label)
    if camel(value) in CSHARP_KEYWORDS:
        raise ScaffoldError(f"{label} '{value}' becomes the C# keyword '{camel(value)}' in identifiers; choose another name")
    return value


APPLICATION_ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)+$")


def validate_application_id(value: str) -> str:
    """Require a lower-case reverse-DNS identifier: at least two dot-separated segments, each starting with a letter."""
    if not APPLICATION_ID_PATTERN.fullmatch(value):
        raise ScaffoldError(f"application identifier '{value}' must be lower-case reverse DNS, for example com.example.acme")
    return value


def validate_company(value: str) -> str:
    """Require a company string that is safe in XML element text and in the template text."""
    if not value.strip():
        raise ScaffoldError("company must not be empty")
    if COMPANY_FORBIDDEN.search(value):
        raise ScaffoldError("company must not contain < > & \" { } or control characters")
    return value.strip()


def camel(value: str) -> str:
    """Lower-case the first letter: Item -> item, ProductCategory -> productCategory."""
    return value[:1].lower() + value[1:]


def pluralize(word: str) -> str:
    """Suggest a plural for an entity name: Item -> Items, Category -> Categories, Box -> Boxes."""
    lower = word.lower()
    if re.search(r"[^aeiou]y$", lower):
        return word[:-1] + "ies"
    if re.search(r"(s|x|z|ch|sh)$", lower):
        return word + "es"
    return word + "s"


def version_stamp(now: datetime) -> str:
    """Version stamp yyyy.1MMdd.1HHmm, for example 2026.11121.11153."""
    return f"{now:%Y}.1{now:%m%d}.1{now:%H%M}"


def build_tokens(options: Options, now: datetime) -> dict[str, str]:
    """Token values for one render. The names are the documented token names."""
    values = {
        "ApplicationName": options.name,
        "applicationname": options.name.lower(),
        "ApplicationId": options.application_id,
        "Company": options.company,
        "Entity": options.entity,
        "Entities": options.entities,
        "entity": camel(options.entity),
        "entities": camel(options.entities),
        "Provider": DATABASE_PROVIDER[options.database],
        "Year": f"{now:%Y}",
        "Version": version_stamp(now),
        **DEFAULT_PORTS,
    }
    values.update(options.overrides)
    return values


def parse_overrides(pairs: Iterable[str]) -> dict[str, str]:
    """Parse --force-token KEY=VALUE pairs for the overridable tokens only.

    Each value is validated as the token it replaces: Version becomes the assembly version, Year is
    written into the copyright line, and a port is bound by a launch profile.
    """
    overrides: dict[str, str] = {}
    for pair in pairs:
        key, sep, value = pair.partition("=")
        if not sep or not key:
            raise ScaffoldError(f"--force-token expects KEY=VALUE, got '{pair}'")
        if key not in OVERRIDABLE_TOKENS:
            raise ScaffoldError(f"--force-token key '{key}' is not overridable; use one of: {', '.join(OVERRIDABLE_TOKENS)}")
        if key in PORT_TOKENS:
            if not value.isdigit() or not 1024 <= int(value) <= 65535:
                raise ScaffoldError(f"--force-token {key} must be a port number between 1024 and 65535")
        elif key == "Version":
            # The templates append a fourth part for AssemblyVersion, and .NET accepts at most four.
            if not re.fullmatch(r"\d+(\.\d+){0,2}", value):
                raise ScaffoldError(f"--force-token Version must be one to three dot-separated numbers "
                                    f"(for example 2026.11121.11153), got '{value}'")
        elif key == "Year":
            if not re.fullmatch(r"\d{4}", value):
                raise ScaffoldError(f"--force-token Year must be a four-digit year, got '{value}'")
        elif not re.fullmatch(r"[A-Za-z0-9.]+", value):
            raise ScaffoldError(f"--force-token {key} must contain only letters, digits and dots")
        overrides[key] = value

    ports = {key: overrides[key] for key in PORT_TOKENS if key in overrides}
    if len(set(ports.values())) != len(ports):
        raise ScaffoldError(f"--force-token ports must differ: {', '.join(f'{k}={v}' for k, v in ports.items())}")
    return overrides


def parse_flags(text: Optional[str], known: Iterable[str]) -> list[str]:
    """Split a comma-separated flag list and reject unknown names."""
    if text is None:
        return []
    items = [item.strip() for item in text.split(",") if item.strip()]
    for item in items:
        if item not in known:
            raise ScaffoldError(f"unknown flag '{item}'; known flags: {', '.join(known)}")
    return items


# ─── Rendering ───────────────────────────────────────────────────────────────


def split_lines(text: str) -> list[str]:
    """Split keeping each line ending, so CRLF and LF files keep their own endings."""
    return re.findall(r"[^\n]*\n|[^\n]+", text)


def apply_conditionals(text: str, active: set[str], label: str) -> str:
    """Keep or drop the lines between {{#if}} and {{/if}} markers, nesting allowed."""
    out: list[str] = []
    stack: list[bool] = []
    for number, line in enumerate(split_lines(text), 1):
        bare = line.rstrip("\r\n")
        opened = MARKER_OPEN.match(bare)
        if opened:
            negate, names = bool(opened.group(1)), opened.group(2).split("|")
            for flag in names:
                if flag not in FLAG_HELP and flag not in DATABASES:
                    raise ScaffoldError(f"{label} line {number}: unknown flag '{flag}' in {{{{#if}}}}")
            if negate and len(names) > 1:
                raise ScaffoldError(f"{label} line {number}: '!' negates one flag, not a list")
            # a list is true when any listed flag is set
            stack.append((any(flag in active for flag in names)) != negate)
            continue
        if MARKER_CLOSE.match(bare):
            if not stack:
                raise ScaffoldError(f"{label} line {number}: {{{{/if}}}} without a matching {{{{#if}}}}")
            stack.pop()
            continue
        if "{{#if" in bare or "{{/if" in bare:
            raise ScaffoldError(f"{label} line {number}: malformed conditional marker")
        if all(stack):
            out.append(line)
    if stack:
        raise ScaffoldError(f"{label}: {len(stack)} {{{{#if}}}} block(s) not closed")
    return "".join(out)


def expand_package_versions(text: str, packages: list[Package], label: str) -> str:
    """Replace a line that holds only {PackageVersions} with one PackageVersion line per package."""
    out: list[str] = []
    for line in split_lines(text):
        bare = line.rstrip("\r\n")
        ending = line[len(bare):]
        match = PACKAGE_LINE.match(bare)
        if match:
            indent = match.group(1)
            for package in packages:
                out.append(f'{indent}<PackageVersion Include="{package.id}" Version="{package.version}" />{ending}')
        else:
            out.append(line)
    return "".join(out)


def replace_tokens(text: str, values: dict[str, str]) -> str:
    """Replace documented token names. Other brace text is left unchanged."""
    pattern = re.compile(r"\{(" + "|".join(sorted(values, key=len, reverse=True)) + r")\}")
    return pattern.sub(lambda match: values[match.group(1)], text)


def check_residual(text: str, label: str) -> None:
    """Fail when a documented token survived rendering."""
    for number, line in enumerate(split_lines(text), 1):
        match = RESIDUAL_TOKEN.search(line)
        if match:
            raise ScaffoldError(f"{label} line {number}: unreplaced token {{{match.group(1)}}}")


def render_path(output: str, values: dict[str, str], label: str) -> str:
    """Render the output path of a manifest entry and check it stays inside the output directory."""
    rendered = replace_tokens(output, values)
    check_residual(rendered, label)
    parts = PurePosixPath(rendered).parts
    if not parts or rendered.startswith("/") or any(part in ("", "..", ".") for part in parts) or "\\" in rendered:
        raise ScaffoldError(f"{label}: rendered path '{rendered}' is not a safe relative path")
    return rendered


def render_file(
    root: Path,
    entry: ManifestEntry,
    values: dict[str, str],
    active: set[str],
    packages: list[Package],
    groups: set[str],
) -> PlannedFile:
    """Render one template into bytes, keeping its BOM and line endings."""
    label = entry.template
    source = root / entry.template
    try:
        raw = source.read_bytes()
    except OSError as exc:
        raise ScaffoldError(f"cannot read template {source}: {exc}") from exc
    has_bom = raw.startswith(codecs.BOM_UTF8)
    try:
        text = (raw[len(codecs.BOM_UTF8):] if has_bom else raw).decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ScaffoldError(f"{label} is not valid UTF-8: {exc}") from exc

    text = apply_conditionals(text, active, label)
    rel = render_path(entry.output, values, label)
    if rel.endswith("Directory.Packages.props"):
        selected = [p for p in packages if groups & set(p.groups)]
        selected.sort(key=lambda p: p.id.lower())
        text = expand_package_versions(text, selected, label)
    text = replace_tokens(text, values)
    check_residual(text, label)

    data = (codecs.BOM_UTF8 if has_bom else b"") + text.encode("utf-8")
    return PlannedFile(rel, data, label)


def plan_files(
    root: Path,
    entries: list[ManifestEntry],
    values: dict[str, str],
    active: set[str],
    packages: list[Package],
) -> list[PlannedFile]:
    """Render every manifest entry whose flags are all active. Nothing is written here."""
    groups = selected_groups(active)
    planned: list[PlannedFile] = []
    seen: dict[str, str] = {}
    for entry in entries:
        if not set(entry.when) <= active:
            continue
        if entry.when_any and not set(entry.when_any) & active:
            continue
        file = render_file(root, entry, values, active, packages, groups)
        key = file.rel.lower()
        if key in seen:
            raise ScaffoldError(f"two templates render to {file.rel}: {seen[key]} and {entry.template}")
        seen[key] = entry.template
        planned.append(file)
    return planned


def write_files(out_dir: Path, planned: list[PlannedFile], dry_run: bool) -> list[tuple[str, str]]:
    """Write files that do not exist yet. Returns (status, relative path) pairs."""
    results: list[tuple[str, str]] = []
    for file in planned:
        target = out_dir.joinpath(*PurePosixPath(file.rel).parts)
        if target.exists() or target.is_symlink():
            results.append(("SKIPPED", file.rel))
            continue
        if dry_run:
            results.append(("WOULD-CREATE", file.rel))
            continue
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(file.data)
        except OSError as exc:
            raise ScaffoldError(f"cannot write {target}: {exc}") from exc
        results.append(("CREATED", file.rel))
    return results


# ─── Template check ──────────────────────────────────────────────────────────


def check_templates(root: Path) -> int:
    """Verify the manifest, package list, README token table and token usage. Returns an exit code."""
    problems: list[str] = []
    try:
        entries = load_manifest(root)
        packages = load_packages(root)
    except ScaffoldError as exc:
        print(f"error: {exc}")
        return 1

    files_dir = root / "files"
    on_disk = {p.relative_to(root).as_posix() for p in files_dir.rglob("*") if p.is_file()}
    in_manifest = [entry.template for entry in entries]
    if len(in_manifest) != len(set(in_manifest)):
        problems.append("manifest lists a template more than once")
    if len(set(entry.output for entry in entries)) != len(entries):
        problems.append("manifest lists an output path more than once")
    for template in sorted(on_disk - set(in_manifest)):
        problems.append(f"no manifest entry for {template}")
    for template in sorted(set(in_manifest) - on_disk):
        problems.append(f"manifest entry without a file: {template}")

    known_flags = set(FLAG_HELP) | set(DATABASES)
    for entry in entries:
        for flag in entry.when + entry.when_any:
            if flag not in known_flags:
                problems.append(f"{entry.template}: unknown flag '{flag}' in when")

    seen_ids: set[str] = set()
    for package in packages:
        if package.id.lower() in seen_ids:
            problems.append(f"package-versions.json lists {package.id} more than once")
        seen_ids.add(package.id.lower())
        for group in package.groups:
            if group not in known_flags and group not in ALWAYS_GROUPS:
                problems.append(f"package {package.id}: unknown group '{group}'")

    undocumented: list[str] = []
    for template in sorted(on_disk):
        path = root / template
        text = path.read_text(encoding="utf-8-sig")
        try:
            apply_conditionals(text, set(), template)
        except ScaffoldError as exc:
            problems.append(str(exc))
        for number, line in enumerate(split_lines(text), 1):
            for match in BRACE_NAME.finditer(line):
                name = match.group(1)
                if name not in DOCUMENTED_TOKENS and name not in CSHARP_BRACE_NAMES:
                    undocumented.append(f"{template} line {number}: {{{name}}}")
    for segment_text in on_disk:
        for match in BRACE_NAME.finditer(segment_text):
            name = match.group(1)
            if name not in DOCUMENTED_TOKENS and name not in CSHARP_BRACE_NAMES:
                undocumented.append(f"path {segment_text}: {{{name}}}")

    readme = (root / "README.md").read_text(encoding="utf-8")
    table_tokens = set()
    for line in readme.splitlines():
        match = README_TOKEN_ROW.match(line)
        if match:
            table_tokens.add(match.group(1))
    for token in sorted(set(DOCUMENTED_TOKENS) - table_tokens):
        problems.append(f"README token table is missing {{{token}}}")
    for token in sorted(table_tokens - set(DOCUMENTED_TOKENS)):
        problems.append(f"README token table lists {{{token}}}, which the script does not replace")

    for item in undocumented:
        problems.append(f"undocumented brace text (token typo or new C# brace?): {item}")

    if problems:
        print(f"template check FAILED with {len(problems)} problem(s):")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    print(f"template check OK: {len(entries)} manifest entries, {len(on_disk)} template files, "
          f"{len(packages)} packages, {len(DOCUMENTED_TOKENS)} documented tokens")
    return 0


# ─── Interaction ─────────────────────────────────────────────────────────────


class Prompter:
    """Asks questions on the terminal. Injectable for tests."""

    def __init__(self, input_func: Callable[[str], str] = input) -> None:
        self._input = input_func

    def ask(self, question: str, default: Optional[str], validate: Callable[[str], str]) -> str:
        """Ask until the answer validates. An empty answer takes the default when there is one."""
        suffix = f" [{default}]" if default is not None else ""
        while True:
            try:
                answer = self._input(f"{question}{suffix}: ").strip()
            except EOFError as exc:
                raise ScaffoldError("no answer available (no terminal); pass the value as a flag or use --yes") from exc
            if not answer and default is not None:
                answer = default
            if not answer:
                print("  a value is required")
                continue
            try:
                return validate(answer)
            except ScaffoldError as exc:
                print(f"  {exc}")

    def yes_no(self, question: str, default: bool) -> bool:
        """Ask a yes/no question."""
        hint = "Y/n" if default else "y/N"
        while True:
            try:
                answer = self._input(f"{question} [{hint}]: ").strip().lower()
            except EOFError as exc:
                raise ScaffoldError("no answer available (no terminal); pass --with or --yes") from exc
            if not answer:
                return default
            if answer in ("y", "yes"):
                return True
            if answer in ("n", "no"):
                return False
            print("  answer y or n")


def resolve_options(args: argparse.Namespace, available: set[str], prompter: Optional[Prompter]) -> Options:
    """Combine flags and prompts into Options. Prompts are skipped for every value given as a flag."""
    interactive = prompter is not None and not args.yes
    known_flags = list(FLAG_HELP)

    name = args.name
    if name is None:
        if not interactive:
            raise ScaffoldError("--name is required (or run without --yes to be prompted)")
        name = prompter.ask("Application name (PascalCase, for example Acme)", None,
                            lambda v: validate_name(v, "application name"))
    validate_name(name, "application name")
    if name in RESERVED_APPLICATION_NAMES:
        raise ScaffoldError(f"application name '{name}' is reserved; choose another")

    company = args.company
    if company is None:
        if not interactive:
            raise ScaffoldError("--company is required (or run without --yes to be prompted)")
        company = prompter.ask("Company (for Directory.Build.props, for example Acme Corp)", None, validate_company)
    company = validate_company(company)

    application_id = args.application_id
    default_application_id = f"com.example.{name.lower()}"
    if application_id is None:
        application_id = prompter.ask("Application identifier (lower-case reverse DNS, for the MAUI head)", default_application_id,
                                      validate_application_id) if interactive else default_application_id
    application_id = validate_application_id(application_id)

    entity = args.entity
    if entity is None:
        entity = prompter.ask("First sample entity, singular (PascalCase)", "Item",
                              lambda v: validate_entity_name(v, "entity")) if interactive else "Item"
    validate_entity_name(entity, "entity")

    entities = args.entities
    if entities is None:
        default_plural = pluralize(entity)
        entities = prompter.ask("First sample entity, plural (PascalCase)", default_plural,
                                lambda v: validate_entity_name(v, "entities")) if interactive else default_plural
    validate_entity_name(entities, "entities")
    if entities == entity:
        raise ScaffoldError("the singular and plural entity names must differ")

    database = args.database
    if database is None:
        database = prompter.ask("Database (sqlserver or postgres)", "sqlserver",
                                lambda v: v if v in DATABASES else _bad_choice(v, DATABASES)) if interactive else "sqlserver"

    if args.with_flags is not None:
        flags = parse_flags(args.with_flags, known_flags)
    elif interactive:
        flags = []
        for flag in known_flags:
            question = f"Include {flag} ({FLAG_HELP[flag]})"
            if flag not in available:
                question += " - templates not available yet"
            if prompter.yes_no(question, default=False):
                flags.append(flag)
    else:
        flags = []

    output = args.output
    if output is None:
        default_output = f"./{name}"
        if interactive:
            output = prompter.ask("Output directory", default_output, lambda v: v)
        else:
            output = default_output
    output_path = Path(output).expanduser()
    if output_path.exists() and not output_path.is_dir():
        raise ScaffoldError(f"output path {output_path} exists and is not a directory")

    return Options(
        name=name,
        company=company,
        entity=entity,
        entities=entities,
        database=database,
        application_id=application_id,
        flags=set(flags),
        output=output_path,
        dry_run=args.dry_run,
        overrides=parse_overrides(args.force_token),
    )


def _bad_choice(value: str, choices: tuple[str, ...]) -> str:
    """Raise the choice error used by the database prompt."""
    raise ScaffoldError(f"'{value}' is not one of: {', '.join(choices)}")


def summarize_flags(options: Options, available: set[str]) -> tuple[set[str], list[str]]:
    """Split the chosen flags into active and ignored. The database provider is always active.

    Active flags are the database provider plus each chosen flag that has templates. Ignored flags are
    chosen flags whose templates do not exist yet.
    """
    active = {options.database} | {flag for flag in options.flags if flag in available}
    ignored = sorted(options.flags - available)
    return active, ignored


# ─── Entry point ─────────────────────────────────────────────────────────────


def build_parser() -> argparse.ArgumentParser:
    """Define the command-line interface."""
    parser = argparse.ArgumentParser(
        description="Render a .NET solution from the template set. Prompts for any value not given as a flag.")
    parser.add_argument("--name", help="application name, PascalCase (for example Acme)")
    parser.add_argument("--company", help="company for Directory.Build.props (for example 'Acme Corp')")
    parser.add_argument("--application-id", metavar="ID",
                        help="application identifier for the MAUI head, lower-case reverse DNS (default com.example.<name>)")
    parser.add_argument("--entity", help="first sample entity, singular, PascalCase (default Item)")
    parser.add_argument("--entities", help="first sample entity, plural, PascalCase (default: plural of --entity)")
    parser.add_argument("--database", choices=DATABASES, help="database provider (default sqlserver)")
    parser.add_argument("--with", dest="with_flags", metavar="a,b,c",
                        help="comma-separated optional flags: " + ", ".join(FLAG_HELP) + " (skips the flag prompts)")
    parser.add_argument("--yes", action="store_true", help="do not prompt; use defaults for values not given")
    parser.add_argument("--output", help="output directory (default ./<name>)")
    parser.add_argument("--dry-run", action="store_true", help="report what would be created; write nothing")
    parser.add_argument("--force-token", action="append", default=[], metavar="KEY=VALUE",
                        help="override a computed token: " + ", ".join(OVERRIDABLE_TOKENS) + " (repeatable)")
    parser.add_argument("--templates", type=Path, default=DEFAULT_TEMPLATE_ROOT,
                        help="template root (default .ai/reference/templates/solution)")
    parser.add_argument("--check-templates", action="store_true",
                        help="verify the manifest, packages, README token table and token usage, then exit")
    return parser


def print_flag_notices(ignored: list[str]) -> None:
    """Explain flags that were chosen but have no templates yet."""
    for flag in ignored:
        print(f"notice: flag '{flag}' - templates not available yet; it is ignored in this render")


def main(argv: Optional[list[str]] = None) -> int:
    """Run the generator. Returns the process exit code."""
    args = build_parser().parse_args(argv)
    root: Path = args.templates
    try:
        if args.check_templates:
            return check_templates(root)

        entries = load_manifest(root)
        packages = load_packages(root)
        available = available_flags(entries)

        prompter = None if args.yes else Prompter()
        options = resolve_options(args, available, prompter)
        now = datetime.now()
        active, ignored = summarize_flags(options, available)
        print_flag_notices(ignored)

        values = build_tokens(options, now)
        planned = plan_files(root, entries, values, active, packages)
        results = write_files(options.output, planned, options.dry_run)
    except ScaffoldError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("cancelled", file=sys.stderr)
        return 130

    print()
    print(f"Solution: {options.name}  Company: {options.company}  Entity: {options.entity}/{options.entities}")
    print(f"Database: {options.database}  Flags: {', '.join(sorted(active)) or 'none'}  Version: {values['Version']}")
    print(f"Output: {options.output.resolve()}")
    print()
    for status, rel in results:
        print(f"  {status:<13} {rel}")
    created = sum(1 for status, _ in results if status == "CREATED")
    would = sum(1 for status, _ in results if status == "WOULD-CREATE")
    skipped = sum(1 for status, _ in results if status == "SKIPPED")
    print()
    print(f"{len(results)} files: {created} created, {would} would be created, {skipped} skipped (already exist).")
    if options.dry_run:
        print("Dry run: nothing was written.")
        return 0
    if skipped:
        print("warning: existing files were not overwritten; check the output directory is empty.")
    print()
    print("Next steps:")
    print(f"  cd \"{options.output.resolve()}\"")
    print("  dotnet tool restore")
    print("  dotnet restore")
    print("  dotnet build -nodeReuse:false")
    print("  dotnet test")
    if options.database:
        provider_project = f"src/{options.name}.Data.{DATABASE_PROVIDER[options.database]}"
        print(f"  dotnet ef migrations add Initial --project {provider_project} "
              f"--startup-project src/{options.name}.Service.Api")
    return 0


if __name__ == "__main__":
    sys.exit(main())
