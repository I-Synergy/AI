# Terminology Glossary

## Core Concepts

| Term | Definition | Example |
|------|------------|---------|
| **Entity** | Persisted POCO: identity and state, no behaviour. Lives in `{ApplicationName}.Entities`. | `{Entity}` class with `{Entity}Id` |
| **Model** | Read model or request record shared with the API and the heads. Lives in `{ApplicationName}.Models`. Never references Entities. | `{Entity}` (a `BaseModel` read model), `Create{Entity}Request` |
| **DTO** | Generic term for data that crosses a boundary. In this template a model is the DTO, and it never takes a `Dto` suffix. | `{Entity}Response`, `Create{Entity}Request` |
| **DataContext** | The EF Core `DbContext` of one provider, in `{ApplicationName}.Data.SqlServer` or `{ApplicationName}.Data.Postgres`. Only the composition root and the tests construct it. | `DataContext : DbContext, IDataContext` |
| **IDataContext** | The data access surface that handlers depend on. Lives in `{ApplicationName}.Data/Abstractions/`. | `DbSet<Item> Items`, `SaveChangesAsync` |
| **Command** | Write operation that changes state (Create, Update, Delete) | `Create{Entity}Command` |
| **Query** | Read operation that returns data without side effects | `Get{Entity}ByIdQuery` |
| **Handler** | Class that executes a Command or Query | `Create{Entity}CommandHandler` |
| **Aggregate** | Cluster of domain objects treated as a single unit. Not scaffolded: entities are plain POCOs. | `{Entity}` with its child `{ChildEntities}` |
| **Bounded Context** | A business boundary with its own language. In the scaffold it is a feature folder, `Features/{Entities}/` in `{ApplicationName}.Domains`, not a project. | `Features/{Entities}/` |
| **Value Object** | Immutable object defined by its attributes, not identity | `Money`, `Address`, `DateRange` |
| **Domain Event** | Notification that something significant happened in the domain. Not scaffolded. | `{Entity}CreatedEvent` |
| **Repository** | Abstraction over data access. Not used in this template. | N/A. Handlers use `IDataContext` DbSet properties directly. |

## Project Type Purposes

| Project | Purpose | Required? | Example |
|---------|---------|-----------|---------|
| **Common** | Shared enumerations, constants, converters, factories | **Required** | `{Entity}Status` in `Enumerations/` |
| **Resources** | Resource strings | **Required** | `Properties/Resources.resx` |
| **Entities** | EF Core POCOs and their `IEntityTypeConfiguration` | **Required** | `{Entity}`, `{Entity}Configuration` |
| **Models** | Read models and request records | **Required** | `{Entity}`, `Create{Entity}Request` |
| **Data** | The `IDataContext` abstraction | **Required** | `IDataContext` |
| **Data.SqlServer** or **Data.Postgres** | Provider `DataContext`, design-time factory, `Initializers/` | **Required** (one of the two) | `DataContext` |
| **Data.Sqlite** | Device store for the MAUI head | Optional (`sqlite-device`) | `LocalDataContext` |
| **Domains** | CQRS commands, queries and handlers | **Required** | `Create{Entity}Command` |
| **Services** | Endpoint groups (Minimal APIs) | **Required** | `{Entities}Endpoints` |
| **Service.Api** | Host and `Program.cs` | **Required** | The OpenAPI document and the Kiota source come from here |
| **Clients** | Kiota client | **Required** | `ApiClient` |
| **App.Shared** | Services and client registration shared by the heads | Optional (any head) | `I{ApplicationName}ApiService` |
| **App** | MAUI head | Optional (`maui`) | `MauiProgram` |
| **App.Web** | Blazor head | Optional (`web`) | `Routes.razor` |
| **AppHost** | Aspire orchestration | Optional (`apphost`) | `DistributedApplication.CreateBuilder` |

**Minimum required for a solution:** Common, Resources, Entities, Models, Data, Data.{Provider}, Domains, Services, Service.Api and Clients (10 projects), plus the test projects.

## Architecture Layers

| Layer | Purpose | Example Projects |
|-------|---------|------------------|
| **Clients and heads** | Heads and the generated client | `{ApplicationName}.App.Web`, `{ApplicationName}.App`, `{ApplicationName}.App.Shared`, `{ApplicationName}.Clients` |
| **API** | Host and endpoint groups | `{ApplicationName}.Service.Api`, `{ApplicationName}.Services` |
| **Use cases** | CQRS handlers | `{ApplicationName}.Domains` |
| **Core model** | Entities, models and the data abstraction | `{ApplicationName}.Entities`, `{ApplicationName}.Models`, `{ApplicationName}.Data`, `{ApplicationName}.Common` |
| **Persistence** | Provider data context and the device store | `{ApplicationName}.Data.SqlServer`, `{ApplicationName}.Data.Sqlite` |

## CQRS Terms

| Term | Definition | When to Use |
|------|------------|-------------|
| **Command** | Request to change system state | Create, Update, Delete operations |
| **Query** | Request to read data without side effects | Get by ID, List, Search operations |
| **Handler** | Executes a Command or Query | Every Command and Query has exactly one Handler |
| **Response** | Result returned by Handler | `Create{Entity}Response`, `Get{Entity}ByIdResponse` |
| **Event** | Notification of state change | After successful Command execution. Not scaffolded. |

## Clean Architecture Terms

| Term | Definition | Rule |
|------|------------|------|
| **Dependency Inversion** | Dependencies point towards the core (`Common`, `Entities`, `Models`) and the abstraction | Handlers depend on `IDataContext`, never on the concrete `DataContext` |
| **Separation of Concerns** | Each project has one responsibility | Endpoints do not query the database; handlers do not know HTTP |
| **Vertical Slice** | Feature organised by business capability, not technical layer | All `{Entity}` code in `Features/{Entities}/` of `{ApplicationName}.Domains` |

## Common Acronyms

| Acronym | Full Term | Usage |
|---------|-----------|-------|
| **DDD** | Domain-Driven Design | Architecture philosophy (not applied by the scaffold) |
| **CQRS** | Command Query Responsibility Segregation | Pattern for separating reads/writes |
| **MVVM** | Model-View-ViewModel | UI pattern for MAUI |
| **DI** | Dependency Injection | Constructor injection pattern |
| **DTO** | Data Transfer Object | Object for moving data between layers |
| **EF Core** | Entity Framework Core | ORM for .NET |
| **ORM** | Object-Relational Mapping | Database abstraction |
| **Kiota** | Microsoft's OpenAPI client generator | Generates `{ApplicationName}.Clients/Api/` from the API document |
| **OTLP** | OpenTelemetry Protocol | Telemetry exporter used in Development |
| **SOLID** | Single responsibility, Open/closed, Liskov substitution, Interface segregation, Dependency inversion | Design principles |
