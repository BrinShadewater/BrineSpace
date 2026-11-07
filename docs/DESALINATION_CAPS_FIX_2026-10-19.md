# Desalination top caps repaired — October 19, 2026

Owner found missing top wall caps in the playable preview. The room inherited the
older expansion shell, whose unpainted path supplies jamb/corner caps but omits
continuous cap strips. Its custom riser face therefore did not get the complete
production hull finish used by neighbouring rooms.

The room leaf now reuses the existing painted-shell cap methods with its own atlas
and rotated database ports. Continuous bevelled strips, mitred corners and closed
port frames follow the existing raised/low and shared-edge state. A full raised
header closes the crown above north-facing doorways. The custom wall face stays
unchanged; shared renderer files, layouts, costs, intake rules and gameplay do not
change. Only Desalination's card was rebaked.

**906 native checks /0 failures**, `output/test-runs/20261019-152501-native`, include
the actual construction/Save/Continue/crew transit suite plus eight cap pixel probes
at the side band and central lintel in all rotations. The pre-fix negative run
(`20261019-152213-native`) failed all four initial crown probes with exact background
pixels. An intermediate side-cap repair passed 902 checks; visual review identified
the doorway-header notch, which the final eight-probe revision also covers.

Agent inspected final Studio, four orientations, north-connected station, card and
the actual resumed playtest capture. [Current rotations](../output/desalination-caps-20261019/orientations.png).
Owner visual acceptance remains separate.

The prior disposable playtest was copied to a new isolated profile and reopened
paused at **cycle 1 /seven rooms**, with resources and hand exactly equal to its
saved checkpoint. All three doors connect; intake remains clear and normal paid
building/failure rules remain enabled. The previous profile is retained. Current
ready capture: `output/desalination-play-preview-20261019/runs/20261019T222511Z/ready.png`.

All validation/helpers use scratch APPDATA. Protected inputs and owner-data
comparison are recorded in `output/desalination-caps-20261019/FINAL.json` and
`preservation.json`. Source only; no export, signing, upload or Git publication.
The new playtest's final after-close audit remains pending while its window is open.
