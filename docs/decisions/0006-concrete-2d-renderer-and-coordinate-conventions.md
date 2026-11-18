# ADR 0006: Concrete 2D renderer and coordinate conventions

- **Status:** Proposed
- **Date:** 2026-11-15
- **Deciders:** Seppe

## Context

Multiple graphics backends are a non-goal, so a renderer interface would be speculative. Coordinate and texture conventions are painful to change later.

## Decision

- Expose one sealed `Renderer2D` (`Begin(camera)`, `DrawSprite`, `DrawRectangle`, `End`). GL is fully internal. No `IRenderer` backend abstraction.
- **Coordinates:** +Y down, origin top-left, 1 world unit = 1 pixel at zoom 1, rotation in radians (clockwise on screen). The orthographic projection absorbs GL's Y-up clip space.
- **Textures:** uploaded unflipped; (0,0) is top-left; source rectangles in pixels; nearest filtering by default; atlas padding documented.
- **Blending:** straight alpha, source-alpha / one-minus-source-alpha by default.
- Culling disabled for 2D.

## Consequences

- Natural for tilemaps, pixel art and screen-space UI.
- Math-style Y-up users must flip; documented in the guide.

## Alternatives considered

- Y-up with origin bottom-left (math convention).
- World units = tiles (needs conversion for sub-tile movement and rendering).

## Validation and revisit triggers

M2 (textured quad orientation test), M3 (camera, world/screen conversion tests in Core).
