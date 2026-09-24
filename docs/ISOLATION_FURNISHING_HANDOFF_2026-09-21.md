# Project handoff

Updated: September 21, 2026 · Project: BrineSpace · Task: Isolation Vault furnishing

## Objective and acceptance
Continue purposeful large/medium room furnishing alongside Bill's unfinished gait,
animation repairs, performance and release preparation. Native geometry checks do
not establish owner visual acceptance.

## Accepted decisions and constraints
Preserve named owner reference rooms and library marks. No Higgsfield. Group
equipment by function; avoid filler accessories and blanket upscaling.

## Current state
Installed four guarded `emergency-isolation-wall/0..3` saved-layout changes: move
the existing control cabinet beside the battery rack and align their lower edges.
No inventory, scale, source art or default-layout changes. Refreshed
`assets/room-cards-v2/isolation_vault.png` and CURRENT_STATUS.md.
Evidence and exact backup: `output/isolation-composition-2026-09-21/`, including
`installation.json`, `installation-backup.json`, candidate and native captures.

## Verification
Native candidate review: four views, 640 walking samples, zero failures. Guarded
installation checked every affected saved row against the reviewed baseline and
preserved other keys. Targeted native card bake: one card, exit zero; inspected
the resulting card and confirmed the grouped equipment and clear central aisle.
Saved-layout changes are local; defaults/export consistency remains outstanding.

## Next action
Review room pilots together at normal gameplay zoom, then continue individual
Bill knee/stride review. Resolve local/default furnishing differences before a
stable release refresh. Apple Silicon native testing remains pending.

## Subsequent live-render repair
The six-room gameplay comparison exposed missing Isolation Vault props after the
first view setup. Its rare-room base filtered all non-dressing props on every
configure, while the layout cache accepted the resulting empty collection as
already applied. Removed that redundant configure override; rebuild retains the
necessary legacy battery-furniture cleanup. No owner layout changes were needed.

Changed `rooms/underwater/rare-dead-ends/isolation_vault_view.gd`; added
`tests/test_isolation_layout_reconfigure.gd` and its UID to the room-art group.
The guard fails 10/15 repeated/rotated setups before the fix and passes 15/15 after.
Native before/after station captures confirm restored furniture in
`output/room-gameplay-scale-2026-09-21/`. Six room centres were visible, but the
initial group images clip room edges; individually framed captures supplement them.
