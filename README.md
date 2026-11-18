# Woad

> A lightweight, reusable 2D game engine for C# and .NET 11, built on OpenGL 3.3 Core.

**Status: pre-alpha.** Nothing is released yet. See the [roadmap](docs/roadmap.md).

Woad is both a learning project in graphics and engine programming and a portfolio project. It provides its own game loop, 2D renderer, input, audio, content management and collision utilities on top of [Silk.NET](https://github.com/dotnet/Silk.NET) (windowing, input, OpenGL, OpenAL). Game code never touches OpenGL directly.

It is deliberately **not** a Unity/Unreal competitor: no editor, no 3D, no scripting, no networking.

## Planned features

| Area | Highlights | Target release |
|---|---|---|
| Core | Game lifecycle, fixed-timestep loop, logging, configuration | 0.1 |
| Rendering | OpenGL 3.3 Core 2D renderer, sprites, batching, orthographic camera | 0.1 - 0.2 |
| Input | Keyboard and mouse with per-update pressed/released states | 0.2 |
| Content | Cached texture/audio loading with explicit ownership | 0.2 |
| Audio | OpenAL sound effects and streamed music | 0.2 |
| Collision | 2D shapes, intersection tests, ray/segment queries | 0.2 |
| Gameplay support | Sprite animation, scene stack, tilemaps | 0.3 |

## Quick start (planned API, not final)

```csharp
using Woad;

public sealed class MyGame : Game
{
    protected override void Update(in GameTime time) { }
    protected override void Draw(in FrameInfo frame) { }
}

new MyGame().Run(new EngineOptions { Title = "Hello Woad" });
```

## Requirements

- .NET 11 SDK (the exact version is pinned in `global.json`)
- A GPU and driver supporting OpenGL 3.3 Core
- Windows x64 or Linux x64 (see [ADR 0010](docs/decisions/0010-supported-platforms-and-linux-validation.md))

## Build and run

```bash
dotnet build
dotnet test
dotnet run --project samples/Sandbox
```

See [development setup](docs/development-setup.md) for details, including headless Linux validation.

## Documentation

- [Architecture overview](docs/architecture/overview.md)
- [Architecture decision records](docs/decisions/README.md)
- [Roadmap and risk register](docs/roadmap.md)
- [Documentation map](docs/README.md)

## License

To be decided in backlog issue M0-01.
