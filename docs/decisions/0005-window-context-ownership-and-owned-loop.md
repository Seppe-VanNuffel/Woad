# ADR 0005: Window/context ownership and owned main loop

- **Status:** Proposed
- **Date:** 2026-11-15
- **Deciders:** Seppe

## Context

Someone has to create the OpenGL context and drive the loop. Silk.NET windows can run their own loop with update/render events, or be driven manually. A fixed timestep with clamping and pause needs control of the loop.

## Decision

- The internal platform layer (`GameWindow`) creates the window and the GL 3.3 Core context and pumps events.
- The host passes the GL instance to `GraphicsDevice`. Graphics never references Platform types.
- Woad owns the loop: poll events, advance the timer, update, draw, swap.
- Fallback if manual driving is not viable (M0-07): use Silk's `Run()` and run the accumulator inside its render callback.

## Consequences

- Full control over pacing, pause and shutdown ordering.
- We must handle resize/drag repaint behaviour ourselves.

## Alternatives considered

- Silk-owned loop with separate update/render rates: less code, weaker control over fixed-step semantics.

## Validation and revisit triggers

M0-07 (manual loop spike), M1-05, M1-06.
