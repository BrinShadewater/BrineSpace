# Josh assists derelict restoration

Updated: October 20, 2026 · Project: BrineSpace · Task: visible companion restoration payoff

## Objective and acceptance

Owner approved Josh helping restore derelict rooms, including Margot's ward,
without new UI, changed costs, bypassed physical access or changed artwork.
His existing 25% work-rate bonus applies only during actual torch assistance.

## Accepted decisions and constraints

The architect retains the paid job and must be standing at its work point and
welding. Josh uses his existing route selection and torch enter/active/exit
animations. Only dry, standable, nearby assistance in the connected workroom
counts; no bonus during travel, deployment, stow, pause, door lockdown, fire,
flooding, worker absence, cancelled work or completed restoration.
Existing hull jobs retain priority. Base 18-second ward work, eight-Metal companion
repair and eight powered seconds to restart/thaw remain unchanged. No materials
are charged or refunded by assistance. Existing research work multipliers compose
with the helper multiplier; no change to permanent companion ownership.

## Current state

- `scripts/companion_repair.gd`: reads the transient paid ward assignment after
  checking hull jobs; verifies current connection/worker/room safety and tags the
  target so ward help cannot accidentally multiply hull work.
- `scripts/ward_repair.gd`: applies the helper multiplier to real crew work only.
- `scripts/companion_npc.gd`: existing activity wording now says assisting repairs,
  covering both job types. No new UI surface or art change.
- `tests/test_josh_ward_assistance.gd` and paired UID: physical route/assistance,
  actual paid work, interruption guards, disk Continue, completion and thaw.
- `tests/test_josh_ward_assistance_native.gd` and paired UID: same controls with
  native capture of the two actors; `tests/index.json` adds the focused subsystem.
- `docs/CURRENT_STATUS.md`: acceptance and remaining scope.

## Verification

Existing hull-assistance, ward-repair and companion fire-save tests pass.
Focused headless fixture passes 34 checks before the final additional immediate
fire guard; final native fixture exercises the updated suite plus rendering and
passes 36 checks. Disk Save/Continue reconstructs the transient ward assignment
and retains physical torch state and paid resources.

Controlled paired checkpoint: 18.0 seconds of remaining welding alone versus
15.5–15.6 seconds with Josh's actual intermittent torch assistance. Both restore
the same checkpoint; helper travel into position happened before this snapshot.
This is not total rescue time or a fresh opening balance comparison. Ordinary
work consumption completes the ward; Margot remains asleep at 7.9 powered seconds
and emerges at 8.0. No shortening of powered thaw.

Native 1600x900 capture reviewed: Josh and Bill stand separately at the connected
corridor's ward-side worksite. First capture was obscured by the hand and unfocused
camera; final fixture hides the hand and centers the workroom. No human-input
automation. Evidence: `D:/bs-josh-ward-20261020`; final image:
`output/josh-ward-20261020/assisting.png`. Runner receipts:
`output/test-runs/20261020-180237-headless`, `20261020-180440-headless`,
`20261020-180631-native`.

Initial fixture passed its functional checks but hit music teardown error; the
fixture now disables the music process before shutdown. All probes used scratch
APPDATA. All 2,971 owner files hash-equal; signed ZIP stat unchanged.

## Next action

Human opening playtest: does Josh visibly helping with the next rescue make his
recovery feel worthwhile? Other ward layouts, natural opening timing and packaged
behavior are not newly certified. Source only; no export/publication. Margot's
proposed resting-crew behavior remains unimplemented and separate.
