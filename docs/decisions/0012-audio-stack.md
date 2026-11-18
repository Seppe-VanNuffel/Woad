# ADR 0012: Audio stack, OpenAL with WAV and Ogg Vorbis

- **Status:** Proposed (pending spike M0-06)
- **Date:** 2026-11-15
- **Deciders:** Seppe

## Context

The brief names Silk.NET.OpenAL. Native OpenAL Soft packaging per runtime, decoding formats and behaviour on machines without audio hardware (including the headless Pi) are unproven.

## Decision

- Low-level API: OpenAL via Silk.NET.OpenAL, internal.
- Formats: PCM WAV for sound effects; Ogg Vorbis for music via a managed decoder (NVorbis is the candidate; verify net11 compatibility and licence in M0-06). MP3 and FLAC are deferred.
- Streaming music uses at least three buffers per source, refilled once per frame on the main thread.
- If no audio device can be opened, log a warning and use a null audio device; the game keeps running.
- Headless Linux uses `ALSOFT_DRIVERS=null`.

## Consequences

- No native audio decoding dependency beyond OpenAL Soft.
- Per-frame refill couples music continuity to frame rate stability; acceptable with generous buffer sizes.

## Alternatives considered

- Other audio libraries (SDL audio, miniaudio bindings): different native dependency, less aligned with the brief.
- Commercial middleware: licensing and scope.

## Validation and revisit triggers

M0-06 (device init, tone playback, native package coverage for win-x64, linux-x64, linux-arm64, decoder evaluation). Amend after the spike.
