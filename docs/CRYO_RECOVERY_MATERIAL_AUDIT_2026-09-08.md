# Cryo recovery material audit and empty-pod fix

scripts/architect_cryo_art.gd still loaded the original bright empty pod after recovery. Its recovered-state source now uses assets/material-polish-cryo-v1/cryo-equipment.png, matching the standard room. The original occupied animation paths and behavior remain unchanged.

A six-frame Bill material repaint candidate is preserved in assets/material-polish-cryo-recovery-v1, with its exact prompt. It improves casing/padding color, but generated RGB with a baked checkerboard rather than alpha. It is NOT installed. Do not treat this candidate as a usable frame pack. Next production step must resolve background isolation and verify six-frame registration before replacing runtime frames; then apply matching materials to Veld and Branforth while preserving identity/poses.

The historical architect playtest is stale relative to current runtime. Its title assertion accesses the removed architect_choice property and times out; initial native.log is rejected as a successful run. A temporary recovery-only copy passed without ERROR, but its core diagnostic records recovered=true before the frame loop. Thus these captures prove the new empty texture renders in core, not occupied animation coverage. Do not use its PASS string to accept those clips.

A separate focused native renderer explicitly sets each architect/frame/recovered state: output/review_cryo_frames.gd. It rendered 18 occupied frames plus 3 recovered pods without ERROR. Evidence: output/art-material-cryo-recovery-v1/explicit-frames, explicit-frames.log. Sealed frames for all three architects were visually inspected and retain brighter glass/cream. Remaining frames are available but not yet visually accepted. This isolated renderer establishes art/state selection, not game progression, NPC handoff or packaged acceptance.

The broader art-match goal remains active: occupied recovery art, other biological rooms, risers and remaining shared/animated art are incomplete. No executable rebuild.
