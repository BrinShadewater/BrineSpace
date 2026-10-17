# Bill south/west cargo turn candidate

September30,2026. Staged/uninstalled; owner visual review pending.

## Master repair selected: master-v4

Selected source is now sources/turn-master-v4.png, original
exec-a1c4a1ee-7a51-4d3b-9ed2-e8b79d488544.png. It restores circular-ring
shoulder emblems, swept/tufted warm brown hair, burgundy chest button grid and
cyan strip, quilted panel detail and cuff/collar fasteners. Full master repair
prompt is prompt-master-v3.txt, followed by prompt-chest-v4.txt. Initial master
edit turn-master-v3.png is preserved. A further six-button draft (v5) was not
selected: its prompt miscounted the actual master's three-column grid and it
introduced additional lighting drift. Canonical-control.png/master-chest-reference
are original-master crops for inspection, not new painted assets.

Approved neutral endpoints remain exact original pixels. Fixed source anatomy
calibration and planted-foot/800ms contract retained. Local endpoint-derived
midtone correction uses one frozen curve at90% strength;107 packaging checks
pass, including endpoint color continuity. The grade preserves new source
alpha/head pixels compared with review-ungraded-master-v3 (the current build's
pre-lift export); artwork itself is a new source, not pixel-identical to v2.
Previous selected package/audit retained in review-before-master-v3.
Updated master comparison records restored/emblem/controls/hair and improved
quilting. Source/master, contact and station-scale views visually reviewed;
owner/native acceptance still pending. No runtime change.

The following notes describe earlier preserved candidates.

Grade-v2 corrects the owner's reported mid-turn darkening. The original suit
cloth medians were42–47 versus endpoint52–53. turn_material.py freezes one
neutral midtone lift from both endpoint cloth bands, bringing intermediates
to50–56 (within4 levels of endpoint average). Face/hair, alpha geometry,
neutral endpoints and timings stay unchanged; deep outlines and bright matte
hardware highlights are outside the lift. Settings/audit recorded in
turn-material-grade.json and color-verification.json. Prior package preserved
in review-before-grade-v2. No source regeneration or shared grade-helper change.

Two directed turns, six poses each. Four independently authored intermediates
connect exact loaded neutral south pickup011 and west pickup011. Reverse turn
reverses the same pixels without mirroring. Original quarter-turn800ms retained;
canvas256, pivot128,224, standing reference148, linear sampling. One frozen
vertical scale and one horizontal shoulder calibration (stricter of the two
endpoint measurements) apply throughout. Small planted boot swivels, no stride.

Selected source `sources/turn-v1.png` is original generation
`exec-08a2ab0a-09ea-4f5b-8d16-0f597995d246.png`; exact prompt in
`sources/prompt-corrected-left.txt`. References are approved bare south/west
loaded neutral cargo endpoints. Earlier source
`exec-6b7f0c08-1afa-4410-a8f0-9b1eb6d0fbcd.png` incorrectly turned toward east
and is retained as `turn-wrong-facing-unselected.png` with original prompt.txt.
It is not selected or mirrored into this pack. Palette uses selected west idle
via the maintained east cargo matte-grade helper. Registration records source
hash, source cells, authorities, grade and fixed scales.

Run build.py, verify.py and build_review.py in this folder using Python.
107 checks pass: metadata, exact neutral/reverse joins, hashes, alpha/clipping,
compact boot spread, fixed scale, shoulder width ceiling, unchanged face/alpha
and endpoint-relative suit midtones. Contact/gameplay
82/54px dark/light samples reviewed; browser loads isolated turn plus complete
pickup→pivot→set-down chain. Packaging and browser evidence do not establish
native or owner visual acceptance.

Next: owner review, north-connected quarter turns, canonical helmet turn art,
opposite turns, then complete cargo installation/native checks in scratch
APPDATA. Preserve neutral endpoints at integration; do not replace them with
carry gait frame zero. Walking-to-turn settling needs its own visual review.
