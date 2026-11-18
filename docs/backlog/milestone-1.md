# Milestone 1: Foundation (epic E02)

**Goal:** a window, a fixed-timestep loop, logging and clean shutdown, consumed through the public API by Sandbox.
**Budget:** about 4 weeks, roughly 47 hours (tight; if behind, cut M1-09 first, then M1-08 to a minimal version).
**Exit criteria:** Sandbox runs on Windows with FPS in the title; `scripts/validate-linux.sh` passes on the Raspberry Pi and in CI; zero warnings; architecture tests green.

Dependency order: M1-01, M1-02, M1-03, M1-04 (independent) -> M1-05 -> M1-06 -> (M1-07, M1-08, M1-09, M1-10, M1-11) -> M1-12 -> M1-13.
All M1 issues are blocked by M0-08 (reviewed ADRs).

---

## M1-01 FixedTimestep accumulator (Woad.Core)
- **Type:** feature (technical task) | **Labels:** `feature`, `testing`, `area:core` | **Priority:** P0 | **Size:** M (4 h) | **Epic:** E02
- **Depends on:** M0-08
- **Description:** A pure type that turns elapsed real time into a number of fixed steps plus an interpolation alpha. Configurable tick rate, maximum frame delta and maximum steps per frame ([ADR 0008](../decisions/0008-fixed-timestep-and-input-sampling.md)).
- **Acceptance criteria:**
  - [ ] Given 60 Hz, when exactly one tick of time has elapsed, then 1 step is returned and alpha is approximately 0.
  - [ ] Given 60 Hz, when half a tick elapses, then 0 steps and alpha is approximately 0.5; when another half tick elapses, then 1 step.
  - [ ] Given a frame delta of 2 s with a 250 ms clamp and 5 max steps, then at most 5 steps are returned, the excess is dropped, and a "clamped" indicator is set (no spiral of death).
  - [ ] Given the timer is paused, when time passes, then 0 steps and the accumulator does not grow; after resume there is no catch-up burst.
  - [ ] Given identical sequences of deltas, then results are identical (deterministic), and over 10 simulated minutes the step count equals floor(total x rate) within 1.
  - [ ] Uses integer ticks internally and allocates nothing per call.
  - [ ] At least 12 unit tests, covering every branch.

## M1-02 GameTime, FrameInfo and IClock
- **Type:** feature | **Labels:** `feature`, `area:core` | **Priority:** P0 | **Size:** S (2 h) | **Epic:** E02
- **Depends on:** M0-08
- **Description:** Value types handed to game code, plus a clock abstraction (a real seam) so timing is testable.
- **Acceptance criteria:**
  - [ ] `GameTime` (fixed delta, total time, tick count) and `FrameInfo` (alpha, frame delta, frame index) are readonly structs with XML docs.
  - [ ] `IClock` exposes a timestamp and frequency; `StopwatchClock` is the real implementation; a `FakeClock` exists in the test project.
  - [ ] Given N ticks at 60 Hz, then `GameTime.Total` equals N/60 s within one tick.

## M1-03 EngineOptions
- **Type:** feature (user story) | **Labels:** `feature`, `area:core` | **Priority:** P0 | **Size:** S (2 h) | **Epic:** E02
- **Depends on:** M0-08
- **Description:** *As a game developer, I want to configure window title, size, vsync, tick rate and frame cap in one options object so that I can start a game without touching low-level settings.*
- **Acceptance criteria:**
  - [ ] Immutable record with defaults: 1280x720, title "Woad", vsync on, 60 updates/s, 5 max steps, 250 ms max frame delta, no frame cap, clear colour, optional logger factory.
  - [ ] Given an invalid value (zero or negative size, tick rate 0, cap below 0), when validated, then `ArgumentOutOfRangeException` names the offending property.
  - [ ] Given `options with { Title = "X" }`, then other values are unchanged.
  - [ ] Public members have XML docs; one unit test per validation rule.

## M1-04 Logging
- **Type:** feature (technical task) | **Labels:** `feature`, `area:core` | **Priority:** P0 | **Size:** S (3 h) | **Epic:** E02
- **Depends on:** M1-03
- **Description:** Engine logs via `ILogger` from `Microsoft.Extensions.Logging.Abstractions`; a minimal internal console logger is used when no factory is supplied, so diagnostics are never silently lost.
- **Acceptance criteria:**
  - [ ] Given no logger factory in options, when the engine starts, then startup information is written to the console at Information level: Woad version, OS, runtime and GL renderer/version.
  - [ ] Given a custom factory, then all engine log output goes through it.
  - [ ] Lifecycle log messages use stable event IDs; log levels are documented in a short table in the XML docs or architecture doc.
  - [ ] No logging package beyond the abstractions is referenced.

