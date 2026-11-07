# Branforth south repair integration

Updated September 22, 2026. Broader crew and animation work remains unfinished.

## Objective and accepted constraints
Connect the detailed south repair pose to standing without size/position jumps.
Preserve current identity, exact idle endpoints, original timing and owner rooms.
OpenAI built-in image generation used for source poses; no Higgsfield.

## Installed state
36 PNGs replaced: six frames each for kneel-south, repair-south and stand-south,
bare and helmeted. Catalogs, manifest timing/pivots and clearance remain unchanged.
Other 2,167 PNG/JSON files in the frozen Branforth baseline remain byte-identical.
Canonical rebuild uses the explicit tools/branforth_repair_revision.py override,
called by tools/rebuild_human_crew_art.py. It does not revise legacy source aliases.
tools/prepare_branforth_south_repair_chain.py rebuilds the connected rows.

Sources and exact prompts: character/crew-repair-polish-v1/sources. Kneel source01
was rejected: large head and insufficient descent stages. Source02 supplies four
interiors, with fixed0.23 scale and a screen-right planted-boot anchor at x148.
The earlier study centered that single boot at x128, shifting the torso left;
the source-study builder is corrected. Final repair uses source01 of the repair
study, slots0/1/2/3/4/0. Stand reverses kneel. Frozen existing idle frames provide
exact endpoints after pivot translation(36,52). Helmet uses the canonical south
head crop, fitted to each pose; no new helmet design.

## Verification
- tests/test_branforth_repair_chain.py: three tests pass; all36 selected frames
  reproduce exactly, binary alpha, registered idle/repair joins, alias isolation.
- tools/validate_human_crew_art.py branforth: zero errors/border touches;
  173body/167equipment states,669original frames/108source manifests unchanged.
- tests/test_crew_complete_packs.gd:19,475checks,zero failures. Initial failure
  was stale coverage for existing bought bunks, Marsh's retained berth and his
  selected south seated depth offsets. Catalog/metadata were unchanged by this
  PNG-only integration. Updated the test to verify those states and offsets;
  retained all existing action/timing checks. Routine raw-image fixture warnings
  remain, distinct from failures.
- Native source-player review:111samples across connected bare/equipped clips.
- Actual station renderer:222controlled samples across both variants, at a
  valid core-room release position. Inspected helmet repair at station scale.
  The fixture directly controls states/time; it is not autonomous workplace
  interaction. A greeting panel appears below the actor in that capture and
  pauses normal simulation; manual review time still advances. Do not call it
  a normal-play pacing or pause test.

Evidence: output/branforth-south-chain-2026-09-22/{before.json,changed.json,
native.log,pack.log,pack-current.log,rebuild-check.log,station.log,native,
station-bare,station-helmet}. Preview:
character/crew-repair-polish-v1/review/branforth-south-chain-02/chain.gif.
Current exported Windows/Mac builds predate this source change.

## Next action
Review autonomous room use as appropriate, then continue Branforth north/west
repair consistency and Marsh's distinct repair/carry/water transition sources.
Do not extrapolate this south-only integration to whole-cast visual acceptance.
