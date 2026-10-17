# Cryopod family material and integration pass

Production scope: Bill, Veld and James/Branforth core and derelict cryolab
emergence; Margot's pet chamber and its two broken human chamber masters.
Earlier rejected master studies remain preserved as sources, not live assets.

The open human padding now uses a single cool neutral calibration, rebuilt
from the preserved original sources without resizing. Registration is still
418×627, pivot210,560. Shell, glass, controls and alpha are unchanged. Exact
mask, multiplication and source/output hashes are in registration.json;
`python tools/build_cryo_material_pass.py` reproduces the three exports.

Human cold modulation is now(.66,.82,1), shared with Margot's cold family.
It holds until floor contact, then fades to natural colour before release.
The human reveal keeps an opaque open housing beneath the fading closed art
to avoid the previous mid-opening shell brightness dip.

## Selected production bindings

| Asset | Source binding and retained contract |
|---|---|
| Human closed shell | cryo-layered-v1/closed.png; existing camera and registration |
| Human open shell | These three exports; architect_cryo_art.OPEN_PATHS |
| Human fall/rise | cryo-fall-recovery-v1, selected idle endpoints, standing148 at world65.28 |
| Human floor fog | Existing painted leak-puff; low opacity, finite saved-clock whoosh |
| Margot chamber/door | cryo-ward-layered-v5; one rigid door,82px upward travel,9px overlap |
| Broken chamber masters | cryo-ward-layered-v5 frames via companions.CRYO_MASTER_PATHS |
| Margot occupant | Live selected nap/wake/walk/idle; central fit,7-world-unit hop |
| Margot endpoint | Runtime512×640 preserves full paws; shared spawn landing |

All poses retain one calibrated scale rather than independent bounding-box
fitting. Human choreography remains slow step, fall, grounded hold, recovery;
Margot retains the approved little hop. Existing pause, power and saved recovery
rules remain in effect. Source game integration covers both starting core and
found cryolabs. Exported executables have not been rebuilt by this pass.

Native evidence and verification are recorded in
docs/CRYO_FAMILY_POLISH_HANDOFF_2026-09-30.md.
