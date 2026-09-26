# Current saved-layout restoration audit

September 21, 2026.

## Objective and constraints
Complete the follow-up deletion/repeated-setup audit after four reproduced wrapper
repairs. Preserve owner layouts and runtime source during this read-only check.

## Evidence
Native Godot audit instantiated Medical Center, Medical Office, Ore Refinery,
Construction Drone Bay, Biodome, Salvage Drone Bay and Quarantine Cell from current
source. Each configured all four rotations twice against a snapshot of the actual
saved layout merged with current defaults through RoomLayoutStore.

For each effective prop, the audit checks that an explicitly null authored entry
is not restored and that no ID is duplicated. It compares the complete ID-to-rect
map before/after a repeated same-quarter setup. All 28 views pass; exit 0, clean
engine log. The source/layout hashes and full per-view maps are recorded under
output/current-wrapper-audit-2026-09-21. Actual saved bytes remained unchanged.
Ore Refinery requires no repair for these tested properties; its owner layout was
not edited. Medical Center/Office also pass this current-layout check.

## Limits and next action
This closes the seven-wrapper current-layout deletion and repeated-setup check.
It does not prove all hypothetical saved configurations, surviving prop completeness,
visual overlaps, routes, animation or rendered pixels. Do not generalize it into a
whole-game layout certificate. The earlier focused planted-deletion regressions
remain the repair guards. Continue Bill motion review in ordinary gameplay and
owner room composition review, then refresh release packages at a useful milestone.
Broad objective remains active; native Apple Silicon acceptance is still pending.
