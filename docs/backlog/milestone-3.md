# Milestone 3: 2D rendering (epic E04)

**Goal:** a reusable sprite renderer: camera, transforms, batching, layers and debug primitives.
**Budget:** about 4 weeks, roughly 48 hours (tight; cut candidates: M3-08, M3-10).
**Detail:** provisional
**Exit criteria:** a resizable Sandbox scene renders sprites and a 100x100 tile grid through `Renderer2D` with few draw calls, and the stats prove it.

## M3-01 Color and Rect types (Core)
- **Type:** feature | **Labels:** `feature`, `area:core` | **Priority:** P0 | **Size:** S (2 h) | **Epic:** E04
- **Depends on:** M0-02
- **Description:** `Color` (8-bit RGBA, straight alpha) and `Rect` (float x, y, width, height) as readonly structs.
- **Acceptance criteria:**
  - [ ] Given "#FF8000", then `Color` is (255, 128, 0, 255); an invalid string throws `FormatException`.
  - [ ] Lerp at 0 and 1 returns the endpoints; the midpoint is within one unit of rounding.
  - [ ] `Rect.Contains` treats left/top as inclusive and right/bottom as exclusive, documented and tested.
  - [ ] At least 15 unit tests; equality and hashing implemented.

## M3-02 Transform2D (Core)
- **Type:** feature | **Labels:** `feature`, `area:core` | **Priority:** P0 | **Size:** M (3 h) | **Epic:** E04
- **Depends on:** M0-02
- **Description:** Position, rotation (radians), scale and origin composing to a `Matrix3x2`.
- **Acceptance criteria:**
  - [ ] The composition order (scale, rotation, translation) is documented.
  - [ ] Given a rotation of pi/2 with +Y down, then point (1, 0) maps to (0, 1), which is clockwise on screen.
  - [ ] The inverse round-trips points within 1e-4 for 100 seeded random transforms.
  - [ ] A zero-scale transform reports failure through `TryInvert` instead of returning NaN.

## M3-03 Camera2D (Core)
- **Type:** feature | **Labels:** `feature`, `area:core`, `area:graphics` | **Priority:** P0 | **Size:** M (5 h) | **Epic:** E04
- **Depends on:** M3-02
- **Description:** Orthographic camera with position, zoom, rotation and viewport size, producing a view-projection matrix and world/screen conversions.
- **Acceptance criteria:**
  - [ ] Given position (100, 50), zoom 2 and viewport 800x600, then world (100, 50) maps to screen (400, 300).
  - [ ] `ScreenToWorld(WorldToScreen(p))` returns p within 1e-4 for seeded random points, zooms and rotations.
  - [ ] +Y is down in both spaces, documented in XML docs with an example.
  - [ ] `VisibleBounds` returns the world rectangle in view; at least 15 unit tests.

## M3-04 Sprite shader and quad geometry
- **Type:** feature | **Labels:** `feature`, `area:graphics` | **Priority:** P0 | **Size:** M (4 h) | **Epic:** E04
- **Depends on:** M2-03, M2-04, M2-07
- **Description:** Internal sprite shader (position, UV, tint; view-projection uniform; texture sampler) and pure quad-vertex generation.
- **Acceptance criteria:**
  - [ ] Quad generation (4 vertices, 6 indices) from position, size, origin, rotation and UV rectangle is a pure function with unit tests.
  - [ ] Blend state is straight alpha; depth test and face culling are disabled.
  - [ ] A GraphicsLab scene draws one rotated, tinted sprite through the new path.

## M3-05 Renderer2D: Begin, DrawSprite, End
- **Type:** feature (user story) | **Labels:** `feature`, `area:graphics` | **Priority:** P0 | **Size:** L (8 h) | **Epic:** E04
- **Depends on:** M3-01, M3-03, M3-04
- **Description:** *As a game developer, I want to draw a texture at a world position with rotation, scale and tint so that I can build scenes without OpenGL.* Public `Renderer2D`; `Game.Draw` becomes `Draw(Renderer2D renderer, in FrameInfo frame)` (planned break, see [ADR 0004](../decisions/0004-game-api-shape.md)). The first version issues one draw call per sprite.
- **Acceptance criteria:**
  - [ ] Given Begin, DrawSprite and End, then the sprite appears at the expected world position and rotation in Sandbox.
  - [ ] Given DrawSprite without Begin, or Begin called twice, then `InvalidOperationException` with a clear message.
  - [ ] Sandbox, GraphicsLab and the README quick start use the new Draw signature; ADR 0004 is amended.
  - [ ] Tint, origin, scale and rotation work, verified in the sprite scene; no GL types are public (M1-10 passes).

