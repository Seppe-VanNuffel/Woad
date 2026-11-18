# ADR 0001: Target .NET 11 and pin the SDK

- **Status:** Accepted
- **Date:** 2026-11-15
- **Deciders:** Seppe

## Context

.NET 11 was released on 10 November 2026 as a Standard Term Support (STS) release, supported until November 2028. .NET 10 (LTS) has the same end-of-support date. The brief asks for .NET 11. Silk.NET 2.x packages target .NET Standard 2.0, .NET Core 3.1 and net5.0, so there is no net11-specific build.

## Decision

Target `net11.0`. Pin the SDK in `global.json` (`rollForward: latestPatch`). Manage package versions centrally in `Directory.Packages.props` with exact versions.

## Consequences

- STS means moving to .NET 12 (the next LTS, expected November 2027) is the natural next step; budget a small upgrade task.
- Silk.NET compatibility on net11 is assumed but unproven until spike M0-04.

## Alternatives considered

- `net10.0` (LTS): same support end date, fewer new features. This is the fallback if M0-04 finds a net11 problem.
- Multi-targeting `net10.0;net11.0`: only worth it at 1.0 if consumers need it.

## Validation and revisit triggers

M0-02 (build pinned), M0-04 (Silk.NET runs on net11). Revisit if Silk.NET or a native dependency fails on net11.
