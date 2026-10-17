from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-rest-west-candidate-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
report=json.loads((O/'validation.json').read_text());assert report['returnCode']==0 and '102 checks,0 failures' in (O/'native.log').read_text()
master=R/'character/crew-runtime-matte-v1/veld/frames/idle-west-transition-matte-v1/000.png'
binding={'generation':'exec-858abccf-95b4-4df1-a5f3-dacb2bb551e6','provider':'built-in imagegen','prompt':'sources/prompt-v1.txt','promptSha256':sha(P/'sources/prompt-v1.txt'),'source':'sources/rest-v1.png','sourceSha256':sha(P/'sources/rest-v1.png'),'reference':master.relative_to(R).as_posix(),'referenceSha256':sha(master),'submittedReference':'sources/master-inspection.png','submittedReferenceSha256':sha(P/'sources/master-inspection.png'),'inspectionScale':4,'closedDonor':'character/veld-death-ground-west-coherent-v1/sources/canonical-head-closed.png','closedDonorSha256':sha(R/'character/veld-death-ground-west-coherent-v1/sources/canonical-head-closed.png')}
(P/'sources/reference-binding.json').write_text(json.dumps(binding,indent=2)+'\n',encoding='utf-8')
index=R/'tests/index.json';data=json.loads(index.read_text());key='test_veld_rest_west_candidate'
if key not in data['subsystems']['veld-rest']:data['subsystems']['veld-rest'].append(key)
data['lanes'][key]={'lane':'native','reason':'Independent west paired rest source and finite/reverse/held playback need native148/82 visual review.'};index.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
note='''

## Veld paired west generic rest candidate - October 1, 2026

Independent west6pose source exec-858abccf-95b4-4df1-a5f3-dacb2bb551e6 references selected idle-west-transition-matte-v1 only. Nose left upright, head right/boots left supine; west teal hip tool and boxed science patch retained, no east mirroring. One148/473=.312896 anatomical ruler and pooled spatial skin/brown-hair/neutral/science grade. Exact selected bare and shared-equipped west standing entries;256/p128,224/H148. Six states/26references from12exports:1840ms finite lie-down and exact reverse rise, held closed sleep. Native34x38west shell at scale1, anchor17,35, roll0/0/0/-12/-70/-70; existing closed donor changes8RGBpixels only, original alpha/hardware outside eye preserved.79package checks/17deterministic files and102actual-player checks pass. Native148/82 whole board and finite browser/held endpoints reviewed. Overall scratch runner FAILED: last_session.json changed among2,931real non-log files during4.95s interval; no attribution or clean-profile claim. Engine0, no fixture failures. Godot generated paired test UID. Candidate not normally selected; accepted bunk unchanged. World/furniture/rest head placement/life death joins and whole-set acceptance remain unproven. Full goal active; own north/south generic rest and seated/life/whole-set polish next. Handoff:character/veld-rest-west-coherent-v1/HANDOFF.md.

Lesson: opposite rest must be authored from its own directional master: upright facing alone cannot establish supine head/boot orientation or tool ownership. Preserve distinct west tool case while grading cloth; one standing-derived ruler must apply through supine length. Reuse exact hardware/closed expression and rotate at a registered neck without per-pose shell scale changes. Source/actual-player proof does not establish life-stage cadence or furnished placement.
'''
for rel in ['docs/CURRENT_STATUS.md','docs/VELD_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    p=R/rel;old=p.read_bytes()
    if note.lstrip().encode() not in old:p.write_bytes(note.lstrip().encode()+old if rel=='docs/CURRENT_STATUS.md' else old+note.encode())
installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')
if note.lstrip().encode() not in installed.read_bytes():
    with installed.open('ab') as f:f.write(note.encode())
html=P/'index.html';s=html.read_text(encoding='utf-8').replace('Packaging and native player review are pending.','79 packaging and102 player checks pass.').replace('fine motion polish remain.</p>','fine motion polish remain. Overall native runner retains a profile-guard failure.</p>').replace('slower1840ms','slower 1840ms');html.write_text(s,encoding='utf-8')
(P/'HANDOFF.md').write_text('''# Project handoff

Updated:2026-10-01 · Project:BrineSpace · Task:Veld west generic rest

## Objective and acceptance
Full master-matched Veld animation set and whole-set polish remain active/incomplete. Independent paired west generic rest candidate; owner/world acceptance unproven.

## Accepted decisions and constraints
Selected west transition idle and shared west equipped idle own identity/geometry/materials. Nose left upright/head right supine; west case and boxed patch, no mirroring. One148/473body scale/pooled grade. Exact native34x38helmet,17,35neck anchor,8pixel closed donor, no hardware resizing.1840ms lower/exact reverse rise/held sleeping endpoint; accepted bunk unchanged, no normal override.

## Current state
This folder holds new raw source/exact prompt/hash-bound sole reference, explicit extraction/ruler/spatial material windows,12paired exports/6states/26refs, canonical fit/closed donor, deterministic verifier, finite browser and full boards. New paired test .gd/.uid and scratch runner; native veld-rest index lane. Current status/continuation/pipeline/bible/maintained and installed skill reference updated. No commit/export.

## Verification
79package checks/17deterministic files: source/473ruler, exact entries/hardware, bounded closed expression, protected body outside head mask, reversed/held paths, floor223±1/no clipping.102actual-player checks cover pixels/metadata/finite1840ms/snapshot/all3roles/both gears. Native148/82 board and browser terminal lowering/rise/sleep reviewed. Engine0/0fixture failures; overall runner FAILED from last_session.json delta among2,931non-log files in4.95s explicit scratch interval. No attribution/restoration/clean-profile/furniture/life/death/normal-selection claim.

## Next action
Author own north/south rest cameras and correct supine helmet projections. Seated/life family, furniture/world-head alignment and interrupted-rest deaths need their own proof; stage duration must match1840ms source before selection. Full cross-family grade/detail/proportion/motion polish and dry-death normal selection remain. No blocker; do not mark full goal complete.
''',encoding='utf-8')
paths=[p for p in P.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='candidate-evidence.json']
paths.extend([R/'tests/test_veld_rest_west_candidate.gd',R/'tests/test_veld_rest_west_candidate.gd.uid',R/'tools/run_veld_rest_west_candidate.py',index,R/'character/veld-death-ground-west-coherent-v1/sources/canonical-head.png',R/'character/veld-death-ground-west-coherent-v1/sources/canonical-head-closed.png'])
paths.extend(O/n for n in ['validation.json','native.log','native-contact.png','profile-before.json','profile-after.json'])
e={'normalSelection':False,'packagingChecks':79,'playerChecks':102,'runner':report,'scope':'paired west source/player/native; no furniture/life/death/full-family acceptance','files':{p.relative_to(R).as_posix():sha(p) for p in paths}}
(P/'candidate-evidence.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8');print(json.dumps({'boundFiles':len(paths),'checks':181,'normalSelection':False}))
