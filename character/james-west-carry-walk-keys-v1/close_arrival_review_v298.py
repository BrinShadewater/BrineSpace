from pathlib import Path
import json,hashlib,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1]
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
receipts=[('arrival-turn-sequence-v291','871abafc-a890-47a0-823d-8ae51da1f20b','rejected_before_native_clipped_and_oversized'),('arrival-turn-pose1-v292','8a03548c-be18-4804-a6d7-58a30c427fa8','rejected_as_early_turn_orientation_clusters_with_midway'),('arrival-turn-pose2-v293','8458299a-2185-454e-8e3e-29acbd4e1066','superseded_early_turn_orientation_clusters_with_midway'),('arrival-turn-pose4-v294','9af3c70e-3fc2-4c2f-9407-2d952a2ec4ca','rejected_late_turn_head_rotated_toward_viewer'),('arrival-turn-pose4-v296','230553f4-7e15-457e-886b-1d01eb75c060','provisional_orientation_preserving_source'),('arrival-turn-pose2-v297','4ea4b121-45be-42cd-84ca-3aad33aa4783','provisional_early_angle_source_registration_and_identity_pending')]
for folder,execution,verdict in receipts:
 o=p/folder;d=json.loads((o/'inputs.json').read_bytes())
 for f,h in d.get('referenceSha256',{}).items():assert sha(r/f)==h
 if 'sourceFile' in d:assert sha(r/d['sourceFile'])==d['sourceSha256']
 assert sha(o/'prompt.txt')==d['promptSha256']
 (o/'generation.json').write_text(json.dumps(dict(state='terminal_copied',execution=execution,method='builtin_imagegen',rawSha256=sha(o/'raw.png'),prompt='prompt.txt',disposition=verdict),indent=2)+'\n')
 if folder.endswith('v291'):continue
 review=dict(disposition=verdict,rawVisuallyReviewed=True,sourceBoardReviewed=True,geometry=json.loads((o/'registration-diagnostic.json').read_bytes()),selected=False,sourceAcceptance=False,normalChanged=False,fullGoalComplete=False)
 (o/'review.json').write_text(json.dumps(review,indent=2)+'\n')
for name,count,captures in [('arrival-turn-pose4-v296',22,1),('arrival-turn-chronology-v298',57,6)]:
 o=p/name;v=json.loads((o/'native_probe-validation.json').read_bytes());n=json.loads((o/'native-evidence.json').read_bytes());f=json.loads((o/'native-inputs.json').read_bytes())
 assert (n['checks'],n['failures'],n['captures'])==(count,0,captures)
 assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'] and not v['profileDelta']
 assert all(sha(r/x)==h for x,h in f['preLaunchSha256'].items())
