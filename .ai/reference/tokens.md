# Template Tokens Reference

There are two token sets.

1. **Reference tokens** (below) are placeholders in the rules, skills and reference files. Replace them when implementing.
2. **Scaffold tokens** are filled by `python .ai/scripts/scaffold-solution.py`. Their contract is in `.ai/reference/templates/solution/README.md`.

The template ships no concrete business domain. Every example is expressed with tokens.

## Reference Tokens

| Token | Meaning | Example Usage |
|-------|---------|---------------|
| `{ApplicationName}` | Your application name (PascalCase) | `{ApplicationName}.Domains` |
| `{Domain}` | Business domain, a concept word (bounded context). It is not a project name: the project is `Domains`. | `Features/{Entities}/` for the feature of a domain |
| `{Entity}` | Aggregate root (PascalCase) | `Create{Entity}Command` |
| `{Entities}` | Aggregate root plural (PascalCase). Used for DbSet names and the plural feature folder. | `dataContext.{Entities}`, `Features/{Entities}/` |
| `{entity}` | Aggregate root (camelCase) | `{entity}Id` |
| `{entities}` | Aggregate root plural (camelCase) | `/{entities}`, `{entities}` table |
| `{ChildEntity}` | Child entity inside an aggregate (PascalCase) | `{Entity}With{ChildEntities}Response` |
| `{ChildEntities}` | Child entity plural (PascalCase) | `dataContext.{ChildEntities}` |
| `{childEntity}` | Child entity (camelCase) | `{childEntity}Id` |
| `{childEntities}` | Child entity plural (camelCase) | `/{childEntities}` |

## Scaffold Tokens

These are rendered into the solution files. The full table, with defaults, is in `.ai/reference/templates/solution/README.md`.

| Token | Meaning | Example |
|-------|---------|---------|
| `{ApplicationName}` | Solution name, PascalCase | `Acme` |
| `{applicationname}` | Lower-case name (schema, container and Aspire names) | `acme` |
| `{ApplicationId}` | Application identifier of the MAUI head | `com.example.acme` |
| `{Company}` | Company for `Directory.Build.props` | `Acme Corp` |
| `{Entity}`, `{Entities}`, `{entity}`, `{entities}` | First sample entity, singular and plural, Pascal and camel case | `Item`, `Items`, `item`, `items` |
| `{Provider}` | `SqlServer` or `Postgres` | `SqlServer` |
| `{Year}`, `{Version}` | Build year and version stamp | `2026`, `2026.11121.11153` |
| `{AppHostHttpsPort}`, `{ApiHttpsPort}`, `{WebHttpsPort}` | HTTPS launch profile ports | `44400`, `44401`, `44402` |
| `{PackageVersions}` | Expanded into `PackageVersion` lines in `Directory.Packages.props` | (whole line only) |

## Derived Forms

Identifiers are composed from the tokens using the naming conventions:

- `Create{Entity}Command`, `Update{Entity}Command`, `Delete{Entity}Command`
- `Get{Entity}ByIdQuery`, `Get{Entities}ListQuery`
- `{Entity}Id`, `{Entity}Status`, `{Entities}Endpoints`, `{Entity}CreatedEvent`
- `{ApplicationName}.{Project}` project names and the namespaces that follow their folders
- `/{entities}` routes, `{entities}` tables, `{entity}Id` columns

## Special Files (Always in .ai/)

- **session-context.md** - Read FIRST at session start, update before session end
- **progress/[task].md** - Active task progress files
- **completed/[task].md** - Completed task archives for future reference

## Example Transformation

- **Template:** `{ApplicationName}.Domains/Features/{Entities}/Commands/Create{Entity}/`
- **After rendering with Acme, Item:** `Acme.Domains/Features/Items/Commands/CreateItem/`

## Namespace Examples

```csharp
// Template format
namespace {ApplicationName}.Domains.Features.{Entities}.Commands.Create{Entity};
namespace {ApplicationName}.Services.Endpoints;
namespace {ApplicationName}.Entities;
namespace {ApplicationName}.Data.Abstractions;
```

## File Path Examples

```
// Template paths
src/{ApplicationName}.Domains/Features/{Entities}/Commands/Create{Entity}/Create{Entity}Command.cs
src/{ApplicationName}.Services/Endpoints/{Entities}Endpoints.cs
src/{ApplicationName}.Data/Abstractions/IDataContext.cs
```
