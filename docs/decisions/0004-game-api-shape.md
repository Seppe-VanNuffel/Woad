# ADR 0004: Game API shape, hybrid `Game` + `GameHost`

- **Status:** Proposed
- **Date:** 2026-11-15
- **Deciders:** Seppe

## Context

The brief sketches an inheritance-based `Game` with static-looking helpers (`Input.IsKeyDown`, `Assets.LoadTexture`) and a parameterless `Draw()`. Statics hurt testing and shutdown ordering; `Draw()` cannot receive a renderer or an interpolation alpha.

## Decision

A hybrid: an abstract `Game` base class for simplicity, running on a composable internal `GameHost`.

```csharp
// Tentative signatures.
public abstract class Game
{
    protected GameContext Context { get; }            // valid from Initialize onward
    protected virtual void Initialize() { }
    protected abstract void Update(in GameTime time); // fixed delta
    protected abstract void Draw(in FrameInfo frame); // M1; gains the renderer in M2/M3
    protected virtual void Shutdown() { }
    public void Run(EngineOptions? options = null);
}
```

- Services (window info, input, graphics, content, audio, logging, stats) are reached through `GameContext`, never statics.
- `Initialize` is synchronous in 0.x.
- `Draw` receives `Renderer2D` as soon as it exists (epic E03/E04). Changing it before 0.1 is an accepted, deliberate break.
- Exceptions from user code propagate out of `Run` after cleanup (see architecture overview, section 8).

## Consequences

- Easy to write a first game; testable host.
- `GameContext` must stay a thin bag of services, not become a service locator.

## Alternatives considered

- Pure composition (callbacks/delegates): flexible, more ceremony for beginners.
- Statics: shortest call sites, global state, harder tests.

## Validation and revisit triggers

M1-06 (lifecycle tests with fakes), Sandbox as first consumer (M1-11). Revisit if the demo needs multiple hosts or async initialisation.
