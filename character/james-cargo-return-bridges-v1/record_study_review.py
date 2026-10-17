from pathlib import Path
import hashlib,json,os,uuid
p=Path(__file__).resolve().parent;r=p.parents[1]
guard=json.loads((p/'package-west-bridge-v2-validation.json').read_bytes())
assert guard['exitCode']==0 and guard['realProfileUnchanged'] and not guard['timedOut']
refs=json.loads((p/'reference-evidence.json').read_bytes())
assert all(hashlib.sha256((r/x['path']).read_bytes()).hexdigest()==x['sha256'] for x in refs['sources'])
def atomic(path,new):
 old=path.read_bytes();temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');temp.write_bytes(new);assert path.read_bytes()==old;os.replace(temp,path)
review={'selected':False,'visualAcceptance':False,'fullGoalComplete':False,'method':'Built-in imagegen; exact prompts and both raw RGBA outputs retained. Native Godot extraction, shared nominal148/450 ruler, original256 canvas/p128224, cutoff32 provider alpha dust; no grading or anatomy repaint.',
 'reviewed':['west-bridge-reference.png','west-bridge-generated-v1-alpha-review.png','west-bridge-generated-v2.png','west-bridge-endpoint-review.png','west-bridge-station-review.png'],
 'findings':['v1 first two columns merge the far leg and read as pure side profile; rejected.','v2 reveals both boots and knees, readable matte materials and case held in front.','v2 shared helmet is visibly too small versus retained original shell at registered scale; not accepted.','v2 settles to a near-identical three-quarter pose too early; first-source and unload boundary still require a gradual anatomical join.','Bare and generated helmet bodies are independent drawings, not exact paired body pixels; no equivalence claim.'],
 'next':'Author more gradual West camera/grip bridge with original shell dimensions and stable paired body/foot stance; then source/native motion review, crate-floor/idle handoff, controller/safety/Continue.'}
(p/'study-review-evidence.json').write_text(json.dumps(review,indent=2)+'\n')
section='''## James West cargo bridge source study — October 2, 2026

New unselected character/james-cargo-return-bridges-v1 retains two built-in
transparent six-pose sheets and exact prompts. Hashed original paired West turn
endpoint/unload entrance/idle references register at p128224/H148. First generation
rejected for merged far leg/pure side camera in first two columns. Revised sheet
reveals both boots/knees with matte material and case held in front, but its helmet
is visibly undersized against the original shared shell and all three poses settle
too early into almost the same angle. Visual acceptance FAILED; no normal change.

Native deterministic six-frame study extraction completed, engine0/no timeout,
whole owner profile unchanged in scratch. Original256/p128224/H148, pooled nominal
148/450 ruler, rounded168x168 full-cell extraction and alpha<32 provider dust cutoff;
no raster grading/anatomy repaint. Per-cell foot-band centers and row soles recorded
for registration; not exact paired body or anatomical contact protection. Both
paired manifests remain unselected source studies. PNG LFS filters verified.
All six packaged sources reviewed beside exact original endpoints/idle at full
and reduced presentation scale. References retain exact recorded hashes.

Lesson: a paired generated sheet can compress helmet height independently of the
body. Never fit each complete figure to the same height to hide shell drift;
preserve a common bare-body ruler and compare shell/neck dimensions separately.
Intermediate poses must progressively bridge the actual boundary rather than
repeat an early destination stance. Next original-shell-size and gradual West
held-to-lowering repair, floor-case/standing join, real controller/safety/Continue
and native motion. Full James master/context/cross-family objective incomplete.
Evidence: character/james-cargo-return-bridges-v1/study-review-evidence.json and
west-bridge-endpoint-review.png. Built-in prompts west-bridge-prompt-v1/v2.txt.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 old=path.read_bytes()
 if section.splitlines()[0].encode() not in old:atomic(path,section.encode()+b'\n'+old if path.name=='CURRENT_STATUS.md' else old+b'\n\n'+section.encode())
handoff='''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James West cargo bridge study

## Objective and acceptance
Full James master/style/perspective/size/height/proportion/matte set then
cross-family polish. Full objective active/incomplete; bridge study not accepted.

## Accepted decisions and constraints
Original shared shell and directional masters govern. Retain selected production
set, belt wrench/case contact and stable stance. No per-pose exposure/scale fix.

## Current state
Two built-in raw6pose sheets/prompts; v1 rejects merged legs. Native packagedv2
six sources/paired manifests remain unselected: undersized shell and prematurely
settled interiors. Full and reduced registered boards reviewed. Five guides updated.
Finite source planner remains staged in james-east-cargo-heads-v3; actual power
interruptions still snap in production. No controller/save integration change.

## Verification
Native package engine0/no timeout; whole owner profile unchanged under scratch.
Six exact reference hashes unchanged; PNG LFS filters verified. Six generated
sources reviewed, no paired-body pixel equivalence, continuous motion, collision,
crate-floor, emergency/needs or ordinary Continue acceptance. Full-cell resize
rounding and foot-band registration explicit in package-evidence.json.

## Next action
Gradual West camera/grip bridge with retained original helmet size/neck and
consistent paired stance. Then endpoint/native motion, floor-case/standing handoff,
real finite return controller and safety/Continue. Remaining cardinal contexts,
West tablet edges and complete cross-family master polish remain open.
No commit/export.
'''
(p/'HANDOFF.md').write_text(handoff)
print('Rejected bridge mismatch recorded; raw sources/prompts, extraction and five updated guides retained.')
