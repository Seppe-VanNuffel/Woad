# Milestone 0: Spike and scaffolding (epic E01)

**Goal:** a building, tested, CI-checked repository, and evidence that the technology stack works on Windows and on headless Linux (the Raspberry Pi).
**Budget:** about 3 weeks, roughly 37 hours.
**Exit criteria:** CI green on Windows and Linux; spike findings written up; ADRs 0001-0012 reviewed (M0-08); roadmap re-baselined.

Dependency order: M0-01 -> M0-02 -> (M0-03, M0-04, M0-06, M0-09) -> M0-05, M0-07 -> M0-08. M0-10 can happen any time.

---

## M0-01 Name verification and license choice
- **Type:** research | **Labels:** `research`, `area:build` | **Priority:** P0 | **Size:** S (2 h) | **Epic:** E01
- **Depends on:** none
- **Description:** The engine was renamed from Woad (a registered trademark) to Woad. Verify the new name properly before the repository goes public: Woad as GitHub repository/organisation name and NuGet package IDs (`Woad`, `Woad.Core`), including any prefix reservation, plus a trademark search for software classes. Note that an unrelated "woad" family of small terminal-colour libraries exists for Python, Ruby and Rust. Choose a licence (MIT or Apache-2.0). This is not legal advice.
- **Acceptance criteria:**
  - [ ] Repository name decided and repository created (private or public as chosen).
  - [ ] NuGet IDs `Woad` and `Woad.Core` confirmed free (no existing package, no reserved `Woad.` prefix by someone else); decision recorded on reserving the `Woad` prefix.
  - [ ] Trademark search (EUIPO TMview, WIPO Global Brand Database; classes 9, 41, 42) summarised in 3-5 lines in an issue comment, with a proceed/rename decision.
  - [ ] Licence chosen; licence text ready for M0-02.

## M0-02 Scaffold repository and solution
- **Type:** chore | **Labels:** `chore`, `area:build` | **Priority:** P0 | **Size:** M (5 h) | **Epic:** E01
- **Depends on:** M0-01
- **Description:** Create the solution structure from the [architecture overview](../architecture/overview.md): `src/Woad.Core`, `src/Woad`, `tests/Woad.Core.Tests`, `tests/Woad.Tests`, `samples/Sandbox`.
- **Acceptance criteria:**
  - [ ] Given a clean clone on Windows with the SDK from `global.json`, when I run `dotnet build -c Release`, then it succeeds with zero warnings.
  - [ ] `global.json` pins the .NET 11 SDK with `rollForward: latestPatch`.
  - [ ] `Directory.Build.props` enables nullable reference types, `TreatWarningsAsErrors` in CI/Release, `EnforceCodeStyleInBuild`, and deterministic builds.
  - [ ] `Directory.Packages.props` uses central package management with exact versions for Silk.NET 2.x, StbImageSharp, Microsoft.Extensions.Logging.Abstractions, xUnit and Microsoft.NET.Test.Sdk.
  - [ ] `.editorconfig`, `.gitignore`, `LICENSE` and a README skeleton are committed.
  - [ ] `dotnet test` runs one passing placeholder test in each test project.
  - [ ] The solution opens in Rider without errors.

## M0-03 CI workflow: build and test on Windows and Linux
- **Type:** ci | **Labels:** `ci`, `area:build` | **Priority:** P0 | **Size:** S (3 h) | **Epic:** E01
- **Depends on:** M0-02
- **Description:** GitHub Actions workflow that restores, builds (Release) and tests on `windows-latest` and `ubuntu-latest`, using the SDK pinned in `global.json`.
- **Acceptance criteria:**
  - [ ] Workflow runs on pushes to `main` and on pull requests.
  - [ ] Both operating systems build and test successfully.
  - [ ] Given a deliberately failing test on a branch, when the workflow runs, then it fails; the test is then removed.
  - [ ] NuGet packages are cached; a typical run takes under 5 minutes.
  - [ ] A build status badge is in the README.

## M0-04 Spike: Silk.NET 2.x on .NET 11, window and GL 3.3 Core (Windows)
- **Type:** research | **Labels:** `research`, `area:platform`, `area:graphics` | **Priority:** P0 | **Size:** M (6 h) | **Epic:** E01
- **Depends on:** M0-02
- **Description:** Throwaway code (kept out of the solution) that opens a window requesting OpenGL 3.3 Core with the forward-compatible hint, clears the screen, draws an indexed triangle with a shader, and prints `GL_VERSION` and `GL_RENDERER`.
- **Acceptance criteria:**
  - [ ] It builds and runs on the pinned .NET 11 SDK on Windows with exact Silk.NET versions recorded.
  - [ ] A triangle is visible; the GL version line shows 3.3 or higher, Core profile.
  - [ ] Window closes cleanly; no unmanaged crash or GL error.
  - [ ] Findings are written in `docs/spikes/m0-silk-net11.md`: versions used, warnings, anything surprising, whether the native GLFW binary was bundled.
  - [ ] Recommendation recorded: stay on Silk.NET 2.x, or alternative if it failed ([ADR 0001](../decisions/0001-target-dotnet-11.md), [ADR 0002](../decisions/0002-opengl-33-core-with-silknet-2x.md)).

