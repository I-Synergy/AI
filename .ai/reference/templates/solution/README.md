# Solution scaffold templates

Source files for `.ai/scripts/scaffold-solution.py`. Everything here is stored as `*.txt` (plus this README, `manifest.json` and `package-versions.json`) so the template repository never contains a buildable solution.

## File layout

A template for output file `src/{ApplicationName}.Common/Constants/AspireNames.cs` is stored at

```
.ai/reference/templates/solution/files/src/{ApplicationName}.Common/Constants/AspireNames.cs.txt
```

i.e. the output path with `.txt` appended, under `files/`. Tokens may appear in path segments. Exactly one type per template file (AGENTS.md rule 6). Dotfiles keep their name (`files/.editorconfig.txt`).

## Tokens

| Token | Meaning | Example |
|---|---|---|
| `{ApplicationName}` | Solution name, PascalCase, valid C# identifier segment | `Acme` |
| `{applicationname}` | lower-case, no separators (Aspire names, container names, schema) | `acme` |
| `{ApplicationId}` | Application identifier of the MAUI head: lower-case reverse DNS, the Android package, the Apple bundle identifier and the Windows package identity. Default `com.example.<name>`, set with `--application-id` | `com.example.acme` |
| `{Company}` | Company for `Directory.Build.props` | `Acme Corp` |
| `{Entity}` | First sample entity, singular, PascalCase | `Item` |
| `{Entities}` | First sample entity, plural, PascalCase | `Items` |
| `{entity}` | First sample entity, singular, camelCase | `item` |
| `{entities}` | First sample entity, plural, camelCase | `items` |
| `{Provider}` | `SqlServer` or `Postgres` | `SqlServer` |
| `{Year}` | Current year | `2026` |
| `{Version}` | Generated version stamp `{yyyy}.1{MMdd}.1{HHmm}` | `2026.11121.11153` |
| `{AppHostHttpsPort}` | HTTPS port of the AppHost launch profile (default `44400`) | `44400` |
| `{ApiHttpsPort}` | HTTPS port of the Service.Api launch profile (default `44401`) | `44401` |
| `{WebHttpsPort}` | HTTPS port of the App.Web launch profile (default `44402`) | `44402` |
| `{PackageVersions}` | Replaced by `<PackageVersion>` lines from `package-versions.json` for the selected groups (only valid as a whole line in `Directory.Packages.props`) | |

Unknown `{Token}` text is a template bug: the generator fails on any unreplaced documented token. Braces that are real C# or JSON (for example `{ get; set; }`, log placeholders such as `{EntityId}`, interpolated `$"{apiServiceName}"`) never match the token pattern because tokens are exactly the names above; do not invent new token names without adding them here and to `DOCUMENTED_TOKENS` in the script.

`python .ai/scripts/scaffold-solution.py --check-templates` verifies that this table lists exactly the documented tokens, that every `{Name}` used in a template is either a documented token or a known C# brace name, that every file has exactly one manifest entry and the reverse, that conditional markers balance, and that every package group is known.

## Conditional blocks

Markers sit on their own line, in any file type (wrap in a comment if the file type needs it, the generator strips the whole line):

```
{{#if sqlserver}}
...
{{/if}}
{{#if postgres}} ... {{/if}}
{{#if !apphost}} ... {{/if}}
{{#if maui|web|sqlite-device}} ... {{/if}}
```

A list (`a|b`) is true when any listed flag is set. `!` negates a single flag only.

Flags: `sqlserver`, `postgres` (exactly one of them is set), `apphost`, `maui`, `web`, `sqlite-device`, `worker`, `tests-acceptance`, `tests-ui`. Blocks may nest. Use blocks only for lines that differ; a file that exists only for one flag is gated in the manifest instead.

A flag whose templates do not exist yet (no manifest entry lists it in `when`) is offered by the script, prints a `templates not available yet` notice when chosen, and is treated as not set. Its conditional blocks therefore render as absent until its templates arrive.

## manifest.json

One entry per template file, authoritative for what is generated and why:

```json
{
  "template": "files/src/{ApplicationName}.Common/Constants/AspireNames.cs.txt",
  "output": "src/{ApplicationName}.Common/Constants/AspireNames.cs",
  "when": []
}
```

