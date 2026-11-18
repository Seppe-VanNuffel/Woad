# Milestone 8: Demonstration game (epics E12, E13)

**Goal:** prove the public API by building a small Stardew-style game, then publish the engine with media and an article.
**Budget:** about 5 weeks, roughly 60 hours (M8-09 is a reserved buffer for engine fixes the demo uncovers).
**Detail:** provisional
**Exit criteria:** `StardewDemo` uses only the public API, runs on Windows and passes the headless smoke test; release 1.0.0 tagged.

## M8-01 StardewDemo project and scope freeze
- **Type:** chore | **Labels:** `chore`, `area:demo` | **Priority:** P0 | **Size:** S (3 h) | **Epic:** E12
- **Depends on:** M7-10
- **Description:** Create the demo project and fix its scope.
- **Acceptance criteria:**
  - [ ] `samples/StardewDemo` references only `Woad` (no InternalsVisibleTo, no Silk.NET).
  - [ ] Every art and audio asset is original, CC0 or otherwise licensed for redistribution, recorded with source and licence in `samples/StardewDemo/ASSETS.md`.
  - [ ] The content layout is documented; the project builds and opens a window on Windows.
  - [ ] A demo scope list of at most 8 bullets is written and frozen.

## M8-02 Tile world
- **Type:** feature | **Labels:** `feature`, `area:demo` | **Priority:** P0 | **Size:** M (6 h) | **Epic:** E12
- **Depends on:** M8-01
- **Description:** A farm-style map built with the engine's `Tilemap`.
- **Acceptance criteria:**
  - [ ] A map of at least 64x64 tiles with ground and object layers renders at 60 FPS.
  - [ ] Map data is content, not hard-coded.
  - [ ] Render stats confirm that only visible tiles are submitted.

## M8-03 Player movement and animation
- **Type:** feature | **Labels:** `feature`, `area:demo` | **Priority:** P0 | **Size:** M (5 h) | **Epic:** E12
- **Depends on:** M8-01
- **Description:** Four-direction walking with idle and walk animations.
- **Acceptance criteria:**
  - [ ] Diagonal speed is normalised; movement happens only in the fixed-step `Update`.
  - [ ] Animations switch without glitches; the frame-reset policy is documented.

## M8-04 Camera tracking and world bounds
- **Type:** feature | **Labels:** `feature`, `area:demo` | **Priority:** P1 | **Size:** S (3 h) | **Epic:** E12
- **Depends on:** M8-02, M8-03
- **Description:** Follow the player inside the world.
- **Acceptance criteria:**
  - [ ] The camera follows the player, stays within world bounds and is pixel-snapped.
  - [ ] Resizing the window keeps the view correct.

## M8-05 World collision
- **Type:** feature | **Labels:** `feature`, `area:demo`, `area:collision` | **Priority:** P0 | **Size:** M (5 h) | **Epic:** E12
- **Depends on:** M8-02, M8-03
- **Description:** Solid tiles and objects such as trees and fences.
- **Acceptance criteria:**
  - [ ] The player cannot walk through solid tiles or objects and slides along their edges.
  - [ ] F4 toggles the collision debug view.
  - [ ] Walking along a row of adjacent solid tiles never snags (manual check plus a test).

## M8-06 Collectables and HUD
- **Type:** feature (user story) | **Labels:** `feature`, `area:demo` | **Priority:** P0 | **Size:** L (8 h) | **Epic:** E12
- **Depends on:** M8-05
- **Description:** *As a player, I want to pick up items and see my counts so that I have something to do in the world.* Item and entity logic uses plain demo classes.
- **Acceptance criteria:**
  - [ ] At least three item types spawn in the world; walking over one collects it.
  - [ ] A bitmap-font HUD shows counts per item and a score.
  - [ ] Candidate engine extractions are listed in `docs/notes/extraction-candidates.md`.

