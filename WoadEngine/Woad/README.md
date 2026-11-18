# Woad

A lightweight 2D game engine for C# and .NET, built on OpenGL 3.3 Core.

> **Pre-alpha placeholder.** Version 0.0.1-alpha reserves the package name and contains no functionality yet. Do not use it in your projects.

## What it will be

Woad provides the pieces a small 2D game needs, without an editor or scripting layer:

- A game loop with a fixed timestep
- A sprite renderer with batching and a 2D camera
- Keyboard and mouse input
- Content loading with explicit ownership
- Sound effects and streamed music
- 2D collision, animation, scenes and tilemaps

It is built on Silk.NET, but game code never touches OpenGL directly.

## Requirements (planned)

- .NET 11
- A GPU and driver supporting OpenGL 3.3 Core
- Windows x64 and Linux x64

## Status

Woad is under active planning and early development. See the repository for the roadmap and architecture decisions: https://github.com/Seppe-VanNuffel/Woad

## License

MIT