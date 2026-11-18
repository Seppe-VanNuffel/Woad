# Milestone 6: Gameplay support (epic E10)

**Goal:** what a tile-based game needs: sprite sheets, animation, scenes, tilemaps, camera follow and tile collision.
**Budget:** about 3 weeks, roughly 36 hours (tight; Tiled import is out of scope).
**Detail:** provisional
**Exit criteria:** an animated character walks on a tilemap with camera follow and collision, with title-to-game scene switching; release 0.3.0 tagged.

## M6-01 SpriteSheet and atlas regions
- **Type:** feature | **Labels:** `feature`, `area:graphics`, `area:core` | **Priority:** P0 | **Size:** M (4 h) | **Epic:** E10
- **Depends on:** M3-06, M4-06
- **Description:** Map frame indices and names to source rectangles.
- **Acceptance criteria:**
  - [ ] Grid slicing (cell size, margin, spacing) maps a frame index to a source rectangle; pure Core code with tests.
  - [ ] Named regions can be registered in code or loaded from a simple JSON file.
  - [ ] An out-of-range index throws `ArgumentOutOfRangeException`.
  - [ ] Padded atlases are supported and documented.

## M6-02 Frame animation player (Core)
- **Type:** feature | **Labels:** `feature`, `area:core` | **Priority:** P0 | **Size:** M (5 h) | **Epic:** E10
- **Depends on:** M1-02
- **Description:** `Animation` (frames with durations) and `AnimationPlayer` driven by fixed ticks.
- **Acceptance criteria:**
  - [ ] Modes: loop, once and ping-pong; playback speed multiplier; a completion event fires once for `once`.
  - [ ] Given frame durations that are not multiples of the tick, then frame selection does not drift over long runs (test).
  - [ ] At least 15 unit tests; no allocations in steady state.

## M6-03 Scene stack
- **Type:** feature (user story) | **Labels:** `feature`, `area:core` | **Priority:** P0 | **Size:** M (5 h) | **Epic:** E10
- **Depends on:** M1-06
- **Description:** *As a game developer, I want title, game and pause scenes that I can push and pop so that I can structure my game.*
- **Acceptance criteria:**
  - [ ] `Scene` offers Enter, Exit, Pause, Resume, Update and Draw; `SceneStack` offers Push, Pop and Replace.
  - [ ] Only the top scene updates; scenes below optionally draw (flag), for example under a pause overlay.
  - [ ] Given the last scene is popped, then the game exits cleanly.
  - [ ] Scene changes requested during Update apply after the tick; lifecycle order is tested with fakes.

## M6-04 Tilemap data and renderer
- **Type:** feature | **Labels:** `feature`, `area:graphics` | **Priority:** P0 | **Size:** L (8 h) | **Epic:** E10
- **Depends on:** M6-01, M3-07
- **Description:** Layered tile grid drawn through `Renderer2D`, culled to the camera.
- **Acceptance criteria:**
  - [ ] A `Tilemap` has tile size, layers and indices into a `SpriteSheet`, buildable from arrays and from a minimal JSON or CSV format.
  - [ ] Given a 200x200 map, then only tiles inside the camera bounds are submitted.
  - [ ] Layers draw in order; an empty tile index is defined and documented.
  - [ ] The visible tile-range computation is pure Core code with tests, including partially visible edges and negative camera positions.

## M6-05 Camera follow and bounds (Core)
- **Type:** feature | **Labels:** `feature`, `area:core` | **Priority:** P1 | **Size:** S (3 h) | **Epic:** E10
- **Depends on:** M3-03
- **Description:** Follow a target with optional deterministic smoothing and clamp to world bounds.
- **Acceptance criteria:**
  - [ ] Smoothing is driven by fixed ticks and is deterministic.
  - [ ] The camera clamps to world bounds; if the world is smaller than the viewport, it is centred.
  - [ ] Optional pixel snapping of the final position; at least 12 unit tests.

## M6-06 Tilemap collision
- **Type:** feature | **Labels:** `feature`, `area:collision` | **Priority:** P0 | **Size:** S (3 h) | **Epic:** E10
- **Depends on:** M6-04, M5-09
- **Description:** Flag solid tiles and query them for collision.
- **Acceptance criteria:**
  - [ ] A tile layer can flag solid tiles; a query returns solid tile rectangles overlapping a given rectangle.
  - [ ] Given a player rectangle and solid tiles, then `MoveAndSlide` prevents overlap (tests with a small map).
  - [ ] Adjacent solid tiles do not snag (regression test).

## M6-07 Animated character demo with scene switching
- **Type:** feature | **Labels:** `feature`, `area:demo` | **Priority:** P0 | **Size:** M (5 h) | **Epic:** E10
- **Depends on:** M6-02, M6-03, M6-04, M6-05, M6-06, M4-04
- **Description:** Sandbox scenes proving the gameplay-support APIs together.
- **Acceptance criteria:**
  - [ ] A title scene starts the game with Enter; Escape returns to the title.
  - [ ] An animated four-direction player walks on a tilemap with camera follow and tile collision.
  - [ ] It uses only the public API; the headless autowalk run passes on the Pi; a 10-second GIF is captured on Windows.
  - [ ] The API friction log is updated.

## M6-08 Release 0.3.0
- **Type:** chore | **Labels:** `chore`, `documentation`, `area:docs` | **Priority:** P0 | **Size:** S (3 h) | **Epic:** E10
- **Depends on:** M6-07
- **Description:** Document the new subsystems and cut the third pre-release.
- **Acceptance criteria:**
  - [ ] Guides for animation, scenes and tilemaps exist; changelog and README features are updated.
  - [ ] CI and the headless smoke test are green; tag `v0.3.0` and a GitHub pre-release.
  - [ ] The roadmap for M7 and M8 is re-baselined with actual hours.
