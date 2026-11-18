# Backlog conventions

How the Woad backlog is organised in GitHub. Epics are in [epics.md](epics.md); issues are in `milestone-0.md` to `milestone-8.md`. Milestones M0-M2 are detailed; M3-M8 are marked **provisional** (they get the `provisional` label) and are revisited when the previous milestone finishes. These Markdown files are the single source of truth: `scripts/github/push_backlog.py` creates the GitHub issues from them.

## Hierarchy

Epic -> issues (user story, technical task, spike, documentation, testing, chore). Link children to the epic with GitHub sub-issues or a task list. Each issue below has a **Plan ID** (for example `M1-06`); put it in the issue title prefix or body so dependencies stay readable.

User stories ("As a game developer, I want ... so that ...") are used only for game-developer-facing behaviour. Internal work is a plain technical task or a spike.

## Issue types

| Type | Use for | Output |
|---|---|---|
| `feature` | New capability | Code, tests, docs |
| `research` (spike) | Unknowns; time-boxed | Written findings in `docs/spikes/` plus a recommendation; code is throwaway |
| `testing` | Test infrastructure, architecture tests | Tests |
| `ci` / `chore` | Tooling, repo hygiene | Config |
| `documentation` | Docs without code changes | Docs |
| `bug` | Defects | Fix plus regression test |

## Labels

- Type: `epic`, `feature`, `bug`, `documentation`, `testing`, `research`, `chore`, `ci`
- Area: `area:core`, `area:platform`, `area:graphics`, `area:input`, `area:content`, `area:audio`, `area:collision`, `area:diagnostics`, `area:demo`, `area:docs`, `area:build`
- Milestone: `milestone:M0` ... `milestone:M8` (also created as real GitHub milestones)
- Priority: `P0` (blocks the milestone), `P1`, `P2`
- Size: `size:S` (up to 3 h), `size:M` (3-8 h), `size:L` (8-16 h). Anything over 16 h must be split.
- Other: `provisional` (detail will be revisited), `good first issue` (if the project ever takes contributors)

## GitHub Project

Board columns: Backlog, Ready, In progress, In review, Done. Custom fields: Priority, Size, Epic, Milestone, Target release. GitHub milestones: M0 to M8, each with its due date set after the roadmap re-baseline.

## Definition of Ready

- Clear title and description; type and size set.
- Acceptance criteria are testable (Given/When/Then or checklist).
- Dependencies are linked as blocked-by.
- Fits in 16 hours or less.

## Definition of Done

- Builds with zero warnings; all tests pass in CI on Windows and Linux.
- Acceptance criteria met and ticked.
- Unit tests for deterministic logic; Sandbox scene or manual check noted for graphics/audio.
- Graphics-related changes: headless Linux smoke test passes.
- Public API has XML docs; relevant docs and ADRs updated; changelog entry for user-visible changes.
- No `TODO` left without an issue.

## Workflow

Trunk-based: short-lived branches, pull requests into `main` (self-review against the Definition of Done), squash merge, Conventional Commits. Releases are git tags.

## Issue format (what the script parses)

```markdown
## M1-06 Title of the issue
- **Type:** feature (user story) | **Labels:** `feature`, `area:core` | **Priority:** P0 | **Size:** L (8 h) | **Epic:** E02
- **Depends on:** M1-01, M1-02
- **Description:** One paragraph.
- **Acceptance criteria:**
  - [ ] Testable criterion.
```

Rules: IDs are `M<milestone>-<nn>`; one `## ` block per issue; sizes S (up to 3 h), M (3-8 h), L (8-16 h); "Blocks" is computed from "Depends on". Run `python scripts/github/push_backlog.py --validate` after every edit.

## Pushing the backlog to GitHub

Prerequisites: [GitHub CLI](https://cli.github.com/) installed and logged in (`gh auth login`), Python 3.9+, and an existing (empty) repository.

```bash
python scripts/github/push_backlog.py --validate                          # parse and check only
python scripts/github/push_backlog.py --repo OWNER/REPO --dry-run         # show what would happen, offline
python scripts/github/push_backlog.py --repo OWNER/REPO --milestones M0,M1  # push only some milestones
python scripts/github/push_backlog.py --repo OWNER/REPO                   # push everything
```

What it creates: all labels (including one `milestone:Mx` label per milestone), the nine GitHub milestones, one issue per epic, and one issue per backlog item with its milestone, labels, acceptance criteria as a task list, and "blocked by" references. Issues carry their Plan ID in the title (`[M1-06] ...`), so re-running the script skips anything that already exists. Optional flags: `--project OWNER/NUMBER` (add items to a Projects v2 board), `--sub-issues` and `--blocked-by` (best-effort native GitHub links), `--relink` (refresh epic checklists), `--delay` (seconds between API calls). Run `--help` for details.
