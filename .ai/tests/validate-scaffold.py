#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validates the solution scaffold (.ai/scripts/scaffold-solution.py and
.ai/reference/templates/solution/):
  1. Template integrity: manifest vs files/, flags, token table, package groups
  2. Render matrix: project set per flag combination, solution file, markers, encoding, idempotency
  3. Template rules on every rendered .cs file (one type per file, naming, CancellationToken, docs ...)
  4. Central package management, audit properties, tool manifest, SDK pin
  5. Forbidden terms over shipped paths and over every rendered file
  6. Command-line negative tests (exit codes, no stack traces)
  7. Provenance: the shipped manifest names no source and no reference project
  8. Build smoke (opt-in: SCAFFOLD_BUILD_SMOKE=1, needs dotnet 11.0.100; never builds the MAUI head)

Renders go to .ai/tmp/validate-scaffold-<pid>/ and are removed afterwards.
"""

import contextlib
import importlib.util
import io
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

SCRIPT_DIR = Path(__file__).parent
ROOT = SCRIPT_DIR.parent.parent
SCAFFOLD_SCRIPT = ROOT / ".ai" / "scripts" / "scaffold-solution.py"
TEMPLATE_ROOT = ROOT / ".ai" / "reference" / "templates" / "solution"
WORK_DIR = ROOT / ".ai" / "tmp" / f"validate-scaffold-{os.getpid()}"

EXPECTED_SDK = "11.0.100"
SMOKE_ENV = "SCAFFOLD_BUILD_SMOKE"
FIXED_TOKENS = ["--force-token", "Version=2026.11121.11153", "--force-token", "Year=2026"]

# ─── Forbidden terms ─────────────────────────────────────────────────────────
# The one place where the names of the private reference projects appear. They are built from
# fragments so that this file does not match its own search.
FORBIDDEN_TERMS = (
    "The" + "Qur" + "an",
    "Qur" + "an",
    "Sur" + "ah",
    "Ay" + "ah",
    "ISynergy" + "." + "Identity",
    "I-Synergy" + "." + "Identity",
    "isynergy" + ".azurecr" + ".io",
)
# A D: drive path is forbidden, except the generic placeholder paths used as examples in shipped docs and fixtures.
FORBIDDEN_DRIVE_PATH = re.compile(r"\bD:(?![\\/]+(?:repo\b|Projects[\\/]+MyProject\b))[\\/]")
# These two count only as whole capitalised words, so minified vendor scripts cannot match.
CASE_SENSITIVE_WORDS = ("Sur" + "ah", "Ay" + "ah")
FORBIDDEN_TERM_PATTERN = re.compile(
    "|".join(re.escape(t) for t in FORBIDDEN_TERMS if t not in CASE_SENSITIVE_WORDS), re.IGNORECASE)
FORBIDDEN_WORD_PATTERN = re.compile(r"\b(?:" + "|".join(CASE_SENSITIVE_WORDS) + r")\w*")

# Shipped paths scanned for forbidden terms (relative to the repository root). The work records
# .ai/tmp, .ai/analysis, .ai/plans, .ai/progress and .ai/completed are deliberately absent.
SHIPPED_PATHS = (
    ".ai/reference",
    ".ai/scripts/scaffold-solution.py",
    ".ai/tests",
    ".ai/skills",
    ".ai/patterns",
    ".ai/project",
    "README.md",
    "AGENTS.md",
    ".claude",
    ".github",
)
SHIPPED_GLOBS = ("TEMPLATE-*.md",)
SKIP_DIR_NAMES = {".git", "__pycache__", "node_modules", "bin", "obj", ".pytest_cache", "worktrees"}
SKIP_FILE_NAMES = {"settings.local.json"}

# ─── Documented exceptions to the template rules ─────────────────────────────
# Async methods that cannot or need not take a CancellationToken.
ASYNC_NAME_EXCEPTIONS = {"DisposeAsync"}          # IAsyncDisposable has no parameters
# The one file that may touch HttpClient directly: the health probe that resolves a client from the factory.
HTTPCLIENT_ALLOWED_FILES = {"HealthChecks/ApiHealthCheck.cs"}

TOKEN_REGEX = None  # filled from the script (documented token names)

# ─── Render matrix ───────────────────────────────────────────────────────────
MATRIX = {
    "sqlserver-apphost": dict(name="Acme", db="sqlserver", flags=["apphost"], entity="Item", entities="Items"),
    "postgres-full": dict(name="Contoso", db="postgres", flags=["apphost", "web", "sqlite-device"],
                          entity="Category", entities="Categories"),
    "sqlserver-maui": dict(name="Acme", db="sqlserver", flags=["web", "maui", "sqlite-device", "apphost"],
                           entity="Item", entities="Items"),
    "sqlserver-plain": dict(name="Acme", db="sqlserver", flags=[], entity="Item", entities="Items"),
    # The device store without a head: it must still build, and the head that would call it is absent.
    "sqlserver-sqlite-only": dict(name="Acme", db="sqlserver", flags=["sqlite-device"], entity="Item", entities="Items"),
}
PROVIDER = {"sqlserver": "SqlServer", "postgres": "Postgres"}


def expected_projects(name, db, flags):
    """Independent statement of the contract: which projects a flag combination generates."""
    provider = PROVIDER[db]
    src = {"Clients", "Common", "Data", f"Data.{provider}", "Domains", "Entities", "Models", "Resources",
           "Service.Api", "Services"}
    if "apphost" in flags:
        src.add("AppHost")
    if "web" in flags:
        src.add("App.Web")
    if "maui" in flags:
        src.add("App")
    if flags and set(flags) & {"maui", "web", "sqlite-device"}:
        src.add("App.Shared")
    if "sqlite-device" in flags:
        src.add("Data.Sqlite")
    tests = {f"Data.{provider}.Tests", "Domains.Tests", "Service.Tests"}
    return ({f"{name}.{p}" for p in src}, {f"{name}.{p}" for p in tests})


# ─── Helpers ─────────────────────────────────────────────────────────────────

_scaffold = None
_renders = {}


def load_scaffold():
    global _scaffold, TOKEN_REGEX
    if _scaffold is None:
        spec = importlib.util.spec_from_file_location("scaffold_solution_under_test", SCAFFOLD_SCRIPT)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        _scaffold = module
        TOKEN_REGEX = re.compile(r"\{(" + "|".join(module.DOCUMENTED_TOKENS) + r")\}")
    return _scaffold


def run_main(argv):
    """Run scaffold main(argv); return (exit code, stdout, stderr). SystemExit from argparse is a code."""
    sc = load_scaffold()
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            code = sc.main(argv)
        except SystemExit as exc:
            code = exc.code if isinstance(exc.code, int) else 1
    return code, out.getvalue(), err.getvalue()


def render_args(spec, output):
    args = ["--name", spec["name"], "--company", "Acme Corp", "--application-id", f"com.example.{spec['name'].lower()}",
            "--entity", spec["entity"], "--entities", spec["entities"], "--database", spec["db"],
            "--output", str(output), "--yes", *FIXED_TOKENS]
    if spec["flags"]:
        args += ["--with", ",".join(spec["flags"])]
    return args


def get_render(key):
    """Render a matrix entry once (cached). Returns (dir, exit code, stdout)."""
    if key not in _renders:
        out_dir = WORK_DIR / key
        code, out, err = run_main(render_args(MATRIX[key], out_dir))
        _renders[key] = (out_dir, code, out + err)
    return _renders[key]


def rendered_files(directory):
    return sorted(p for p in directory.rglob("*") if p.is_file())


def rel(path, base):
    return path.relative_to(base).as_posix()


def read_text(path):
    return path.read_bytes().decode("utf-8-sig")


class Check:
    """Collects PASS/FAIL lines for one test."""

    def __init__(self):
        self.ok = True

    def verify(self, label, problems):
        if problems:
            self.ok = False
            print(f"  FAIL: {label}")
            for problem in problems[:12]:
                print(f"        - {problem}")
            if len(problems) > 12:
                print(f"        ... {len(problems) - 12} more")
        else:
            print(f"  PASS: {label}")


def strip_block_comments(text):
    return re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)


def code_lines(text):
    """Lines of C# without full-line comments (XML docs included)."""
    text = strip_block_comments(text)
    return [("" if line.lstrip().startswith("//") else line) for line in text.split("\n")]


