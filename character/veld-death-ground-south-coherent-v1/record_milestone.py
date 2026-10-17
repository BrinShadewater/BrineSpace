"""Bind staged south source, native evidence and scoped project lessons."""
from pathlib import Path
import json,hashlib
import numpy as np
from scipy.ndimage import label
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-death-ground-south-candidate-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
native=json.loads((O/'validation.json').read_text());pack=json.loads((P/'paired-verification.json').read_text())
assert pack['checks']==56 and pack['failures']==0 and native['returnCode']==0
raw=P/'sources/death-v1.png';a=np.array(Image.open(raw));labs,n=label(a[:,:,3]>180);counts=np.bincount(labs.ravel());counts[0]=0
ids=sorted(np.argsort(counts)[-6:],key=lambda k:(np.where(labs==k)[0].mean()//512,np.where(labs==k)[1].mean()))
poses=[]
for k in ids:
    y,x=np.where(labs==k);poses.append({'box':[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)],'opaquePixels':int(counts[k])})
(P/'sources/source-review.json').write_text(json.dumps({'generation':'exec-fabe8c7f-d6bd-449f-854c-c1a26d00ebff','sourceSha256':sha(raw),'size':list(Image.open(raw).size),'poses':poses,'review':'six independent frontal poses, connected limbs, original front chest/scanner/vial ownership and boxed patches; fixed-ruler full-size/native review retained'},indent=2)+'\n')
index=R/'tests/index.json';data=json.loads(index.read_text());key='test_veld_death_ground_south_candidate'
if key not in data['subsystems']['veld-dry-death']:data['subsystems']['veld-dry-death'].append(key)
data['lanes'][key]={'lane':'native','reason':'Paired south dry-collapse candidate and authored forward-pitch heads need native148/82 visual board.'}
index.write_text(json.dumps(data,indent=2)+'\n')
note='''

## Veld south paired dry-collapse candidate — October 1, 2026

Independent frontal6pose source exec-fabe8c7f-d6bd-449f-854c-c1a26d00ebff fitted at one148/492=.300813 ruler, exact selected bare/helmet idle entries, dry256/p128,224/H148 and original1420ms finite corpse. Master35x39front helmet with bounded16RGBpixel closed-eye source exec-bf6e7f3c-ec9c-4fee-8dc2-91edbd2991d3 for4/5; original component alpha/shell/visor/collar/face outline protected. Upright helmet on early lowered bare heads missed depth pitch. Authored15/25degree source v2 exec-80f14b1a-e3b4-4b7c-be2b-3a8bb48473ad now fits1/2 at one35/588source ruler, native35x39/36x39/36x38; no per-angle normalization. First pitch source had5–8% width growth, retained/revised; v2 rounds to1extra native pixel while allowing foreshortening. Both source generations/exact prompts kept. Bare6 and helmet0/3/4/5 exact through pitch revision.56 paired package checks/22deterministic files and70 actual-player checks PASS; native148/82 reviewed. Overall runner FAILED profile guard: last_session.json changed,2,930real non-log files fingerprinted, scratchAPPDATA explicit; current7.21s and earlier6.35s failed guard reports retained. No unchanged-owner claim, no attribution/restore or green-chasing rerun. Candidate only; normal survival/Continue/clearance/other-state joins unproven. North dry collapse, generic rest/life and complete family identity/material/detail/perspective/motion polish remain. Full goal active. Handoff:character/veld-death-ground-south-coherent-v1/HANDOFF.md.

Lesson: unchanged upright master pixels certify construction, not depth pitch. Compare head/visor orientation with actual lowering poses before reusing a cardinal component. Author changed projection from the master; calibrate a single source ruler from its upright component and keep source/face/material/size comparisons explicit. Preserve unchanged poses and retain width-drift sources rather than resizing each angle to make a test pass. Record native rounding differences separately from visual acceptance. Idempotent milestone insertion must compare the same whitespace-normalized text it writes; one exact duplicate west status entry was removed without modifying neighboring owner/actor entries.
'''
for rel in ['docs/CURRENT_STATUS.md','docs/VELD_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    p=R/rel;old=p.read_bytes()
    if note.lstrip().encode('utf-8') not in old:p.write_bytes(note.lstrip().encode('utf-8')+old if rel=='docs/CURRENT_STATUS.md' else old+note.encode('utf-8'))
installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')
if note.lstrip().encode('utf-8') not in installed.read_bytes():
    with installed.open('ab') as f:f.write(note.encode('utf-8'))
handoff='''# Project handoff

Updated:2026-10-01 · Project:BrineSpace · Task:Veld south paired dry-collapse source/pitch

## Objective and acceptance
Full matching Veld animation set, then whole-set master/perspective/proportion/material/detail/motion polish. South paired pack is staged; goal remains incomplete and active.

## Accepted decisions and constraints
Selected idle-south-breathing-v1 and selected shared south helmet/native35x39 are authorities. Independent front chest/tool/department ownership and connected two-arm/two-leg anatomy. One148/492body ruler, original1420ms finite6slots/dry256/p128,224/H148. Exact cardinal entries; no normal selection, commit/export, owner profile restoration or gameplay change.

## Current state
Raw6pose frontal source, exact prompt/reference binding and6bare/6helmet exports. One clip/material master grade. Closed source adds16native RGBpixels to terminal4/5, protecting all original component alpha/outside eye pixels. Initial front native overlay in1/2 missed depth pitch; preserved in revisions/upright-head-v1. Two pitched source generations kept: v1 had5–8% width growth; corrected v2 fitted by one35/588ruler to35x39/36x39/36x38, source upright calibrates only, selected original upright remains0. Authored15/25pitch inserted1/2; bare6/helmet0,3,4,5 exact. fit_pitched_heads.py/build_helmet.py/registration/verification bind source, grade and neck anchors. Finite paired HTML/native boards retain source-scale review.

## Verification
56paired package/master/component/protected-body/pitch/source checks PASS;22files deterministic.70actual CrewSpritePlayer checks0failures: paired12source pixels/metadata/slots, finite corpse, arbitrary initial clock, validated in-memory snapshot/paused restore. Native148/82 complete board reviewed after pitch revision. Overall native runner FAILED because last_session.json changed among2,930real non-log files during7.21s interval; explicit scratchAPPDATA recorded. Previous6.35s guard failure also retained. No clean-profile/attribution/normal loader/mortality/disk Continue/clearance claim. Source size/pose/detail visually close;1pixel pitched width difference and fine face/hardware/cadence/cross-family consistency remain reviewable.

## Next action
Independent north dry-collapse source from its selected rear master; fit actual pitch/neck/head hardware and fixed body scale. Then complete cardinal family and actual death-entry joins from lowered/cargo/walk states, survival/save/Continue/world clearance before normal selection. Generic rest/life and broad master/detail/material/motion polish remain. No blocker; profile failures are retained evidence, not a reason to restore owner data or retry unchanged art.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
paths=[p for p in P.rglob('*') if p.is_file() and '__pycache__' not in p.parts and 'revisions' not in p.parts and p.name!='candidate-evidence.json']
paths += [R/'tests/test_veld_death_ground_south_candidate.gd',R/'tests/test_veld_death_ground_south_candidate.gd.uid',R/'tools/run_veld_death_ground_south_candidate.py',index]+[O/n for n in ['validation.json','native.log','native-contact.png','profile-before.json','profile-after.json']]
evidence={'scope':'paired south dry candidate with authored forward pitch, actual-player pixels/finite/in-memory paused snapshot; no normal survival/Continue/world claim','normalSelection':False,'packagingChecks':56,'nativePlayerChecks':70,'nativeRunner':native,'files':{p.relative_to(R).as_posix():sha(p) for p in paths}}
(P/'candidate-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
print(json.dumps({'boundFiles':len(paths),'packagingChecks':56,'playerChecks':70,'runnerPassed':native['passed'],'normalSelection':False}))
