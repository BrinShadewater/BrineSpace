"""Record observed complete source coverage and bounded alias correction evidence."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-current-family-audit-2026-10-03-post-cargo'
ALIAS=ROOT/'character/marsh-v2/supplemental/cargo-unload-matched-v1'
read=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=read(BASE/'inventory.json');pending=r['heldReviewReconciliation'].get('newlyReviewedFamilies',r['heldReviewReconciliation']['pendingFamilies'])
assert len(pending)==37
observations={
 'unloaded-water':'Start/stop whole poses reverse between tread and prone swim. Turns show genuine cardinal progression; oppose turns route through intermediate facing. Broad arm spread and projected height vary with camera/pose. Head/body detail, kick, root and transitions remain provisional; no continuous cadence/contact inference.',
 'walk-step-and-stop-phases':'All walk-step directions and six North/six South stop-phase banks inspected through exact complete readable pages. Recognizable selected identity, but South head/face and suit-panel detail varies between gait phases. Occupied height varies with stride; do not fit poses to a rectangle. Foot contact/phase-to-idle motion still needs native review.',
 'retained-gestures':'Complete equip/remove aliases inspected, six150ms holds with own idle endpoints. Generic right-arm action retained; android helmet capability remains disabled. Head/material/boot and moving joins still provisional.',
 'cargo':'Full carry, pickup/unload, drain, loaded swimming and all turns inspected. Case/hand and directional progression visible. Detail/grade/body/root/kick/contact consistency still provisional. Retained cargo-unload board revealed stale old-case/body sources; corrected separately with exact reviewed unload drawings.'}
records=[]
for b in r['boards']:
    assert sha(BASE/b['file'])==b['sha256']
    for k in b['keys']:
        assert all(sha(ROOT/f['path'])==f['sha256'] for f in r['states'][k]['frames'])
    if b['family'] in pending:
        f=b['family']
        group='unloaded-water' if f in ['swim-start','swim-stop','tread'] or f.startswith('swim-turn-') else 'walk-step-and-stop-phases' if f=='walk-step' or f.startswith(('walk-stop-p','walk-stop-phase')) else 'retained-gestures' if f in ['equip-helmet','remove-helmet'] else 'cargo'
        evidence={'scope':'Complete held-source drawings actually inspected this turn; no continuous motion or full master-detail/native/contact acceptance.','observations':observations[group]}
        if group=='walk-step-and-stop-phases':evidence['readablePagesReceipt']='readable-pages.json'
        records.append({'family':f,'board':b['file'],'sha256':b['sha256'],'sourceStates':{k:r['states'][k] for k in b['keys']},**evidence})
        b.update(visualReviewed=True,reviewScope=evidence['scope'])
    else:b.update(visualReviewed=True,reviewScope='Exact full board/source evidence reuse in heldReviewReconciliation; no new motion/native acceptance.')
coverage={'inventorySha256BeforeReview':sha(BASE/'inventory.json'),'newlyInspectedFamilyBoards':records,'reusedCompleteFamilyBoards':r['heldReviewReconciliation']['reused'],'coveredHeldFamilyBoards':74,'selectedStates':228,'selectedSlots':1190,'scope':'Pre-alias normal snapshot:37exact reused boards+37newly inspected complete family boards. Four cargo-unload states subsequently replaced; new sources are exact inspected unload drawings plus bounded native evidence. Static coverage is not visual quality or full-goal acceptance.','observations':observations,'fullGoalComplete':False}
(BASE/'held-review-coverage.json').write_text(json.dumps(coverage,indent=2)+'\n')
r['heldReviewReconciliation']['newlyReviewedFamilies']=pending;r['heldReviewReconciliation']['pendingFamilies']=[];r['heldReviewReconciliation']['pendingCount']=0
r['heldReviewScope']='Complete held-source review accounted; master/detail, continuous motion, contact, full save/Continue and polish still incomplete.'
(BASE/'inventory.json').write_text(json.dumps(r,indent=2)+'\n')
p=ALIAS/'verification.json';v=read(p)
for b in v['boards']:assert sha(ALIAS/b['file'])==b['sha256'];b['actuallyInspected']=True
v['visualScope']='All four complete native first/middle/last alias comparison triplets inspected (12captures). Whole four-pose donor unload states already inspected in complete source board; reused exact16PNG sources. No continuous cadence/live actor/fullSave/Continue acceptance.'
v['visualObservations']='Old broad body/case drawings replaced by the same selected unload drawings used elsewhere; exact own-idle endpoint retained. Remaining donor head/detail/material/contact limitations preserved rather than declared fixed.'
p.write_text(json.dumps(v,indent=2)+'\n')
latest=ROOT/'character/marsh-selected-normal-audit-2026-10-03-post-cargo-alias/inventory.json';current=read(latest)
for k,s in current['states'].items():
    donor=k.removeprefix('cargo-') if k.startswith('cargo-unload-') else k
    reviewed=r['states'][donor]
    assert [f['sha256'] for f in s['frames']]==[f['sha256'] for f in reviewed['frames']]
    assert s['state']['frameDurationsMs']==reviewed['durationsMs'] and s['state']['loop']==reviewed['loop']
    assert s['pivot']==reviewed['pivot'] and s['standingHeight']==reviewed['standingHeight']
current['heldReviewEvidence']={'coverage':(BASE/'held-review-coverage.json').relative_to(ROOT).as_posix(),'sha256':sha(BASE/'held-review-coverage.json'),'aliasVerification':p.relative_to(ROOT).as_posix(),'aliasVerificationSha256':sha(p),'method':'Every current228state ordered source hashes/holds/loop/pivot/height match reviewed frozen state; cargo-unload matches same-direction reviewed unload. Static whole-source coverage only.','fullGoalComplete':False}
latest.write_text(json.dumps(current,indent=2)+'\n')
note='''
## Marsh complete held-family review and unload aliases — October 3, 2026

Current source review reconciled against normal catalogue, not private overlay:
character/marsh-current-family-audit-2026-10-03-post-cargo.74complete family boards,
228states/1190slots:37byte-identical complete boards reuse scoped prior evidence;
37remaining complete boards actually inspected. Tall walk-step split into two
whole-direction pages; six North and six South stop-phase boards stacked whole.
Exact crops/stack receipts retained; no resizing/paint/interpolation. All current
drawings have held-source coverage, NOT complete master/detail/style/proportion/
grade/cadence/contact acceptance. Source coverage should now direct specific polish,
not repeat inventory generation as proof of quality.

Unloaded swimming start/stop/tread/turns show genuine pose/camera progression;
preserve crouch and foreshortening. Gait head/face and panel detail varies by phase,
especially South; moving idle joins, root/kick/floor contact remain open. Loaded/
dry cargo case/body/head/material transitions still provisional. Generic retained
gestures remain latent and do not enable Marsh's helmet capability.

Concrete mismatch: retained cargo-unload still used old body/case sources despite
unload selecting new reviewed cargo art. tools/rebuild_marsh_art.py and cargo-chain
tools define unload/cargo-unload as the same action. New normal final overlay:
character/marsh-v2/supplemental/cargo-unload-matched-v1/manifest.json,4aliases/16slots
reuse16whole selected unload paths. Original alias holds/facings/waterKinds/depth/
loop/pivot/H preserved, exact own idle endpoints,224other selected states unchanged.
No new generation/raster painting/runtime/controller/room/resource/save changes.
228states/1190slots now87ordered body manifests. Actual controller uses unload-north;
retained alias change is library consistency, not new gameplay reachability.

Native normal player proof109checks/0failures,16exactslots/16same-clock restores,
12captures; all four full comparison triplets inspected.5308bounded source/runtime/
art inputs and2931owner non-log files unchanged under scratchAPPDATA. Terminalexit0,
no ERROR/WARNING/SCRIPT ERROR. New aliases share reviewed whole donor sources;
head/material/cadence/contact limitations remain. Latest authoritative inventory:
character/marsh-selected-normal-audit-2026-10-03-post-cargo-alias/inventory.json.
All228current state hashes/ordered holds/loop/pivot/H matched full reviewed source
coverage (four aliases matched same-direction unload), without inferring quality.

Lesson: same-action aliases can escape a family admission allowlist and retain old
body/prop construction. Trace their actual definitions and consumer first, preserve
alias metadata, share reviewed whole donor paths, verify unchanged unrelated states.
Do not reauthor identical actions independently or overwrite historical masters.
Full Marsh objective active. Next native movement/seams/contact and cross-family
head/detail/material/grade polish, original master references, supported construction/
furniture/expedition behavior and full disk save/title Continue scope as needed.
'''
canonical=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md'
installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md')
assert canonical.read_bytes()==installed.read_bytes()
for path in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',canonical]:
    with path.open('rb') as f:f.seek(max(0,path.stat().st_size-100000));tail=f.read().decode('utf-8',errors='ignore')
    if '## Marsh complete held-family review and unload aliases' not in tail:
        with path.open('a',encoding='utf-8') as f:f.write(note)
installed.write_bytes(canonical.read_bytes())
print('74held family boards accounted;4aliases/16slots corrected;228current states matched reviewed drawings;full goal remains active')
