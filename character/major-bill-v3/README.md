# Major Bill: complete local revision

Selected by `scripts/grid_canvas.gd`. `catalog.json` lists all body and precomposed
helmet profiles: 175 body states (1,134 frame references), 168 helmet states
(1,080 references). Original source packs are preserved outside this revision.

Every profile declares standingHeight 148. The figure retains its 65.28-world-unit
size; canvases and pivots vary with pose/props. All durations and loop modes retain
the existing action contract. Locker manifests preserve handoff events.

Rebuild from the checkout root:

```powershell
python tools/rebuild_bill_art.py
python tools/validate_bill_art.py
python tools/review_bill_art.py
```

East/west walk legs are articulated from separate original source regions, with
alternating stance/swing and a one-source-pixel body rise. Their stride overrides
are 0.1056756757 cells per cycle. North/south/diagonal walk retain the existing
0.12-cell stride. This changes animation cadence, not simulated movement speed.
Equipment is rebuilt with the same body phase and head position.

The source-density stage retains the original base palette; extensions retain
their authored source colours. No generation service is needed for these rebuilds.
The direct walk-study command reconstructs its own pre-repair source so it cannot
feed the installed repair back into itself.

Full provenance, scope, validation and limitations:
`docs/BILL_FULL_REPLACEMENT_2026-09-12.md`. Review media remain under `output/`;
they are not runtime dependencies. This source revision is not an exported EXE.
