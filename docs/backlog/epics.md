# Epics

Machine-readable: `scripts/github/push_backlog.py` creates one GitHub issue per epic below and lists each epic's child issues (from the `Epic:` field of every issue) in its body. Keep the format exactly as shown.

## E01 Repository, tooling and feasibility
- **Milestone:** M0 | **Labels:** `epic`, `area:build` | **Priority:** P0
- **Goal:** A building, tested, CI-checked repository, and evidence that the technology stack works on Windows and on headless Linux.
- **Outcome:** Spike findings written, ADRs reviewed, roadmap re-baselined. Issues: [milestone-0.md](milestone-0.md).

## E02 Application core
- **Milestone:** M1 | **Labels:** `epic`, `area:core` | **Priority:** P0
- **Goal:** Window, fixed-step loop, logging, error handling and clean shutdown behind the public `Game` API.
- **Outcome:** Sandbox runs with FPS in the title; headless smoke test passes on the Raspberry Pi. Issues: [milestone-1.md](milestone-1.md).

## E03 Graphics fundamentals
- **Milestone:** M2 | **Labels:** `epic`, `area:graphics` | **Priority:** P0
- **Goal:** Learn and implement the OpenGL 3.3 Core pipeline: shaders, buffers, textures.
- **Outcome:** Textured rectangle in GraphicsLab; release 0.1.0. Issues: [milestone-2.md](milestone-2.md).

## E04 2D rendering
- **Milestone:** M3 | **Labels:** `epic`, `area:graphics` | **Priority:** P0
- **Goal:** A reusable sprite renderer with camera, batching, layers and debug primitives.
- **Outcome:** Sprites and a 100x100 tile grid render through `Renderer2D` with few draw calls. Issues: [milestone-3.md](milestone-3.md).

## E05 Input
- **Milestone:** M4 | **Labels:** `epic`, `area:input` | **Priority:** P0
- **Goal:** Keyboard and mouse input with per-update pressed/released semantics.
- **Outcome:** `Context.Input` works in Sandbox. Issues: [milestone-4.md](milestone-4.md).

## E06 Content management
- **Milestone:** M4 | **Labels:** `epic`, `area:content` | **Priority:** P0
- **Goal:** Cached content loading with explicit ownership and good error messages.
- **Outcome:** Textures load through `ContentManager`. Issues: [milestone-4.md](milestone-4.md).

## E07 Diagnostics and debug overlay
- **Milestone:** M4 | **Labels:** `epic`, `area:diagnostics` | **Priority:** P1
- **Goal:** See what the engine is doing: bitmap text and a debug overlay; first dogfooding prototype.
- **Outcome:** F3 overlay and a walkable tile scene. Issues: [milestone-4.md](milestone-4.md).

## E08 Audio
- **Milestone:** M5 | **Labels:** `epic`, `area:audio` | **Priority:** P1
- **Goal:** OpenAL sound effects and streamed music with a null-device fallback.
- **Outcome:** Sound in Sandbox, also headless. Issues: [milestone-5.md](milestone-5.md).

## E09 Collision and geometry
- **Milestone:** M5 | **Labels:** `epic`, `area:collision` | **Priority:** P0
- **Goal:** Pure, well-tested 2D collision for tile-based games.
- **Outcome:** Walls block a sprite; release 0.2.0. Issues: [milestone-5.md](milestone-5.md).

## E10 Animation, scenes and tilemap
- **Milestone:** M6 | **Labels:** `epic`, `area:graphics` | **Priority:** P0
- **Goal:** What a tile-based game needs on top of rendering and collision.
- **Outcome:** Animated character on a tilemap with camera follow; release 0.3.0. Issues: [milestone-6.md](milestone-6.md).

## E11 Hardening and release
- **Milestone:** M7 | **Labels:** `epic`, `area:build` | **Priority:** P0
- **Goal:** A stable API surface, clean lifecycle audit, benchmarks, packaging and release pipeline.
- **Outcome:** Release candidate 1.0.0-rc.1. Issues: [milestone-7.md](milestone-7.md).

## E12 Demonstration game
- **Milestone:** M8 | **Labels:** `epic`, `area:demo` | **Priority:** P0
- **Goal:** Prove the public API with a small Stardew-style game and ship 1.0.0.
- **Outcome:** `StardewDemo` using only the public API; release 1.0.0. Issues: [milestone-8.md](milestone-8.md).

## E13 Documentation and portfolio
- **Milestone:** M7 | **Labels:** `epic`, `area:docs` | **Priority:** P1
- **Goal:** Documentation that lets someone else use Woad, plus portfolio material.
- **Outcome:** Getting-started guide, media and a technical article. Issues: [milestone-7.md](milestone-7.md), [milestone-8.md](milestone-8.md).
