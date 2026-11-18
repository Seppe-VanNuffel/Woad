# ADR 0003: Assembly layout, dependency rules, no DI container

- **Status:** Proposed
- **Date:** 2026-11-15
- **Deciders:** Seppe

## Context

The brief proposes six engine assemblies plus a facade. For one developer that is a lot of project plumbing, and it has contradictions: Content cannot be a peer of Graphics and Audio if `LoadTexture` returns a `Texture2D`, and the main loop cannot live in Core if it pumps window events.

## Decision

Two assemblies:

- `Woad.Core`: pure managed code with no native or Silk.NET dependency (maths, collision, timing, configuration records, asset path/cache logic).
- `Woad`: the engine (host, platform, input, graphics, audio, content loaders, diagnostics). Only this assembly references Silk.NET.

Rules (enforced by tests, M1-10): Core references nothing of Woad; Graphics does not reference Platform; no public Silk.NET types; no static mutable state or service locator.

No DI container. Services are passed by constructor, and games reach them through `GameContext`. Only `ILogger` from `Microsoft.Extensions.Logging.Abstractions` is used. Interfaces exist only at real seams (clock, window, file source, logger); other types are sealed concrete classes.

## Consequences

- Less project plumbing, one NuGet package plus Core at 1.0.
- Subsystem boundaries inside `Woad` rely on namespace rules and tests rather than assembly boundaries.
- Split `Woad.Audio` out later if native packaging makes audio optional.

## Alternatives considered

- Six assemblies as in the brief: stronger compile-time boundaries, much more overhead.
- One assembly: loses the guarantee that testable logic is free of native code.

## Validation and revisit triggers

M1-10 architecture tests. Revisit if a second consumer needs a subsystem without the rest, or if namespace rules get violated repeatedly.
