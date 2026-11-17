---
name: architecture-blueprint-generator
description: "Comprehensive project architecture blueprint generator that analyzes codebases to create detailed architectural documentation. Automatically detects technology stacks and architectural patterns, generates visual diagrams, documents implementation patterns, and provides extensible blueprints for maintaining architectural consistency and guiding new development. Use when documenting an existing project's architecture, patterns and diagrams, or when creating an architecture blueprint."
disable-model-invocation: true
---

# Comprehensive Project Architecture Blueprint Generator

## Configuration Variables

Use these settings unless the user specifies otherwise. Options are listed after the setting name; the default is in brackets.

- PROJECT_TYPE: Auto-detect, .NET, Java, React, Angular, Python, Node.js, Flutter or Other [Auto-detect]. Primary technology.
- ARCHITECTURE_PATTERN: Auto-detect, Clean Architecture, Microservices, Layered, MVVM, MVC, Hexagonal, Event-Driven, Serverless, Monolithic or Other [Auto-detect]. Primary architectural pattern.
- DIAGRAM_TYPE: C4, UML, Flow, Component or None [C4]. Architecture diagram type.
- DETAIL_LEVEL: High-level, Detailed, Comprehensive or Implementation-Ready [Detailed]. Level of detail to include.
- INCLUDES_CODE_EXAMPLES: true or false [true]. Include sample code that illustrates patterns.
- INCLUDES_IMPLEMENTATION_PATTERNS: true or false [true]. Include detailed implementation patterns.
- INCLUDES_DECISION_RECORDS: true or false [true]. Include architectural decision records.
- FOCUS_ON_EXTENSIBILITY: true or false [true]. Emphasize extension points and patterns.

## Generated Prompt

"Create a comprehensive 'Project_Architecture_Blueprint.md' document that thoroughly analyzes the architectural patterns in the codebase to serve as a definitive reference for maintaining architectural consistency. Use the following approach:

### 1. Architecture Detection and Analysis
- If PROJECT_TYPE is Auto-detect, analyze the project structure to identify all technology stacks and frameworks in use by examining:
  - Project and configuration files
  - Package dependencies and import statements
  - Framework-specific patterns and conventions
  - Build and deployment configurations
  Otherwise, focus on the specific patterns and practices of the chosen PROJECT_TYPE.

- If ARCHITECTURE_PATTERN is Auto-detect, determine the architectural pattern(s) by analyzing:
  - Folder organization and namespacing
  - Dependency flow and component boundaries
  - Interface segregation and abstraction patterns
  - Communication mechanisms between components
  Otherwise, document how the chosen ARCHITECTURE_PATTERN is implemented.

### 2. Architectural Overview
- Provide a clear, concise explanation of the overall architectural approach
- Document the guiding principles evident in the architectural choices
- Identify architectural boundaries and how they're enforced
- Note any hybrid architectural patterns or adaptations of standard patterns

### 3. Architecture Visualization
If DIAGRAM_TYPE is not None, create diagrams of that type at multiple levels of abstraction:
- High-level architectural overview showing major subsystems
- Component interaction diagrams showing relationships and dependencies
- Data flow diagrams showing how information moves through the system
- Ensure diagrams accurately reflect the actual implementation, not theoretical patterns

If DIAGRAM_TYPE is None, describe the component relationships based on actual code dependencies, providing clear textual explanations of:
- Subsystem organization and boundaries
- Dependency directions and component interactions
- Data flow and process sequences

### 4. Core Architectural Components
For each architectural component discovered in the codebase:

- **Purpose and Responsibility**:
  - Primary function within the architecture
  - Business domains or technical concerns addressed
  - Boundaries and scope limitations

- **Internal Structure**:
  - Organization of classes/modules within the component
  - Key abstractions and their implementations
  - Design patterns utilized

- **Interaction Patterns**:
  - How the component communicates with others
  - Interfaces exposed and consumed
  - Dependency injection patterns
  - Event publishing/subscription mechanisms

- **Evolution Patterns**:
  - How the component can be extended
  - Variation points and plugin mechanisms
  - Configuration and customization approaches

### 5. Architectural Layers and Dependencies
- Map the layer structure as implemented in the codebase
- Document the dependency rules between layers
- Identify abstraction mechanisms that enable layer separation
- Note any circular dependencies or layer violations
- Document dependency injection patterns used to maintain separation

### 6. Data Architecture
- Document domain model structure and organization
- Map entity relationships and aggregation patterns
- Identify data access patterns (repositories, data mappers, etc.)
- Document data transformation and mapping approaches
- Note caching strategies and implementations
- Document data validation patterns

### 7. Cross-Cutting Concerns Implementation
Document implementation patterns for cross-cutting concerns:

- **Authentication & Authorization**:
  - Security model implementation
  - Permission enforcement patterns
  - Identity management approach
  - Security boundary patterns

- **Error Handling & Resilience**:
  - Exception handling patterns
  - Retry and circuit breaker implementations
  - Fallback and graceful degradation strategies
  - Error reporting and monitoring approaches

- **Logging & Monitoring**:
  - Instrumentation patterns
  - Observability implementation
  - Diagnostic information flow
  - Performance monitoring approach

- **Validation**:
  - Input validation strategies
  - Business rule validation implementation
  - Validation responsibility distribution
  - Error reporting patterns

- **Configuration Management**:
  - Configuration source patterns
  - Environment-specific configuration strategies
  - Secret management approach
  - Feature flag implementation

### 8. Service Communication Patterns
- Document service boundary definitions
- Identify communication protocols and formats
- Map synchronous vs. asynchronous communication patterns
- Document API versioning strategies
- Identify service discovery mechanisms
- Note resilience patterns in service communication

