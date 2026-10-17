# Project handoff

Updated: 2026-09-26 · BRINE float style correction

## Objective and acceptance
Match the existing animated BRINE's style more closely after the first reference-driven body became too realistic.

## Accepted decisions and constraints
Original brine-cleaned-v5.png now governs character proportions, face, painted sprite shading and hair. Keep the blue suit and suspended pose; retain the eight-second float rig, tube and room. Earlier candidate and original remain preserved.

## Current state
New imagegen source and 64x168 proportional transparent export. production.json records exact prompt/reference/provenance; build.py and manifest.json provide reproduction and hashes. preview_room.gd retains the previous mesh rig with only the body texture path changed. Shared native preview launcher now selects this revision.

## Verification
Native-size body composite and eight captured loop phases visually reviewed. Head/body ratio, broader readable silhouette, stylized eyes and shading are closer to original BRINE than the first realistic version. Remaining generated variation is subject to owner review. Native 32-sample capture and rig loop-closure assertion passed without logged errors; owner saves unchanged (session-f755214e389f4dfca05875ecc4bd7efb). GIF shows the eight-second cycle at four samples per second; native animation is continuous. No production integration or broader gameplay validation claimed.

## Next action
Owner visual review. Preview-only; original art and saved room are unchanged.