def is_generated(text):
    return "<auto-generated" in "\n".join(text.split("\n")[:6])


TYPE_DECL = re.compile(
    r"^(?:(?:public|internal|file)\s+)?(?:(?:sealed|static|abstract|partial|readonly|unsafe|ref)\s+)*"
    r"(class|struct|interface|enum|record\s+struct|record\s+class|record)\s+(\w+)", re.M)


def top_level_types(text):
    """(kind, name, offset) of declarations that start in column 0 (files use file-scoped namespaces)."""
    cleaned = "\n".join(code_lines(text))
    return [(m.group(1).split()[0], m.group(2), m.start()) for m in TYPE_DECL.finditer(cleaned)]


def csharp_files(directory, subdir=None):
    base = directory / subdir if subdir else directory
    return [p for p in rendered_files(base) if p.suffix == ".cs"] if base.exists() else []


# ─── Tests ───────────────────────────────────────────────────────────────────


def test_template_integrity():
    print("TEST 1: Template integrity")
    print("-" * 40)
    sc = load_scaffold()
    c = Check()
    entries = sc.load_manifest(TEMPLATE_ROOT)
    packages = sc.load_packages(TEMPLATE_ROOT)

    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = sc.check_templates(TEMPLATE_ROOT)
    c.verify("script --check-templates passes", [] if code == 0 else out.getvalue().strip().splitlines())

    on_disk = {rel(p, TEMPLATE_ROOT) for p in (TEMPLATE_ROOT / "files").rglob("*") if p.is_file()}
    templates = [e.template for e in entries]
    problems = [f"duplicate template {t}" for t in set(templates) if templates.count(t) > 1]
    problems += [f"no manifest entry: {t}" for t in sorted(on_disk - set(templates))]
    problems += [f"manifest entry without file: {t}" for t in sorted(set(templates) - on_disk)]
    c.verify("manifest and files/ match 1:1", problems)

    problems = [f"{e.template}: stored without .txt suffix" for e in entries if not e.template.endswith(".txt")]
    problems += [f"{e.template}: template path is not 'files/' + output + '.txt'" for e in entries
                 if e.template != f"files/{e.output}.txt"]
    c.verify("every template path is files/<output>.txt and exists", problems)

    outputs = [e.output for e in entries]
    c.verify("entries are sorted by output (ordinal) with unique outputs",
             ([] if outputs == sorted(outputs) else ["manifest is not sorted by output"])
             + [f"duplicate output {o}" for o in set(outputs) if outputs.count(o) > 1])

    known = set(sc.FLAG_HELP) | set(sc.DATABASES)
    problems = [f"{e.template}: unknown flag {f}" for e in entries for f in e.when + e.when_any if f not in known]
    c.verify("every when/whenAny flag is known", problems)

    problems = []
    for p in sorted(on_disk):
        text = (TEMPLATE_ROOT / p).read_bytes().decode("utf-8-sig")
        for number, line in enumerate(text.splitlines(), 1):
            for m in re.finditer(r"\{\{#if\s+!?([a-z0-9|-]+)\s*\}\}", line):
                for flag in m.group(1).split("|"):
                    if flag not in known:
                        problems.append(f"{p}:{number}: unknown flag {flag}")
    c.verify("every {{#if}} flag in a template is known", problems)

    # AGENTS.md rule 6: one top-level type per file. A nested type is part of its parent and is not counted;
    # a Kiota-generated model is exempt, as it is in the rendered-file check.
    problems = []
    for p in sorted(on_disk):
        if not p.endswith(".cs.txt"):
            continue
        text = (TEMPLATE_ROOT / p).read_bytes().decode("utf-8-sig")
        if is_generated(text):
            continue
        types = top_level_types(text)
        if len(types) > 1:
            problems.append(f"{p}: {len(types)} top-level types ({', '.join(t[1] for t in types)})")
    c.verify("every C# template declares at most one top-level type", problems)

    readme = (TEMPLATE_ROOT / "README.md").read_text(encoding="utf-8")
    table = {m.group(1) for m in (sc.README_TOKEN_ROW.match(l) for l in readme.splitlines()) if m}
    problems = [f"README lacks token {t}" for t in sorted(set(sc.DOCUMENTED_TOKENS) - table)]
    problems += [f"README lists undocumented token {t}" for t in sorted(table - set(sc.DOCUMENTED_TOKENS))]
    c.verify("token table is complete", problems)

    ids = [p.id.lower() for p in packages]
    allowed_groups = set(sc.ALWAYS_GROUPS) | known
    problems = [f"duplicate package {i}" for i in set(ids) if ids.count(i) > 1]
    problems += [f"{p.id}: unknown group {g}" for p in packages for g in p.groups if g not in allowed_groups]
    problems += [f"{p.id}: no groups" for p in packages if not p.groups]
    problems += [f"{p.id}: version '{p.version}' is not a version" for p in packages
                 if not re.fullmatch(r"\d+(\.\d+){1,3}(-[0-9A-Za-z.-]+)?", p.version)]
    c.verify("package groups are valid, ids unique, versions well-formed", problems)
    return c.ok


