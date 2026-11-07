# Marsh charging pod

Open docking cradle with attached pump reservoirs and hoses; approved Marsh V3 identity. Engineering/medical servicing equipment, localized derelict wear, matte olive-grey frame and dark padding. Shared south-facing room camera; world width62 at the standard pod socket, 684-source-pixel visible width, pivot(512,1435).

`occupied-source.png` and `empty-source.png` are generated sources; exact prompts stored alongside. `build.py` packages registered 512×768 PNGs and hashes. The occupied output uses the cleaned empty source's exterior alpha silhouette to remove its halo. No independent crop, body repaint or pose substitution. `rejected-cleanup-source.png` failed its background instruction and is not loaded.

`scripts/marsh_charging_art.gd` owns source-coordinate hoses, white fluid and charge indicator. Its clock is saved recharge progress, so power loss and pause freeze motion. New chamber, inspector and selected-Marsh core pod use it. Review captures live in `review/`; implementation and validation scope are in `docs/MARSH_CHARGING_2026-09-09.md`.
