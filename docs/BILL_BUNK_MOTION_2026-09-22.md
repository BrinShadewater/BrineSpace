# Bill bought-bunk motion candidate

Updated: September 22, 2026. Project: BrineSpace.

## Objective and acceptance
Replace the visible standing-to-reclining style discontinuity for Bill's bought-bunk
interaction. Preserve current standing identity, body scale and owner furnishing.
This is a staged bare sequence; live generic sleep art is unchanged.

## Accepted decisions and constraints
Built-in image generation supplied six missing coherent poses; no Higgsfield/API.
Use current idle palette, exact idle endpoint and unchanged pivot. Helmet fitting
must retain the accepted reduced overall helmet size.

## Current state
character/bunk-contact-study-2026-09-21/ contains bill-entry-source.png, exact
bill-entry-prompt.txt and build_bill_entry.py. Seven output frames, manifest,
recipe, choreography and validation are in bill-entry/. Uniform source scale is
0.28; canonical idle is padded at (36,52), pivot (128,224), standingHeight 148.
Canvas is 256x272: the initial 256-square candidate clipped the hanging boot.
Adding transparent space preserves scale and registration and restores the boot.
The final sleeping endpoint comes from the same source sequence. Generic runtime
catalogs remain unchanged pending equipment and controller integration.

## Verification
output/layout-default-audit-2026-09-21/bunk-fit/bill-existing-sleep-board.png
records the older rounder seated/reclining art alongside current standing identity.
The new sequence has 47 actual-player native samples in bill-bunk-native.log.
Native seated, boarding, leaning and resting contact reviewed; the corrected
boarding capture keeps the complete boot in front of the rail. Deterministic
rebuild, exact idle, binary alpha, clear borders and identical native first/last
pixels pass in bill-entry/validation.json. Review: bunk-fit/bill-full-entry.gif.

## Next action
Fit the reduced helmet consistently to all new poses, then bind Bill's profile
without changing other crew's base behavior. Verify chooser, claims, interruption,
saves and actual rendered source pixels. Owner motion acceptance, full expedition
and packaged evidence remain open.


## Equipped candidate - September 22
build_bill_bunk_equipment.py now fits the existing east shell with the accepted
48px cap inside its unchanged 46x56 registration canvas. Head centers, angles,
limited cleanup boxes and preserved visor region are recorded in the recipe.
Bill's exact current equipped idle is reused; every output is 256x272 with the
same pivot as the bare sequence. This pass uses no generation.

The normal equipment loader rendered 47 native samples in bill-bunk-equipped.log.
Seated, boarding, leaning and sleeping contacts were inspected under the upper
mattress. Deterministic rebuild, exact idle, unchanged bare frames, binary alpha,
clear borders and identical first/last native pixels pass in
bill-entry-helmet/validation.json. Review: bunk-fit/bill-equipped-entry.gif.

Next: bind Bill's profile with special care for the shared base controller and
its human/nonhuman subclasses. Do not add inherited Bill behavior to other cast.
Then verify actor-specific source pixels, all relevant save validators, shared
bunk claims and existing Veld/Branforth/Marsh regressions. Runtime binding and
full gameplay/release acceptance are still open.