def parse_slnx(sln_path):
    text = sln_path.read_text(encoding="utf-8")
    folders = re.findall(r'<Folder Name="([^"]+)"', text)
    projects = re.findall(r'<Project Path="([^"]+)"', text)
    empty = []
    for m in re.finditer(r'<Folder Name="([^"]+)"\s*/>', text):
        empty.append(m.group(1))
    for m in re.finditer(r'<Folder Name="([^"]+)">(.*?)</Folder>', text, flags=re.S):
        if not re.search(r"<(Project|File)\s", m.group(2)):
            empty.append(m.group(1))
    return folders, projects, empty


def test_render_matrix():
    print("\nTEST 2: Render matrix")
    print("-" * 40)
    sc = load_scaffold()
    c = Check()
    for key, spec in MATRIX.items():
        directory, code, output = get_render(key)
        name = spec["name"]
        print(f"  [{key}]")
        c.verify(f"{key}: render exits 0", [] if code == 0 else output.strip().splitlines()[-3:])
        if code != 0:
            continue
        want_src, want_tests = expected_projects(name, spec["db"], spec["flags"])
        have_src = {p.name for p in (directory / "src").iterdir() if p.is_dir()}
        have_tests = {p.name for p in (directory / "tests").iterdir() if p.is_dir()}
        c.verify(f"{key}: src/ project set",
                 [f"missing {n}" for n in sorted(want_src - have_src)] + [f"unexpected {n}" for n in sorted(have_src - want_src)])
        c.verify(f"{key}: tests/ project set",
                 [f"missing {n}" for n in sorted(want_tests - have_tests)] + [f"unexpected {n}" for n in sorted(have_tests - want_tests)])

        problems = []
        for base in ("src", "tests"):
            for d in sorted((directory / base).iterdir()):
                if d.is_dir() and not (d / f"{d.name}.csproj").exists():
                    problems.append(f"{base}/{d.name} lacks {d.name}.csproj")
        c.verify(f"{key}: every project folder has <folder>.csproj", problems)

        problems = []
        for csproj in directory.rglob("*.csproj"):
            for ref in re.findall(r'<ProjectReference\s+Include="([^"]+)"', csproj.read_text(encoding="utf-8")):
                if not (csproj.parent / ref.replace("\\", "/")).resolve().exists():
                    problems.append(f"{rel(csproj, directory)} references missing {ref}")
        c.verify(f"{key}: project references resolve", problems)

        features = directory / "src" / f"{name}.Domains" / "Features"
        have_features = sorted(p.name for p in features.iterdir()) if features.exists() else []
        c.verify(f"{key}: Features/ holds only the plural entity folder {spec['entities']}",
                 [] if have_features == [spec["entities"]] else [f"found {have_features}"])

        slnx = directory / f"{name}.slnx"
        if not slnx.exists():
            c.verify(f"{key}: solution file", [f"{name}.slnx missing"])
        else:
            folders, projects, empty = parse_slnx(slnx)
            on_disk = {rel(p, directory) for p in directory.rglob("*.csproj")}
            c.verify(f"{key}: solution lists exactly the generated projects",
                     [f"not in solution: {p}" for p in sorted(on_disk - set(projects))]
                     + [f"in solution but absent: {p}" for p in sorted(set(projects) - on_disk)]
                     + [f"listed twice: {p}" for p in set(projects) if projects.count(p) > 1])
            c.verify(f"{key}: solution folders alphabetical, none empty",
                     ([] if folders == sorted(folders, key=str.lower) else [f"order is {folders}"])
                     + [f"empty folder {f}" for f in empty])
            solution_items = re.search(r'<Folder Name="/Solution Items/">(.*?)</Folder>', slnx.read_text(encoding="utf-8"), re.S)
            listed = re.findall(r'<File Path="([^"]+)"', solution_items.group(1)) if solution_items else []
            c.verify(f"{key}: solution items exist on disk", [f"missing {f}" for f in listed if not (directory / f).exists()])

        problems = []
        for path in rendered_files(directory):
            data = path.read_bytes()
            label = rel(path, directory)
            try:
                text = data.decode("utf-8")
            except UnicodeDecodeError:
                problems.append(f"{label}: not UTF-8")
                continue
            for m in TOKEN_REGEX.finditer(text):
                problems.append(f"{label}: unresolved token {m.group(0)}")
            if "{{#if" in text or "{{/if" in text:
                problems.append(f"{label}: conditional marker left")
            if TOKEN_REGEX.search(label):
                problems.append(f"{label}: unresolved token in path")
            crlf = data.count(b"\r\n")
            lf_only = data.count(b"\n") - crlf
            if crlf and lf_only:
                problems.append(f"{label}: mixed line endings ({crlf} CRLF, {lf_only} LF)")
        c.verify(f"{key}: UTF-8, consistent line endings, no unresolved tokens or markers", problems)

        problems = []
        before = {rel(p, directory): p.read_bytes() for p in rendered_files(directory)}
        sentinel = directory / "README.md"
        sentinel.write_bytes(b"keep me")
        before["README.md"] = b"keep me"
        code2, out2, err2 = run_main(render_args(spec, directory))
        statuses = [line.split()[0] for line in out2.splitlines() if line.startswith("  ") and line.split()
                    and line.split()[0] in ("CREATED", "SKIPPED", "WOULD-CREATE")]
        if code2 != 0:
            problems.append(f"second render exit code {code2}")
        if statuses.count("CREATED"):
            problems.append(f"second render created {statuses.count('CREATED')} file(s)")
        if statuses.count("SKIPPED") != len(before):
            problems.append(f"second render skipped {statuses.count('SKIPPED')} of {len(before)} files")
        after = {rel(p, directory): p.read_bytes() for p in rendered_files(directory)}
        if after != before:
            problems.append("files changed or appeared on the second render")
        c.verify(f"{key}: second render skips every file, creates none, overwrites nothing", problems)
    return c.ok