o=p/'arrival-turn-chronology-v298';d=json.loads((o/'inputs.json').read_bytes());assert all(sha(r/x['file'])==x['sha256'] for x in d['sources'])
report=dict(disposition='provisional_partial_bare_turn_chronology',sourceBoardReviewed=True,detailBoardReviewed=True,nativeBoardsReviewed=6,nativeChecks=57,nativeFailures=0,decodedFramesExact=6,clockTotalMs=800,normalChanged=False,selected=False,sourceAcceptance=False,continuousMotionObserved=False,fullGoalComplete=False,findings=['V295 full chronology exposes multi-reference yaw clustering:292/293 similar to290,294 late head turns toward viewer. All within148-149 extent did not certify correct rotation.', '296 single original-pose target preserves mostly rear-facing orientation,149high/crown76/sole224; right bound moves1pixel. Raw/source/native4sizes viewed;22checks0. Fine cloth is still less dense than original master and whole identity not accepted.', '297 single original early-pose target restores early side-facing angle.150high/crown76/sole225 versus original148/crown77/sole224; onepixel sole shift and head/material differences remain, not body-fit corrected.', '298 includes old0/1/5 and new297/290/296, with exact existing800ms timing. Middle290 brighter and more face exposed than neighbors; old1/2 angle spacing still weak. Equipment/head/boot shapes and materials change across joins.', 'Latest west carry and current north-unload remain incompatible exact endpoints; paired helmet/stance physical contact/controller arrival/adoption/save lifecycle not covered. No normal code/art selectors changed.'])
(o/'review.json').write_text(json.dumps(report,indent=2)+'\n')
ledger=p/'material-repair-progress.json';old=ledger.read_bytes();j=json.loads(old);j['arrivalTurnChronologyReview']=dict(version=298,file=(o/'review.json').relative_to(r).as_posix(),sources=[290,296,297],retainedOldPhases=[0,1,5],selected=False,sourceAcceptance=False,normalChanged=False);j['arrivalTurnReview']['rejectedSourceTrials']=[288,289,291,292,293,294];j['nextVisualRepair']='298 provisional bare chronology restores early/late angles using single original-pose targets. Correct bright/face-exposed290 middle, weak early angle spacing, exact latest carry/unload joins and head/hardware/material identity.297 sole1pixel low; no fitting to hide it. Paired helmet, actual arrival, stance contact, normal lifecycle and full-library polish remain.';assert ledger.read_bytes()==old;ledger.write_text(json.dumps(j,indent=2)+'\n')
section='''### James full arrival-turn chronology exposes yaw collapse - October3,2026

V291 multi-pose atlas rejected before native: two sources207/208high clipped at
canvas floor; later201high, versus original148/149.292/293/294 single-pose edits
keep148/149extents but V295 chronology proves wrong angle spacing:292/293 cluster
with290 and294 late head faces viewer. Rejected/superseded for intended chronology;
raw/source/detail/full boards inspected, six builtin terminal receipts frozen.

Single original-pose-only refinements296/297 preserve late/early orientation better.
296149high/crown76/sole224 like original, right edge1px wider;22nativechecks0/1
four-size comparison viewed.297150/crown76/sole225 vs original148/77/224; gross
registration close but sole1px low and head/material still provisional. No body-fit
scaling, translation, recoloring or anatomy patching. One whole1254to256 resize.

V298 full six bare chronology old0/1/5 plus297/290/296, original800ms clocks.
Six decoded APNGframes byte-exact,57nativechecks0/6four-size phase boards all viewed.
Both native runs scratch-isolated, owner unchanged, frozen sources/runtime stable.
Middle290 brighter and face more exposed than neighbors; weak early yaw spacing,
equipment/head/boot detail and latest carry/north-unload endpoint joins unresolved.
Not continuous observed motion, paired helmet, physical stance contact, ordinary
arrival/controller/save acceptance. Normal bank unchanged; full goal incomplete.

Lesson: matching source extents does not prove correct orientation or sequence
continuity. Multi-reference appearance can pull distinct poses toward one angle.
Full chronology must judge actual head/torso/hip/foot projection and equipment,
not requested degree labels. Single pose targets preserve orientation better in
these retries, but do not automatically recover original master fidelity.
Next middle/early spacing and exact endpoint source joins, full master grade and
anatomy/gear continuity, shared helmet and actual arrival/lifecycle, then full-family
consistency/polish. Handoff:
character/james-west-carry-walk-keys-v1/arrival-turn-chronology-v298/HANDOFF.md.
'''
guides=record_guides(r,section,'### James planted turn geometry anchor yields provisional source')
(o/'HANDOFF.md').write_text('''# Project handoff

Updated: October3,2026 · Project: Brine Space · Task: James arrival-turn sources

## Objective and acceptance
Complete master-matched James animation set, normal lifecycle, then all-family polish.

## Accepted decisions and constraints
Matte original grade, muted yellow, original proportions and perspective. Wrench on
belt, case in hands. Preserve whole registered source; no fitting/regrading to hide drift.

## Current state
291 rejected oversized/clipped atlas.292/293/294 chronology exposed yaw clustering.
296 mostly-rear and297 early side-facing single-target retries improve orientation.
298 partial six-source bare turn old0/1/5+297/290/296 with comparison sources, APNG,
native manifest/probe/paired UID, six captures, frozen inputs and review. Normal bank
unchanged. Generation receipts and ledger closed; pipeline/bible/skills updated.

## Verification
All source/raw boards actually inspected;295 and298 full chronologies/detail boards.
296 native22/0/1board,298 native57/0/6boards at148/82/54/27 all viewed. Both scratch
owner unchanged; frozen hashes stable. Six APNGdecoded frames exact at800ms. No
continuous observed playback, shared helmet or ordinary arrival/lifecycle proved.

## Remaining work and next action
Correct290 brighter middle and head yaw, weak early angle spacing,297 sole1px drift,
case/belt/wrench/backpack/head/body consistency and exact latest carry/unload joins.
Then shared helmet and actual arrival integration/stance/normal bank/checkpoint/
interruptions/Continue. Full action/direction coverage and consistency/polish remain.
''',encoding='utf-8')
with (p/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n'+section)
folders=[p/x[0] for x in receipts]+[p/'arrival-turn-chronology-v295',o]
rasters=[f.relative_to(r).as_posix() for folder in folders for f in folder.glob('*') if f.suffix in ('.png','.apng')]
attrs=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(rasters)+'\0').encode(),cwd=r,capture_output=True,check=True).stdout.split(b'\0');assert all(attrs[i+2]==b'lfs' for i in range(0,len(attrs)-1,3))
print(json.dumps(dict(receipts=6,nativeRuns=2,checks=79,failures=0,capturesReviewed=7,decodedExact=6,guides=guides,lfsRasters=len(rasters),goalComplete=False)))
