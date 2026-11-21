# {ApplicationName}.Data.{Provider}.Tests

Tests for the {Provider} persistence layer. `DataContextModelTests` build the model through the design-time
factory without opening a connection: they pin the entity configuration, the provider and the migrations
history table in the `system` schema.
{{#if postgres}}

`Postgres{Entity}PersistenceTests` run against a real `postgres:18` container started by Testcontainers and are
tagged `[TestCategory("Postgres")]`. They skip loudly (Inconclusive) when no container runtime answers, or when
`POSTGRES_TESTS_SKIP` is set. Exclude them with `dotnet test --filter "TestCategory!=Postgres"`.
{{/if}}