def cs_rules(directory, spec, c, key):
    name = spec["name"]
    files = csharp_files(directory)
    problems_types, problems_dto, problems_enum, problems_suffix = [], [], [], []
    problems_async, problems_http, problems_doc, problems_test = [], [], [], []
    for path in files:
        label = rel(path, directory)
        text = read_text(path)
        generated = is_generated(text) or path.name.endswith(".Designer.cs")
        in_tests = label.startswith("tests/")
        types = top_level_types(text)

        for _, type_name, _ in types:
            if re.search(r"Dto|DTO", type_name):
                problems_dto.append(f"{label}: type {type_name}")
        if re.search(r"Dto|DTO", path.name):
            problems_dto.append(f"{label}: file name")

        if generated:
            continue
        if len(types) > 1:
            problems_types.append(f"{label}: {len(types)} top-level types ({', '.join(t[1] for t in types)})")

        for kind, type_name, _ in types:
            if kind == "enum" and not (type_name.endswith("s") or type_name.endswith("Status")):
                problems_enum.append(f"{label}: enum {type_name} is not plural")
            if kind in ("class", "record") and type_name.endswith("Handler") and not re.search(r"(Command|Query)Handler$", type_name):
                problems_suffix.append(f"{label}: handler {type_name} needs a Command/Query prefix")
        cleaned = "\n".join(code_lines(text))
        for m in TYPE_DECL.finditer(cleaned):
            head = cleaned[m.start(): cleaned.find("{", m.start())] if "{" in cleaned[m.start():] else cleaned[m.start():]
            if re.search(r"\bICommandHandler<", head) and not m.group(2).endswith("CommandHandler"):
                problems_suffix.append(f"{label}: {m.group(2)} implements ICommandHandler but is not *CommandHandler")
            if re.search(r"\bIQueryHandler<", head) and not m.group(2).endswith("QueryHandler"):
                problems_suffix.append(f"{label}: {m.group(2)} implements IQueryHandler but is not *QueryHandler")
        if "/Commands/" in label:
            for _, type_name, _ in types:
                if not re.search(r"(Command|CommandHandler|Response)$", type_name):
                    problems_suffix.append(f"{label}: {type_name} in Commands/ must end Command, CommandHandler or Response")
        if "/Queries/" in label:
            for _, type_name, _ in types:
                if not re.search(r"(Query|QueryHandler|Response)$", type_name):
                    problems_suffix.append(f"{label}: {type_name} in Queries/ must end Query, QueryHandler or Response")

        # async methods take a CancellationToken (tests, overrides, async void handlers, lambdas, DisposeAsync exempt)
        if not in_tests:
            lines = cleaned.split("\n")
            for m in re.finditer(r"\basync\b", cleaned):
                after_text = cleaned[m.end():]
                if re.match(r"\s*(\(|\w+\s*=>|delegate\b)", after_text):
                    continue  # lambda
                line_start = cleaned.rfind("\n", 0, m.start()) + 1
                prefix = cleaned[line_start:m.start()]
                if "override" in prefix:
                    continue  # framework override: signature is fixed by the base class
                decl = re.match(r"\s*(?:[\w<>\[\],.?\s]+?)\s+(\w+)\s*(?:<[^>]*>)?\s*\(", after_text)
                if not decl:
                    continue
                method = decl.group(1)
                if method in ASYNC_NAME_EXCEPTIONS:
                    continue
                if re.match(r"\s*void\b", after_text):
                    continue  # async void event handler
                open_at = m.end() + decl.end() - 1  # the regex ends on the opening parenthesis
                depth, i = 0, open_at
                while i < len(cleaned):
                    ch = cleaned[i]
                    depth += ch == "("
                    depth -= ch == ")"
                    if depth == 0:
                        break
                    i += 1
                if "CancellationToken" not in cleaned[open_at:i + 1]:
                    number = cleaned.count("\n", 0, m.start()) + 1
                    problems_async.append(f"{label}:{number}: {method}")

        # HttpClient: never constructed, never used as a type in consumer code (src/)
        if not in_tests:
            for number, line in enumerate(code_lines(text), 1):
                if re.search(r"new\s+HttpClient\s*\(", line):
                    problems_http.append(f"{label}:{number}: new HttpClient(")
                elif re.search(r"(?<![\w.])HttpClient(?![\w])", line) and not line.lstrip().startswith("using ") \
                        and not any(label.endswith(allowed) for allowed in HTTPCLIENT_ALLOWED_FILES):
                    problems_http.append(f"{label}:{number}: raw HttpClient")

        # public top-level types carry an XML doc comment
        raw_lines = text.split("\n")
        for kind, type_name, offset in types:
            number = cleaned.count("\n", 0, offset)
            if not re.match(r"\s*public\b", raw_lines[number]):
                continue
            before = "\n".join(raw_lines[:number])
            while True:  # step over attribute blocks, which may span several lines
                stripped = re.sub(r"\s*\[(?:[^\[\]]|\[[^\]]*\])*\]\s*$", "", before)
                if stripped == before:
                    break
                before = stripped
            if not before.rstrip().split("\n")[-1].strip().startswith("///"):
                problems_doc.append(f"{label}: public {kind} {type_name}")

        if in_tests:
            if re.search(r"\[ExpectedException", text):
                problems_test.append(f"{label}: [ExpectedException]")
            if re.search(r"Mock<\s*\w*(DataContext|DbContext)\w*\s*>", text):
                problems_test.append(f"{label}: mocked DataContext")
            if re.search(r"Assert\.Throws(Async)?\s*<", text):
                problems_test.append(f"{label}: Assert.Throws instead of Assert.ThrowsExactly")
            for m in re.finditer(r"Assert\.Throws(Async)?\s*\(", text):
                problems_test.append(f"{label}: Assert.Throws instead of Assert.ThrowsExactly")
            if re.search(r"\b(Xunit|NUnit)\b|\[(Fact|Theory|Test)\]", text):
                problems_test.append(f"{label}: xUnit/NUnit")

    c.verify(f"{key}: one top-level type per file", problems_types)
    c.verify(f"{key}: no Dto in type or file names", problems_dto)
    c.verify(f"{key}: enum names plural (Status exempt)", problems_enum)
    c.verify(f"{key}: handler, command and query suffix rules", problems_suffix)
    c.verify(f"{key}: async methods take a CancellationToken", problems_async)
    c.verify(f"{key}: no raw HttpClient in consumer code", problems_http)
    c.verify(f"{key}: public types have XML docs", problems_doc)
    c.verify(f"{key}: test conventions (MSTest, ThrowsExactly, no mocked DataContext)", problems_test)

    # every mapped route declares Produces metadata
    endpoints = list((directory / "src" / f"{name}.Services" / "Endpoints").glob("*Endpoints.cs"))
    problems = []
    for path in endpoints:
        body = "\n".join(code_lines(read_text(path)))
        for m in re.finditer(r"\.Map(Get|Post|Put|Delete|Patch)\s*\(", body):
            chain_end = body.find(";", m.start())
            chain = body[m.start():chain_end]
            if not re.search(r"\.Produces(?:<[^>]*>)?\(", chain):
                problems.append(f"{rel(path, directory)}: route near line {body.count(chr(10), 0, m.start()) + 1} has no .Produces(")
            if "Status429" not in chain and "429" not in chain:
                problems.append(f"{rel(path, directory)}: route near line {body.count(chr(10), 0, m.start()) + 1} lacks a 429 Produces")
    c.verify(f"{key}: every mapped route declares .Produces(...)", problems if endpoints else ["no endpoints file found"])


