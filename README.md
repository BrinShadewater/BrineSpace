# BrineSpace

A Godot 4.7 underwater station-restoration roguelite prototype. You play BRINE,
a damaged AI core rebuilding a silent station through blueprint drafting,
modular placement, interdependent production and discovered room synergies.

> “The station is quiet. That does not mean it is empty.”

**[Play BrineSpace on itch.io](https://brinshadewater.itch.io/brinespace).** The
Windows 0.4.0 RC1 preview and Mac 0.3.0 alpha are available there; iPad is in
testing. The downloads are playable builds, separate from this repository.

## What this repository contains

This is a **code-and-documentation snapshot**. It contains GDScript, Godot
scenes and project configuration, text data, tools, tests and development notes.
It does **not** contain the raster art, animation frames, audio, video, fonts,
binary resources or release packages used by the game. A fresh clone cannot
import, run or export BrineSpace on its own. Use a complete local project copy
with matching assets for development and builds.

This clean snapshot was made from `main` at
`bcf9834a0ed62df3b1417b4a87ba68b035791c8f` on November 7, 2026.
Older Git history and its LFS objects are intentionally absent. Historical
documents may refer to art paths, screenshots or branches that are not hosted
here. Those references record the work as it stood at the time; the playable
downloads and current availability are on itch.io.

## The game

Draft and rotate room blueprints, connect them to the station, and balance
power, oxygen, food and materials. Discover room synergies, recover crew and
companions, send drones to mine and salvage, and conclude expeditions to bank
Archived Data for later loops. BRINE is a damaged AI core with opinions.

BrineSpace is still in development. Large-station performance, Mac and iPad
work, and longer playtests remain under evaluation. For a runnable build and
current platform details, use [the itch.io page](https://brinshadewater.itch.io/brinespace).

## Development reference

Read [AGENTS.md](AGENTS.md), [current status](docs/CURRENT_STATUS.md),
[development notes](docs/DEVELOPMENT_NOTES.md) and [NOTICE.md](NOTICE.md)
before changing the full local project. The scripts and tests here describe
the source snapshot, but art-dependent validation requires the local assets.
GitHub CI checks only that tracked files remain source-only; it does not build
or test the game. Do not commit generated media or local player saves here.

All rights reserved; see [NOTICE.md](NOTICE.md) for rights and reuse terms.
Third-party components retain their own licences.
