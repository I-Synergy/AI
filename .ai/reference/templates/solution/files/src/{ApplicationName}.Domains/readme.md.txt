# {ApplicationName}.Domains

CQRS commands and queries for the application. Each operation has its own folder under `Features/{Entities}/` holding the command or query, its handler and its response. Handlers depend on `IDataContext`, use EF Core primitives directly and return models, never entities.
