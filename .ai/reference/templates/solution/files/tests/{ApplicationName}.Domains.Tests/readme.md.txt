# {ApplicationName}.Domains.Tests

Unit tests for the CQRS handlers in `{ApplicationName}.Domains`. Each handler runs against a real
`DataContext` on the EF Core in-memory provider (`Infrastructure/TestDatabase.cs`) with `NullLogger`; nothing
is mocked. Run with `dotnet test tests/{ApplicationName}.Domains.Tests`.
