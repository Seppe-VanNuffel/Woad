# Milestone 5: Audio and collision (epics E08, E09)

**Goal:** OpenAL sound effects and streamed music, plus pure, well-tested 2D collision.
**Budget:** about 4 weeks, roughly 49 hours (tight; cut Ogg streaming, M5-04 and M5-05, first and ship WAV only).
**Detail:** provisional
**Exit criteria:** Sandbox plays an effect and music; a sprite is blocked by walls and slides along them; release 0.2.0 tagged.

## M5-01 AudioDevice with null-device fallback
- **Type:** feature | **Labels:** `feature`, `area:audio` | **Priority:** P0 | **Size:** M (5 h) | **Epic:** E08
- **Depends on:** M0-06, M1-06
- **Description:** Open the default OpenAL device per [ADR 0012](../decisions/0012-audio-stack.md); fall back to a null device so games and headless runs keep working. Introduces an internal `IAudioBackend` seam.
- **Acceptance criteria:**
  - [ ] Given a working audio device, then it opens, the context is current on the main thread, and both are released on dispose.
  - [ ] Given no device or `ALSOFT_DRIVERS=null`, then a warning is logged and a `NullAudioDevice` is used; the game continues.
  - [ ] `Context.Audio` exposes master volume.
  - [ ] A fake `IAudioBackend` allows tests without OpenAL.
  - [ ] The headless smoke test passes on the Pi with the null backend.

## M5-02 WAV decoding (Core)
- **Type:** feature | **Labels:** `feature`, `area:audio`, `area:core` | **Priority:** P0 | **Size:** M (4 h) | **Epic:** E08
- **Depends on:** M0-02
- **Description:** Pure WAV parser producing `AudioData` (sample rate, channels, 16-bit PCM).
- **Acceptance criteria:**
  - [ ] PCM 8-bit and 16-bit, mono and stereo decode correctly.
  - [ ] Unsupported formats (float, compressed) throw `NotSupportedException` naming the format code.
  - [ ] Corrupt or truncated headers throw `InvalidDataException`; unknown chunks such as LIST are skipped.
  - [ ] Test WAV data is generated in tests; at least 12 unit tests.

## M5-03 SoundEffect playback
- **Type:** feature (user story) | **Labels:** `feature`, `area:audio` | **Priority:** P0 | **Size:** M (6 h) | **Epic:** E08
- **Depends on:** M5-01, M5-02
- **Description:** *As a game developer, I want to play a short sound with volume and looping so that I can add effects without handling OpenAL.*
- **Acceptance criteria:**
  - [ ] `SoundEffect.Play(volume, pitch, loop)` returns a `SoundInstance` with Stop, Pause, Resume and Volume.
  - [ ] Given more simultaneous plays than the source pool (default 32), then the oldest non-looping instance is stolen; documented and tested with the fake backend.
  - [ ] Master and per-instance volume multiply correctly (tests); pause-all and resume-all exist on `Context.Audio`.
  - [ ] Disposal frees buffers and sources, is tracked by the leak tracker, and use after dispose throws.

## M5-04 Ogg Vorbis decoding
- **Type:** feature | **Labels:** `feature`, `area:audio` | **Priority:** P1 | **Size:** M (5 h) | **Epic:** E08
- **Depends on:** M0-06, M5-02
- **Description:** Decode Ogg Vorbis with the decoder chosen in M0-06 and expose an `IAudioStream` for streaming.
- **Acceptance criteria:**
  - [ ] A short test .ogg (under 50 KB) decodes to the expected sample rate and sample count.
  - [ ] `IAudioStream` supports reading PCM frames, restarting and looping.
  - [ ] The decoder's licence is recorded in `THIRD-PARTY-NOTICES.md`.
  - [ ] Corrupt files throw descriptive exceptions.

## M5-05 Music streaming
- **Type:** feature | **Labels:** `feature`, `area:audio` | **Priority:** P1 | **Size:** M (7 h) | **Epic:** E08
- **Depends on:** M5-01, M5-04
- **Description:** `MusicStream` playing through at least three buffers refilled once per frame on the main thread.
- **Acceptance criteria:**
  - [ ] Play, pause, resume, stop, loop and volume work.
  - [ ] Given a 60 s file and a 5-minute soak at 60 FPS, then there are no audible gaps and no underrun warnings (manual result in the PR).
  - [ ] Given a 200 ms frame hitch, then playback continues without a crash and any underrun is logged.
  - [ ] Looping is seamless; the null device runs headless without error.

