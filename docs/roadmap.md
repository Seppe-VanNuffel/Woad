# Roadmap, estimates and risk register

Status: **Draft v1**. Re-baselined at the end of milestone 0 (issue M0-08) using real spike hours.

## 1. What changed from the planning brief

| Change | Reason |
|---|---|
| Added **M0: spike and scaffolding** | Retire the Silk.NET/.NET 11, Linux headless and OpenAL unknowns before committing to the plan |
| CI, analyzers and the first tests moved from M6 to M0/M1 | Quality gates are cheaper when they exist from day one |
| Old M4 split into **Input + Content + Debug overlay** (M4) and **Audio + Collision** (M5) | M4 was 5+ subsystems in four weeks |
| UI toolkit and engine entity model removed | See [ADR 0011](decisions/0011-scope-guard.md) |
| Tilemap and animation grouped in M6 | The demo is tile-based; the brief had no tilemap scope |
| Demo prototype starts in M4 inside Sandbox | The API gets exercised long before week 24 |

## 2. Milestones

Estimates assume 8-12 hours per week. Nominal total: **34 weeks (about 8 months, 270-410 hours)**. With roughly 20% contingency: **about 41 weeks (9-10 months)**.

| M | Name | Weeks | Release | Demonstrable outcome |
|---|---|---|---|---|
| M0 | Spike and scaffolding | 3 | - | Triangle on Windows and headless Linux; CI green on Windows and Linux; ADRs reviewed |
| M1 | Foundation | 4 | - | Sandbox runs the fixed-step loop, FPS in window title, clean shutdown; headless smoke test passes on the Pi |
| M2 | Graphics fundamentals | 4 | **0.1.0** | Shader, buffers, VAO; coloured triangle, then textured rectangle; basic docs |
| M3 | 2D rendering | 4 | - | Sprite scene with camera motion and zoom, resize handling, batching with draw-call count, tile-grid stress scene |
| M4 | Input, content, diagnostics | 4 | - | Textures through `ContentManager`, keyboard-moved sprite, bitmap-font debug overlay, first walkable tile prototype |
| M5 | Audio and collision | 4 | **0.2.0** | Sound effects and streamed music; sprite blocked by walls; collision tests |
| M6 | Gameplay support | 3 | **0.3.0** | Animated character on a tilemap, camera follow, scene switching |
| M7 | Hardening and release | 3 | 1.0.0-rc | Clean clone builds and runs per docs; XML docs and public-API analyzer; leak audit clean; benchmarks; NuGet packages built; tagged release workflow |
| M8 | Demonstration game | 5 | **1.0.0** | StardewDemo using only the public API; GIF/video, article, getting-started guide |

**Bottom-up check (from the issue files):** the 100 backlog issues add up to **403 hours** (`python scripts/github/push_backlog.py --validate` prints the per-milestone totals). That is the top of the 270-410 h range, so the planned 34 weeks only holds at about 12 h/week. At 10 h/week it is about 40 weeks (roughly 9 months) *before* any contingency, and about 48 weeks with 20% contingency. Decide your realistic weekly hours now; the cut list below is how you protect the date if the answer is lower.

Cumulative: M0 week 3, M1 week 7, M2 week 11, M3 week 15, M4 week 19, M5 week 23, M6 week 26, M7 week 29, M8 week 34.

## 3. Planning rules

- **Rolling wave:** every milestone has issues now, but M3-M8 are marked `provisional`. Re-read and re-estimate a milestone's issues when the previous milestone finishes, then edit the plan files and the GitHub issues together.
- **WIP limit:** two issues in progress.
- **Re-estimate** at the end of every milestone using actual hours.
- **Release rule:** a release needs its demonstrable outcome working, CI green and docs updated.
- **Cut list (drop in this order if behind):** debug overlay polish, Ogg streaming (WAV only), batching optimisations beyond one dynamic buffer, tilemap import formats, NuGet publishing, Linux ARM64 smoke test, macOS.

## 4. Risk register

L = likelihood, I = impact (Low / Medium / High).

| # | Risk | L | I | Mitigation | Validation |
|---|---|---|---|---|---|
| R1 | Silk.NET 2.x misbehaves on .NET 11 (it targets .NET Standard 2.0 / .NET Core 3.1 / net5.0) | L | H | Spike first; pin versions; fall back to net10 ([ADR 0001](decisions/0001-target-dotnet-11.md)) | M0-04 |
| R2 | Silk.NET 3.0 rewrite or slowed maintenance forces a migration | M | M | Keep Silk internal; own enums; System.Numerics in public API ([ADR 0002](decisions/0002-opengl-33-core-with-silknet-2x.md)) | M1-10 |
| R3 | GL context/thread mistakes (wrong thread, leaked objects) | M | H | Main-thread assertions, leak tracker, ownership rules ([ADR 0007](decisions/0007-threading-and-resource-ownership.md)) | M1-05, M2, M7 |
| R4 | Native audio packaging or missing hardware (including headless Pi) | M | M | Spike; null-device fallback; `ALSOFT_DRIVERS=null` ([ADR 0012](decisions/0012-audio-stack.md)) | M0-06 |
| R5 | Linux validation is headless only, software GL differs from real drivers | H | M | Windows visual checks; headless smoke test; consider a Linux desktop or VM later ([ADR 0010](decisions/0010-supported-platforms-and-linux-validation.md)) | M0-05, M1-12 |
| R6 | ARM64 native libraries (GLFW, OpenAL Soft) unavailable on the Pi | M | L | Treat ARM64 as best-effort; system packages as fallback | M0-05, M0-06 |
| R7 | Scope creep | H | H | Scope guard ADR, WIP limit, rolling-wave planning | Milestone reviews |
| R8 | Estimates are optimistic (learning graphics) | H | M | M0 re-baseline, 20% contingency, cut list | M0-08 |
| R9 | Motivation and continuity with part-time work | M | H | Demonstrable outcome every milestone, small issues, 0.1.0 early | Milestone reviews |
| R10 | Public API churn before 1.0 | H | M | 0.x semver, API exercised by Sandbox and demo prototype from M4, PublicApiAnalyzers from M7 | M7 |
| R11 | Driver/GL differences on Windows (Intel, AMD, NVIDIA) | M | M | Stay within 3.3 Core; GL error checking in debug; RenderDoc; Sandbox test scenes | M2, M3 |
| R12 | Pixel-art artifacts (texture bleeding, sub-pixel jitter) | M | L | Nearest filtering, atlas padding, integer camera snapping option, test scene | M3 |
| R13 | Name or trademark conflict (an unrelated "woad" family of small terminal-colour libraries exists for Python, Ruby and Rust; a .NET port could appear) | L | M | Verify the NuGet ID and prefix, GitHub name and trademark databases before going public, and claim the IDs early; not legal advice | M0-01 |
