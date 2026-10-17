from pathlib import Path
import json, hashlib
P=Path(__file__).resolve().parent
R=P.parent.parent
f=P/'review.json'
e=json.loads(f.read_text())
e['visualReview']='Original master, both seven-pose rows and common4x head/shoulder crops inspected. Revised crouch/push have slimmer torso/shorter compact arms and smaller heads than V1, closer to standing and later compact endpoints. Crouch-v2 merged gloves; crouch-v3 exposes two recognizable gloves. Exact identity, shoulder patch/detail, subtle grade and continuous motion remain unaccepted; no native proof for West.'
e['visualAcceptance']='Improved source anatomy/readability; full-family identity and continuous motion pending.'
e['generationMode']='built-in image_gen'
raw=[]
for reg in e['registrations'].values():
    raw.extend([P.parent/reg['source'],P.parent/reg['prompt']])
e['generatedRawAndPromptSHA256']={str(p.relative_to(P.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for p in raw}
e['retainedDraft']={'source':'bill-land-water-west-v1/sources/crouch-canvas-v2.png','generation':'exec-a2fb1022-f360-4646-a091-b57fe9f588bd','reason':'Compact torso improved but gloves merged; superseded by v3 far-arm edit. Raw/native/comparison retained.'}
f.write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
html=P/'index.html'
t=html.read_text()
t=t.replace('Smaller crouch/push bodies; visual acceptance pending.','Smaller crouch/push bodies; continuous motion and complete identity acceptance pending.')
if 'head-shoulder-details.png' not in t:
    t+='<h2>Common4x head and shoulder comparison</h2><img src="head-shoulder-details.png"><p>'+e['visualReview']+'</p>'
html.write_text(t,encoding='utf-8')
note='''## Bill West compact crouch/push source revision — October 2, 2026

New unselected bill-land-water-west-v2 seven-pose entry bank repairs the early
oversized build from V1. Crouch-v2 authored against exact West idle/compact lift;
merged gloves prompted local far-arm edit crouch-v3. Push-v2 independently
authored from those master-scale references with two compact bent arms. Built-in
imagegen sources/prompts retained under V1 sources, including superseded v2.
Final generations:exec-8b370156-7165-4781-8e72-8ade255a3b08 crouch;
exec-cd0be74a-4083-4b82-b17d-7049a30e2384 push. Raw/prompt/native hashes recorded.

Actual1254square uses single wholecanvas320/1254 rule and opaque-component3px
fringe. Crouch semantic boot sole239 shifts wholefigureY-15 to224; push remains
untranslated buoyant pose. All extracted painted support preserved; no per-pose
height fit or invented limb painting. Five other V1 poses remain RGBA exact.
Seven decoded APNG frames/holds exact, total500ms; common320/p160224/H148.
Full original-master/V1/V2 board and common4x head/shoulder crops reviewed.
New crouch/push slimmer with compact arms/smaller heads, closer to exact idle and
compact lift; v3 crouch shows two recognizable gloves. Head identity, patch/detail,
subtle grade and continuous motion still need full-family acceptance. Local image
edit regenerated pixels beyond the hand; do not claim an exact protected body.

No West helmet pairing/live gait endpoints/native phase/material/clearance/save/
Continue or normal admission yet. No Godot or owner profile writes this interval.
Preserved historical V1 bank. Review:character/bill-land-water-west-v2/index.html.
Lesson: check hand readability after anatomy correction; overlapping gloves can
hide missing far-arm articulation. Inspect generated local edits as full figures
because unchanged-pixel wording is not evidence of pixel preservation.
Next canonical West helmet pairing and actual boundary/motion/native validation;
North/South water bridges, cargo lifecycle and whole Bill set master/style/size/
perspective/proportion/matte-grade polish remain. Full goal active/incomplete.

'''
heading=note.splitlines()[0]
for rel in ['docs/CURRENT_STATUS.md','docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']:
    p=R/rel
    t=p.read_text(encoding='utf-8')
    if heading not in t:p.write_text(note+t,encoding='utf-8')
for p in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    t=p.read_text(encoding='utf-8')
    if heading not in t:p.write_text(t+'\n'+note,encoding='utf-8')
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October2,2026 · BrineSpace · Bill West compact water-entry revision

## Objective and acceptance
Complete full Bill set matching original masters/style/perspective/anatomy/grade,
then cross-family polish. This source revision is not full-set acceptance.

## Accepted decisions and constraints
Original West master is left-facing right figure; no East mirror. Common148 ruler,
320 canvas/p160224, fixed wholecanvas normalization, semantic dry boot registration.
Keep original sources and selected gameplay intact while candidates are reviewed.

## Current state
V2 build.py/build_details.py produce seven bare entry frames/manifest/APNG500ms,
master-comparison.png/head-shoulder-details.png/review.json/index.html. New raw
crouch-v2/v3 and push-v2 plus prompts under V1 sources. Historical V1 bank preserved.
Pipeline/bible/current status/continuation/maintained+installed consistency updated.

## Verification
Five unchanged poses exact; seven decoded APNG frames and holds exact. Full common
master/old/new board and4x crops inspected. Slimmer early poses/two visible gloves;
full identity/detail/grade and continuous motion acceptance pending. No Godot run,
owner profile changes, normal selection, native or Continue proof for West.

## Next action
Canonical West helmet pairing, live gait joins/continuous motion, actual native
material/phase/clearance/save/Continue. North/South bridges/cargo lifecycle and
full Bill cross-family fidelity/polish remain. Goal active/incomplete.
''',encoding='utf-8')
print('Recorded source revision; six guidance files and handoff updated. Goal incomplete.')
