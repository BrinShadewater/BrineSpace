# Project handoff

Updated: October 3, 2026 · Project: Brine Space · Task: James Windows release candidate

## Objective and acceptance
Finish James and prepare next playable version. Candidate packaged and tested; full visual goal remains incomplete.

## Accepted decisions and constraints
Accepted artwork preserved, forward torch/tablet/belt-wrench decisions retained, owner saves protected. Local Windows preparation authorised; no publication performed.

## Current state
### James Windows release candidate — October 3, 2026

V351 Windows candidate brinespace-5024faab0e485c1a physically frozen from selected runtime
dependencies; source fingerprint 5024faab0e485c1a7b02e376389a6df22bda865a5c41461e0094f7fbabfa2574. Preserved accepted James
artwork and installed V347 water rows. Corrected CrewLife profile lookup through
script ancestry: actual James cargo actor previously fell back to Bill's differently
sized distress/cargo-turn outline.57 focused human-profile/low-air admission checks0.
Existing concurrent CrewLife changes preserved. Exporter fixes: shared preloaded
icon registry receives normal importer roles (2 regression tests pass); referenced
Theora video collected/exported (9 manifest tests pass). Maintained exporter pass;
selected frozen source release-safety2 tests pass. Whole authoring checkout safety
check still flags10 older BRINE preview assertions, absent from selected snapshot.
Initial failed export attempts preserved: old icon parsing, omitted intro video and
fresh font-import Unicode diagnostics; successful retry reused generated import data.

Exact packed-art audit and actual release New Game/intro skip/saved-loop Continue/F8
pass; debug=false,0 failures, no missing-art placeholders. Native screenshots reviewed
as recorded in release-build-review-v351/review.json. Isolated scratch APPDATA,
owner unchanged; temporary override confined to separate QA copy and removed.
EXE/PCK hashes in output/james-release-closeout-v351/release-validation.json.
Native fixture exit reports32 leaked ObjectDB instances; no engine/script errors
captured during smoke. Long-session memory behaviour is outside this check.
Deliverable: output/james-release-closeout-v351/deliverable/BrineSpace.exe
(keep BrineSpace.pck alongside). Local Windows candidate only; no upload/commit.

Remaining review limits: not continuous visual acceptance of every selected clip,
autonomous water/exterior/hazard coverage or Mac gameplay. Coarse cargo quilt and
wide North unload stance remain polish concerns; no speculative material redo.
Full James animation goal remains incomplete; this milestone supplies a packaged
candidate for playtest and release decision. Handoff:
character/james-west-carry-walk-keys-v1/release-build-review-v351/HANDOFF.md.

## Verification
See review.json for actual package identity, exact audit, release-template smoke and owner profile evidence. Three native package captures and source seated endpoint reviewed.

## Next action
Playtest this exact Windows candidate. Resolve visible defects within existing accepted set; record remaining material/stance polish explicitly. Publication or Mac validation requires its own scope.