### 9. Technology-Specific Architectural Patterns
If PROJECT_TYPE is Auto-detect, document specific architectural patterns for each detected technology stack. Otherwise, document the PROJECT_TYPE-specific architectural patterns.

Include the section for each relevant stack:

#### .NET Architectural Patterns (if detected)
- Host and application model implementation
- Middleware pipeline organization
- Framework service integration patterns
- ORM and data access approaches
- API implementation patterns (controllers, minimal APIs, etc.)
- Dependency injection container configuration

#### Java Architectural Patterns (if detected)
- Application container and bootstrap process
- Dependency injection framework usage (Spring, CDI, etc.)
- AOP implementation patterns
- Transaction boundary management
- ORM configuration and usage patterns
- Service implementation patterns

#### React Architectural Patterns (if detected)
- Component composition and reuse strategies
- State management architecture
- Side effect handling patterns
- Routing and navigation approach
- Data fetching and caching patterns
- Rendering optimization strategies

#### Angular Architectural Patterns (if detected)
- Module organization strategy
- Component hierarchy design
- Service and dependency injection patterns
- State management approach
- Reactive programming patterns
- Route guard implementation

#### Python Architectural Patterns (if detected)
- Module organization approach
- Dependency management strategy
- OOP vs. functional implementation patterns
- Framework integration patterns
- Asynchronous programming approach

### 10. Implementation Patterns
If INCLUDES_IMPLEMENTATION_PATTERNS is true, document concrete implementation patterns for key architectural components:

- **Interface Design Patterns**:
  - Interface segregation approaches
  - Abstraction level decisions
  - Generic vs. specific interface patterns
  - Default implementation patterns

- **Service Implementation Patterns**:
  - Service lifetime management
  - Service composition patterns
  - Operation implementation templates
  - Error handling within services

- **Repository Implementation Patterns**:
  - Query pattern implementations
  - Transaction management
  - Concurrency handling
  - Bulk operation patterns

- **Controller/API Implementation Patterns**:
  - Request handling patterns
  - Response formatting approaches
  - Parameter validation
  - API versioning implementation

- **Domain Model Implementation**:
  - Entity implementation patterns
  - Value object patterns
  - Domain event implementation
  - Business rule enforcement

If it is false, mention that detailed implementation patterns vary across the codebase.

### 11. Testing Architecture
- Document testing strategies aligned with the architecture
- Identify test boundary patterns (unit, integration, system)
- Map test doubles and mocking approaches
- Document test data strategies
- Note testing tools and frameworks integration

### 12. Deployment Architecture
- Document deployment topology derived from configuration
- Identify environment-specific architectural adaptations
- Map runtime dependency resolution patterns
- Document configuration management across environments
- Identify containerization and orchestration approaches
- Note cloud service integration patterns

### 13. Extension and Evolution Patterns
If FOCUS_ON_EXTENSIBILITY is true, provide detailed guidance for extending the architecture:

- **Feature Addition Patterns**:
  - How to add new features while preserving architectural integrity
  - Where to place new components by type
  - Dependency introduction guidelines
  - Configuration extension patterns

- **Modification Patterns**:
  - How to safely modify existing components
  - Strategies for maintaining backward compatibility
  - Deprecation patterns
  - Migration approaches

- **Integration Patterns**:
  - How to integrate new external systems
  - Adapter implementation patterns
  - Anti-corruption layer patterns
  - Service facade implementation

If it is false, document the key extension points in the architecture.

If INCLUDES_CODE_EXAMPLES is true, add the section "Architectural Pattern Examples":

### 14. Architectural Pattern Examples
Extract representative code examples that illustrate key architectural patterns:

- **Layer Separation Examples**:
  - Interface definition and implementation separation
  - Cross-layer communication patterns
  - Dependency injection examples

- **Component Communication Examples**:
  - Service invocation patterns
  - Event publication and handling
  - Message passing implementation

- **Extension Point Examples**:
  - Plugin registration and discovery
  - Extension interface implementations
  - Configuration-driven extension patterns

Include enough context with each example to show the pattern clearly, but keep examples concise and focused on architectural concepts.

If INCLUDES_DECISION_RECORDS is true, add the section "Architectural Decision Records":

### 15. Architectural Decision Records
Document key architectural decisions evident in the codebase:

- **Architectural Style Decisions**:
  - Why the current architectural pattern was chosen
  - Alternatives considered (based on code evolution)
  - Constraints that influenced the decision

- **Technology Selection Decisions**:
  - Key technology choices and their architectural impact
  - Framework selection rationales
  - Custom vs. off-the-shelf component decisions

- **Implementation Approach Decisions**:
  - Specific implementation patterns chosen
  - Standard pattern adaptations
  - Performance vs. maintainability tradeoffs

For each decision, note:
- Context that made the decision necessary
- Factors considered in making the decision
- Resulting consequences (positive and negative)
- Future flexibility or limitations introduced

Number the remaining sections in order, skipping any section whose setting is turned off. The next section is "Architecture Governance".

### Architecture Governance
- Document how architectural consistency is maintained
- Identify automated checks for architectural compliance
- Note architectural review processes evident in the codebase
- Document architectural documentation practices

### Blueprint for New Development
Create a clear architectural guide for implementing new features:

- **Development Workflow**:
  - Starting points for different feature types
  - Component creation sequence
  - Integration steps with existing architecture
  - Testing approach by architectural layer

- **Implementation Templates**:
  - Base class/interface templates for key architectural components
  - Standard file organization for new components
  - Dependency declaration patterns
  - Documentation requirements

- **Common Pitfalls**:
  - Architecture violations to avoid
  - Common architectural mistakes
  - Performance considerations
  - Testing blind spots

Include information about when this blueprint was generated and recommendations for keeping it updated as the architecture evolves."