## M5-06 Audio content loaders and audio guide
- **Type:** feature | **Labels:** `feature`, `documentation`, `area:audio`, `area:content` | **Priority:** P1 | **Size:** S (3 h) | **Epic:** E08
- **Depends on:** M5-03, M5-05, M4-06
- **Description:** Integrate audio into `ContentManager` and document it.
- **Acceptance criteria:**
  - [ ] `Content.Load<SoundEffect>("Audio/pickup.wav")` and a music load method work with caching and ownership rules.
  - [ ] Music streams are owned by the caller or manager (decision documented).
  - [ ] `docs/guides/audio.md` covers formats, the null device and headless notes.

## M5-07 Collision shapes and overlap tests (Core)
- **Type:** feature | **Labels:** `feature`, `area:collision`, `area:core` | **Priority:** P0 | **Size:** M (5 h) | **Epic:** E09
- **Depends on:** M3-01
- **Description:** Point, rectangle and circle shapes with overlap tests.
- **Acceptance criteria:**
  - [ ] Point-rect, point-circle, rect-rect, circle-circle and circle-rect tests exist.
  - [ ] Touching edges do not count as overlap; the policy is documented and tested.
  - [ ] Degenerate shapes (zero size or radius) have defined, tested behaviour.
  - [ ] At least 25 unit tests; shapes are readonly structs and allocate nothing.

## M5-08 Segment and ray queries
- **Type:** feature | **Labels:** `feature`, `area:collision`, `area:core` | **Priority:** P1 | **Size:** M (3 h) | **Epic:** E09
- **Depends on:** M5-07
- **Description:** Segment-segment, ray-rect, ray-circle and segment-rect queries.
- **Acceptance criteria:**
  - [ ] Each query returns a hit flag, distance or fraction, and the surface normal.
  - [ ] A ray starting inside a shape reports a hit at distance 0 (documented).
  - [ ] Parallel and collinear cases are tested; at least 20 unit tests.

## M5-09 Collision information and movement resolution
- **Type:** feature | **Labels:** `feature`, `area:collision`, `area:core` | **Priority:** P0 | **Size:** M (5 h) | **Epic:** E09
- **Depends on:** M5-07, M5-08
- **Description:** Penetration depth and normal, plus an axis-separated move-and-slide helper for tile-based games.
- **Acceptance criteria:**
  - [ ] Penetration depth and normal exist for rect-rect, circle-circle and circle-rect.
  - [ ] `MoveAndSlide` moves a rectangle against rectangle obstacles and slides along walls without tunnelling up to the documented maximum speed.
  - [ ] Given a row of adjacent tiles, then there is no snagging on internal edges (regression test).
  - [ ] At least 20 unit tests.

## M5-10 Collision debug draw and wall demo
- **Type:** feature | **Labels:** `feature`, `area:collision`, `area:demo` | **Priority:** P1 | **Size:** S (3 h) | **Epic:** E09
- **Depends on:** M5-09, M3-10, M4-04
- **Description:** Visualise shapes and prove collision in a Sandbox scene.
- **Acceptance criteria:**
  - [ ] F4 toggles drawing of collision shapes through the debug primitives.
  - [ ] A Sandbox scene shows a sprite blocked by walls and sliding along them.
  - [ ] Given `--scene walls --autowalk`, then the process exits with code 0 only if the player stopped at the wall, so the check works headless.

## M5-11 Collision guide and release 0.2.0
- **Type:** chore | **Labels:** `chore`, `documentation`, `area:docs` | **Priority:** P0 | **Size:** S (3 h) | **Epic:** E09
- **Depends on:** M5-06, M5-10, M2-11
- **Description:** Document collision and cut the second pre-release.
- **Acceptance criteria:**
  - [ ] `docs/guides/collision.md` is written; the changelog has a 0.2.0 section; README features are updated.
  - [ ] The 0.1.0 release criteria are met again, and Sandbox demonstrates an effect and music.
  - [ ] Git tag `v0.2.0` and a GitHub pre-release.