def test_template_rules():
    print("\nTEST 3: Template rules on rendered C# files")
    print("-" * 40)
    c = Check()
    for key, spec in MATRIX.items():
        directory, code, _ = get_render(key)
        if code != 0:
            c.verify(f"{key}: render available", ["render failed"])
            continue
        print(f"  [{key}]")
        cs_rules(directory, spec, c, key)
    return c.ok


def test_package_management():
    print("\nTEST 4: Central package management")
    print("-" * 40)
    c = Check()
    for key, spec in MATRIX.items():
        directory, code, _ = get_render(key)
        if code != 0:
            c.verify(f"{key}: render available", ["render failed"])
            continue
        print(f"  [{key}]")
        props_path = directory / "Directory.Packages.props"
        props = props_path.read_text(encoding="utf-8")
        versions = re.findall(r'<PackageVersion\s+Include="([^"]+)"\s+Version="([^"]+)"', props)
        defined = {i.lower() for i, _ in versions}
        problems, referenced = [], set()
        for csproj in sorted(directory.rglob("*.csproj")):
            text = csproj.read_text(encoding="utf-8")
            for attrs in re.findall(r"<PackageReference\s+([^>]*?)/?>", text):
                inc = re.search(r'Include="([^"]+)"', attrs)
                if not inc:
                    continue
                referenced.add(inc.group(1).lower())
                if re.search(r'\bVersion(Override)?\s*=', attrs):
                    problems.append(f"{rel(csproj, directory)}: {inc.group(1)} carries a version attribute")
                if inc.group(1).lower() not in defined:
                    problems.append(f"{rel(csproj, directory)}: {inc.group(1)} has no PackageVersion")
        c.verify(f"{key}: PackageReference has no Version, every package has a PackageVersion", problems)
        c.verify(f"{key}: Directory.Packages.props switches central management on and has no duplicates",
                 ([] if re.search(r"<ManagePackageVersionsCentrally>\s*true\s*<", props) else ["ManagePackageVersionsCentrally is not true"])
                 + [f"duplicate PackageVersion {i}" for i in {i.lower() for i, _ in versions}
                    if [x.lower() for x, _ in versions].count(i) > 1])
        build_props = (directory / "Directory.Build.props").read_text(encoding="utf-8")
        combined = props + build_props
        c.verify(f"{key}: NuGet audit properties present",
                 [f"{p} missing" for p in ("NuGetAudit", "NuGetAuditMode", "NuGetAuditLevel") if f"<{p}>" not in combined]
                 + ([] if re.search(r"<NuGetAudit>\s*true\s*<", combined) else ["NuGetAudit is not true"]))

        tools = json.loads((directory / ".config" / "dotnet-tools.json").read_text(encoding="utf-8"))
        tool_ids = {k.lower(): v for k, v in tools.get("tools", {}).items()}
        commands = {cmd for v in tool_ids.values() for cmd in v.get("commands", [])}
        c.verify(f"{key}: dotnet-tools.json has kiota and dotnet-ef",
                 [f"command {cmd} missing" for cmd in ("kiota", "dotnet-ef") if cmd not in commands]
                 + [f"{k}: no version" for k, v in tool_ids.items() if not v.get("version")])
        gj_path = directory / "global.json"
        problems = []
        if not gj_path.exists():
            problems.append("global.json missing")
        else:
            sdk = json.loads(gj_path.read_text(encoding="utf-8")).get("sdk", {})
            if sdk.get("version") != EXPECTED_SDK:
                problems.append(f"sdk.version is {sdk.get('version')}, expected pinned {EXPECTED_SDK}")
            if sdk.get("rollForward") not in ("disable", "latestPatch"):
                problems.append(f"sdk.rollForward is {sdk.get('rollForward')}")
        c.verify(f"{key}: global.json pins the SDK", problems)
    return c.ok


