# Human cryopod emergence — September 30, 2026

Latest owner revision: slower exit followed by falling and standing up is now
installed through `character/cryo-fall-recovery-v1/`. Its4.6-second physical
sequence supersedes the1.2-second timing described below; this folder still owns
the closed chamber source and registration. Latest preview:
`output/cryo-fall-recovery-v1/thaw-and-exit.gif`.

Installed for Bill, Veld and Branforth in the startup pod and recovered wards.
Uses the actual selected bare south idle/walk textures from the live players,
including their standing-height/pivot metadata and linear sampling. Characters
retain the live renderer's 65.28 world-unit standing scale throughout.

Saved wake progress gradually fades blue to natural colour before the final
1.2-second exit: 0.45 seconds opening, 0.67 seconds stepping, then idle. The
endpoint uses the same clear navigation node as release, including the live
14.592-unit drawing offset. Pause and Continue use existing saved wake progress.
Recovery duration, costs, berths, resources and unlocks retain their current rules.
Marsh's separate charging chamber is unchanged.

Opening now emits a short icy-blue vapour puff from the chamber seam, using the
existing painted leak-puff texture. Expansion/fade follows saved wake progress;
Reduced Motion holds the cloud geometry still. Follow-up native review:
`output/cryo-layered-vapour-v1/thaw-and-exit.gif`.

`empty-closed-source.png` is a generated empty-interior edit of the selected Bill
closed pod. Exact prompt:

> Edit target: this cryopod game sprite. Remove the entire human occupant, revealing the empty padded backrest, seat and footwell inside the capsule behind clear smoky-blue glass. Keep exactly the same pod, camera perspective, framing, dimensions, outline, cream graphite matte painted pixel-art material style, top cyan bar, hinges, bottom control panel. Reconstruct concealed padding seamlessly. No person, no silhouette or body-shaped impression remaining. Transparent exterior. This is an empty version of exactly the supplied closed chamber, not a redesign.

`python tools/build_cryo_layered.py` rebuilds `closed.png` locally from that source,
preserving original housing pixels outside the registered interior insert. The
existing actor-specific empty-open pods are retained. Opening blends registered
closed/open pod artwork; it is not a newly authored hinge-motion strip.

Evidence: `output/cryo-layered-v1/`, native room captures and review GIFs; see
`docs/CRYO_EMERGENCE_HANDOFF_2026-09-30.md`. Owner visual acceptance and release
export remain separate from source/native verification.
