# ADR 0009: Asset identity and synchronous-first loading

- **Status:** Proposed
- **Date:** 2026-11-15
- **Deciders:** Seppe

## Context

Assets need stable identity and predictable caching. Windows paths are case-insensitive, Linux paths are not, so a game that loads on Windows can fail on Linux.

## Decision

- Asset identity is a normalised relative path under a content root: `/` separators, case-exact, no `..` escape. Cache key is (asset type, normalised path).
- Default content root: `<app base directory>/Content`, configurable in `EngineOptions`.
- Loading is synchronous in 0.x. Decoding (for example StbImageSharp to `ImageData`) is separate from GPU upload (`Texture2D` creation) so async decode can be added later.
- In debug builds on case-insensitive systems, verify the exact case on disk and warn on mismatch.
- Errors raise `ContentLoadException` with the requested path, resolved path and cause.
- No manifests, handles or hot reload before 1.0.

## Consequences

- Cross-platform path bugs are caught on Windows, and path normalisation is a pure, well-tested Core component.
- Typed handles can be layered on later without changing identity.

## Alternatives considered

- Numeric IDs or GUIDs: need a build step or manifest; rejected as premature.
- Async-first: more complexity before there is a need.

## Validation and revisit triggers

M4 content epic (path and cache tests in `Woad.Core.Tests`). Revisit if load hitches are visible in the demo.
