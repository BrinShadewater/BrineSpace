# Desalination intake floor decal — October 19, 2026

Owner found the initial arrow text hard to read and wanted the marker to look like
a decal on the deck. The room now uses larger **INTAKE** lettering (font size
10→22, with 80% vertical scale), matte grey-green paint and no offset shadow.
Narrow stencil bridges and small edge nicks leave real floor pixels visible.
Translucent arrow/text ink lets the deck texture and seams show through; fixed
letter-opacity variation adds restrained applied-paint variation. This is static
paint, with no glow, animation, collision or operating-status behavior.

The arrow still turns toward the sealed, non-door intake wall in all four rotations.
Text stays upright and is projected onto the floor plane, with the host transform
restored immediately afterward. Vector clipping is cached once per script load.
Shared fonts/floor/renderers, machinery/layouts, caps, rules and original rasters
are unchanged. Only Desalination's card was rebaked.

**910 native checks /0 failures**, `output/test-runs/20261019-155521-native`.
The existing actual-ocean-face pixel probes, three-door routes, paid construction,
Save/Continue, Studio and cap checks still pass. Agent visually reviewed the card,
Studio, all four orientations and refreshed playtest at gameplay scale. Readability
and material review are visual judgments; owner acceptance remains separate.

[Updated four rotations](../output/desalination-intake-decal-20261019/orientations.png)
and [Studio](../output/desalination-intake-decal-20261019/studio.png) show the finish.

The previous disposable trial was backed up, then its exact known preview window
received a normal close request. The game's save/quit path completed with exit 0;
no forced termination or original-player-game close occurred. A refreshed preview
was launched from a copy of that saved private profile. Exact readiness, preserved
resources/hand and protection audit are recorded in
`output/desalination-intake-decal-20261019/FINAL.json`. New trial after-close audit
remains pending while open. Source only; no export, signing, upload, Git publication
or new packaged/performance acceptance.
