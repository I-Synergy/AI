# {ApplicationName}.Data.Sqlite

Device-local store on SQLite for the heads that keep data on the device (`sqlite-device` flag).

- `LocalDataContext` holds the device tables. `Favorite` is a generic sample entity; its configuration is in `Entities/FavoriteConfiguration.cs`.
- The schema is created with `EnsureCreated`. No migrations ship with the store, so an app that changes the schema must recreate the file or add its own upgrade step.
- `Services/SqliteLocalDataService` implements `ISqliteLocalDataService` from `{ApplicationName}.App.Shared`. Every operation takes a `CancellationToken` and uses the DbSet primitives directly. A gate serializes access, because SQLite allows one writer at a time.
- `Extensions/ServiceCollectionExtensions.AddLocalSqliteStore(path)` registers the context factory and the service. The head calls `EnsureCreatedAsync` once at startup.