## M1-05 GameWindow (internal platform wrapper)
- **Type:** feature (technical task) | **Labels:** `feature`, `area:platform` | **Priority:** P0 | **Size:** L (8 h) | **Epic:** E02
- **Depends on:** M0-04, M0-07, M1-03, M1-04
- **Description:** Internal class that creates the window and the OpenGL 3.3 Core context through Silk.NET, exposes sizes and events, pumps events, swaps buffers, and disposes cleanly ([ADR 0005](../decisions/0005-window-context-ownership-and-owned-loop.md)). Also introduces the internal window seam interface used by tests.
- **Acceptance criteria:**
  - [ ] Given default options, when the window is created, then a GL 3.3 Core context is current and the version is logged.
  - [ ] Given the driver cannot provide 3.3 Core, when creation fails, then `EngineInitializationException` explains what was requested and what the driver reported.
  - [ ] Given the user resizes the window, when events are polled, then a resized event reports the new framebuffer size.
  - [ ] Given the close button is clicked, then `IsClosing` becomes true.
  - [ ] `Dispose` is idempotent and releases the window and context.
  - [ ] Calls from a non-main thread fail an assertion in Debug builds.
  - [ ] No Silk.NET type appears in any public signature (checked by M1-10).
  - [ ] Verified manually on Windows; verified headlessly on Linux by M1-12.

## M1-06 Game, GameHost and GameContext
- **Type:** feature (user story) | **Labels:** `feature`, `area:core` | **Priority:** P0 | **Size:** L (8 h) | **Epic:** E02
- **Depends on:** M1-01, M1-02, M1-03, M1-04, M1-05
- **Description:** *As a game developer, I want to subclass `Game` and call `Run()` so that I get a working window and update/draw loop without writing loop code.* Implements [ADR 0004](../decisions/0004-game-api-shape.md). In M1 the host clears the backbuffer with the configured colour before `Draw`; `Draw(in FrameInfo)` has no renderer yet.
- **Acceptance criteria:**
  - [ ] Given a `Game` subclass, when `Run()` is called, then the window opens, `Initialize` runs once before the first `Update`, `Update` runs at the fixed rate, `Draw` runs once per frame, and `Shutdown` runs once at the end.
  - [ ] Given the window close button is clicked, then the loop exits after the current frame, `Shutdown` runs, and `Run` returns normally.
  - [ ] `GameContext` exposes window size and logging, and is designed so later epics can add Input, Graphics, Content and Audio without breaking changes.
  - [ ] Given `Run()` is called twice or re-entrantly, then `InvalidOperationException` is thrown.
  - [ ] Given a fake window and fake clock, then a unit test asserts the exact call order (Initialize, Update x N, Draw, Shutdown) and that no more than the max steps run per frame.
  - [ ] All public members have XML docs.

## M1-07 Exceptions and shutdown ordering
- **Type:** feature (technical task) | **Labels:** `feature`, `testing`, `area:core` | **Priority:** P1 | **Size:** M (4 h) | **Epic:** E02
- **Depends on:** M1-06
- **Description:** Implement the error policy in the architecture overview, section 8.
- **Acceptance criteria:**
  - [ ] Given `Initialize` throws, then the window is disposed, the error is logged, and the original exception propagates from `Run`.
  - [ ] Given `Update` or `Draw` throws, then the error is logged with tick/frame context, `Shutdown` is still invoked (best effort), the window is disposed, and the original exception is rethrown with its stack trace preserved.
  - [ ] Given `Shutdown` itself throws after an earlier exception, then it is logged and does not mask the original.
  - [ ] Disposal order (game shutdown, then graphics, then window) is asserted with recording fakes.

## M1-08 Frame pacing and limiter
- **Type:** feature (technical task) | **Labels:** `feature`, `area:core` | **Priority:** P1 | **Size:** M (3 h) | **Epic:** E02
- **Depends on:** M1-06
- **Description:** With vsync off and a frame cap set, wait without a busy loop: sleep for most of the interval, spin only for the last millisecond.
- **Acceptance criteria:**
  - [ ] Given vsync on, then the limiter adds no waiting.
  - [ ] Given vsync off and a cap of 60, then the average frame time over 10 s on an idle scene is within 1 ms of 16.67 ms.
  - [ ] Given a cap of 60 with vsync off, then process CPU time over 10 s stays well below one full core (manual check, number recorded in the PR).
  - [ ] Wait-duration computation is unit-tested with `FakeClock`.

