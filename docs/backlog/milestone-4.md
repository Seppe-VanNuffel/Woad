# Milestone 4: Input, content and diagnostics (epics E05, E06, E07)

**Goal:** engine-facing input, cached content loading with explicit ownership, bitmap text and a debug overlay; first walkable tile prototype.
**Budget:** about 4 weeks, roughly 48 hours (tight; cut M4-11 first, then M4-10 polish).
**Detail:** provisional
**Exit criteria:** a sprite walks over a tile grid with WASD using textures loaded through `ContentManager`; F3 shows the overlay; friction log started.

## M4-01 Key and MouseButton enums and the Silk input adapter
- **Type:** feature | **Labels:** `feature`, `area:input`, `area:platform` | **Priority:** P0 | **Size:** M (5 h) | **Epic:** E05
- **Depends on:** M1-06
- **Description:** Woad's own `Key` and `MouseButton` enums plus an internal adapter that buffers Silk.NET input events ([ADR 0002](../decisions/0002-opengl-33-core-with-silknet-2x.md)).
- **Acceptance criteria:**
  - [ ] `Key` covers letters, digits, arrows, function keys, modifiers, space, enter, escape, tab and backspace.
  - [ ] A test enumerates every Silk key and asserts it maps to a Woad key or is explicitly listed as unmapped.
  - [ ] The adapter buffers events on the main thread; no Silk.NET type is public.
  - [ ] On a machine without a keyboard device (headless Linux) the adapter initialises without error.

## M4-02 ButtonStateTracker (Core)
- **Type:** feature | **Labels:** `feature`, `area:input`, `area:core` | **Priority:** P0 | **Size:** M (5 h) | **Epic:** E05
- **Depends on:** M0-02
- **Description:** Pure, generic tracker implementing the latching rules from [ADR 0008](../decisions/0008-fixed-timestep-and-input-sampling.md).
- **Acceptance criteria:**
  - [ ] Given a tap shorter than a frame and a frame that runs zero Update steps, then the next Update sees Pressed exactly once.
  - [ ] Given two Update steps in one frame, then Pressed is true in the first step only.
  - [ ] Given press and release within one tick interval, then that tick reports Pressed and Released true and Down false.
  - [ ] Given a held key, then Down stays true and Pressed fires only on the first tick.
  - [ ] At least 15 unit tests; no allocations in steady state.

## M4-03 Mouse buttons, position and wheel
- **Type:** feature | **Labels:** `feature`, `area:input` | **Priority:** P1 | **Size:** S (3 h) | **Epic:** E05
- **Depends on:** M4-01, M4-02, M3-03
- **Description:** Mouse input built on the tracker; position in window, framebuffer and world coordinates.
- **Acceptance criteria:**
  - [ ] Mouse buttons use the tracker; wheel delta accumulates per tick and resets after each tick.
  - [ ] Given a high-DPI display, then position is in framebuffer pixels consistent with M3-09; world position uses the camera.
  - [ ] Given the cursor outside the window, then the last known position is retained and `IsInsideWindow` is false.

## M4-04 GameContext.Input and Sandbox input demo
- **Type:** feature (user story) | **Labels:** `feature`, `area:input` | **Priority:** P0 | **Size:** S (2 h) | **Epic:** E05
- **Depends on:** M4-01, M4-02, M3-05
- **Description:** *As a game developer, I want `Context.Input.IsDown(Key.W)` and edge queries so that I can move things in `Update`.*
- **Acceptance criteria:**
  - [ ] `Context.Input` offers IsDown, WasPressed and WasReleased for keys and mouse buttons, valid inside `Update` and reflecting the current tick (documented).
  - [ ] `Context.RequestExit()` exists; Sandbox quits on Escape.
  - [ ] Sandbox moves a sprite with WASD; diagonal speed behaviour is documented.
  - [ ] Given OS key repeat, then WasPressed is not retriggered.

## M4-05 AssetPath and AssetCache (Core)
- **Type:** feature | **Labels:** `feature`, `area:content`, `area:core` | **Priority:** P0 | **Size:** S (3 h) | **Epic:** E06
- **Depends on:** M0-02
- **Description:** Pure path normalisation and a cache keyed by (type, path) per [ADR 0009](../decisions/0009-content-identity-and-sync-first-loading.md).
- **Acceptance criteria:**
  - [ ] `AssetPath` converts backslashes to `/`, collapses `./`, and rejects rooted paths and `..` segments that escape the root.
  - [ ] Case is preserved; two paths differing only by case are different keys.
  - [ ] `AssetCache` returns the same instance on repeated requests and supports removal and clear.
  - [ ] At least 15 unit tests including Windows-style input.

