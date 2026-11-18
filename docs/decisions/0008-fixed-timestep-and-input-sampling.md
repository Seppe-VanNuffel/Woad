# ADR 0008: Fixed timestep and input sampling

- **Status:** Proposed
- **Date:** 2026-11-15
- **Deciders:** Seppe

## Context

Simulation should be deterministic and independent of render rate. Input edges ("pressed this update") are easy to miss or double-count when update and render rates differ.

## Decision

**Timing**
- Default 60 updates per second, configurable.
- Accumulator in integer stopwatch ticks (no floating-point drift).
- Clamp frame delta to 250 ms and run at most 5 steps per frame; excess time is dropped and logged at debug level.
- Pause stops ticking but keeps rendering. A focus-loss pause option is deferred.
- `Draw` receives `alpha` (0..1). The engine does not interpolate automatically.
- When vsync is off and a frame cap is set, wait with sleep for most of the interval and spin only for the final millisecond.

**Input**
- Window events are buffered. `BeginTick()` runs before each `Update` step and publishes the state.
- Pressed/released edges are true for exactly one `Update`, even if a key tap was shorter than a frame or a frame ran zero or two steps.
- Held state persists. Mouse wheel delta accumulates per tick. Mouse position is sampled per frame for drawing.

## Consequences

- Predictable gameplay logic and straightforward unit tests.
- At refresh rates above 60 Hz, movement can look steppy until the game uses `alpha`.

## Alternatives considered

- Variable timestep: simpler, non-deterministic, harder collision behaviour.
- Per-frame input edges: wrong when Update runs 0 or 2 times per frame.

## Validation and revisit triggers

M1-01/M1-08 (timestep and limiter tests), M4 (input tests). Revisit if the demo shows visible stutter even with interpolation available.