def shipped_files():
    files = []
    for entry in SHIPPED_PATHS:
        path = ROOT / entry
        if path.is_file():
            files.append(path)
        elif path.is_dir():
            for dirpath, dirnames, filenames in os.walk(path):
                dirnames[:] = [d for d in dirnames if d not in SKIP_DIR_NAMES
                               and not os.path.islink(os.path.join(dirpath, d))
                               and not (hasattr(os.path, "isjunction") and os.path.isjunction(os.path.join(dirpath, d)))]
                for f in filenames:
                    if f not in SKIP_FILE_NAMES:
                        files.append(Path(dirpath) / f)
    for pattern in SHIPPED_GLOBS:
        files.extend(ROOT.glob(pattern))
    return sorted(set(files))


def find_forbidden(text):
    hits = [m.group(0) for m in FORBIDDEN_TERM_PATTERN.finditer(text)]
    hits += [m.group(0) for m in FORBIDDEN_WORD_PATTERN.finditer(text)]
    hits += [m.group(0) for m in FORBIDDEN_DRIVE_PATH.finditer(text)]
    return hits


def test_forbidden_terms():
    print("\nTEST 5: Forbidden terms")
    print("-" * 40)
    c = Check()
    problems, count = [], 0
    for path in shipped_files():
        count += 1
        label = rel(path, ROOT)
        hits = find_forbidden(path.read_bytes().decode("utf-8", errors="ignore")) + find_forbidden(label)
        if hits:
            problems.append(f"{label}: {sorted(set(h.lower() for h in hits))}")
    c.verify(f"{count} shipped files contain none of the forbidden terms or a drive path", problems)

    problems, scanned = [], 0
    for key in MATRIX:
        directory, code, _ = get_render(key)
        if code != 0:
            problems.append(f"{key}: render failed")
            continue
        for path in rendered_files(directory):
            scanned += 1
            hits = find_forbidden(path.read_bytes().decode("utf-8", errors="ignore")) + find_forbidden(rel(path, directory))
            if hits:
                problems.append(f"{key}/{rel(path, directory)}: {sorted(set(h.lower() for h in hits))}")
    c.verify(f"{scanned} rendered files contain none of the forbidden terms", problems)
    return c.ok


