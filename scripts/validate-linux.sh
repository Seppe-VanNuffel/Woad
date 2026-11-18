#!/usr/bin/env bash
# Headless smoke test for Woad on Linux (console-only machines, CI).
# DRAFT: becomes real in backlog issues M0-05 / M1-12.
set -euo pipefail

FRAMES="${1:-120}"

export LIBGL_ALWAYS_SOFTWARE=1   # force Mesa software rendering (llvmpipe)
export ALSOFT_DRIVERS=null       # OpenAL Soft: no audio hardware required
export DOTNET_NOLOGO=1

cd "$(dirname "$0")/.."

dotnet build samples/Sandbox -c Release --nologo
xvfb-run -a -s "-screen 0 1280x720x24" \
  dotnet run --project samples/Sandbox -c Release --no-build -- --frames "$FRAMES"

echo "Woad headless smoke test passed ($FRAMES frames)."
