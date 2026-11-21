# {ApplicationName}.AppHost

.NET Aspire orchestration host. It starts the database, the API and, when selected, the web and MAUI heads, and wires their references and health checks.

Before the first run, set the database password once per machine. It is stored in the user secrets store and is never committed:

```
aspire secret set Parameters:{applicationname}-database-password <password>
```

Run with `aspire run` from the repository root, or `dotnet run --project src/{ApplicationName}.AppHost`. The dashboard is at the address the console prints.
