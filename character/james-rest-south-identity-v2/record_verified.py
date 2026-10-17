from pathlib import Path
import json, os, uuid, hashlib
P=Path(__file__).resolve().parent;R=P.parents[1]
n=json.loads((P/'validate-evidence.json').read_text());w=json.loads((P/'validate-validation.json').read_text());v=json.loads((P/'packaging-validation.json').read_text())
assert n['failures']==0 and len(n['records'])==36 and not v['failures']
assert w['exitCode']==0 and not w['timedOut'] and (P/'validate.gd.uid').exists()
status='installed_native_source_verified_owner_review_pending'
for mode in ['bare','helmet']:
    f=P/(mode+'-manifest.json');pack=json.loads(f.read_text());pack['status']=status;f.write_text(json.dumps(pack,indent=2)+'\n')
selection={'status':status,'runtimeInstalled':True,'fullSetComplete':False,'sourceVersion':'source-v2.png lying + template-v8 chest interiors','sourceReferences':36,'statesPerMode':3,'fixedBodyScale':.4152542372881356,'fixedHelmetScale':.3644859813084112,'packageChecks':v['checks'],'nativeChecks':n['checks'],'nativeFailures':0,'nativeCaptures':36,'profileGuard':{'realProfileUnchanged':w['realProfileUnchanged'],'profileDelta':w['profileDelta']},'visualReview':'All36 paired source poses and all36 normal-renderer native captures reviewed; expanded chest comparison reviewed. Static supported head and alpha; four template-authored chest interior details only. No claim of whole generated breathing geometry.','nativeScope':n['scope'],'remaining':['Owner full-motion review','Continuous motion and actual furniture/gear/travel/task handoffs across full James library'],'sources':{str(f.relative_to(R)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [P/'source-v2.png',R/'character/james-rest-south-sleep-template-v8/source.png']}}
(P/'selection.json').write_text(json.dumps(selection,indent=2)+'\n')
note='''

## James South reclining identity and supported sleep — October 1, 2026

Installed james-rest-south-identity-v2 paired lie/sleep/get-up override after
ordinary rest material. Whole source-v2 lying figures retain adult leg projection
and compact upward-pitched heads; one inherited .4152542373 body ruler, accepted
South shell donors at .3644859813. Exact standing masters, neutral joins, reversed
get-up and six600ms sleep slots retained. Other facings unchanged.

Template-v8 generated chest details provide four sleep interiors inside the
exact neutral silhouette. Head/collar/hands/tools/pelvis/boots and every alpha
pixel remain exact neutral; source0/5 exact whole neutral. This is small stationary
chest-detail motion, not a newly articulated full-body breathing source. Template
copies were reference-only; generated output is separate and hashed. One frozen
.2246958511 template ruler, constant[0,1] translation, approved matte curve once
and pooled shared material gains. No per-frame shape/exposure normalization.
Reclining full-face v2/v3 sleep rows and narrow/tall v4/v5 rejected. Direct v6/v7
both terminal/downloaded/rejected for camera/sole drift; estimated $0.19 each,
not verified billing. No provider/native job remains live; earlier submitted note
is superseded. Expanded chest/source boards and all36 native pose crops reviewed.

173package/225normal-renderer native checks,0failures; all36 prescribed South
life-stage source poses captured, clocks/pivots/depth/pixels checked. Engine0,
no timeout; scratch APPDATA and strict owner fingerprint unchangedtrue/delta[].
No actual South furniture journey/Continue/locker claim: ordinary retained berths
choose North, specialized East bunk remains its separate action family. Full
James goal active; continuous/full-family joins and owner review remain open.

Lesson: a stationary rest edit may freeze supported anatomy while adopting
registered chest detail, but cannot claim whole-body authoring or measurable
breathing merely from unique hashes. Review original/source-size and native-scale
consecutive poses. Fixed-ruler matching does not cure video camera zoom. Freeze
nonbreathing supports to avoid boot/tool/material flashes. Handoff:
character/james-rest-south-identity-v2/HANDOFF.md.
'''
for f in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    data=f.read_bytes()
    if b'## James South reclining identity and supported sleep' in data:continue
    content=note.encode();new=content.lstrip(b'\n')+b'\n'+data if f.name=='CURRENT_STATUS.md' else data+content
    tmp=f.with_name(f.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(new);os.replace(tmp,f)
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: 2026-10-01 · Project: Brine Space · Task: James South rest identity

## Objective and acceptance
Full James master/style/proportion/material/motion consistency. Goal active;
South revision installed and source/native verified, owner review pending.

## Accepted decisions and constraints
Compact upward head pitch, adult reclining legs, matte engineering materials,
belt wrench. Fixed inherited rulers, exact standing/shared joins,3600ms sleep.

## Current state
source-v2 lying figures plus generated template-v8 chest interiors. Supported
head/collar/hands/tools/pelvis/boots/all alpha exactly neutral during sleep;
four chest RGB variants, exact neutral0/5. No whole-body motion claim.
Paired36references selected by grid_canvas.gd and ACTIVE_ASSETS.json. Frozen
baseline templates, reproducible builders, source/prompt/hash/rejection evidence.
validate.gd/.uid paired; record_verified.py updates selection and five guides.

## Verification
173package/225native checks0fail, all36 normal-renderer prescribed life-stage
captures reviewed in both gears; enlarged chest and whole source boards reviewed.
Engine0/no timeout/strict real-profile unchangedtrue,delta[]. No natural South
berth/Continue/locker claims; ordinary berth selectsNorth, East bunk separate.
Direct v6/v7 terminal rejected for zoom/sole drift, estimated$0.38 unverified bill.

## Next action
Verify deterministic rebuild and refresh selected inventory. Continue full-family
source/master/motion joins and actual applicable furniture/gear/travel contexts.
No provider/native job live. Full objective remains active/incomplete.
''')
print(json.dumps({'status':status,'packageChecks':v['checks'],'nativeChecks':n['checks'],'profileDelta':w['profileDelta']}))
