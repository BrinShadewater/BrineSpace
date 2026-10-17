from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];S=P.with_name('veld-rest-south-coherent-v1');O=R/'output/veld-rest-family-candidate-v1';SO=R/'output/veld-rest-south-candidate-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
report=json.loads((O/'validation.json').read_text());south=json.loads((SO/'validation.json').read_text());assert report['returnCode']==0 and '402 checks,0 failures' in (O/'native.log').read_text();assert south['returnCode']==0 and '102 checks,0 failures' in (SO/'native.log').read_text()
refs={'body':('exec-84300261-92e7-42ca-97f4-414f3a493e43','sources/rest-v1.png','sources/prompt-v1.txt','character/crew-runtime-matte-v1/veld/frames/idle-south-breathing-v1/000.png','sources/master-inspection.png'),'helmet':('exec-31af3da4-070c-4260-8dcd-c0989461a04b','sources/pitched-heads-v1.png','sources/helmet-prompt-v1.txt','character/veld-shared-helmet-south-v1/fitted-helmet.png','sources/helmet-master-inspection.png')}
binding={}
for key,(generation,source,prompt,master,submitted) in refs.items():
    binding[key]={'provider':'built-in imagegen','generation':generation,'source':source,'sourceSha256':sha(S/source),'prompt':prompt,'promptSha256':sha(S/prompt),'master':master,'masterSha256':sha(R/master),'submittedReference':submitted,'submittedReferenceSha256':sha(S/submitted)}
binding['helmet']['supportingPoseReference']='sources/rest-v1.png';binding['helmet']['supportingPoseReferenceSha256']=sha(S/'sources/rest-v1.png')
(S/'sources/reference-binding.json').write_text(json.dumps(binding,indent=2)+'\n',encoding='utf-8')
index=R/'tests/index.json';data=json.loads(index.read_text())
for key,reason in [('test_veld_rest_south_candidate','South body/front depth/closed expression source and finite native player review.'),('test_veld_rest_family_candidate','All cardinal paired sources/finite lowering and reverse/held sleep need native148/82 review.')]:
    if key not in data['subsystems']['veld-rest']:data['subsystems']['veld-rest'].append(key)
    data['lanes'][key]={'lane':'native','reason':reason}