def test_cli_negative():
    print("\nTEST 6: Command-line negative tests")
    print("-" * 40)
    sc = load_scaffold()
    c = Check()
    base = ["--company", "Acme Corp", "--yes"]

    def case(label, argv, expect_codes, out_dir=None, expect_text=None):
        code, out, err = run_main(argv)
        problems = []
        if code not in expect_codes:
            problems.append(f"exit code {code}, expected {sorted(expect_codes)}")
        if "Traceback" in out + err:
            problems.append("stack trace printed")
        if expect_text and expect_text not in out + err:
            problems.append(f"output lacks '{expect_text}'")
        if out_dir is not None and out_dir.exists() and any(out_dir.iterdir()):
            problems.append("files were written despite the error")
        c.verify(label, problems)
        return code, out, err

    def target(name):
        return WORK_DIR / "cli" / name

    case("lower-case name is rejected", ["--name", "acme", "--output", str(target("a1")), *base], {2}, target("a1"), "error:")
    case("name with a separator is rejected", ["--name", "Ac-me", "--output", str(target("a2")), *base], {2}, target("a2"), "error:")
    case("reserved name is rejected", ["--name", "System", "--output", str(target("a3")), *base], {2}, target("a3"), "reserved")
    case("--yes without a name is rejected", ["--output", str(target("a4")), *base], {2}, target("a4"), "--name is required")
    case("unknown --with flag is rejected", ["--name", "Acme", "--with", "bogus", "--output", str(target("a5")), *base], {2}, target("a5"), "unknown flag")
    case("unknown option is rejected by the parser", ["--name", "Acme", "--bogus"], {2})
    case("unknown database is rejected by the parser", ["--name", "Acme", "--database", "oracle"] + base, {2})
    case("keyword entity is rejected", ["--name", "Acme", "--entity", "Class", "--entities", "Classes", "--output", str(target("a6")), *base], {2}, target("a6"), "keyword")
    case("equal singular and plural entity is rejected", ["--name", "Acme", "--entity", "Item", "--entities", "Item", "--output", str(target("a7")), *base], {2}, target("a7"), "must differ")
    case("empty company is rejected", ["--name", "Acme", "--company", " ", "--yes", "--output", str(target("a8"))], {2}, target("a8"), "company")
    case("bad application id is rejected", ["--name", "Acme", "--application-id", "Com.Example", "--output", str(target("a9")), *base], {2}, target("a9"), "application identifier")
    case("non-overridable token is rejected", ["--name", "Acme", "--force-token", "Company=x", "--output", str(target("a10")), *base], {2}, target("a10"), "not overridable")
    case("out-of-range port is rejected", ["--name", "Acme", "--force-token", "ApiHttpsPort=80", "--output", str(target("a11")), *base], {2}, target("a11"), "port")
    case("version with more than three parts is rejected", ["--name", "Acme", "--force-token", "Version=1.2.3.4.5.6.7.8.9.10", "--output", str(target("a13")), *base], {2}, target("a13"), "Version")
    case("version with a non-numeric part is rejected", ["--name", "Acme", "--force-token", "Version=1.x.3", "--output", str(target("a14")), *base], {2}, target("a14"), "Version")
    case("non-numeric year is rejected", ["--name", "Acme", "--force-token", "Year=abc", "--output", str(target("a15")), *base], {2}, target("a15"), "Year")
    case("two heads on one port are rejected", ["--name", "Acme", "--force-token", "ApiHttpsPort=44401", "--force-token", "WebHttpsPort=44401", "--output", str(target("a16")), *base], {2}, target("a16"), "must differ")
    case("missing template root is a clean error", ["--name", "Acme", "--templates", str(WORK_DIR / "no-such-root"), "--output", str(target("a12")), *base], {2}, target("a12"), "error:")

    blocker = target("blocker-file")
    blocker.parent.mkdir(parents=True, exist_ok=True)
    blocker.write_text("not a directory", encoding="utf-8")
    case("output path that is a file is rejected", ["--name", "Acme", "--output", str(blocker), *base], {2}, None, "not a directory")

    dry = target("dry")
    code, out, _ = case("--dry-run exits 0 and writes nothing", ["--name", "Acme", "--dry-run", "--output", str(dry), *base], {0}, None, "Dry run")
    c.verify("--dry-run leaves no output directory", [] if not dry.exists() or not any(dry.iterdir()) else ["files were written"])

    existing = target("existing")
    existing.mkdir(parents=True, exist_ok=True)
    (existing / "README.md").write_text("mine", encoding="utf-8")
    code, out, _ = case("existing file is skipped, not overwritten", ["--name", "Acme", "--output", str(existing), *base], {0}, None, "SKIPPED")
    c.verify("existing README.md keeps its content and is reported SKIPPED",
             ([] if (existing / "README.md").read_text(encoding="utf-8") == "mine" else ["README.md was overwritten"])
             + ([] if re.search(r"SKIPPED\s+README\.md", out) else ["no SKIPPED line for README.md"])
             + ([] if (existing / "Acme.slnx").exists() else ["the other files were not created"]))

    ignored = target("ignored-flag")
    case("flag without templates only prints a notice", ["--name", "Acme", "--with", "worker", "--dry-run", "--output", str(ignored), *base], {0}, None, "templates not available yet")

    code, out, err = run_main(["--check-templates"])
    c.verify("--check-templates exits 0", [] if code == 0 else [out.strip()])
    return c.ok


