# Biomass vessel integration

Updated September 21, 2026. Broad objective remains active.

## Objective and acceptance
Give Biomass a readable digestion vessel with integrated feed handling, coherent
large/medium furnishing and restrained functioning feedback. Agent visual review
and owner acceptance are separate; the room remains sparse and open to refinement.

## Decisions and constraints
No Higgsfield. One built-in image edit of a bought tank reference, preserved as a
separate derived asset. Bought atlases, bulk registry and owner marks were not
edited. Ten protected owner rooms and every non-Biomass layout key are preserved.
No commit, publication or package refresh in this pass.

## Installed state
assets/biomass-vessel-v1/ retains normalized vessel, raw generation, reference,
exact prompt and hashed provenance. Matte olive panels, organic-material emblem
and attached covered inlet replace the white water tank treatment. Raw1420x1108
RGBA with real alpha was cropped and nearest-neighbor reduced to246x193; actual
world width160. This is a generated derivative, not pixel-identical local recoloring.
Two new registrations: biomass-vessel-v1 and biomass-controls-v1. The latter uses
unchanged mtp2-84 source pixels with a local screen rectangle [491,124,14,11] and
muted green telemetry. Other users of the bought cabinet are unaffected.
Four complete effective saved/default Biomass keys install vessel[-174,-156],
feed sacks[-116,-20], controls[30,-112]. Loose source props and old bank are hidden.
Single assets/room-cards-v2/biomass_digester.png rebaked and inspected.

## Verification
Candidate r4c and installed defaults: four views/640 walking samples each, zero
failures; full RGBA equality in all four views. Candidate all-four stills and live
52/75 framing inspected; live fixture exited0. Funded/free fixture proves framing,
not expedition balance. Installed control feedback passes four-view active motion,
off-state stability and held-clock equality with changed pixels confined to the
screen envelope. This is not a separate actual-station pause test.
Guarded installation and post-write comparison prove exactly four Biomass keys
changed in both files, all other keys unchanged. Card bake1 completed exit0.

Crew review: front, inlet and controls positions are clear in all four quarters;
q0 images visually reviewed. Initial rear position[-85,-170] also clears. A later
probe deliberately tried[-85,-128] over the top plane and was blocked in all four
views: collision uses the full rectangle. Its failed probe log must not be counted
as a passing depth test. No claim of verified rear-body occlusion at that point.
The registration footprint [.04,.35,.92,.62] controls floor shadow only; it does
not define collision. No separate collision_boxes were supplied. Earlier notes
suggesting footprint changed navigation were incorrect; full rectangle governed
all route checks. Keep this conservative behavior unless separately reviewed.

Evidence/backups: output/power-layout-review-2026-09-21, including installed-pixel-
parity.json, installed-defaults.log, operation-installed.log, card-bake.log,
pre-install-saved.json and pre-install-defaults.json.

## Next action
Owner visual acceptance, normal expedition observation and room density refinement
remain open. Current e3d4c7647fe9e73f Windows/Mac packages predate this integration;
refresh through maintained export and exact-PCK/runtime checks at the next release
checkpoint. No new claim of Mac hardware acceptance.
