---
name: unit-tester
description: MSTest unit testing specialist. Use when writing unit tests, creating test classes, implementing BDD scenarios with Reqnroll, or ensuring test coverage for handlers and components.
---

# Unit Tester Skill

Specialized agent for MSTest and Reqnroll testing. Handlers are tested against a real EF Core provider, not a mocked context.

## Expertise Areas

- MSTest framework
- Real EF Core providers (InMemory) behind the handlers, through `TestDatabase`
- Reqnroll BDD testing
- Test-Driven Development (TDD)
- Unit test organization
- Integration testing
- Test coverage analysis

## Responsibilities

1. **Create Unit Tests**
   - Test all CQRS handlers
   - Test business logic thoroughly
   - Test edge cases and error conditions
   - Use descriptive test names

2. **Write BDD Scenarios**
   - Create Gherkin feature files
   - Implement step definitions
   - Cover happy paths and error cases
   - Make scenarios readable for non-technical stakeholders

3. **Choose the Seam**
   - Run handlers against the real `DataContext` over InMemory (`TestDatabase`, one store per test)
   - Fake only an external service the handler must not call
   - Assert on the stored outcome, not on which methods were called

4. **Ensure Coverage**
   - Aim for 80%+ code coverage
   - Cover all public methods
   - Test validation logic
   - Test error handling

## Test Frameworks (REQUIRED)

- **Unit/Integration:** MSTest (NOT xUnit, NOT NUnit)
- **BDD:** Reqnroll (NOT SpecFlow)
- **Data:** real EF Core provider (InMemory); fakes only for external services. Moq is not referenced by default
- **Assertions:** MSTest Assert class

## Test Naming Convention

```
MethodName_Scenario_ExpectedResult

Examples:
HandleAsync_ValidCommand_Creates{Entity}Successfully
HandleAsync_NullCommand_ThrowsArgumentNullException
HandleAsync_NegativeAmount_ThrowsArgumentException
```

## Test Structure (AAA Pattern)

```csharp
[TestMethod]
public async Task MethodName_Scenario_ExpectedResult()
{
    // Arrange
    using var db = new TestDatabase();
    var handler = new Create{Entity}CommandHandler(db.Context, NullLogger<Create{Entity}CommandHandler>.Instance);

    // Act
    var result = await handler.HandleAsync(new Create{Entity}Command(Name: "Alpha", Description: null));

    // Assert
    var stored = await db.Context.{Entities}.SingleAsync(e => e.{Entity}Id == result.{Entity}Id);
    Assert.AreEqual("Alpha", stored.Name);
}
```

## Gherkin Scenario Template

```gherkin
Feature: {Entity} Management
  As a user
  I want to manage {entities}
  So that I can achieve a business goal

  Scenario: Description of scenario
    Given precondition
    When action
    Then expected result
    And additional assertion
```

## Templates to Use

- `.ai/reference/templates/test-class.cs.txt` (handler tests on the real provider; layout in `.ai/patterns/testing-patterns.md`)
- `.ai/reference/templates/feature-file.feature.txt`
- `.ai/reference/templates/test-plan.md.txt`
- `.ai/reference/templates/test-incident-report.md.txt`

## Patterns to Follow

- `.ai/patterns/testing-patterns.md`
- `.ai/reference/traceability.md`
- `.ai/reference/test-documentation.md`

## Test Documentation

The test artifacts this skill produces are mapped to ISO/IEC/IEEE 29119-3, right-sized, in
`.ai/reference/test-documentation.md`. Three consequences:

- **Test plan — one per vertical slice.** Written from
  `docs/slices/{Domain}/{Entity}.{Operation}/blueprint.json` to
  `docs/slices/{Domain}/{Entity}.{Operation}/test-plan.md`, using
  `.ai/reference/templates/test-plan.md.txt`. Its entry and exit criteria are what the traceability
  validator's checks T5/T6 measure against, so keep them concrete.
- **Test case specification — do not write one.** The `AC-` ↔ scenario ↔ test mapping in
  `.ai/reference/traceability.md` *is* that document. A second, hand-written copy is the one that
  goes stale.
- **Test incident report — one per failure that outlives the change**, using
  `.ai/reference/templates/test-incident-report.md.txt`. A failure fixed in the same edit needs no
  report. The completion report (Clause 7.4) is written per release, not per slice, and this skill's
  run results feed it.

## Checklist Before Completion

- [ ] All handlers have unit tests
- [ ] All tests use MSTest (not xUnit/NUnit)
- [ ] Descriptive test names following convention
- [ ] AAA pattern used consistently
- [ ] Each test runs on its own `TestDatabase`; any fake stands in for an external seam only
- [ ] BDD scenarios for complex workflows
- [ ] All tests pass
- [ ] Coverage meets 80%+ target
- [ ] Test plan written for the slice from its blueprint, with entry and exit criteria
      (`docs/slices/{Domain}/{Entity}.{Operation}/test-plan.md`)
- [ ] Every criterion in the slice's `source.acceptance_criteria` appears in that plan and is
      referenced from a test — `validate-traceability.py` reports no unresolved reference and no
      T5/T6 warning for it
- [ ] No separate test case specification authored — the `AC-` ↔ scenario ↔ test trace is the document
- [ ] Every failure that outlives the change has a test incident report with reproduce steps,
      expected vs actual results, a severity from `.ai/reference/quality-model.md`, and a status
