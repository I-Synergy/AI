# {ApplicationName}

Solution scaffolded from the .NET template.

## Layout

| Folder | Projects | Role |
|---|---|---|
| `src/{ApplicationName}.Common` | Constants, enumerations, converters, shared models | Shared types, no dependency on other solution projects |
| `src/{ApplicationName}.Resources` | Localized strings | Resource lookup |
| `src/{ApplicationName}.Entities` | Persistence entities and their EF Core mapping | Database shape |
| `src/{ApplicationName}.Models` | Read models and request bodies | Data crossing the API boundary |
| `src/{ApplicationName}.Data` | `IDataContext` abstraction | Data access contract |
| `src/{ApplicationName}.Data.<Provider>` | `DataContext`, design-time factory, startup migration | Provider implementation |
| `src/{ApplicationName}.Domains` | CQRS handlers | Use cases |
| `src/{ApplicationName}.Services` | Endpoint mappings | HTTP surface |
| `src/{ApplicationName}.Service.Api` | ASP.NET Core host | Runs the API |
| `src/{ApplicationName}.Clients` | Kiota-generated client | Client for the API |
| `tests/` | Test projects per layer | Automated tests |

## Before you expose it

The API is **anonymous**: no route requires authentication, and none declares `401`. Rate limiting, HTTPS and HSTS are
configured; authentication is not. Add an authentication module before the API is reachable outside a trusted network,
and before any write route is exposed.

## Common tasks

- Build: `dotnet build {ApplicationName}.slnx`
- Test: `dotnet test {ApplicationName}.slnx`
- Create the first migration (no migrations are shipped):
  `dotnet ef migrations add Initial --project src/{ApplicationName}.Data.<Provider> --startup-project src/{ApplicationName}.Data.<Provider>`
- Design-time connection string: set `DESIGN_TIME_CONNECTION_STRING` in the environment. The factory carries no credentials.
