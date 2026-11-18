# Security policy

## Supported versions

Woad is pre-1.0. Only the latest release receives security fixes. After 1.0, the latest minor release will.

## Reporting a vulnerability

Please do not open a public issue for security problems.

Use GitHub's private vulnerability reporting: open the **Security** tab of this repository and choose **Report a vulnerability**.

Please include the affected version, a description of the problem, steps to reproduce (for example a crafted image, audio or map file), and the impact you expect.

## What to expect

Woad is maintained by one person in their spare time. I aim to acknowledge reports within about a week and will coordinate a fix and disclosure with you. I'm happy to credit you if you want.

## Scope

In scope:
- The code in Woad and Woad.Core, especially loaders that parse untrusted files (images, WAV/Ogg audio, tilemap data).
- Packaging and CI configuration in this repository.

Out of scope:
- Vulnerabilities in third-party dependencies such as Silk.NET, StbImageSharp, OpenAL Soft or an Ogg decoder. Please report those upstream.
- Games built on Woad.
- Issues that need an attacker to already control your build or machine.
