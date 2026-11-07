# Project handoff

Updated: October 20, 2026 · BrineSpace · Gameplay, construction access and emergency Save/Continue

## Objective and acceptance

Owner asked to park this session and resume in a fresh one. Current local source work is complete for the requested warning and fresh-opening check. Read this handoff after `docs/CURRENT_STATUS.md`; dated evidence is not an instruction to restart its scripts.

## Accepted decisions and constraints

- Normal building/resource failures and physical crew work remain enabled. Desalination costs5 Metal and converts2 Power to2 Water per functioning cycle; companion repair remains8 Metal. Paid repair pause/resume retains progress and does not charge again. Rerolls spend charges, not Metal.
- Construction warning is advisory: allow a risky legal placement at normal cost. Distinguish safe crew routes, busy crew, powered dedicated drone alternatives and eventual room operation. No emergency automation was added.
- Preserve Desalination's accepted matte blue-green equipment, custom riser, top caps, three west/east/south doors and north intake, reviewed prop scale and worn INTAKE floor decal. Accepted source look: enabled bloom30%, pixel20%/2px, tilt0.50px, focus30%; sharp surrounding interface.
- Background diagnostics use scratch APPDATA, never the real progress/Studio folder. Copy checkpoints before loading and retarget `run_save_path` before stepping. Do not clean, seed or restore player files. Keep existing dirty work, UID pairs, prior cohorts and frozen/signed packages.
- Source checks do not publish or certify a Windows/Mac/iPad build. The existing Mac listing and older Windows signing/publication receipts retain their own scope. Do not infer source parity or Apple acceptance.

## Current state

Workspace: `C:/Users/Alex/Documents/Brine Space`; HEAD remains `1fb93e508f782e5109385e5fa9de12ea743e4cd9`. Many earlier source/art changes are intentionally dirty; no commit, integration or build was made in this closeout.

Latest implementation: `scripts/construction_preview.gd` +UID and a narrow `main.gd` placement-feedback hook show NO SAFE CREW ROUTE / CHECK BUILD ACCESS before spending, with emergency Water text and drone availability. Two paired-UID preview tests are in the `construction-preview` group.

Fresh testing found the companion wrapper rejected Josh's legitimate fire-retreat although its NPC/playback/personality records validated. `scripts/companions.gd` now admits that active dry evacuation while retaining strict invalid-job/legacy checks. New `tests/test_companion_fire_save.gd` +UID belongs to `companions`. Actual position/route are saved, not normalized to idle. No save-format or cost change.

Earlier local work remains documented: [Desalination](DESALINATION_UNIT_2026-10-19.md), [traffic and Marsh recharge](CREW_TRAFFIC_RECHARGE_2026-10-19.md), [polish/balance](POLISH_BALANCE_FOLLOWUP_2026-10-19.md), [bug/optimization pass](BUG_OPTIMIZATION_POLISH_2026-10-19.md), [companion guidance](COMPANION_RECOVERY_GUIDANCE_2026-10-19.md). Later Desalination art/door/decal revisions in the visual bible supersede the initial one-door report. Do not export the entire dirty checkout on the strength of these summaries.

## Verification

- Preview implementation: four relevant headless tests/one native test pass,21/25 preview checks; normal/compact views reviewed. [Implementation report](CONSTRUCTION_ACCESS_PREVIEW_2026-10-20.md), `output/construction-preview-20261020/FINAL.json`.
- Six main fresh600s openings (three seeds x calm/artificial double fire) all survive with Josh/Margot and zero blackouts. In the hard seed, the actual warning rejects19,18 and selects reachable18,21 before payment; Margot joins428.6s. The other two fire recoveries are288.6s. Costs stay5/8 and paid pause/resume is exact.
- All fire cases still have64.8s fires and89.6 dry sprinkler room-seconds, versus prior prepared-water12.9s/no dry spray. No natural hazard frequency, human-fun or broad balance acceptance.
- Seven relevant regression tests pass; final new fire-save fixture15 checks. Six main end checkpoints validate, three fire continuations pass; a separate post-fix fresh confirmation has three successful checkpoint continuations: two during the emergency and one at the end. Initial refused captures and a separate diagnostic reproduction remain retained, not merged into a larger balanced cohort.
- 18 native checks/four actual fresh-emergency normal/compact captures reviewed. Fixture teardown RID/ObjectDB warnings retained; no leak, general performance, headroom, endurance, Apple or actual-release acceptance.
- All2,971 real player files hash-equal; prior cohorts and signed Windows ZIP stat unchanged in the gameplay receipts. No desktop input, export, signing or upload.

[Full results, save diagnosis and source evidence](CONSTRUCTION_WARNING_FRESH_RUN_2026-10-20.md). Authoritative gameplay receipt: `output/construction-warning-opening-20261020/FINAL.json`. This documentation/skill closeout has a separate manifest under `output/session-closeout-gameplay-20261020/`.

## Next action

Recommended next task, **not started or scheduled**: select the intended accumulated source/art changes and prepare an isolated Windows candidate via [RELEASE_WORKFLOW.md](RELEASE_WORKFLOW.md). Validate the actual package's paid opening, construction warning/alternative,5/8-Metal payments, companion emergency Save/Continue, accepted look and room rotations before considering signing/publication. The existing signed runtimef298 ZIP is retained; it has not acquired these local features.

Optional owner review can check warning legibility during a real emergency. No work remains running from this task and no app/host cleanup is requested. Scheduled monitoring was not changed by this closeout. Resume only when the owner starts the next session.
