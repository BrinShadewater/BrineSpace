from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1]
report=json.loads((P/'package-checks.json').read_text());assert report['failures']==0
note='''## Veld early bunk floor-fall artwork - October 1, 2026

Staged character/veld-bunk-early-fall-v1 adds paired crouching-to-floor and
standing-to-floor sources before mattress support. Built-in image generation
exec-3624f6c9-d877-422c-b155-4cc96460e212 authored six whole poses; raw PNG,
exact prompt and reference roles retained. Selected East idle sets identity,
master physique/materials; existing bunk source supplies rear-reaching crouch;
existing ground fall supplies landing choreography. Only three new interior
poses2/3/4 used. Exact current bunk pose1 is initial crouching frame; exact
existing ground terminal5 is resting endpoint. Existing six-frame standing
fall reused, with transparent bottom16 padding only. No old PNG overwrite.

One148/495 generated standing anatomical ruler for every new interior, no
per-pose box fitting. One pooled semantic skin/hair/science/neutral grade to
current master applied before resampling. Original body canvas256x272 and
pivot128,224/H148; explicit authored floor-contact anchors, no bunk furniture
depth metadata. Helmet inserts use original native35x39 master/closed-eye
variant, rigid rotations at native scale; body pixels outside bounded head
insert exactly equal paired bare. Original equipment, warm skin, brown bun,
blue boxed science patch, silver specimen tubes, knee rivets and connected
hips/arms retained. Raw low-opacity background halo excluded by body component
isolation; exported transparent margins and source views checked.

35 source-builder checks and105 independent package/alpha/endpoint/body checks
pass,22RGBA exports/two finite states per gear. Four three-times-slower source
previews use pooled GIF palette; paired whole source board reviewed against
same-pixel-scale standing master. These are source-only previews, not native
room/furniture contact or world mortality evidence. Manifests explicitly staged,
normal library unchanged, no production/owner room/save changes or Godot run.

Lesson: before supported contact, a partial crouch needs its own authored fall
trajectory, rather than borrowed seated or lying silhouettes. Bind the exact
incoming pose and existing terminal to new complete-body interiors; keep one
anatomical ruler/material mapping and the canonical helmet, rather than fitting
each pose/head to a convenient box. Retain generated source and extraction
provenance, and distinguish source package acceptance from physical floor/bed
registration and finite temporal/native/save validation.

Next integrate strict opt-in early standing/crouching selectors, source clocks,
floor registration and native mortality/Continue; lounge falls still open.
Whole-world hazard cadence and normal paired body selection need their own
evidence. Remaining full Veld set/master cross-family polish remains active;
no commit/export and owner visual acceptance open.
'''
targets=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for i,path in enumerate(targets):
 old=path.read_bytes();payload=note.replace('\n','\r\n').encode()
 if note.splitlines()[0].encode() not in old:path.write_bytes(payload+b'\r\n'+old if i==0 else old+b'\r\n'+payload)
handoff='''# Project handoff

Updated:2026-10-01 - Project:BrineSpace - Task:Veld early floor falls

## Objective and acceptance
Full Veld master-matching animation set, then cross-family consistency/polish.
Goal active/incomplete. Early fall artwork staged; native/owner acceptance open.

## Accepted decisions and constraints
Selected East master sets identity, physique and matte grade. Generated source
one148/495 anatomical ruler, pooled semantic grade.256x272/p128,224/H148.
Exact existing bunk crouch entry and ground resting terminal; native master
helmet at original scale. Preserve old artwork and all owner room geometry.

## Current state
Raw built-in source, exact prompt/reference roles in sources/. build.py exports
22paired PNGs: new five-frame crouch fall with three generated interiors, and
existing six-frame standing fall padded16transparent rows. Two staged states
per gear. No production selector/normal manifest installation this interval.
review.py/validate.py, four source GIFs and paired standing-master board here.

## Verification
35builder and105independent package checks0fail. Exact entry/terminal and all
six standing source pixels retained; helmet body outside head insert unchanged.
Full source board reviewed; body component isolation removes raw low-alpha halo.
No Godot run/owner save writes. Source-only evidence in candidate-evidence.json;
native temporal/contact/mortality/Continue not certified by these source checks.
Prior paired bunk evidence in character/veld-bunk-body-master-v1: six fire full
Continue cases23389checks and four partial death Continue cases8125checks pass.
That family's full lifecycle/service/approach/held/water evidence stays separate.

## Next action
Strict opt-in early fall selectors for bunk poses0/1, floor registration/clock,
native actual mortality and saved continuation. Then lounge fall sources,
whole-world hazard cadence and normal paired body installation. Finish remaining
Veld families and full-set master/cross-family polish; no commit/export requested.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
files=[P/n for n in ['sources/fall-v1.png','sources/prompt-v1.txt','build.py','validate.py','review.py','record.py','bare-manifest.json','helmet-manifest.json','registration.json','material-grade.json','package-checks.json','paired-source-review.png','index.html','HANDOFF.md']]+list((P/'frames').rglob('*.png'))+list(P.glob('*.gif'))+[R/'character/crew-runtime-matte-v1/veld/frames/idle-east-breathing-v1/000.png',R/'character/veld-bunk-body-master-v1/sources/bunk-body-v1.png',R/'character/veld-death-ground-east-coherent-v1/sources/death-v1.png',R/'character/veld-death-ground-east-coherent-v1/sources/canonical-head.png',R/'character/veld-death-ground-east-coherent-v1/sources/canonical-head-closed.png']
(P/'candidate-evidence.json').write_text(json.dumps({'sourceGeneration':'built-in imagegen exec-3624f6c9-d877-422c-b155-4cc96460e212','sourceBuilderChecks':35,'independentPackageChecks':105,'exports':22,'generatedInteriorsPerGear':3,'nativeMortalityProven':False,'normalSelection':False,'visualReview':'Paired five-pose original-scale floor-fall board against standing master','scope':'Staged source artwork; temporal/room/floor registration, engine and save integration pending','bindings':{f.relative_to(R).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}},indent=2)+'\n')
old_handoff=R/'character/veld-bunk-body-master-v1/HANDOFF.md';s=old_handoff.read_text(encoding='utf-8')
s=s.replace('Early standing/crouching bunk fall and lounge death artwork, then whole-world\nhazard cadence and normal paired body installation with lifecycle evidence.','Early floor-fall artwork now staged in character/veld-bunk-early-fall-v1;\nintegrate strict selectors/native floor contact and mortality/Continue next.\nThen lounge falls, whole-world hazards and normal paired body installation.')
old_handoff.write_text(s,encoding='utf-8')
print('35builder/105package checks;22exports;five lesson records and concise handoffs saved')
