"""Bind matching rest source and preserve source/player/world distinctions."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-rest-east-candidate-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
report=json.loads((O/'validation.json').read_text());assert report['returnCode']==0 and '102 checks,0 failures' in (O/'native.log').read_text()
master=R/'character/crew-runtime-matte-v1/veld/frames/idle-east-breathing-v1/000.png'
binding={'generation':'exec-67b9279e-b045-4804-83c8-971d1710f621','provider':'built-in imagegen','prompt':'sources/prompt-v1.txt','promptSha256':sha(P/'sources/prompt-v1.txt'),'source':'sources/rest-v1.png','sourceSha256':sha(P/'sources/rest-v1.png'),'reference':master.relative_to(R).as_posix(),'referenceSha256':sha(master),'submittedReference':'sources/master-inspection.png','submittedReferenceSha256':sha(P/'sources/master-inspection.png'),'inspectionScale':4,'closedHelmetDonor':'character/veld-death-ground-east-coherent-v1/sources/canonical-head-closed.png','closedHelmetDonorSha256':sha(R/'character/veld-death-ground-east-coherent-v1/sources/canonical-head-closed.png'),'expressionGeneration':'exec-3873a1fe-c231-4fb0-bc95-64cd2c548f92'}
(P/'sources/reference-binding.json').write_text(json.dumps(binding,indent=2)+'\n')
index=R/'tests/index.json';data=json.loads(index.read_text());key='test_veld_rest_east_candidate'
if 'veld-rest' not in data['subsystems']:data['subsystems']['veld-rest']=[]
if key not in data['subsystems']['veld-rest']:data['subsystems']['veld-rest'].append(key)
data['lanes'][key]={'lane':'native','reason':'Paired floor rest source/finite lowering and rising/held sleep need native148/82 review.'};index.write_text(json.dumps(data,indent=2)+'\n')
note='''

## Veld paired east generic rest candidate — October 1, 2026

Current selected generic rest still comes from dr-veld-v2;177bare/171helmet states/2,972refs refreshed with zero path/RGBA failures, inventory not visual acceptance. Older rest helmet projection differs from current east master. Independent6pose source exec-67b9279e-b045-4804-83c8-971d1710f621 now authors voluntary squat/ground sit/recline/closed-eye sleep. One148/517=.286267 anatomical ruler, grounded256/p128,224/H148, pelvis x130 registration and exact selected bare/helmet standing entries. Single pooled material grade; spatial face windows separate bright brown hair from skin across upright/reclined views. Twelve unique paired exports serve6states/26refs: finite1840ms lie-down, exact reverse get-up, single held sleeping endpoint. Canonical35x39east helmet at scale1, native19,36anchor and0/0/0/12/70/70roll. Reused authored15RGBpixel closed-eye component for4/5; all original hardware/alpha/outside eye region preserved. Warm-only head erasure left gray hairband arc; head-local18px whole-material mask removes it. Lying helmet initially reachedfloor227; neck anchor corrected14source pixels upward to floor223, no helmet rescaling. Protected body outside local head/component region exact.79packaging checks/17deterministic files and102actual-player checks pass, all3roles/both gears/paused snapshots/native148/82 reviewed. First70check lowering-only interval retained; broadened102role checks justify second run. Browser review found800ms abrupt; staged1840ms cadence keeps identical pose pixels and exact reverse rise, fast timing retained in revisions/fast-timing-v1. A stale800ms manifest caused four timing failures before rebuilding; failed interval retained and corrected1840ms native102check run passes. Overall runner FAILED: last_session.json delta among2,931non-log files,5.48s scratchAPPDATA interval. No clean-profile/normal-loader/world/rest head contact/life death interrupt claim. Accepted furniture-specific bunk unchanged. Full goal active: paired other cardinal generic rest, seated/life art and master/detail/material/camera/motion polish, correct furniture/rest death joins and dry normal selection remain. Handoff:character/veld-rest-east-coherent-v1/HANDOFF.md.

Lesson: brightness alone confuses brown hair highlights with shaded skin. Use anatomical face regions and one clip-wide material curve, then inspect full-size/native poses rather than normalizing each frame. A gray hairband is head material even when it fails warm RGB predicates. Check a rotated wearable against the actual ground plane; its correct native dimensions alone do not prove neck contact or floor clearance. Preserve accepted furniture-specific sequences while developing generic rest; a free-standing source pack and pixel checks cannot certify its room placement or interrupted life transitions.
'''
for rel in ['docs/CURRENT_STATUS.md','docs/VELD_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    p=R/rel;old=p.read_bytes()
    if note.lstrip().encode() not in old:p.write_bytes(note.lstrip().encode()+old if rel=='docs/CURRENT_STATUS.md' else old+note.encode())
installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')
if note.lstrip().encode() not in installed.read_bytes():
    with installed.open('ab') as f:f.write(note.encode())
(P/'HANDOFF.md').write_text('''# Project handoff

Updated:2026-10-01 · Project:BrineSpace · Task:Veld east generic rest source

## Objective and acceptance
Full master-matched Veld set and whole-set polish remain active/incomplete. Paired east generic floor-rest candidate only; owner/world/full-family acceptance unproven.

## Accepted decisions and constraints
Actual selected east breathing idle and fitted east equipped idle are authorities. Independent anatomical lowering, closed eyes, connected hips/knees and handed tools/boxed science insignia. One148/517body ruler and pooled semantic material grade. Native35x39helmet/19,36neck anchor, closed donor15RGBpixels; no rescaling hardware. Finite1840ms lowering/exact reverse rising and held sleeping endpoint. Accepted bunk unchanged; no normal override/commit/export.

## Changed files and current state
This folder: raw6pose source/exact prompt/hash-bound reference, ungraded scale review, bare/helmet builders, pooled material curves/registration,6states/26refs from12exports,79check package verifier, finite paired browser and contact boards. tests/test_veld_rest_east_candidate.gd/.uid, tools/run_veld_rest_east_candidate.py and tests/index.json native lane. Current status, continuation, pipeline, visual bible and maintained/installed consistency reference record lessons. Prior dry role/world/rest-death work preserved.

## Verification
79packaging checks/17deterministic files: exact standing entries, fixed517ruler, protected body, original hardware/alpha/eye bounds, reverse path, held endpoint, floor223±1, no clipping.102actual CrewSpritePlayer checks pass for all3roles/both gears, source pixels, timing, metadata, arbitrary initial clocks, validated paused snapshots. Complete native148/82 board reviewed. Hairband arc removed through anatomical head-local mask; lying wearable floor corrected by neck registration, not resizing. Overall native runner FAILED: last_session.json changed among2,931real non-log files during5.48s explicit scratch interval; earlier6.81s70check lowering-only report retained. No attribution/restoration/clean-profile/world placement or life-state death claim.

## Remaining work and next action
Finite browser lowering/rising and held sleep reviewed;1840ms cadence staged, fast revision retained. Author own west/north/south generic rest from selected cameras, preserving handed details and appropriate supine projection. Fit furniture/head alignment and interruptions, including bed/seated deaths that must preserve pose/world offset. Seated/life family and whole-set identity/grade/detail/motion polish remain; dry-death normal selection/fresh-process/rest interrupts still staged. No blocker; do not mark full goal complete.
''',encoding='utf-8')
paths=[p for p in P.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='candidate-evidence.json']
paths.extend([R/'tests/test_veld_rest_east_candidate.gd',R/'tests/test_veld_rest_east_candidate.gd.uid',R/'tools/run_veld_rest_east_candidate.py',index,R/'character/veld-death-ground-east-coherent-v1/sources/canonical-head.png',R/'character/veld-death-ground-east-coherent-v1/sources/canonical-head-closed.png',R/'character/veld-death-ground-east-coherent-v1/sources/expression/closed-v1.png'])
paths.extend(O/n for n in ['validation.json','native.log','native-contact.png','profile-before.json','profile-after.json'])
evidence={'normalSelection':False,'packagingChecks':79,'playerChecks':102,'runner':report,'scope':'paired east generic rest source/player/native; no world head placement/life/death/normal/family completion','files':{p.relative_to(R).as_posix():sha(p) for p in paths}}
(P/'candidate-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n');print(json.dumps({'boundFiles':len(paths),'packageChecks':79,'playerChecks':102,'normalSelection':False}))