- `when`: list of flags that must ALL be set; `[]` means always. Use `"when": ["sqlserver"]` for provider-only files.
- `whenAny` (optional): list of flags of which ONE must be set. A file is rendered when `when` holds and, if `whenAny` is present, at least one of its flags is set. `App.Shared` uses `whenAny: ["maui", "web", "sqlite-device"]` because each of those heads or stores needs the shared layer. `whenAny` does not make a flag "available": availability still comes from `when` only, so a flag with no `when` template stays "not available yet".
- Every file under `files/` has exactly one entry and vice versa. Entries are sorted by `output`.
- No `source` field. Provenance (which reference file a template was derived from) is private working data, never shipped in the manifest or in any template.

## package-versions.json

One entry per central package version (`id`, `version`, `groups`). Ids are unique; when two parts disagreed the newest stable version was kept, and a preview is kept only when no stable version exists.

Group semantics:

- A package is emitted into `Directory.Packages.props` when **any** of its groups is selected.
- `core` and `tests` are always selected. `core` holds the packages of the projects that are always generated (framework, CQRS, EF Core tooling, API, Kiota client). `tests` holds the unit-test packages.
- Every other group is selected by the flag of the same name: `sqlserver`, `postgres`, `apphost`, `maui`, `web`, `worker`, `sqlite-device`, `tests-acceptance` (Reqnroll), `tests-ui` (Playwright).
- A package may list several groups. `Testcontainers.PostgreSql` is in `tests` and `postgres`, so the Postgres test project finds it; it is emitted for every render because `tests` is always selected.

## Rules every template must follow

1. Keep structure, naming and signatures consistent with the architecture documents; keep comments that explain non-obvious MSBuild behaviour in neutral wording.
2. Follow AGENTS.md Critical Coding Rules 1-15 without exception.
3. Never include licence keys, connection strings, signing identities, registry hosts, GUIDs, credentials, company or repository URLs. Use tokens or secret parameters.
3a. Never mention or sample-copy from any real project. Sample content uses placeholders and generic sample names only (application `Acme`, entity `Item`, company `Acme Corp`).
4. Plural names for collections of a kind (`Domains`, `Entities`, `Models`, `Features/{Entities}/`), `Service.Api` stays singular.
5. Generated code must build with the bare .NET 11 SDK for every project except the MAUI head.
6. XML docs on public types and members (CS1591 is suppressed in `Directory.Build.props`, but the template shows the standard).

## Kiota client and build order

`src/{ApplicationName}.Clients/Api/` ships as templates: the Kiota output for the sample entity, tokenised. It is the only source of the client in a fresh render, and it solves the ordering problem that a fresh build would otherwise hit (`App.Shared` uses `ApiClient`, but only the API's Debug build generates it).

- `{ApplicationName}.Clients` references `{ApplicationName}.Service.Api` with `ReferenceOutputAssembly="false"`. The API's Debug build, which regenerates the client, finishes before the client compiles. The reference adds no assembly dependency.
- The client reads `Api/` at compile time through `Directory.GetFiles` in a target, not through a wildcard item. MSBuild's file-enumeration cache can hold a listing taken before the regeneration, which gave a stale compile item in testing.
- The templates are the Debug output for `Item`, aligned against the output for `Product`: a word that differs between the two runs became a token, and a word Kiota fixes stayed literal (the collection indexer is always named `Item`).
- A fresh render compiles with no generator run, in Debug and in Release. A Debug build regenerates `Api/` from `openapi/{ApplicationName}.Service.Api.json`; a route change adds or removes generated files, and the next build compiles them.
- `kiota-lock.json` is written by the generator and is not shipped (it holds a hash of the document).
- Known limitation, accepted: Kiota sorts `using` directives, members and deserializers alphabetically. Where an entity-named member sorts depends on the name, so for an entity whose names sort differently from `Item` the first Debug build reorders members in the generated models and request builders. The code is equivalent; the change is ordering only.
- Opt-out: `-p:{ApplicationName}GenerateApiClient=false` skips regeneration on the API build.

## Generating

```
python .ai/scripts/scaffold-solution.py --check-templates
python .ai/scripts/scaffold-solution.py --name Acme --company "Acme Corp" --application-id com.example.acme --entity Item --entities Items --database sqlserver --with apphost --output ./Acme --yes
python .ai/scripts/scaffold-solution.py ... --dry-run
```

Without `--yes` the script prompts for every value that is not given as a flag. `--force-token` overrides `Version`, `Year`, `AppHostHttpsPort` or `ApiHttpsPort` (for reproducible renders). Existing files are never overwritten.