def test_provenance():
    print("\nTEST 7: Provenance rule")
    print("-" * 40)
    c = Check()
    raw = (TEMPLATE_ROOT / "manifest.json").read_text(encoding="utf-8")
    manifest = json.loads(raw)
    c.verify("no manifest entry has a source key",
             [f"entry {i}: has 'source'" for i, e in enumerate(manifest) if "source" in e]
             + ([] if '"source"' not in raw else ["manifest text contains \"source\""]))
    phrases = re.compile(r"reference\s+(repo|project|solution)|derived\s+from|copied\s+from|provenance", re.I)
    problems = []
    for i, e in enumerate(manifest):
        text = json.dumps(e)
        if find_forbidden(text) or phrases.search(text):
            problems.append(f"entry {i} ({e.get('output')}) mentions a reference project")
    problems += [f"manifest.json text: {h}" for h in find_forbidden(raw)]
    c.verify("no manifest entry mentions a reference project", problems)
    c.verify("manifest keys are limited to template, output, when, whenAny",
             [f"entry {i}: unexpected keys {sorted(set(e) - {'template', 'output', 'when', 'whenAny'})}"
              for i, e in enumerate(manifest) if set(e) - {"template", "output", "when", "whenAny"}])
    return c.ok


def find_dotnet():
    dotnet = shutil.which("dotnet")
    if not dotnet:
        return None
    try:
        result = subprocess.run([dotnet, "--list-sdks"], capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return dotnet if re.search(rf"^{re.escape(EXPECTED_SDK)}\s", result.stdout, re.M) else None


def test_build_smoke():
    print("\nTEST 8: Build smoke (opt-in)")
    print("-" * 40)
    if os.environ.get(SMOKE_ENV) != "1":
        print(f"  SKIP: set {SMOKE_ENV}=1 to render, restore, build and test the sqlserver+apphost solution")
        return True
    dotnet = find_dotnet()
    if not dotnet:
        print(f"  SKIP: dotnet SDK {EXPECTED_SDK} not found; the build smoke needs exactly that SDK (see global.json)")
        return True
    directory, code, output = get_render("sqlserver-apphost")
    if code != 0:
        print("  FAIL: render failed")
        return False
    env = dict(os.environ, MSBUILDDISABLENODEREUSE="1", DOTNET_CLI_TELEMETRY_OPTOUT="1", DOTNET_NOLOGO="1")
    # The MAUI head is never rendered here (no maui flag), so nothing below can build it.
    steps = [
        ("dotnet tool restore", [dotnet, "tool", "restore"]),
        ("dotnet restore", [dotnet, "restore"]),
        ("dotnet build", [dotnet, "build", "-nodeReuse:false", "--no-incremental", "--no-restore"]),
        ("dotnet test", [dotnet, "test", "--no-build"]),
    ]
    c = Check()
    for label, argv in steps:
        started = time.time()
        try:
            result = subprocess.run(argv, cwd=directory, env=env, capture_output=True, text=True,
                                    encoding="utf-8", errors="replace", timeout=1500)
        except subprocess.TimeoutExpired:
            c.verify(label, ["timed out after 1500 s"])
            return False
        text = result.stdout + result.stderr
        problems = []
        if result.returncode != 0:
            problems += text.strip().splitlines()[-8:]
        if label == "dotnet build":
            if not re.search(r"\b0 Warning\(s\)", text):
                problems.append("build did not report 0 Warning(s)")
            if not re.search(r"\b0 Error\(s\)", text):
                problems.append("build did not report 0 Error(s)")
        c.verify(f"{label} ({time.time() - started:.0f}s)", problems)
        if problems:
            break
    return c.ok


# ─── Runner ──────────────────────────────────────────────────────────────────


def cleanup():
    """Remove this run's work directory, and nothing else."""
    target = WORK_DIR.resolve()
    allowed = (ROOT / ".ai" / "tmp").resolve()
    if target.parent != allowed or not target.name.startswith("validate-scaffold-"):
        print(f"  refusing to remove {target}")
        return

    def on_error(func, path, _exc):
        os.chmod(path, 0o700)
        func(path)

    if target.exists():
        shutil.rmtree(target, onerror=on_error)


def main():
    print("=" * 60)
    print("  Solution Scaffold Validation")
    print("=" * 60)
    tests = [test_template_integrity, test_render_matrix, test_template_rules, test_package_management,
             test_forbidden_terms, test_cli_negative, test_provenance, test_build_smoke]
    results, started = [], time.time()
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    try:
        for test in tests:
            t0 = time.time()
            try:
                ok = test()
            except Exception as exc:  # a crash in a test is a failure, reported with its type
                print(f"  FAIL: {test.__name__} raised {type(exc).__name__}: {exc}")
                ok = False
            print(f"  ({time.time() - t0:.1f}s)")
            results.append(ok)
    finally:
        cleanup()
    print()
    print("=" * 60)
    print(f"  {sum(results)}/{len(results)} tests passed in {time.time() - started:.1f}s")
    print("=" * 60)
    if all(results):
        print("  ALL SCAFFOLD TESTS PASSED")
        return 0
    print("  SOME SCAFFOLD TESTS FAILED")
    return 1


if __name__ == "__main__":
    sys.exit(main())
