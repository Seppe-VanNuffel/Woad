# Woad.Core

The pure managed core of **Woad**, a lightweight 2D game engine for C# and .NET.

> **Pre-alpha placeholder.** Version 0.0.1-alpha reserves the package name and contains no functionality yet. Do not use it in your projects.

## What it will contain

Woad.Core is the part of the engine with no native or graphics dependencies:

- Maths: colours, rectangles, 2D transforms and cameras
- Collision: 2D shapes, overlap tests and ray/segment queries
- Timing: the fixed-timestep game loop logic
- Content: asset path handling and caching logic

Keeping this separate from the rendering engine means it can be unit-tested without a GPU.

## Status

Woad is under active planning and early development. See the repository for the roadmap and architecture decisions: https://github.com/Seppe-VanNuffel/Woad

## License

MIT