## M8-07 Audio in the demo
- **Type:** feature | **Labels:** `feature`, `area:demo`, `area:audio` | **Priority:** P1 | **Size:** S (3 h) | **Epic:** E12
- **Depends on:** M8-06
- **Description:** Sound effects and music.
- **Acceptance criteria:**
  - [ ] Pickup and footstep or ambient effects plus looping music play; mute and volume keys work.
  - [ ] The demo runs with the null audio device without errors on the Pi.

## M8-08 Title, game and pause scenes
- **Type:** feature | **Labels:** `feature`, `area:demo` | **Priority:** P1 | **Size:** M (4 h) | **Epic:** E12
- **Depends on:** M8-04
- **Description:** Use the scene stack for the game flow.
- **Acceptance criteria:**
  - [ ] Title, game and pause scenes work; Escape pauses.
  - [ ] Quitting from the title and from pause exits cleanly with no leak warnings.

## M8-09 Engine gaps found by the demo (reserved buffer)
- **Type:** feature | **Labels:** `feature`, `area:core` | **Priority:** P1 | **Size:** L (8 h) | **Epic:** E12
- **Depends on:** M8-05
- **Description:** Triage the friction log and extraction candidates; fix only what the demo proves is needed ([ADR 0011](../decisions/0011-scope-guard.md)).
- **Acceptance criteria:**
  - [ ] Each item is marked engine change, demo-only or won't do.
  - [ ] At most three engine improvements are implemented, each with tests and a changelog note or short ADR.
  - [ ] The public API baseline is updated; breaking changes appear in the changelog.

## M8-10 Demo polish and validation
- **Type:** testing | **Labels:** `testing`, `area:demo` | **Priority:** P0 | **Size:** S (3 h) | **Epic:** E12
- **Depends on:** M8-07, M8-08, M8-09
- **Description:** Make the demo robust and prove it uses only the public API.
- **Acceptance criteria:**
  - [ ] The demo runs on Windows from a clean clone following the README, and the Pi headless smoke run with `--frames` passes.
  - [ ] A 10-minute soak shows zero warnings, zero leak warnings and no unhandled exceptions.
  - [ ] A test or CI check confirms the demo references only the public API.

## M8-11 Portfolio media
- **Type:** documentation | **Labels:** `documentation`, `area:docs` | **Priority:** P1 | **Size:** S (3 h) | **Epic:** E13
- **Depends on:** M8-10
- **Description:** Visuals for the README and portfolio.
- **Acceptance criteria:**
  - [ ] A 10-30 second GIF or MP4 and at least three screenshots (one with the debug overlay) are committed under `docs/images/` and linked from the README.
  - [ ] An architecture diagram is exported as PNG or SVG for the README.

## M8-12 Technical article
- **Type:** documentation | **Labels:** `documentation`, `area:docs` | **Priority:** P1 | **Size:** M (6 h) | **Epic:** E13
- **Depends on:** M8-10, M2-10
- **Description:** An article explaining the Woad rendering pipeline for a portfolio audience.
- **Acceptance criteria:**
  - [ ] An article of 1,500-2,500 words stored in `docs/articles/` follows a sprite from `DrawSprite` to the GPU draw call, covering batching and conventions, with diagrams and code excerpts.
  - [ ] It is reviewed against the code and every code excerpt compiles.
  - [ ] It is published or ready to publish, with a link from the README.

## M8-13 Release 1.0.0
- **Type:** chore | **Labels:** `chore`, `area:build` | **Priority:** P0 | **Size:** S (3 h) | **Epic:** E12
- **Depends on:** M8-10, M8-11, M8-12
- **Description:** The final release and a retrospective.
- **Acceptance criteria:**
  - [ ] The release checklist passes: epic outcomes met, documentation map complete, CI green on both operating systems, packages built, platform matrix current.
  - [ ] Tag `v1.0.0` and a GitHub release with notes; the README no longer says pre-alpha.
  - [ ] A retrospective (planned versus actual hours per milestone) is added to the roadmap.
