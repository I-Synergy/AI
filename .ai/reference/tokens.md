# Template Tokens Reference

Throughout this template, the following placeholders are used. Replace them when implementing.
The template itself ships no concrete business domain: every example is expressed with tokens.

| Token | Meaning | Example Usage |
|-------|---------|---------------|
| `{ApplicationName}` | Your application name | `{ApplicationName}.Domain.{Domain}` |
| `{Domain}` | Bounded context name | `{ApplicationName}.Domain.{Domain}` |
| `{Entity}` | Aggregate root (PascalCase) | `Create{Entity}Command` |
| `{Entities}` | Aggregate root plural (PascalCase) — used for DbSet names | `dataContext.{Entities}` |
| `{entity}` | Aggregate root (camelCase) | `{entity}Id` |
| `{entities}` | Aggregate root plural (camelCase) | `/{entities}` |
| `{ChildEntity}` | Child entity inside an aggregate (PascalCase) | `{Entity}With{ChildEntities}Response` |
| `{ChildEntities}` | Child entity plural (PascalCase) | `dataContext.{ChildEntities}` |
| `{childEntity}` | Child entity (camelCase) | `{childEntity}Id` |
| `{childEntities}` | Child entity plural (camelCase) | `/{childEntities}` |

## Derived Forms

Identifiers are composed from the tokens using the naming conventions:

- `Create{Entity}Command`, `Update{Entity}Command`, `Delete{Entity}Command`
- `Get{Entity}ByIdQuery`, `Get{Entities}ListQuery`
- `{Entity}Id`, `{Entity}Status`, `{Entity}Endpoints`, `{Entity}CreatedEvent`
- `{ApplicationName}.{Layer}.{Domain}` namespaces
- `/{entities}` routes, `{entities}` tables, `{entity}_id` columns

## Special Files (Always in .ai/)

- **session-context.md** - Read FIRST at session start, update before session end
- **progress/[task].md** - Active task progress files
- **completed/[task].md** - Completed task archives for future reference

## Example Transformation

- **Template:** `{ApplicationName}.Domain.{Domain}`
- **After replacement:** the same pattern with your own application and bounded-context names

## Namespace Examples

```csharp
// Template format
namespace {ApplicationName}.Domain.{Domain}.Features.{Entity}.Commands;
namespace {ApplicationName}.Services.{Domain}.Endpoints;
namespace {ApplicationName}.Entities.{Domain};
```

## File Path Examples

```
// Template paths
src/{ApplicationName}.Domain.{Domain}/Features/{Entity}/Commands/Create{Entity}Command.cs
src/{ApplicationName}.Services.{Domain}/Endpoints/{Entity}Endpoints.cs
```
