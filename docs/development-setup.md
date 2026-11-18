# Development setup

Status: draft. Items marked (verify) are confirmed during milestone 0 spikes.

## Primary environment: Windows

1. Install the .NET SDK version pinned in `global.json` (.NET 11).
2. Install JetBrains Rider (or any editor with C# support).
3. Make sure your GPU driver supports OpenGL 3.3 Core (any GPU from the last decade does).
4. Clone, then:

```bash
dotnet restore
dotnet build -c Release
dotnet test
dotnet run --project samples/Sandbox
```

## Linux validation on a console-only machine (for example a Raspberry Pi)

A machine without a display server cannot open a real window. Instead, Woad is validated headlessly: a virtual X server (Xvfb) plus Mesa software rendering provides an OpenGL 3.3+ context, and OpenAL Soft runs with its null backend. This catches build, native-library, context-creation, shader-compilation and crash problems. It does **not** replace looking at the output on Windows.

Prerequisites on Debian/Raspberry Pi OS (verify package names in M0-05):

```bash
sudo apt install xvfb mesa-utils libgl1-mesa-dri libopenal1
# .NET 11 SDK for linux-arm64 (verify):
curl -sSL https://dot.net/v1/dotnet-install.sh -o dotnet-install.sh
chmod +x dotnet-install.sh && ./dotnet-install.sh --channel 11.0
```

Run from the repository root, over SSH if you like:

```bash
scripts/validate-linux.sh        # defaults to 120 frames
scripts/validate-linux.sh 600
```

Expected result: exit code 0 and a logged GL renderer/version line (3.3 or higher). See [ADR 0010](decisions/0010-supported-platforms-and-linux-validation.md).

Notes:
- The Pi is ARM64. GitHub Actions' ubuntu runners are x64, so both architectures get covered.
- Do not register the Pi as a self-hosted GitHub Actions runner for a public repository.

## Backlog tooling

`scripts/github/push_backlog.py` (Python 3.9+, GitHub CLI) validates the backlog files and creates the GitHub labels, milestones, epics and issues. Always run `--validate` and `--dry-run` first. See [backlog/README.md](backlog/README.md#pushing-the-backlog-to-github).

## Conventions

- Conventional Commits: `feat(graphics): ...`, `fix(core): ...`, `docs: ...`, `test(core): ...`.
- Trunk-based: short-lived branches, pull requests into `main` (self-reviewed), squash merge.
- Warnings are errors in CI. Nullable reference types are on.
