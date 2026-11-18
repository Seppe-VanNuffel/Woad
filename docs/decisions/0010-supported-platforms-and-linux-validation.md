# ADR 0010: Supported platforms and Linux validation

- **Status:** Proposed
- **Date:** 2026-11-15
- **Deciders:** Seppe

## Context

Development happens on Windows. The only Linux machine is a Raspberry Pi running Linux with no GUI (console only), which is ARM64. A console-only machine cannot open a window, but can run a virtual X server with Mesa software rendering. GitHub-hosted Ubuntu runners are x64. macOS OpenGL is deprecated and capped below modern versions.

## Decision

- **Supported for 0.x and 1.0:** Windows x64 and Linux x64. Both are built and unit-tested in CI.
- **Linux validation is headless:** Xvfb + Mesa software GL (`LIBGL_ALWAYS_SOFTWARE=1`) + OpenAL Soft null backend (`ALSOFT_DRIVERS=null`), driven by `scripts/validate-linux.sh` and Sandbox's `--frames N` mode.
- **Linux ARM64** (the Pi) is smoke-tested headless and documented as best-effort, subject to native libraries being available (verified in M0-05/M0-06).
- **macOS** is unsupported for now; it may become best-effort after 1.0.
- Visual correctness is checked on Windows. Linux checks prove: builds, native libraries load, a GL 3.3 Core context is created, shaders compile, frames render without GL errors, clean exit.
- The Pi is not registered as a self-hosted runner for a public repository.

## Consequences

- Linux rendering differences between software and real GPU drivers are not caught. Accepted and listed in the risk register.
- A Linux desktop or VM would improve coverage later; adding one would amend this ADR.

## Alternatives considered

- Windows only: weaker cross-platform claim for a portfolio project.
- Self-hosted runner on the Pi: security risk on a public repo.

## Validation and revisit triggers

M0-05 (spike on the Pi), M1-12 (smoke test in CI and on the Pi). Revisit if software GL cannot provide a 3.3 Core context or native ARM64 libraries are missing.
