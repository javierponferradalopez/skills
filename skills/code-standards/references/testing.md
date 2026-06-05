# Testing — examples and red flags

Core principle: tests verify behavior through public interfaces, not implementation
details. Code can change entirely; tests shouldn't break unless behavior changed.

> Examples below are in TypeScript for concreteness; the principles are language-agnostic.

## Good tests

Tests that exercise real code paths through public APIs. They describe *what* the system
does, not *how*.

```typescript
// GOOD: tests observable behavior through the public interface
test("createUser makes the user retrievable", async () => {
  const user = await createUser({ name: "Alice" });
  const retrieved = await getUser(user.id);
  expect(retrieved.name).toBe("Alice");
});
```

- Test behavior callers care about.
- Use the public API only.
- Survive internal refactors.
- One logical assertion per test.

## Bad tests

```typescript
// BAD: mocks an internal collaborator — tests HOW, not WHAT
test("checkout calls paymentService.process", async () => {
  const mockPayment = jest.mock(paymentService);
  await checkout(cart, payment);
  expect(mockPayment.process).toHaveBeenCalledWith(cart.total);
});

// BAD: bypasses the interface to verify via the database
test("createUser saves to the database", async () => {
  await createUser({ name: "Alice" });
  const row = await db.query("SELECT * FROM users WHERE name = ?", ["Alice"]);
  expect(row).toBeDefined();
});

// BAD: test restates the implementation — the function IS the spec
test("pitchHref includes the from param", () => {
  expect(pitchHref("abc")).toBe("/pitches/abc?from=deliverables");
});
```

## Red flags

- Mocking internal collaborators (your own classes/modules).
- Testing private methods.
- Asserting on call counts or the order of internal calls.
- A test that breaks when refactoring without a behavior change.
- A test name that describes HOW, not WHAT.
- Verifying through external means (e.g. querying a DB) instead of through the interface.
- Testing a trivial function (one-liner, simple mapping, string concatenation) where the
  test just mirrors the code — adds no confidence, breaks on any refactor.
- Thin delegation tests — when a handler's only job is to parse input and call a service
  method, testing that it "delegates correctly" by mocking the service just duplicates
  the handler. The real behavior lives in the service; test that instead.

## Mocking — system boundaries only

Mock only at **system boundaries**:

- External APIs (payment, email, etc.).
- Time and randomness.
- File system or databases when a real instance isn't practical.

**Never mock your own classes/modules or internal collaborators.** If something is hard
to test without mocking internals, redesign the interface.

## TDD: vertical slices

Do NOT write all tests first, then all the implementation — that produces tests that
verify *imagined* behavior and are insensitive to real changes.

Correct approach — one test, one implementation, repeat:

```
RED→GREEN: test1 → impl1
RED→GREEN: test2 → impl2
RED→GREEN: test3 → impl3
```

Each test responds to what you learned from the previous cycle. Never refactor while RED
— get to GREEN first.
