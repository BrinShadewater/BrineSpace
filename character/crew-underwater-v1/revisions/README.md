# Crew swimming revisions

All three crew have four runtime swim directions and matched helmet frames.
Eleven directions use provisional revisions; Veld north retains its passing
pilot. All artwork remains provisional pending continuous motion review.

| Direction | Bill | Veld | Branforth | Canvas / shoulder pivot |
| --- | --- | --- | --- | --- |
| East | Revision | Revision | Revision | 104 x 92 / (61,44) |
| West | Revision | Revision | Revision | 104 x 92 / (43,44) |
| South | Revision | Revision | Revision | 104 x 112 / (52,76) |
| North | v2 | Retained pilot | v3 | Revisions: 104 x 112 / (52,36); Veld uses its manifest |

`current-swim-coverage.json` inventories all 12 body/helmet pairs and hashes their
manifests and frames. Rebuild with `build_swim_coverage.py`. This inventory does
not certify motion quality. `check_swim_revisions.py` covers eleven revised packs;
the review controller has five tests, including retained Veld north selection.

## Runtime evidence and limits

Native phase checks pass all six bare/equipped phases in each direction.
Furnished doorway route fixtures pass for all three crew east, west, south and
north. Directional route evidence JSON and native logs are stored here. The
fixtures use individual actors, not concurrent crew traffic or exterior water.

South moving run 93436 produced 78 captures; three middle-crossing samples were
inspected. North produced 78 captures and 21 sampled frames were inspected.
East/west capture history is preserved in the linked history. Sampled inspection
is not continuous playback acceptance. Compare current source hashes before
relying on old captures. Failed or UI-obscured runs remain historical evidence.

Use `review.html?direction=east` (or west, south, north) for synchronized old/new
playback, helmet toggling and scrubbing. The review sizes its canvas from each
pack's pivot-relative extents. The main `../review.html` follows runtime selection.

## Remaining work

- Continuous loop, turning and swim-to-tread visual refinement, including differences in directional projection.
- Review and refine treading, death and equip/remove endpoints across all crew.
- Refine locker pickup/return joins and shared shelf/held-helmet proportions; composed actions now include pickup and deposit.
- Real flood/exterior medium transitions and remaining airlock transit integration.
- Complete remaining character skill evaluations; the recorded fresh-context locker trial is partial evidence.

The full expansion scope remains in [the parent README](../README.md).
[Revision history](README-history.md) preserves experiments, earlier failures,
superseded status and source-specific observations; this page is the current summary.
