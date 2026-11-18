# Milestone 7: Hardening and release (epics E11, E13)

**Goal:** make the engine distributable: stable API surface, documentation, leak audit, benchmarks, packaging and a release pipeline.
**Budget:** about 3 weeks, roughly 37 hours (tight; NuGet publishing is on the cut list, local packages are enough).
**Detail:** provisional
**Exit criteria:** release candidate `v1.0.0-rc.1` with packages built from a tag, a verified getting-started guide and a clean leak audit.

## M7-01 Public API review
- **Type:** documentation | **Labels:** `documentation`, `area:core` | **Priority:** P0 | **Size:** M (5 h) | **Epic:** E11
- **Depends on:** M6-08
- **Description:** Review every public type and member before the API is frozen.
- **Acceptance criteria:**
  - [ ] `docs/api-review.md` lists each public type with a keep, internalise or rename decision.
  - [ ] Naming is consistent, types are sealed by default, and there are no public mutable statics.
  - [ ] Breaking changes are listed in the changelog.
  - [ ] [ADR 0004](../decisions/0004-game-api-shape.md) and the architecture overview match the final API.

## M7-02 PublicApiAnalyzers and API baseline
- **Type:** ci | **Labels:** `ci`, `area:build` | **Priority:** P0 | **Size:** S (3 h) | **Epic:** E11
- **Depends on:** M7-01
- **Description:** Make accidental API changes fail the build.
- **Acceptance criteria:**
  - [ ] The analyzer package is referenced centrally; `PublicAPI.Shipped.txt` and `PublicAPI.Unshipped.txt` exist for both assemblies.
  - [ ] Given a new public member without a baseline update, then CI fails.
  - [ ] The process is documented in `docs/development-setup.md`.

## M7-03 XML documentation and analyzer cleanup
- **Type:** chore | **Labels:** `chore`, `area:build`, `area:docs` | **Priority:** P1 | **Size:** S (3 h) | **Epic:** E11
- **Depends on:** M7-01
- **Description:** Enforce documentation and code-style quality gates.
- **Acceptance criteria:**
  - [ ] CS1591 is an error for public API; the analysis level is set; nullable warnings are zero.
  - [ ] `dotnet format --verify-no-changes` passes in CI.
  - [ ] Every suppression has a justification comment.

## M7-04 Resource lifecycle audit
- **Type:** testing | **Labels:** `testing`, `area:graphics`, `area:audio` | **Priority:** P0 | **Size:** M (5 h) | **Epic:** E11
- **Depends on:** M6-08
- **Description:** Verify [ADR 0007](../decisions/0007-threading-and-resource-ownership.md) holds across the whole engine.
- **Acceptance criteria:**
  - [ ] Every `IDisposable` type is reviewed; findings go in `docs/notes/lifecycle-audit.md`.
  - [ ] A stress test creates and disposes 1,000 textures and 100 audio sources, and the leak tracker reports zero.
  - [ ] Sandbox scenes shut down with no leak warnings.
  - [ ] Exceptions during disposal are logged and never mask each other.

## M7-05 Benchmarks and profiling pass
- **Type:** testing | **Labels:** `testing`, `area:core`, `area:graphics` | **Priority:** P1 | **Size:** M (5 h) | **Epic:** E11
- **Depends on:** M6-08
- **Description:** Measure before claiming performance.
- **Acceptance criteria:**
  - [ ] A BenchmarkDotNet project covers timestep, collision, quad generation and tile-range computation; results are stored in `docs/performance.md`.
  - [ ] Steady-state allocations are zero per frame in the Sandbox scenes, or exceptions are documented.
  - [ ] Frame time of the 10,000-sprite scene is measured on Windows and recorded; at least one hotspot is investigated.

## M7-06 Cross-platform validation pass
- **Type:** testing | **Labels:** `testing`, `area:platform` | **Priority:** P0 | **Size:** S (3 h) | **Epic:** E11
- **Depends on:** M6-08
- **Description:** Verify the claims in [ADR 0010](../decisions/0010-supported-platforms-and-linux-validation.md) against the current commit.
- **Acceptance criteria:**
  - [ ] `docs/supported-platforms.md` has a matrix: Windows x64 (full), Linux x64 (CI headless), Linux ARM64 (Pi headless, best effort), macOS (unsupported).
  - [ ] Each row has evidence from the current commit (CI run link or log excerpt).
  - [ ] Problems found are fixed or listed as known limitations.

## M7-07 NuGet packaging
- **Type:** chore | **Labels:** `chore`, `area:build` | **Priority:** P1 | **Size:** M (4 h) | **Epic:** E11
- **Depends on:** M7-02, M7-03
- **Description:** Pack `Woad.Core` and `Woad`.
- **Acceptance criteria:**
  - [ ] Both packages pack with metadata, README, licence, symbols and SourceLink in a deterministic build.
  - [ ] A fresh project referencing the local package builds and shows a window (documented test).
  - [ ] The packaging layout is recorded as ADR 0013.
  - [ ] Native dependencies and runtime requirements are listed in the package README.

## M7-08 Release workflow on tag
- **Type:** ci | **Labels:** `ci`, `area:build` | **Priority:** P1 | **Size:** S (3 h) | **Epic:** E11
- **Depends on:** M7-07
- **Description:** GitHub Actions workflow that turns a version tag into a GitHub release.
- **Acceptance criteria:**
  - [ ] On a `v*` tag, the workflow builds, tests, packs and attaches the packages and changelog notes to a GitHub release.
  - [ ] Publishing to NuGet is behind a manual approval and a secret, and disabled by default.
  - [ ] A tag with a pre-release suffix (for example `-rc.1`) is marked as a pre-release.

## M7-09 Getting-started guide and CONTRIBUTING
- **Type:** documentation | **Labels:** `documentation`, `area:docs` | **Priority:** P0 | **Size:** M (4 h) | **Epic:** E13
- **Depends on:** M7-01
- **Description:** A tutorial from an empty project to a moving sprite with sound, and contribution guidelines.
- **Acceptance criteria:**
  - [ ] `docs/getting-started/` covers an empty project to a moving, animated sprite with sound.
  - [ ] The guide was followed from scratch on a clean machine or VM and fixed wherever it failed.
  - [ ] `CONTRIBUTING.md` (commits, build, tests, API baseline process) and the issue and pull request templates are committed.

## M7-10 Release 1.0.0-rc.1
- **Type:** chore | **Labels:** `chore`, `area:build` | **Priority:** P0 | **Size:** S (2 h) | **Epic:** E11
- **Depends on:** M7-04, M7-05, M7-06, M7-08, M7-09
- **Description:** Release candidate.
- **Acceptance criteria:**
  - [ ] All M7 issues are closed and known issues are listed in the release notes.
  - [ ] Documentation links are checked, and the documentation map has no Planned rows except post-1.0 items.
  - [ ] Tag `v1.0.0-rc.1` produces a GitHub pre-release with the packages attached.
