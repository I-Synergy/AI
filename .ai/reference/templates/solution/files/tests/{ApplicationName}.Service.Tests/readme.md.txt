# {ApplicationName}.Service.Tests

Integration tests for `{ApplicationName}.Service.Api`. `CustomWebApplicationFactory` boots the real host in
process and replaces the database with the EF Core in-memory provider, so no server is needed. Each test
creates its own factory and therefore its own store. Run with
`dotnet test tests/{ApplicationName}.Service.Tests`.
