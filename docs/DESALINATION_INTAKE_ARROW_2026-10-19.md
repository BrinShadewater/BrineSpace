# Desalination intake arrow — October 19, 2026

The intake faces the **sealed wall without a door**. Default orientation is north;
quarter-turns move it east, south and west while the three doors rotate together.
The owner requested a visible arrow to make this clear.

Added a matte teal **INTAKE** floor stencil in the clear central space between
machines. The pointer turns with the room; its text stays upright. It points toward
the outside cell that must remain open ocean. It does not animate water flow or
indicate whether the room is powered. No collision, costs, output, intake checks,
layouts or wall geometry changed. Only Desalination's card was rebaked.

**910 native checks /0 failures**, `output/test-runs/20261019-154148-native`, retain
paid construction, economy, Save/Continue, all three-door routes, Studio and caps.
Four new rendered probes use the game's actual ocean-exterior cells to check the
pointer direction. The no-arrow negative run (`20261019-153958-native`) failed all
four probes. Agent reviewed all four orientations, the card and the actual refreshed
playtest. [Current four rotations](../output/desalination-intake-arrow-20261019/orientations.png).

A refreshed preview is open in a new, separate window named **Desalination Unit
intake-arrow preview**, loaded from a copy of the previous trial's checkpoint.
Resources and hand match that saved checkpoint; normal paid building/failures remain.
The existing playtest window was left untouched. Its new profile and ready receipt
are under `output/desalination-play-preview-20261019/runs/20261019T224232Z/`.

All validation/helpers use isolated APPDATA. Exact preservation, hashes and launch
details are in `output/desalination-intake-arrow-20261019/FINAL.json`. Source only;
no export, signing, upload, Git publication or new packaged/performance acceptance.
Owner visual acceptance remains separate; playtest after-close audits remain pending
while their windows stay open.
