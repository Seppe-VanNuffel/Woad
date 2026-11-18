# Milestone 2: Graphics fundamentals (epic E03)

**Goal:** learn and implement the OpenGL 3.3 Core pipeline (shaders, buffers, textures), ending with a textured rectangle and release 0.1.0.
**Budget:** about 4 weeks, roughly 41 hours.
**Detail:** detailed
**Exit criteria:** GraphicsLab shows a coloured triangle and a correctly oriented textured rectangle on Windows; headless smoke passes with zero GL errors; release 0.1.0 tagged.

## M2-01 GraphicsDevice with GL error checking
- **Type:** feature | **Labels:** `feature`, `area:graphics` | **Priority:** P0 | **Size:** M (5 h) | **Epic:** E03
- **Depends on:** M1-06
- **Description:** Internal `GraphicsDevice`, created by the host from the window's GL context ([ADR 0005](../decisions/0005-window-context-ownership-and-owned-loop.md)). It wraps viewport and clear, logs GL vendor/renderer/version, and provides error checking.
- **Acceptance criteria:**
  - [ ] Given a debug build, when a GL call produces an error, then `CheckError(context)` throws `GraphicsException` naming the call site; in release builds checking is disabled unless enabled by option.
  - [ ] Given KHR_debug is available, then debug output is routed to the logger at matching levels.
  - [ ] The host creates the device after the window and disposes it before the window (disposal-order test from M1-07 updated).
  - [ ] Graphics types assert main-thread access and do not reference `Woad.Platform` types (M1-10 tests stay green).

## M2-02 Native object leak tracker
- **Type:** feature | **Labels:** `feature`, `area:graphics`, `area:diagnostics` | **Priority:** P0 | **Size:** S (3 h) | **Epic:** E03
- **Depends on:** M2-01
- **Description:** Debug-only registry of live GL objects ([ADR 0007](../decisions/0007-threading-and-resource-ownership.md)); the same mechanism is reused for audio objects later.
- **Acceptance criteria:**
  - [ ] Given a debug build, when a GL object wrapper is created, then it registers with a name and creation stack.
  - [ ] Given objects still alive at `GraphicsDevice` disposal, then each is logged as a warning with name and creation stack, and the total count is reported.
  - [ ] Release builds incur no tracking overhead (conditional compilation).
  - [ ] Unit tests with a fake registry cover register, release, double release and leak report.

## M2-03 Shader program with compile and link diagnostics
- **Type:** feature | **Labels:** `feature`, `area:graphics` | **Priority:** P0 | **Size:** M (5 h) | **Epic:** E03
- **Depends on:** M2-01
- **Description:** Internal shader program wrapper for vertex and fragment stages using `#version 330 core`.
- **Acceptance criteria:**
  - [ ] Given valid vertex and fragment sources, then a program compiles, links and can be used.
  - [ ] Given invalid GLSL, then `ShaderCompilationException` includes the stage, shader name and the driver log.
  - [ ] Given a link failure, then the exception includes the program log.
  - [ ] Uniform locations are cached; setting an unknown uniform logs once and does not throw.
  - [ ] Shader sources are embedded resources; disposal deletes program and shaders and is tracked by M2-02.

## M2-04 Vertex buffers, index buffers and vertex arrays
- **Type:** feature | **Labels:** `feature`, `area:graphics` | **Priority:** P0 | **Size:** M (5 h) | **Epic:** E03
- **Depends on:** M2-01, M2-02
- **Description:** Internal wrappers with a vertex layout description (attribute index, component count, type, offset) that configures the VAO.
- **Acceptance criteria:**
  - [ ] Layout-to-stride and offset computation is a pure function with unit tests.
  - [ ] Static and dynamic buffers can be created, updated with sub-data and disposed.
  - [ ] Given an update larger than the buffer capacity, then `ArgumentException` is thrown instead of a GL error.
  - [ ] Given use after dispose, then `ObjectDisposedException`; all objects are tracked by M2-02.

## M2-05 GraphicsLab project and coloured triangle
- **Type:** feature | **Labels:** `feature`, `area:graphics`, `area:build` | **Priority:** P0 | **Size:** S (3 h) | **Epic:** E03
- **Depends on:** M2-03, M2-04
- **Description:** Create `samples/GraphicsLab`, a sample with `InternalsVisibleTo` access for low-level scenes. It is the only sample allowed to use internals; Sandbox stays public-API-only. First scene: an indexed triangle with per-vertex colours.
- **Acceptance criteria:**
  - [ ] Scenes are selected with `--scene triangle`; an unknown scene prints usage and exits with code 2.
  - [ ] The triangle renders correctly on Windows and a screenshot is saved under `docs/images/`.
  - [ ] The architecture overview documents the GraphicsLab exception.
  - [ ] Given `--frames 120`, then it exits with code 0 and logs zero GL errors.

