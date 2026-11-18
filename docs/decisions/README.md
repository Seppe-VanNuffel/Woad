# Architecture decision records

ADRs record consequential, hard-to-reverse decisions. Keep them short. Status values: **Proposed**, **Accepted**, **Amended**, **Superseded**, **Rejected**. All ADRs below are *Proposed* until the milestone 0 review (backlog issue M0-08).

| # | Title | Status | Validated by |
|---|---|---|---|
| [0001](0001-target-dotnet-11.md) | Target .NET 11 and pin the SDK | Accepted | M0-02, M0-04 |
| [0002](0002-opengl-33-core-with-silknet-2x.md) | OpenGL 3.3 Core via Silk.NET 2.x, kept internal | Accepted | M0-04 |
| [0003](0003-assembly-layout-and-dependency-rules.md) | Assembly layout, dependency rules, no DI container | Proposed | M1-10 |
| [0004](0004-game-api-shape.md) | Game API shape: hybrid `Game` + `GameHost` | Proposed | M1-06 |
| [0005](0005-window-context-ownership-and-owned-loop.md) | Window/context ownership and owned main loop | Proposed | M0-07 |
| [0006](0006-concrete-2d-renderer-and-coordinate-conventions.md) | Concrete 2D renderer and coordinate conventions | Proposed | M2, M3 |
| [0007](0007-threading-and-resource-ownership.md) | Threading model and resource ownership | Proposed | M1-05, M2 |
| [0008](0008-fixed-timestep-and-input-sampling.md) | Fixed timestep and input sampling | Proposed | M1-01, M4 |
| [0009](0009-content-identity-and-sync-first-loading.md) | Asset identity and synchronous-first loading | Proposed | M4 |
| [0010](0010-supported-platforms-and-linux-validation.md) | Supported platforms and Linux validation | Proposed | M0-05, M1-12 |
| [0011](0011-scope-guard.md) | Scope guard: no ECS, editor, scripting before 1.0 | Proposed | Ongoing |
| [0012](0012-audio-stack.md) | Audio stack: OpenAL, WAV and Ogg Vorbis | Proposed (pending spike) | M0-06 |

Use [0000-template.md](0000-template.md) for new records. Number sequentially; never renumber.
