from pathlib import Path
import json,hashlib,subprocess,collections
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'selected-family-audit-v333';bend=p/'north-unload-low-support-v332'
validation=json.loads((o/'inventory_probe-validation.json').read_bytes());assert validation['exitCode']==0 and validation['realProfileUnchanged'] and not validation['timedOut']
uid=json.loads((o/'allocate_uid-validation.json').read_bytes());assert uid['exitCode']==0 and uid['realProfileUnchanged']
inventory=json.loads((o/'selected-inventory.json').read_bytes());coverage=json.loads((o/'family-coverage.json').read_bytes());provenance=json.loads((o/'pixel-provenance.json').read_bytes())
assert inventory['checks']==9821 and inventory['failures']==0 and coverage['matchedSelectedSlots']==8058 and coverage['unmatchedSelectedSlots']==0 and not coverage['coreMissing']
for source,digest in provenance['bindings'].items():assert hashlib.sha256((r/source).read_bytes()).hexdigest()==digest,source
for file in ['inventory_probe.gd','allocate_uid.gd']:assert (o/(file+'.uid')).is_file()
differences=json.loads((o/'equipment-key-differences.json').read_bytes())
review=dict(normalChanged=False,fullGoalComplete=False,checks=9821,failures=0,selectedStates=coverage['states'],selectedPoses=coverage['poses'],coreFamilies=['idle','walk','interact','inspect','repair','weld','carry','unload'],coreCoverageMissing=[],
    sourceReconciliation=dict(manifests=143,sourceFiles=11453,selectedSlots=8058,unmatched=0,afterRunSourceBindingsStable=True,prelaunchSourceFreeze=False),
    visualReview=dict(boardsViewed=['bare-family-00','bare-family-01','bare-family-02','bare-family-03','diving-helmet-family-00','diving-helmet-family-01','diving-helmet-family-02','diving-helmet-family-03','south-tablet-head-diagnosis'],representativeSlots=192,fullContinuousMotion=False,nativeRenderedReview=False),
    equipmentDifference=dict(bareOnlyCount=len(differences['bareOnly']),helmetOnlyCount=len(differences['helmetOnly']),bareOnlyFamilies=dict(collections.Counter(k.split('-')[0] for k in differences['bareOnly'])),interpretation='Meal/cup and equipment handoff keys; actor predicates require helmet off for meal lifecycle/returns. This is not a blanket missing-helmet diagnosis.'),
    findings=['All eight tested core families have four directions in both gear banks','carry limb/suit bulk differs from selected idle/diagnostics and remains master-polish priority','North unload retains known wide stance/final rise mismatch','South tablet head detail confirms helmet retained at sampled start/middle/end; small-gallery impression of bare head was not a verified defect','repair/weld and core sampled poses do not cover full life/water/death/turn/controller transitions'],
    next='Review full selected carry/idle and turn/unload motion for master identity, cloth, support and bulk; expand actual-source comparison to life/water/hazard/death families, then ordinary lifecycle interruptions/Continue. Keep unload support repair open; do not repeat identical failed leg-edit prompts.')
