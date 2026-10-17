from pathlib import Path
import hashlib,json,os,uuid
P=Path(__file__).resolve().parent;R=P.parents[1]
if (P/'SUPERSEDED.md').exists():
    raise SystemExit('Historical study superseded; use current selected rest review. No guide mutation.')
before=json.loads((R/'character/james-berth-rotation-motion-v1/runtime-inputs-before.json').read_bytes())
changed=[rel for rel,h in before.items() if hashlib.sha256((R/rel).read_bytes()).hexdigest()!=h]
assert not changed,changed
(P/'review-evidence.json').write_text(json.dumps({'sourceInputsUnchanged':len(before),'reviewedHeadBoards':['north','south','east','west'],'displayedReferences':96,'method':'All four existing native-density directional head boards visually inspected, followed by original/generated and registered representative comparisons. Get-up reverse sources were established by earlier material evidence, not re-authored here.','finding':'South bare reclining cheeks/jaw are visibly broader and warmer than standing master; helmet face also broad. Other facings show expected pose tilt, but these boards alone do not prove anatomical identity.','representativeDecision':'Unselected. Generated head is less round, but still broader than master; head/neck crop can include collar pixels. Do not install a single altered pose and create a sequence flash.','productionChanges':False},indent=2)+'\n')
note='''

## James South reclining head repair study — October 1, 2026

`character/james-south-rest-head-polish-v1`: inspected all four ordinary rest
head boards (96 lie/sleep displayed references). South bare reclining cheek/jaw
width and warm skin drift visibly from standing master; helmet face also needs
review. Protected head/shell pixels in a material pass preserve existing defects
as well as identity. Correct pivot/standingHeight is not anatomical acceptance.

One built-in image_gen pose2 edit retained with exact prompt and input/output
hashes. Raw1254x1254 replaces source256x256; canvas-normalized bounds and3380
alpha changes show it altered body/equipment despite head-only request. Raw
full-frame replacement rejected. Staged head/neck-only extraction keeps original
pixels outside112..144/105..135 and all body rows135+ exact;755 pixels/445 alpha
values change inside that window. Window is rectangular, can include upper collar,
and is not a semantic face mask. Face appears less round, but remains wider than
master. Candidate is UNSELECTED, not installed or approved for expansion.

Same-pixel master/current/generated and registered-head boards reviewed.171
previously frozen source/manifest/controller inputs remain unchanged. No production,
timing, pivot, height or engine changes; no new native probe needed for this study.
Next: author one coherent South head progression matching master cranial width,
chin/neck contact and tilt, then pair helmet-visible faces and review all joins
before installation. Whole-body rescaling or single-pose insertion cannot certify
this correction. Full James library/master/polish goal remains active.
'''
for path in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    data=path.read_bytes()
    if b'## James South reclining head repair study' in data:continue
    new=note.lstrip().encode()+b'\n'+data if path.name=='CURRENT_STATUS.md' else data+note.encode()
    tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(new);os.replace(tmp,path)
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: 2026-10-01 · Project: Brine Space · Task: James South reclining head study

## Objective and acceptance
Full James library/master/style/perspective/proportion/grade consistency and polish.
Goal active. South reclining head drift remains unresolved.

## Accepted decisions and constraints
Master cranial proportions and matte materials govern. Natural tilt/foreshortening
must remain; do not scale the body to repair a head. Preserve original equipment.

## Current state
One generated pose2 raw edit, exact prompt, hashes, candidate comparisons and
one extracted head/neck representative. Candidate UNSELECTED, not installed:
face less round but still too broad. Extraction window can touch collar pixels.
All four directional head boards reviewed. Five guides record the new evidence.

## Verification
Raw full-frame changes body/alpha geometry; rejected. Representative outside
window and rows135+ exact,755pixel/445alpha changes inside.171 frozen original
inputs unchanged. No new Godot or save run; previous berth run completed cleanly.
No single-pose or native cadence acceptance claimed.

## Next action
Author a coherent South six-pose head progression with narrower master cranial
width, correct chin/neck and backward tilt. Pair visible helmet faces, preserve
shared sleeps/reversals, review exact joins and actual rest before installation.
Image generation cell829 finished; raw copied into workspace; no live job.
''')
print('Head repair study recorded; candidate unselected, original171 inputs unchanged.')