## M4-06 ContentManager for textures
- **Type:** feature (user story) | **Labels:** `feature`, `area:content` | **Priority:** P0 | **Size:** M (5 h) | **Epic:** E06
- **Depends on:** M4-05, M2-07
- **Description:** *As a game developer, I want `Content.Load<Texture2D>("Characters/Player.png")` so that I don't manage files, decoding or caching myself.*
- **Acceptance criteria:**
  - [ ] Given a file under the content root, then it is decoded, uploaded and cached; a second call returns the same instance.
  - [ ] The content root defaults to `<base>/Content` and is configurable in `EngineOptions`; a documented MSBuild snippet copies content to the output.
  - [ ] Loaders are registered per asset type by the Graphics subsystem (Content has no direct dependency on Graphics).
  - [ ] Disposing the manager disposes everything it loaded exactly once.

## M4-07 Content errors and case-mismatch warning
- **Type:** feature | **Labels:** `feature`, `testing`, `area:content` | **Priority:** P1 | **Size:** S (3 h) | **Epic:** E06
- **Depends on:** M4-06
- **Description:** Good errors, and protection against Windows-only paths that break on Linux.
- **Acceptance criteria:**
  - [ ] A missing file raises `ContentLoadException` with the requested and resolved paths.
  - [ ] A corrupt image raises `ContentLoadException` with the inner exception.
  - [ ] Given a path whose case differs from the file on disk on Windows, then a Debug-build warning names both spellings.
  - [ ] Tests use temporary directories; the Linux CI run demonstrates the case-sensitive failure.

## M4-08 Content ownership and unload tests
- **Type:** testing | **Labels:** `testing`, `area:content` | **Priority:** P1 | **Size:** S (2 h) | **Epic:** E06
- **Depends on:** M4-06, M2-02
- **Description:** Pin down [ADR 0007](../decisions/0007-threading-and-resource-ownership.md) ownership rules for content.
- **Acceptance criteria:**
  - [ ] Disposing the manager disposes its textures once; a second dispose is safe; loading after dispose throws.
  - [ ] A texture loaded by a manager that is never disposed is reported by the leak tracker.
  - [ ] Two managers loading the same path produce two independent textures.

## M4-09 Bitmap fonts and text drawing
- **Type:** feature | **Labels:** `feature`, `area:graphics`, `area:diagnostics` | **Priority:** P0 | **Size:** L (8 h) | **Epic:** E07
- **Depends on:** M3-07, M4-06
- **Description:** Text rendering with bitmap fonts: an embedded debug font plus a loader for the BMFont text format.
- **Acceptance criteria:**
  - [ ] An embedded ASCII (32-126) debug font is authored in-repo, so there is no third-party font licence.
  - [ ] A BMFont text-format loader reads characters, advances, offsets and optional kerning.
  - [ ] `DrawString(font, text, position, color, scale)` supports newlines; `MeasureString` is available.
  - [ ] Layout and measurement are pure Core code with unit tests; steady-state drawing allocates nothing.

## M4-10 Debug overlay
- **Type:** feature | **Labels:** `feature`, `area:diagnostics` | **Priority:** P1 | **Size:** M (5 h) | **Epic:** E07
- **Depends on:** M4-09, M3-10, M3-11
- **Description:** Toggleable overlay for FPS and renderer/content statistics.
- **Acceptance criteria:**
  - [ ] F3 toggles an overlay showing FPS, frame/update/draw milliseconds, draw calls, sprites, live textures and loaded assets.
  - [ ] It draws last, on a screen-space camera, through the normal renderer.
  - [ ] No allocations in steady state while visible (test).
  - [ ] It can be disabled through `EngineOptions`.

## M4-11 Walkable tile prototype and API friction log
- **Type:** feature | **Labels:** `feature`, `area:demo` | **Priority:** P1 | **Size:** M (4 h) | **Epic:** E07
- **Depends on:** M4-04, M4-06, M3-12
- **Description:** First dogfooding scene: walk a sprite over a tile grid and write down every awkward moment in the API.
- **Acceptance criteria:**
  - [ ] A Sandbox scene lets a player sprite walk over a tile grid with WASD, using textures loaded through `ContentManager`.
  - [ ] `docs/notes/api-friction.md` lists each awkward API moment (or states none).
  - [ ] Given `--autowalk`, then the player follows a scripted path so the scene can run headless.

## M4-12 Input and content guides
- **Type:** documentation | **Labels:** `documentation`, `area:docs` | **Priority:** P1 | **Size:** S (3 h) | **Epic:** E05
- **Depends on:** M4-04, M4-07
- **Description:** User-facing guides for the new subsystems.
- **Acceptance criteria:**
  - [ ] `docs/guides/input.md` and `docs/guides/content.md` exist with runnable snippets.
  - [ ] The documentation map is updated and relative links resolve.