(o/'review.json').write_text(json.dumps(review,indent=2)+'\n')
media=list(o.glob('*.png'))+list(bend.glob('*.png'));args=b''.join(str(f.relative_to(r)).replace('\\','/').encode()+b'\0' for f in media)
attrs=subprocess.run(['git','check-attr','--stdin','-z','filter'],input=args,cwd=r,capture_output=True,check=True).stdout.split(b'\0');assert all(attrs[i]==b'lfs' for i in range(2,len(attrs)-1,3))
section='''### James selected full-bank inventory and core-family comparison — October 3, 2026

V333 invokes actual Grid replacement loader/ownedJamesCargoPlayer headless under
scratchAPPDATA:9821checks0,338bare/248helmet states,4287/3771selected texture slots.
All148standing-density metadata.143catalog/literal loader manifests,11453unique
source images hashed;8058selectedRGBA slots match current source files,0unmatched.
Post-run source bindings rechecked stable; no prelaunch freeze claim. Duplicate
equivalent file matches are not proof of final load provenance. Probe/UID allocator
paired; two scratch validations confirm owner's real profile unchanged.

Core idle/walk/interact/inspect/repair/weld/carry/unload: four directions each both
gears present. All8family boards/192first-middle-last samples viewed at declared
density/pivot, no pose-bound scaling. Carry legs/suit bulk versus idle/diagnostics,
known North unload stance/final rise remain master-polish concerns. South tablet
detail verifies helmet retained in sampled0/70/140. Initial head crop incorrectly
assumed256canvas; actual184/p92,172 requires registered+36,+52 first. Corrected
diagnostic viewed, no false helmet-loss report.90bare-only keys are84meal+4cup+
2equipmenthandoffs; meal actor predicates require helmet off. Not90missing clips.
Counts/source hashes/sample boards prove coverage/provenance, not full fidelity,
continuous cadence, life/water/death transitions or normal controller acceptance.

V332 built-in lower-body edit uses314bent source, exact standing boot crop and
original master. Crown112/sole224 vs314113/224, butboot spans102..124/131..153
remain wide versusstanding106..125/128..148. Rejected alignment before native.
Raw/corrected three-source H148/82/54/27 board/prompt/input hashes retained;
curved cloth visible, no normal admission. Do not repeat same failed pose request.

Next compare selected carry/idle and full turn/unload motion for master volume,
finish and support; broaden actual-source review to life/water/hazard/death, then
ordinary interruptions/Continue. Full goal active; no production changes here.
Handoff: character/james-west-carry-walk-keys-v1/selected-family-audit-v333/HANDOFF.md.
'''
guides=record_guides(r,section,'### James full unloading clip fidelity review — October 3, 2026')
handoff='''# Project handoff

Updated: October 3, 2026 · James selected family audit and unload support

## Objective and acceptance
Full James set following original masters/style/height/proportions/grade, then
whole-family consistency/polish. Coverage alone is not completion; goal active.

## Accepted decisions and constraints
Original masters, no body fitting/regrading to hide failures, gear identity,
belt wrench/tablet/forward torch, fixed support and actual runtime provenance.

## Current state
332 support edit rejected: floor held, requested knee/boot alignment not achieved.
333 actual normal loader inventory and CPU texture hashes, bounded source match,
complete core-family 192-sample gallery, corrected South tablet helmet detail.
All helper scripts/reports, paired probe UIDs, full provenance, five guides updated.
No production code/source selection changed. Existing unload repair remains open.

## Verification
Headless9821checks0;338bare/248helmet states,8058selected slots.143manifests and
11453sourceimages reconcile all selected pixels. Post-run bindings rechecked;
not prelaunch frozen. Both scratch runs owner-profile unchanged. All8familyboards,
South head detail and332 raw/support board viewed. LFS attributes verified.
Sample/static source review, not full continuous native behavior/master acceptance.

## Next action
Full selected carry/idle motion and turn/unload joins: bulk, matte finish, anatomy,
fixed support; no blind repeat of failed332 leg edit. Broaden selected source review
to life/water/hazard/death, then ordinary controller interruptions/titleContinue.
90bare-only meal/cup/equipment keys are not blanketmissing helmet coverage. Complete
original-master and all-family fidelity before adopting newer provisional sources.
'''
(o/'HANDOFF.md').write_text(handoff)
(bend/'HANDOFF.md').write_text(handoff)
with (p/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n'+section)
ledger=p/'material-repair-progress.json';old=ledger.read_bytes();data=json.loads(old)
data['selectedFamilyAudit']=dict(version=333,file=str((o/'review.json').relative_to(r)),bareStates=338,helmetStates=248,sourceAcceptance=False,normalChanged=False)
data['nextVisualRepair']='Cross-reference selected carry/idle and complete turn/unload motion against original master for bulk/finish/support; broaden full-set life/water/hazard/death comparison and ordinary lifecycle checks.332 support edit rejected; no blind identical retry.'
assert ledger.read_bytes()==old;ledger.write_text(json.dumps(data,indent=2)+'\n')
print(f'Closed actual selected-bank/core-family evidence:9821checks0,8058pixelslots reconciled,192samples viewed,{guides}guides,{len(media)}LFSreviewPNGs. Full goal active.')