index.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
note='''

## Veld south rest and cardinal generic family staged - October 1, 2026

South independent6pose body exec-84300261-92e7-42ca-97f4-414f3a493e43 references frontal master: boots downstage/head upstage supine, image-left blue-cap vial rack/image-right teal tool, fixed camera. One148/520=.284615body ruler and pooled spatial face/brown hair/neutral/science grade; exact selected standing entry. New front helmet depth exec-31af3da4-070c-4260-8dcd-c0989461a04b binds canonical component plus body as supporting depth reference. One35/523ruler across four components35x38/35x37/35x35/35x29; standing/seated use exact35x39master, other15/-35/-80pitch views authored, no inplane roll. Closed-eye face authored in80degree view. Whole-circle head erasure cut collar and left gap: constrain erasure below registered neck, preserving all body pixels below that cutoff outside component overlay.92south package/22deterministic and102south actual-player checks pass; native148/82 reviewed. South runner overall FAILED: last_session.json delta among2,931non-log files,7.11s scratch interval.

Cardinal family character/veld-rest-family-v1 assembles24paired states/104literal whole-path refs to48unchanged exports. All direction sources independently authored;1840ms finite lowering/exact reversed rise/held sleeping endpoint. Sleep restHeadOffset records anatomical bare/component helmet center in CELL384*.17/148 world units for later furniture integration.249packaging checks/4deterministic files and402actual-player checks pass across all directions/both gears; four complete native148/82 boards and family browser reviewed. Family runner overall FAILED: last_session.json delta among2,931non-log files in5.58s scratch interval, engine0/0fixture failures. No attribution/restore/clean-profile/normal-loader/furniture/life/death acceptance claim. All generic rest sources staged, accepted furniture-specific bunk unchanged. Full goal active. Generic Veld life_stage_seconds remains800ms and shared offset/head_alignment divide by.8, while authored source is1840ms; align per-actor timings/gear-specific head metadata and prove contact/interrupts before normal selection. Existing bunk remains1.84s/bunk-specific. Next: family integration/contact/interrupts, seated/life sources and whole-set cross-animation grade/detail/camera/anatomy/motion polish. Handoff:character/veld-rest-family-v1/HANDOFF.md.

Lesson: rear versus front supine projection must follow depth rather than image-plane rotation, with semantic face/hair/visor/hardware grade against that camera's master. A head-only repair mask must preserve the suit collar under the registered neck; protected body tests should use that actual mask bound. Combining proven source packs is a distinct player/metadata check, and a finite source clock must not be truncated by the life controller. Generic and accepted furniture-specific rest must remain distinct through integration.
'''
for rel in ['docs/CURRENT_STATUS.md','docs/VELD_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    p=R/rel;old=p.read_bytes()
    if note.lstrip().encode() not in old:p.write_bytes(note.lstrip().encode()+old if rel=='docs/CURRENT_STATUS.md' else old+note.encode())
installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')
if note.lstrip().encode() not in installed.read_bytes():
    with installed.open('ab') as f:f.write(note.encode())
html=S/'index.html';s=html.read_text(encoding='utf-8').replace('Packaging and native player review pending.','92 packaging and102 player checks pass.').replace('fine motion polish remain. </p>','fine motion polish remain. Overall native runner retains a profile-guard failure.</p>').replace('slower1840ms','slower 1840ms');html.write_text(s,encoding='utf-8')
handoff='''# Project handoff

Updated:2026-10-01 · Project:BrineSpace · Task:Veld cardinal generic rest source family

## Objective and acceptance
Full master-matched Veld animation set and whole-set polish active/incomplete. Four independent paired directional rest sources now packaged as one staged family; normal/world/life/owner acceptance unproven.

## Accepted decisions and constraints
Selected directional idle owns anatomy/camera/material/handed tools. Each body has one standing-derived ruler, pooled semantic grade, exact standing entry. East/west use exact rolled native hardware/closed donors; north/south have authored depth projection components at one calibrated component ruler, no per-pose rescaling. All1840ms lowering/exact reverse rise/held sleep. Accepted east furniture-specific bunk unchanged; no normal override/commit/export.

## Current state
South new body/front depth/closed-eye sources, exact prompts/reference bindings, skin polygons/material grade/neck-cutoff protected collar,12exports/6states/26refs. Family24states/104whole literal res paths/48unchanged exported files, world-unit sleeping head offsets, four native boards and browser. South and family .gd/.uid, scratch runners and native index lanes. Current status/continuation/pipeline/bible/maintained+installed skill lessons updated.

## Verification
South92package checks/22deterministic files and102actual-player checks pass; family249package checks/4deterministic files and402actual-player checks pass. Native148/82 boards show connected limbs/collar and appropriate camera depth, finite browser endpoints reviewed. Source/package/player proof only. Strict runners FAILED from last_session.json delta among2,931non-log files: South7.11s/family5.58s scratch intervals; engine0/0fixture failures. No attribution/restore/clean-profile/normal selection/furniture/interrupt claim.

## Next action
Integrate family with generic Veld per-actor1840ms life stages; crew_life.offset/head_alignment currently hardcode.8 and head_alignment uses bare metadata even with helmet. Preserve accepted1.84s east bunk branch. Prove exact normal-loader selection, directional head/furniture contact, phase-aware interruption/rise and paused/fresh-scene checkpoint continuity in scratch profile. Resting/seated death pose/world offset continuity still needs proof. Then own seated/life sources and full-set detail/grade/proportion/camera/motion acceptance. No blocker; keep full goal active.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8');(S/'HANDOFF.md').write_text(handoff,encoding='utf-8')
paths=[p for root in [P,S] for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='candidate-evidence.json']
paths.extend([index]+[R/f'tests/test_veld_rest_{kind}_candidate.gd{suffix}' for kind in ['south','family'] for suffix in ['', '.uid']]+[R/f'tools/run_veld_rest_{kind}_candidate.py' for kind in ['south','family']])
paths.extend(O/n for n in ['validation.json','native.log','profile-before.json','profile-after.json','native-east.png','native-south.png','native-west.png','native-north.png']);paths.extend(SO/n for n in ['validation.json','native.log','profile-before.json','profile-after.json','native-contact.png'])
e={'normalSelection':False,'familyPackagingChecks':249,'familyPlayerChecks':402,'southPackagingChecks':92,'southPlayerChecks':102,'familyRunner':report,'southRunner':south,'scope':'cardinal source/player family only; no furniture/life/death/normal/full-set acceptance','files':{p.relative_to(R).as_posix():sha(p) for p in paths}}
(P/'candidate-evidence.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8');print(json.dumps({'boundFiles':len(paths),'familyChecks':651,'normalSelection':False}))
