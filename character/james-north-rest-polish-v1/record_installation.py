from pathlib import Path
import json

P = Path(__file__).resolve().parent
R = P.parents[1]

def atomic(path, transform):
    before = path.read_bytes() if path.exists() else b''
    after = transform(before)
    if after == before:
        return
    tmp = path.with_name(path.name + '.north-rest.tmp')
    tmp.write_bytes(after)
    if (path.read_bytes() if path.exists() else b'') != before:
        tmp.unlink()
        raise RuntimeError('Concurrent edit: ' + str(path))
    tmp.replace(path)

for name in ('native-staged', 'native-staged-berth-bare', 'native-staged-berth-helmet',
             'native-installed', 'native-installed-berth-bare', 'native-installed-berth-helmet'):
    result = json.loads((P / (name + '-validation.json')).read_text())
    assert result['exitCode'] == 0 and not result['timedOut'] and result['realProfileUnchanged'], name

note = '''### James North rest breathing and coherent source — September 30, 2026

North ordinary lie-down, sleep and get-up now select james-north-rest-polish-v1:
three states and18 references per equipment mode. Source-lying-v6 supplies one
coherent body with subtle breathing; source6 is the shared lie/sleep/rise neutral
and closes the loop. Use fixed whole-atlas148/492 scale, exact selected standing
masters, one material curve and owned shared-helmet regions. Do not fit each pose
to silhouette height or stretch calves to reconcile different source rows.

Rejected v4 inherited the old oversized cranium; v5 stretched its second-row
calves. V6 source5 still differed from the breathing row, so all rest joins use
source6. Preserve originals/prompts/hashes and this explicit selection. Projection
still changes skull width; do not claim identical lying/standing head bounds.

231 package checks,187 staged/186 installed player checks and128 staged/127
installed berth checks per mode PASS. Final36 normal-loader native berth poses
and updated lie-down/sleep/get-up master comparison boards visually reviewed.
Scratch owner profiles unchanged. Existing clocks, depth corrections and other
directions retained. This proves the retained North q0 whole-room berth only;
current East-facing station-props bunk is separate. Owner/full-motion/all-layout
acceptance remains open. See docs/JAMES_NORTH_REST_POLISH_HANDOFF_2026-09-30.md.
'''

headline = '''## James North rest polish installed — September 30, 2026

Coherent North lie-down/sleep/get-up now includes subtle breathing and exact
standing master joins in both equipment modes.231 package,186 installed player
and127 installed retained-berth checks per mode PASS;36 final native poses and
updated master comparisons reviewed. Owner profiles unchanged. Current East
bunk is separate; other furniture and full-set motion remain to verify.
[Handoff](JAMES_NORTH_REST_POLISH_HANDOFF_2026-09-30.md). James goal active.

'''
atomic(R / 'docs/CURRENT_STATUS.md', lambda b: b if headline.encode() in b else headline.encode() + b)
for path in (R / 'docs/JAMES_ANIMATION_CONTINUATION_2026-09-29.md',
             R / 'docs/ASSET_PIPELINE_AND_WORKFLOW.md',
             R / 'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',
             R / 'skills/brinespace-character-pipeline/references/crew-consistency.md',
             Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')):
    atomic(path, lambda b: b if note.encode() in b else b + b'\n\n' + note.encode())

handoff = '''# Project handoff

Updated:2026-09-30 · Project:Brine Space · Task:James North rest polish

## Objective and acceptance
Continue all James animations and match accepted masters/material/proportions.
North rest revision installed for owner review; full-set goal remains active.

## Accepted decisions and constraints
Matte neutral suit, consistent body density, exact standing masters, shared helmet.
One fixed source scale; no per-pose body resizing, calf splicing or mirrored art.
Preserve existing furniture geometry, clocks, clearance and save behavior.

## Current state
character/james-north-rest-polish-v1 contains paired three-state manifests,
36 references, reproducible builder/verification/native/review helpers.
scripts/grid_canvas.gd and character/ACTIVE_ASSETS.json select literal paired
manifest paths. Raw source-lying-v6, prompt and origins remain in
character/james-lying-north-v1; v4/v5 rejected candidates retained.
Source6 is the common neutral: lie[0,1,2,3,4,6],sleep[6,7,8,9,10,6],rise reverse.
Fixed148/492 scale and exact idle endpoints. Sleep960ms; lie/rise800ms retained.
Pipeline, bible, continuation, canonical and installed skill lessons updated.

## Verification
231 package checks PASS. Candidate187 player and128 berth per mode PASS.
Installed186 player and127 berth per mode PASS, zero failures/timeouts/profile
changes.36 final normal-loader berth captures reviewed; native82/54/27 paired
source preview and updated lie-down/sleep/get-up master boards reviewed.
Actual retained North q0 whole-room berth chooser, contact, occlusion and all
poses covered. Current East station-props bunk and other layouts not re-tested.
Source/frame contracts do not establish full motion or owner acceptance.

## Next action
Review North ordinary water tread/start/stop boot proportions and West water
death limb seam. Prove workstation-specific facing changes and complete
furniture/meal/equipment/exterior dispatch-airlock-cargo-return handoffs.
Do not rerun old lying-family installation helpers over the new North selection.
No native processes remain. Goal active.
'''
atomic(R / 'docs/JAMES_NORTH_REST_POLISH_HANDOFF_2026-09-30.md', lambda b: handoff.encode())
ledger_path = R / 'character/james-animation-coverage-2026-09-30/consistency-review/review-ledger.json'
def ledger_update(b):
    ledger = json.loads(b)
    ledger['remaining'] = [x for x in ledger['remaining'] if x not in
                           ('North neutral sleep breathing', 'Actual non-East activity arrival facing continuity')]
    for item in ('Generic arrival facing and complete dry tablet clock', 'Coherent North rest body and subtle sleep breathing'):
        if item not in ledger['corrected']:
            ledger['corrected'].append(item)
    item = 'Workstation-specific arrival facing continuity'
    if item not in ledger['remaining']:
        ledger['remaining'].append(item)
    ledger['northRestRevision'] = dict(pack='character/james-north-rest-polish-v1',
                                    finalNativePosesReviewed=36, installedPlayerChecks=186,
                                    installedBerthChecksPerMode=127, ownerReviewPending=True)
    return (json.dumps(ledger, indent=2) + '\n').encode()
atomic(ledger_path, ledger_update)
print('North rest installed evidence and scoped visual milestone recorded; full James goal active')