## M0-05 Spike: headless Linux validation on the Raspberry Pi
- **Type:** research | **Labels:** `research`, `area:platform`, `area:build` | **Priority:** P0 | **Size:** M (5 h) | **Epic:** E01
- **Depends on:** M0-04
- **Description:** The Pi has no GUI. Run the M0-04 spike over SSH under Xvfb with Mesa software rendering. Install the .NET 11 SDK for ARM64, work out the required apt packages, and turn the draft `scripts/validate-linux.sh` into a verified script. Find out whether Silk.NET's bundled GLFW provides a `linux-arm64` binary or a system library is needed.
- **Acceptance criteria:**
  - [ ] Given a console-only Pi with the documented prerequisites, when I run `scripts/validate-linux.sh`, then it exits 0 and logs a GL version of 3.3 or higher.
  - [ ] .NET 11 SDK install steps for ARM64 and the exact apt packages are documented in `docs/development-setup.md`.
  - [ ] Spike code supports an auto-exit option so it can run unattended.
  - [ ] Findings in `docs/spikes/m0-linux-headless.md` cover: GLFW native binary availability on ARM64, which GL renderer string appears, run time, anything that needed a workaround.
  - [ ] Optional experiment recorded: same script on `ubuntu-latest` in GitHub Actions (works / does not work).
  - [ ] [ADR 0010](../decisions/0010-supported-platforms-and-linux-validation.md) updated if findings contradict it.

## M0-06 Spike: OpenAL through Silk.NET and Ogg decoder candidate
- **Type:** research | **Labels:** `research`, `area:audio` | **Priority:** P1 | **Size:** M (5 h) | **Epic:** E01
- **Depends on:** M0-02
- **Description:** Initialise an OpenAL device, play a generated 440 Hz tone for one second, and dispose everything. Check native OpenAL Soft availability for win-x64, linux-x64 and linux-arm64. Evaluate NVorbis (or another managed Ogg Vorbis decoder) for net11 compatibility and licence.
- **Acceptance criteria:**
  - [ ] Windows: the tone plays; device, context, source and buffer are released with no AL errors.
  - [ ] Pi: with `ALSOFT_DRIVERS=null`, the same program initialises, "plays" and exits 0.
  - [ ] Findings in `docs/spikes/m0-openal.md`: which packages supply OpenAL Soft per runtime, whether a system `libopenal` is needed on Linux, decoder candidate verdict.
  - [ ] [ADR 0012](../decisions/0012-audio-stack.md) updated to Accepted, Amended or Rejected.

## M0-07 Spike: owning the main loop
- **Type:** research | **Labels:** `research`, `area:platform` | **Priority:** P0 | **Size:** S (3 h) | **Epic:** E01
- **Depends on:** M0-04
- **Description:** Check that a Silk.NET window can be driven manually (initialise, poll events, swap buffers) instead of through `Run()`, and that a fixed-step accumulator works on top of it.
- **Acceptance criteria:**
  - [ ] Manual loop works: window events, close button and resize are delivered.
  - [ ] Vsync can be toggled; frame time min/avg/max recorded over 60 s with vsync on and off on Windows.
  - [ ] Behaviour during window drag/resize noted (does the loop stall?).
  - [ ] Recommendation recorded; if manual driving is not viable, the fallback is written into [ADR 0005](../decisions/0005-window-context-ownership-and-owned-loop.md).

## M0-08 Review ADRs and re-baseline the roadmap
- **Type:** documentation | **Labels:** `documentation` | **Priority:** P0 | **Size:** S (2 h) | **Epic:** E01
- **Depends on:** M0-04, M0-05, M0-06, M0-07
- **Description:** Compare spike results with ADRs 0001-0012; update statuses; replace estimates with real hours.
- **Acceptance criteria:**
  - [ ] Every ADR is marked Accepted, Amended or Rejected with a date.
  - [ ] [roadmap.md](../roadmap.md) estimates and risk register updated with M0 actuals and any new risks.
  - [ ] M1 issues confirmed or adjusted.

## M0-09 Documentation skeleton
- **Type:** documentation | **Labels:** `documentation`, `area:docs` | **Priority:** P1 | **Size:** S (3 h) | **Epic:** E01
- **Depends on:** M0-02
- **Description:** Commit the `docs/` tree, ADR template and index, README draft, architecture overview and development setup.
- **Acceptance criteria:**
  - [ ] `docs/` structure matches the [documentation map](../README.md).
  - [ ] README, architecture overview, development setup, ADR index and template are committed.
  - [ ] All relative links resolve.

## M0-10 GitHub project setup
- **Type:** chore | **Labels:** `chore`, `area:build` | **Priority:** P1 | **Size:** S (3 h) | **Epic:** E01
- **Depends on:** none
- **Description:** Configure GitHub for the backlog described in [README.md](README.md), using `scripts/github/push_backlog.py` for labels, milestones, epics and issues.
- **Acceptance criteria:**
  - [ ] Labels created as listed in the conventions.
  - [ ] Milestones M0-M8 created.
  - [ ] Project board with the documented columns and fields.
  - [ ] Issue templates (feature, spike, bug) and a pull request template with the Definition of Done checklist.
  - [ ] After reviewing `python scripts/github/push_backlog.py --repo OWNER/REPO --dry-run`, the script has created all labels, GitHub milestones, epics and issues (`--validate` and `--dry-run` were clean first).
