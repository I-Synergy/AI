# Terminology Glossary

## Core Concepts

| Term | Definition | Example |
|------|------------|---------|
| **Entity** | Domain object with business logic, identity, and behavior. Lives in Domain layer. | `{Entity}` class with validation rules |
| **Model** | Data Transfer Object (DTO) for persistence/API. No business logic. Lives in Models or Entities projects. | `{Entity}Model` for database mapping |
| **DTO** | Data Transfer Object - POCO for moving data between layers | `{Entity}Response`, `Create{Entity}Request` |
| **DataContext** | Your EF Core `DbContext` subclass. The gateway to your database. | `public class DataContext : DbContext` |
| **Command** | Write operation that changes state (Create, Update, Delete) | `Create{Entity}Command` |
| **Query** | Read operation that returns data without side effects | `Get{Entity}ByIdQuery` |
| **Handler** | Class that executes a Command or Query | `Create{Entity}CommandHandler` |
| **Aggregate** | Cluster of domain objects treated as a single unit | `{Entity}` with its child `{ChildEntities}` |
| **Bounded Context** | Domain boundary with its own models and language | `{Entities}`, `{ChildEntities}`, `Authentication` |
| **Value Object** | Immutable object defined by its attributes, not identity | `Money`, `Address`, `DateRange` |
| **Domain Event** | Notification that something significant happened in the domain | `{Entity}CreatedEvent` |
| **Repository** | Abstraction over data access (NOTE: We don't use explicit repositories in this template) | N/A - Inject `DataContext` and use EF Core primitives on DbSet properties directly |

## Project Type Purposes

| Project Type | Purpose | Required? | Example |
|--------------|---------|-----------|---------|
| **Contracts.{Domain}** | Interfaces and service contracts | Optional | `I{Entity}Service` |
| **Entities.{Domain}** | EF Core entity classes (database mapping) | **Required** | `{Entity}` entity with EF attributes |
| **Models.{Domain}** | DTOs for API requests/responses | **Required** | `{Entity}Model`, `{Entity}Response` |
| **Domain.{Domain}** | CQRS Commands/Queries/Handlers | **Required** | `Create{Entity}Command` |
| **Services.{Domain}** | API Endpoints (Minimal APIs) | **Required** | `{Entity}Endpoints.cs` |
| **ViewModels.{Domain}** | MVVM ViewModels for UI | Optional (UI only) | `{Entity}ViewModel` |

**Minimum required for a domain:** Entities, Models, Domain, Services (4 projects)

## Architecture Layers

| Layer | Purpose | Example Projects |
|-------|---------|------------------|
| **Presentation** | User interface (Blazor, MAUI, etc.) | `{ApplicationName}.UI.Web`, `{ApplicationName}.App.Mobile` |
| **Application** | API endpoints, orchestration | `{ApplicationName}.Services.{Domain}` |
| **Domain** | Business logic, CQRS handlers | `{ApplicationName}.Domain.{Domain}` |
| **Infrastructure** | Data access, external integrations | `{ApplicationName}.Data`, `{ApplicationName}.Entities.{Domain}` |

## CQRS Terms

| Term | Definition | When to Use |
|------|------------|-------------|
| **Command** | Request to change system state | Create, Update, Delete operations |
| **Query** | Request to read data without side effects | Get by ID, List, Search operations |
| **Handler** | Executes a Command or Query | Every Command and Query has exactly one Handler |
| **Response** | Result returned by Handler | `Create{Entity}Response`, `{Entity}Response` |
| **Event** | Notification of state change | After successful Command execution |

## Clean Architecture Terms

| Term | Definition | Rule |
|------|------------|------|
| **Dependency Inversion** | Outer layers depend on inner layers, not vice versa | Domain has no dependencies on Infrastructure |
| **Separation of Concerns** | Each layer has distinct responsibilities | Don't mix API concerns with business logic |
| **Vertical Slice** | Feature organized by business capability, not technical layer | All {Entity}-related code in {Entity} feature folder |

## Common Acronyms

| Acronym | Full Term | Usage |
|---------|-----------|-------|
| **DDD** | Domain-Driven Design | Architecture philosophy |
| **CQRS** | Command Query Responsibility Segregation | Pattern for separating reads/writes |
| **MVVM** | Model-View-ViewModel | UI pattern for Blazor/MAUI |
| **DI** | Dependency Injection | Constructor injection pattern |
| **DTO** | Data Transfer Object | Object for moving data between layers |
| **EF Core** | Entity Framework Core | ORM for .NET |
| **ORM** | Object-Relational Mapping | Database abstraction |
| **SOLID** | Single responsibility, Open/closed, Liskov substitution, Interface segregation, Dependency inversion | Design principles |
