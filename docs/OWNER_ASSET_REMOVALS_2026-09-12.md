# Owner asset removals — verified state

Updated September 12, 2026. This note maps the informal playtest names to current room IDs and native output. It does not change gameplay or character animation work owned by other tasks.

## Verified removals

- **Hydroponics harvest stand:** `hydro_harvest_stand` is dressing, distinct from the functional `hydro_harvest`. Current preferred layouts tombstone the stand, and it is absent in native q0-q3. The functional harvester remains.
- **Anomaly task light:** `anomaly_task_light` is tombstoned wherever it appeared and is absent in native q0-q3.
- **Shield hull cradle:** `hull_panel_cradle` is absent in native q0-q3. The selected Shield wall assembly and functional room equipment remain.

Evidence is in `output/owner-removals-2026-09-12/before/runtime.json` and its four-rotation room captures. These requests were already effective in the current worktree, so no source, card or renderer change was needed.

## Isolation Vault mapping

The selected `full_wall_emergency-isolation-wall` is the stronger Side Emergency Isolation Wall South direction the owner asked to keep. It is not the item to remove. The older baked enclosure pieces map to `flush_back`, `flush_left` and `flush_right`; native q0 still contains the two side wings alongside the selected emergency wall, while q1-q3 do not show the old enclosure. Removing that q0 residue remains open and should preserve the selected emergency wall and independent isolation equipment.

## Validation boundary

This is a source/runtime audit of current preferred layouts. It does not establish owner acceptance of the remaining room art, battery styling, orange balance, or Isolation Vault replacement across all directions.