## M3-06 Source rectangles and flipping
- **Type:** feature | **Labels:** `feature`, `area:graphics` | **Priority:** P0 | **Size:** S (3 h) | **Epic:** E04
- **Depends on:** M3-05
- **Description:** Draw a sub-rectangle of a texture, with optional horizontal/vertical flip.
- **Acceptance criteria:**
  - [ ] Given a source rectangle in pixels, then the correct sub-image is drawn; UV computation is a pure function with tests, including an optional half-pixel inset.
  - [ ] FlipX and FlipY mirror the sprite without moving it.
  - [ ] Given a source rectangle outside the texture, then `ArgumentOutOfRangeException`.

## M3-07 Sprite batching
- **Type:** feature | **Labels:** `feature`, `area:graphics` | **Priority:** P0 | **Size:** L (8 h) | **Epic:** E04
- **Depends on:** M3-05, M3-06
- **Description:** Batch sprites into a reused dynamic vertex buffer, flushing on texture change, capacity, and End.
- **Acceptance criteria:**
  - [ ] Given 10,000 sprites using one texture, then draw calls equal the number of capacity-sized batches (capacity documented).
  - [ ] Given alternating textures A, B, A, B, then a flush occurs at each switch.
  - [ ] Steady-state frames allocate zero bytes (test with `GC.GetAllocatedBytesForCurrentThread`).
  - [ ] Capacity overflow flushes automatically and draws in the correct order.
  - [ ] 10,000 sprites render at 60 FPS on the development machine (measurement recorded in the PR).

## M3-08 Layers and sort order
- **Type:** feature | **Labels:** `feature`, `area:graphics` | **Priority:** P2 | **Size:** M (4 h) | **Epic:** E04
- **Depends on:** M3-07
- **Description:** Layer depth per sprite with deferred (submission order) and by-layer sort modes.
- **Acceptance criteria:**
  - [ ] Given sprites on layers 0, 1 and 2 submitted out of order in by-layer mode, then they draw in layer order and equal layers keep submission order.
  - [ ] Sorting reuses arrays and allocates nothing per frame.
  - [ ] Sort modes are documented in the rendering guide.

## M3-09 Viewport, resize and high-DPI handling
- **Type:** feature | **Labels:** `feature`, `area:graphics`, `area:platform` | **Priority:** P0 | **Size:** S (3 h) | **Epic:** E04
- **Depends on:** M3-05
- **Description:** Keep the GL viewport and camera viewport in sync with the framebuffer.
- **Acceptance criteria:**
  - [ ] Given a window resize, then the GL viewport and camera viewport follow the framebuffer size.
  - [ ] Given a minimised (0x0) window, then rendering is skipped without an exception.
  - [ ] Window size and framebuffer size are both exposed; 1 world unit equals 1 framebuffer pixel at zoom 1.

## M3-10 Debug primitives
- **Type:** feature | **Labels:** `feature`, `area:graphics`, `area:diagnostics` | **Priority:** P1 | **Size:** M (3 h) | **Epic:** E04
- **Depends on:** M3-07
- **Description:** Filled and outline rectangles and lines drawn through the same batching path using a 1x1 white texture.
- **Acceptance criteria:**
  - [ ] `DrawRectangle` (filled and outline) and `DrawLine` accept colour and thickness.
  - [ ] Given a 1-pixel line at zoom 1, then it covers exactly one pixel row.
  - [ ] Primitives batch correctly with sprites (verified by render stats).

## M3-11 Render statistics
- **Type:** feature | **Labels:** `feature`, `area:diagnostics` | **Priority:** P1 | **Size:** S (2 h) | **Epic:** E04
- **Depends on:** M3-07
- **Description:** Per-frame renderer counters exposed on `GameContext`.
- **Acceptance criteria:**
  - [ ] `RenderStats` reports draw calls, sprites, batches flushed and texture switches, reset at frame start.
  - [ ] Collecting stats allocates nothing per frame (test).
  - [ ] Sandbox shows the draw-call count in the window title.

## M3-12 Sprite scene, tile-grid stress and pixel-art checks
- **Type:** testing | **Labels:** `testing`, `area:graphics` | **Priority:** P1 | **Size:** S (3 h) | **Epic:** E04
- **Depends on:** M3-08, M3-09, M3-10, M3-11
- **Description:** Sandbox scenes that exercise the renderer: sprites with a scripted camera pan and zoom (input arrives in M4), and a 100x100 tile grid from a padded atlas, with pixel-art correctness checks.
- **Acceptance criteria:**
  - [ ] The sprite scene runs in a resizable window with a scripted camera.
  - [ ] The 100x100 tile grid renders with a handful of draw calls (count visible in the title).
  - [ ] With nearest filtering and atlas padding there is no bleeding; optional camera pixel snapping removes shimmer; notes go in the rendering guide.
  - [ ] The headless smoke test runs the scenes on Linux and the Pi with zero GL errors.