## M2-06 ImageData and PNG decoding
- **Type:** feature | **Labels:** `feature`, `area:content`, `area:core` | **Priority:** P0 | **Size:** S (3 h) | **Epic:** E03
- **Depends on:** M0-02
- **Description:** `ImageData` (width, height, RGBA8 pixels) lives in `Woad.Core`; decoding uses StbImageSharp in `Woad`.
- **Acceptance criteria:**
  - [ ] Given a PNG with alpha, then decoding returns RGBA8 of the expected size with alpha preserved and no vertical flip.
  - [ ] Given a corrupt or truncated file, then a descriptive exception names the file (wrapped later by content loading).
  - [ ] `ImageData` validates that the pixel buffer length equals width x height x 4.
  - [ ] Tests use small test images checked into the test project.

## M2-07 Texture2D with filtering and wrapping
- **Type:** feature | **Labels:** `feature`, `area:graphics` | **Priority:** P0 | **Size:** M (5 h) | **Epic:** E03
- **Depends on:** M2-01, M2-02, M2-06
- **Description:** Public `Texture2D` created from `ImageData`, with no GL types exposed.
- **Acceptance criteria:**
  - [ ] Given `ImageData`, then a texture is created with Width and Height properties.
  - [ ] Filtering (nearest by default, linear option) and wrapping (clamp by default, repeat option) are configurable.
  - [ ] Given an image whose width is not a multiple of 4 (for example 3 px), then it displays without skew (unpack alignment handled).
  - [ ] Disposal deletes the GL texture, is tracked by M2-02, and use after dispose throws.

## M2-08 Textured rectangle in GraphicsLab
- **Type:** feature | **Labels:** `feature`, `area:graphics` | **Priority:** P0 | **Size:** M (4 h) | **Epic:** E03
- **Depends on:** M2-05, M2-07
- **Description:** Second GraphicsLab scene that draws a textured rectangle following the conventions in [ADR 0006](../decisions/0006-concrete-2d-renderer-and-coordinate-conventions.md).
- **Acceptance criteria:**
  - [ ] `--scene texture` shows an asymmetric test image (a letter F) upright and unmirrored.
  - [ ] Transparent pixels blend with the background using straight alpha.
  - [ ] Resizing the window keeps the image at its pixel size and undistorted.
  - [ ] A screenshot is saved under `docs/images/`.

## M2-09 GL smoke checks on Linux
- **Type:** testing | **Labels:** `testing`, `ci`, `area:platform` | **Priority:** P1 | **Size:** S (2 h) | **Epic:** E03
- **Depends on:** M2-08, M1-12
- **Description:** Extend `scripts/validate-linux.sh` to run the GraphicsLab scenes.
- **Acceptance criteria:**
  - [ ] The script runs Sandbox plus GraphicsLab scenes `triangle` and `texture` for a fixed number of frames.
  - [ ] The run fails if any GL error is logged.
  - [ ] It passes on the Raspberry Pi and in the CI `linux-smoke` job.

## M2-10 Rendering pipeline guide (draft)
- **Type:** documentation | **Labels:** `documentation`, `area:docs` | **Priority:** P1 | **Size:** S (3 h) | **Epic:** E03
- **Depends on:** M2-08
- **Description:** First draft of `docs/guides/rendering.md`, written while the knowledge is fresh.
- **Acceptance criteria:**
  - [ ] Explains pipeline stages, buffers and VAO, shaders, textures and the conventions from ADR 0006, with one diagram.
  - [ ] Every code excerpt matches the current source (checked and noted in the PR).
  - [ ] Documentation map marks the guide as Draft.

## M2-11 Release 0.1.0
- **Type:** chore | **Labels:** `chore`, `area:build` | **Priority:** P0 | **Size:** S (3 h) | **Epic:** E03
- **Depends on:** M2-09, M2-10, M1-13
- **Description:** First tagged pre-release.
- **Acceptance criteria:**
  - [ ] `CHANGELOG.md` has a 0.1.0 section; README status and feature table are updated.
  - [ ] Given a clean clone, when following the development setup, then build, tests, Sandbox and GraphicsLab all run.
  - [ ] CI is green on Windows and Linux, and the headless smoke test is green.
  - [ ] Git tag `v0.1.0` and a GitHub pre-release with notes, including known limitations.