## M1-09 FrameStats
- **Type:** feature | **Labels:** `feature`, `area:core` | **Priority:** P2 | **Size:** S (2 h) | **Epic:** E02
- **Depends on:** M1-06
- **Description:** Rolling averages over the last 60 frames: frame time, FPS, update time, draw time; exposed read-only on `GameContext`.
- **Acceptance criteria:**
  - [ ] Given a fake clock with constant 16 ms frames, then FPS is approximately 62.5 and frame time 16 ms.
  - [ ] Steady-state updates allocate zero bytes (asserted with `GC.GetAllocatedBytesForCurrentThread` in a test).
  - [ ] Sandbox shows FPS in the window title, updated at most twice per second.

## M1-10 Architecture and public API surface tests
- **Type:** testing | **Labels:** `testing`, `area:build` | **Priority:** P0 | **Size:** S (3 h) | **Epic:** E02
- **Depends on:** M1-05, M1-06
- **Description:** Make the rules from [ADR 0003](../decisions/0003-assembly-layout-and-dependency-rules.md) executable, using hand-rolled reflection or NetArchTest.Rules (decide in the PR after checking net11 compatibility).
- **Acceptance criteria:**
  - [ ] `Woad.Core` has no reference to Silk.NET, native-binding packages, or the `Woad` assembly.
  - [ ] No public type or member in `Woad` or `Woad.Core` exposes a `Silk.NET.*` type in its signature.
  - [ ] `Woad.Graphics` types do not use `Woad.Platform` types.
  - [ ] Given a deliberate temporary violation of each rule, then the corresponding test fails.

## M1-11 Sandbox as the first public-API consumer
- **Type:** feature (user story) | **Labels:** `feature`, `area:build` | **Priority:** P0 | **Size:** S (2 h) | **Epic:** E02
- **Depends on:** M1-06
- **Description:** *As the engine developer, I want a Sandbox app that uses only the public API and supports `--frames N` and `--seconds N` auto-exit so that I can smoke-test locally and headlessly.*
- **Acceptance criteria:**
  - [ ] Sandbox references only the `Woad` project, and has no Silk.NET reference.
  - [ ] Given no arguments, then a 1280x720 window opens with a solid clear colour and FPS in the title.
  - [ ] Given `--frames 120`, then it exits with code 0 after 120 drawn frames; `--seconds 5` behaves likewise.
  - [ ] Given an unknown argument, then it prints usage and exits with code 2.

## M1-12 Headless Linux smoke test in CI and on the Pi
- **Type:** testing | **Labels:** `testing`, `ci`, `area:platform` | **Priority:** P0 | **Size:** M (3 h) | **Epic:** E02
- **Depends on:** M0-03, M0-05, M1-11
- **Description:** Make `scripts/validate-linux.sh` the standard Linux check for graphics-related changes ([ADR 0010](../decisions/0010-supported-platforms-and-linux-validation.md)).
- **Acceptance criteria:**
  - [ ] Given a console-only Pi with prerequisites installed, when I run the script over SSH, then it exits 0 and the log contains the GL version line (3.3 or higher).
  - [ ] A `linux-smoke` CI job on `ubuntu-latest` runs the same script; failures show the tail of the log.
  - [ ] The job is non-blocking until it has 5 consecutive green runs, then made required.
  - [ ] `docs/development-setup.md` is updated with the verified steps.

## M1-13 M1 documentation and quick start
- **Type:** documentation | **Labels:** `documentation`, `area:docs` | **Priority:** P1 | **Size:** S (3 h) | **Epic:** E02
- **Depends on:** M1-06, M1-12
- **Description:** Make the docs match what was built.
- **Acceptance criteria:**
  - [ ] No missing-XML-doc warnings (`GenerateDocumentationFile` on, CS1591 not suppressed) for public M1 types.
  - [ ] README quick start compiles and matches Sandbox.
  - [ ] Architecture overview sections 4-8 reviewed against the code; differences fixed in code or docs.
  - [ ] `CHANGELOG.md` started (Keep a Changelog format).
