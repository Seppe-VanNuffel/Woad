# ADR 0011: Scope guard, no ECS, editor or scripting before 1.0

- **Status:** Proposed
- **Date:** 2026-11-15
- **Deciders:** Seppe

## Context

The brief lists strong non-goals but also schedules "basic entity/component composition" and "basic UI rendering". For a solo, part-time project, scope creep is the largest threat.

## Decision

Before 1.0 Woad will not include: ECS or any engine-level entity model, visual editor, scripting or hot reload, 3D, additional graphics backends, networking, rigid-body physics, async asset pipeline, gamepad/rebinding/input contexts, or a UI toolkit beyond the debug overlay.

Entity, UI and gameplay abstractions are *extracted* from the demo game only when duplication or pain is demonstrated. Any exception requires a new ADR. Work is limited to two issues in progress, and detailed issues exist only for the current and next milestone.

## Consequences

- A smaller, finishable engine. The demo may contain code that later moves into the engine.

## Alternatives considered

- Predictive design of an entity model up front: high risk of building the wrong thing.

## Validation and revisit triggers

Milestone reviews. Revisit only with evidence from the demo prototype.
