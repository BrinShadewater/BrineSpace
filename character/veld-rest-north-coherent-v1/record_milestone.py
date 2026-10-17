from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-rest-north-candidate-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
report=json.loads((O/'validation.json').read_text());assert report['returnCode']==0 and '102 checks,0 failures' in (O/'native.log').read_text()
refs={'body':('exec-8dab7a37-c432-4859-b317-a02464072aa6','sources/rest-v1.png','sources/prompt-v1.txt','character/crew-runtime-matte-v1/veld/frames/idle-north-breathing-v1/000.png','sources/master-inspection.png'), 'helmet':('exec-8a06b411-a4b4-40b6-a58b-a371e667f50b','sources/pitched-heads-v1.png','sources/helmet-prompt-v1.txt','character/veld-shared-helmet-v1/fitted-north.png','sources/helmet-master-inspection.png')}
binding={}
for key,(generation,source,prompt,master,submitted) in refs.items():
    binding[key]={'provider':'built-in imagegen','generation':generation,'source':source,'sourceSha256':sha(P/source),'prompt':prompt,'promptSha256':sha(P/prompt),'master':master,'masterSha256':sha(R/master),'submittedReference':submitted,'submittedReferenceSha256':sha(P/submitted)}
(P/'sources/reference-binding.json').write_text(json.dumps(binding,indent=2)+'\n',encoding='utf-8')
index=R/'tests/index.json';data=json.loads(index.read_text());key='test_veld_rest_north_candidate'
if key not in data['subsystems']['veld-rest']:data['subsystems']['veld-rest'].append(key)
data['lanes'][key]={'lane':'native','reason':'North independent rest axis/helmet depth pitch and paired player source need native148/82 review.'};index.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
note='''

## Veld paired north generic rest candidate - October 1, 2026

Independent6pose source exec-8dab7a37-c432-4859-b317-a02464072aa6 binds selected rear idle. Straight north axis: feet upstage/head toward viewer supine, no sideways camera drift; rear panel appropriately gives way to chest in sleep, teal tool image-left/white blue-cap vials image-right retained. One148/468=.316239 body ruler and pooled semantic matte grade; source ears/neck spatial windows and selected shaded rear ears own skin, all master warm brown highlights own hair. Exact selected bare/shared helmet standing entry,256/p128,224/H148. Sixstates/26refs from12exports:1840ms finite lie-down/reverse get-up/held sleeping endpoint. New reference-bound helmet depth source exec-8a06b411-a4b4-40b6-a58b-a371e667f50b at one33/500=.066 ruler, sizes33x34/33x33/32x33/33x33. Exact canonical33x35rear shell in standing/seated; authored forward15/back35/back80depth in other poses, no inplane roll or per-pose scaling. Backward tilt moves neck aperture to far/top edge; face hidden. Original supine fit floor225 corrected7source pixels at neck to floor223 without resizing. Protected body outside local head/component regions exact.92package checks/22deterministic files and102actual-player checks pass; native148/82 board and finite browser/held endpoints reviewed. Overall runner FAILED: last_session.json delta among2,931non-log files during6.33s explicit scratch interval; engine0/0fixture failures, no attribution/clean-profile claim. No normal selection, accepted bunk unchanged. Furniture/rest-head placement, life cadence1840ms and death joins unproven. Full goal active: south generic rest, seated/life family and cross-family grade/detail/perspective/anatomy/motion polish remain. Handoff:character/veld-rest-north-coherent-v1/HANDOFF.md.

Lesson: a rear upright bitmap rotated on the image plane cannot supply a backward depth tilt; the collar must move to the appropriate far edge, rails/vents/ear hardware follow projection. Use a single upright-derived component ruler for authored pitches, distinguish authored hardware projection from unchanged master pixels, and inspect head/neck/floor contact at native scale. Preserve warm master hair highlights before replacing the rear skin mask with explicit ear authority.
'''
for rel in ['docs/CURRENT_STATUS.md','docs/VELD_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    p=R/rel;old=p.read_bytes()
    if note.lstrip().encode() not in old:p.write_bytes(note.lstrip().encode()+old if rel=='docs/CURRENT_STATUS.md' else old+note.encode())
installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')
if note.lstrip().encode() not in installed.read_bytes():
    with installed.open('ab') as f:f.write(note.encode())
html=P/'index.html';s=html.read_text(encoding='utf-8').replace('Packaging and native player review pending.','92 packaging and102 player checks pass.').replace('fine motion polish remain. </p>','fine motion polish remain. Overall native runner retains a profile-guard failure.</p>').replace('slower1840ms','slower 1840ms');html.write_text(s,encoding='utf-8')
(P/'HANDOFF.md').write_text('''# Project handoff

Updated:2026-10-01 · Project:BrineSpace · Task:Veld north generic rest

## Objective and acceptance
Full master-matched Veld set and whole-set polish active/incomplete. Independent paired north generic floor-rest candidate only; owner/world/full-family acceptance unproven.

## Accepted decisions and constraints
Selected north bare/shared-equipped idle own camera/material/height; teal tool left/vials right. Straight north axis, supine boots upstage/head downstage; fixed camera/natural foreshortening. One148/468body ruler/pooled semantic grade.33x35exact canonical rear head in standing/seated; authored15/-35/-80depth projections at one33/500component ruler, no inplane roll.1840ms lower/exact reverse rise/held rear sleeping endpoint. Accepted bunk unchanged; no normal override/commit/export.

## Current state
New body and depth helmet sources with exact prompts/reference hashes, explicit source geometry/skin windows/material grade,12paired exports/6states/26refs, pitch calibration/registration/native review boards/browser. Paired .gd/.uid Godot-generated UID and isolated runner/native veld-rest lane. Current status/continuation/pipeline/bible/maintained+installed skill lessons updated.

## Verification
92package checks/22deterministic files:468body/500component rulers, exact selected entries/rear shell, authored pitch hashes and sizes, protected body, no clipping/floor223±1, reverse/held contracts.102actual-player checks cover pixels/metadata/1840ms/all3roles/both gears/arbitrary clocks/paused snapshots. Complete148/82 native board and finite browser endpoints reviewed. Sleeping helmet initially floor225 corrected via7source pixel neck offset, not scale. Overall runner FAILED from last_session.json delta among2,931real non-log files in6.33s explicit scratch interval; engine0/0fixture failures. No attribution/restore/clean-profile/normal/furniture/life/death claim.

## Next action
Author south generic rest from frontal master and appropriate foreshortened supine/helmet projection. Align life stage durations/furniture head contact before selecting complete family. Seated/life sources and already-resting deaths need pose/world-offset continuity; full cross-animation details/grade/anatomy/camera/motion acceptance remains. No blocker; keep full goal active.
''',encoding='utf-8')
paths=[p for p in P.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='candidate-evidence.json']
paths.extend([R/'tests/test_veld_rest_north_candidate.gd',R/'tests/test_veld_rest_north_candidate.gd.uid',R/'tools/run_veld_rest_north_candidate.py',index,R/'character/veld-shared-helmet-v1/fitted-north.png',R/'character/veld-shared-helmet-v1/frames/idle-north/000.png',R/'character/crew-runtime-matte-v1/veld/frames/idle-north-breathing-v1/000.png'])
paths.extend(O/n for n in ['validation.json','native.log','native-contact.png','profile-before.json','profile-after.json'])
e={'normalSelection':False,'packagingChecks':92,'playerChecks':102,'runner':report,'scope':'paired north source/player/native authored depth projection; no furniture/life/death/full-family acceptance','files':{p.relative_to(R).as_posix():sha(p) for p in paths}}
(P/'candidate-evidence.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8');print(json.dumps({'boundFiles':len(paths),'checks':194,'normalSelection':False}))
