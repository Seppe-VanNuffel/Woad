# ADR 0007: Threading model and resource ownership

- **Status:** Proposed
- **Date:** 2026-11-15
- **Deciders:** Seppe

## Context

OpenGL and OpenAL contexts are bound to a thread, and GPU objects must be created and destroyed on it. A simple, predictable ownership model matters more than cleverness for a solo project.

## Decision

**Threading**
- One main thread owns the window, GL context, OpenAL context and input. Debug builds assert it (`MainThread.Assert()`).
- Worker threads may do file I/O and decoding only. Results return through a main-thread queue drained at the start of each frame.
- In 0.x, loading is synchronous; the decode/upload split keeps async possible.

**Ownership**
- The creator owns a resource and disposes it. `ContentManager` owns what it loads and disposes it on `Dispose`.
- No reference counting or handles initially.
- `Dispose` is idempotent; use after dispose throws `ObjectDisposedException`.
- No finalizers release GL/AL objects. Debug builds track live native objects and log leaks at shutdown.

## Consequences

- Simple mental model, easy leak detection.
- Games that want to unload a subset of assets need multiple `ContentManager` instances.

## Alternatives considered

- Reference counting: more bookkeeping, easy to get wrong.
- Finalizer-based cleanup: runs on the finalizer thread, invalid for GL.
- Handles/IDs: useful later for hot reload, unnecessary now.

## Validation and revisit triggers

M1-05 (main-thread assertions), M2 (leak tracker on GL objects), M7 resource lifecycle audit. Revisit if the demo needs partial unloading.
