# EF Core Migration Commands & Entity Configuration

The `dotnet ef` command set for this solution's layout, and the Fluent API entity-configuration pattern. Load this when creating/applying/rolling back a migration or configuring an entity.

## Migration Commands

### Create Migration
```bash
# From solution root
dotnet ef migrations add {MigrationName} --project src/{ApplicationName}.Data.{Provider} --startup-project src/{ApplicationName}.Service.Api

# Example
dotnet ef migrations add Add{Entity}Table --project src/{ApplicationName}.Data.{Provider} --startup-project src/{ApplicationName}.Service.Api
```

### Apply Migration
```bash
# Update database to latest migration
dotnet ef database update --project src/{ApplicationName}.Data.{Provider} --startup-project src/{ApplicationName}.Service.Api

# Update to specific migration
dotnet ef database update {MigrationName} --project src/{ApplicationName}.Data.{Provider} --startup-project src/{ApplicationName}.Service.Api
```

### Rollback Migration
```bash
# Rollback to previous migration
dotnet ef database update {PreviousMigrationName} --project src/{ApplicationName}.Data.{Provider} --startup-project src/{ApplicationName}.Service.Api

# Rollback all migrations
dotnet ef database update 0 --project src/{ApplicationName}.Data.{Provider} --startup-project src/{ApplicationName}.Service.Api
```

### Remove Migration
```bash
# Remove last migration (if not applied)
dotnet ef migrations remove --project src/{ApplicationName}.Data.{Provider} --startup-project src/{ApplicationName}.Service.Api
```

### Generate SQL Script
```bash
# Generate SQL for review
dotnet ef migrations script --project src/{ApplicationName}.Data.{Provider} --startup-project src/{ApplicationName}.Service.Api --output migration.sql

# Generate SQL from specific migration
dotnet ef migrations script {FromMigration} {ToMigration} --project src/{ApplicationName}.Data.{Provider} --startup-project src/{ApplicationName}.Service.Api
```

## First Migration (the generated solution)

The generated solution ships no migrations. Create the first one against the provider project, with the API as the startup project so the API's configuration and its design-time context are used:

```bash
dotnet ef migrations add Initial --project src/{ApplicationName}.Data.{Provider} --startup-project src/{ApplicationName}.Service.Api
```

`{Provider}` is `SqlServer` or `Postgres`, the value the generator wrote. The migration files land in the provider project (`Migrations/`), not in the API.

### Design-time factory

`dotnet ef` builds the context through the design-time factory in the provider project, not through the API host. The SQL Server factory is `DataContextFactory : IDesignTimeDbContextFactory<DataContext>`:

- It reads the connection string from `DESIGN_TIME_CONNECTION_STRING`. When the variable is missing it uses a well-formed default that names a local server. Migrations are generated without opening a connection, so the default never needs to answer.
- It carries no credentials. Set `DESIGN_TIME_CONNECTION_STRING` only when you apply migrations to a real server from a developer machine, and keep the value out of source control.
- It configures the same migrations history table as the runtime context (below), so the design-time and runtime paths agree.

### System schema for the migrations history

The history table lives in a `system` schema, apart from the application schema, so an application schema can be dropped or reset without losing migration history. The table name and schema are set in two places, which must match:

```csharp
// Provider DataContext: the conventions hold however the context is created (DI, factory, or new).
public void Configure(IServiceProvider serviceProvider, DbContextOptionsBuilder optionsBuilder)
    => optionsBuilder.UseSqlServer(sqlServer => sqlServer.MigrationsHistoryTable("__EFMigrationsHistory", DatabaseConstants.SystemSchema));
```

The factory calls the same `MigrationsHistoryTable("__EFMigrationsHistory", DatabaseConstants.SystemSchema)`. `DatabaseConstants.SystemSchema` is `"system"`, in `{ApplicationName}.Common/Constants/`. The application schema is set once in `OnModelCreating` with `modelBuilder.HasDefaultSchema("{applicationname}")`.

### Startup

`DatabaseInitializer.InitializeAsync` in the provider project applies pending migrations at startup, through the context's execution strategy so a transient failure while the server starts is retried. The API calls it after the endpoints are mapped and skips it while the OpenAPI document is generated. A non-relational test store (InMemory) has no migrations, so the initializer returns before it touches relational members.

Apply in production through your release pipeline, not only at startup, when the change is destructive. See `.ai/skills/database-migration/SKILL.md` for the review gate.

## Entity Configuration Pattern

Each entity has its own configuration class, in its own file, next to the entity in `{ApplicationName}.Entities`. The provider `DataContext` applies every configuration in the assembly with `ApplyConfigurationsFromAssembly`, so a new entity needs no change to the context beyond its `DbSet`.

```csharp
// File: {ApplicationName}.Entities/{Entity}Configuration.cs
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace {ApplicationName}.Entities;

/// <summary>
/// Fluent EF Core mapping for <see cref="{Entity}"/>. Applied by <c>ApplyConfigurationsFromAssembly</c> in the DataContext.
/// </summary>
public sealed class {Entity}Configuration : IEntityTypeConfiguration<{Entity}>
{
    /// <inheritdoc />
    public void Configure(EntityTypeBuilder<{Entity}> builder)
    {
        builder.ToTable("{entities}");
        builder.HasKey(e => e.{Entity}Id);
        builder.Property(e => e.{Entity}Id).ValueGeneratedNever();
        builder.Property(e => e.Name).IsRequired().HasMaxLength(100);
        builder.Property(e => e.Description).HasMaxLength(500);
        builder.Property(e => e.Status).IsRequired();
        builder.Property(e => e.CreatedAt).IsRequired();
        builder.HasIndex(e => e.Name);
    }
}
```

Rules:

- **One configuration per file.** Name it `{Entity}Configuration`, and keep it in the entities project, the same project as the entity.
- **Keys are set explicitly.** `HasKey` names the key, and `ValueGeneratedNever()` is set when the application assigns the identifier (`Guid.NewGuid()` in the handler).
- **Enum properties are enum types.** EF Core stores them as integers, so the enum's pinned values are the stored values. Never renumber them (see `.ai/reference/critical-rules.md`, rule 24).
- **Relationships go in the configuration of the dependent entity.** Use `HasOne`/`HasMany` with an explicit `OnDelete`. Cascade delete is a decision, not a default.
- **Indexes and lengths are declared here**, so the model tests in `{ApplicationName}.Data.{Provider}.Tests` can check them.
- **Table names** use the plural, lower-case form (`items`). The Postgres provider uses snake_case table and column names if the team's convention requires it; set it in the configuration, not in the entity.
