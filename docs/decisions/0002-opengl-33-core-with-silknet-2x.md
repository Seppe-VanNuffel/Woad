# ADR 0002: OpenGL 3.3 Core via Silk.NET 2.x, kept internal

- **Status:** Accepted
- **Date:** 2026-11-15
- **Deciders:** Seppe

## Context

The goal is to learn the modern programmable pipeline. The newest stable Silk.NET found is 2.23.0 (January 2026); the 3.0 rewrite is still in preview. Silk.NET 2.x windowing is GLFW-based. The 3.0 rewrite changes windowing and bindings, so a future migration is plausible.

## Decision

- Use OpenGL 3.3 Core (forward-compatible context hint set) through Silk.NET 2.x (`Windowing`, `Input`, `OpenGL`, `OpenAL`).
- All Silk.NET types are `internal`. Woad defines its own `Key` and `MouseButton` enums and uses `System.Numerics` for maths in the public API.
- No legacy/fixed-function GL.

## Consequences

- Wrapper code costs some effort but confines a Silk.NET 3.0 migration to internal code.
- No GL 4.x features (compute, direct state access) without a new ADR.

## Alternatives considered

- Silk.NET 3.0 preview: not production-ready; rejected for now.
- OpenTK or SDL3 bindings directly: no reason to switch without a Silk.NET failure.
- Exposing Silk.NET types publicly: cheaper now, expensive at any migration.

## Validation and revisit triggers

M0-04 (window and GL 3.3 on net11, Windows), M0-05 (Linux headless), M1-10 (public API contains no Silk types). Revisit when Silk.NET 3.0 reaches stable or 2.x stops being maintained.
