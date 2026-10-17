from pathlib import Path
import json,hashlib,os,uuid
P=Path(__file__).resolve().parent;R=P.parents[1]
inputs=json.loads((P/'inputs-before.json').read_bytes());changed=[p for p,h in inputs.items() if hashlib.sha256((R/p).read_bytes()).hexdigest()!=h]
assert not changed,changed
e=json.loads((P/'full-cycle-evidence.json').read_bytes());assert all(d['slots']==141 and d['clockMs']==6000 for d in e['modes'].values())
(P/'review-acceptance.json').write_text(json.dumps({'all282SourceFramesReviewed':True,'boardsReviewed':10,'inputsUnchanged':len(inputs),'generatedStudySelected':False,'fullGoalComplete':False,'remaining':'Source-preserving full-cycle correction of visible key spill and tablet material, then paired full-cycle/source clocks/native selection/context review. Broad perceptual suit grading remains open; opaque median is insufficient to clear it.'},indent=2))
note='''

## James East tablet full-cycle material diagnosis — October 2, 2026

`character/james-tablet-east-matte-v3` currently contains review/study only, no
new selected pack. All141 current source frames per gear reviewed in10boards,
including lift, reading, genuine stow and exact master endpoints. Current selected
tablet-east-belt-fixed-source-v2 remains authoritative for East inspect/interact
and associated sealed compatibility poses.290frozen sources/manifests/masters/
loader/registry inputs unchanged; six-second inspection clock retained.

Refinement of previous sampled purple-cast finding: opaque low-chroma torso
median is already close to master: master47/43/46, pooled48/43/47 and pose70
46/41/46. This diagnostic does not establish perceptual whole-body equivalence
or rule out temporal cast. Tablet is visibly pale/violet; hair/body vary across
source. Clearly visible key-green spill occurs in139interior frames per gear:
max325bare/283helmet RGB key-green pixels, at most8/7opaque. Pose60bare321,
alpha median17/P90113;69pixels alpha>=32,27>=128. Criterion g>1.3r,g>1.3b,g>70
diagnoses green residue; it is not a semantic material mask or all-art defect test.
Inspect alpha/composited edges separately from opaque torso statistics. Do not
darken the whole body to solve a local matte/keying/tablet problem or crush shadows.

Built-in image edit of eight sampled poses with exact selected East master
reference improves neutral appearance but redraws face/cloth/tools. Raw1774x887
vs target736x368; normalized alpha differs58168pixels. Entire output unselected,
prompt/input layout/hash preserved as unselected-material-study.png. Numeric
height/pose registration cannot make these redraws source-preserving. Do not
install partial sampled poses into the141frame motion. Material reference study
is distinct from final source geometry, belt wrench and shared-shell acceptance.

Next: full-source key-spill/tablet material correction retaining approved motion,
wrench, shared helmet, alpha/body registration/clocks and exact master endpoints;
review every revised source and native playback before admission. No native run,
profile access, production change or final owner/full James acceptance this turn.
Full James library/master/cross-family goal remains active and incomplete.
'''
paths=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for path in paths:
    data=path.read_bytes()
    if b'## James East tablet full-cycle material diagnosis' in data:continue
    updated=note.lstrip().encode()+b'\n'+data if path.name=='CURRENT_STATUS.md' else data+note.encode()
    tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(updated)
    assert path.read_bytes()==data;os.replace(tmp,path)
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: 2026-10-02 · Project: Brine Space · Task: East tablet full-cycle material

## Objective and acceptance
Full James set/master/style/perspective/height/proportion/grade and cross-family
polish goal remains active/incomplete. This turn yields full source diagnosis.

## Accepted decisions and constraints
Preserve approved141pose cycle, belt wrench, shared shell, alpha and masters.
Do not install eight sampled redraws or globally darken already matched torso.

## Current state
All282current selected paired source frames reviewed in10boards.290input hashes,
opaque cloth/key-green/alpha diagnostics and eight-pose built-in edit retained.
Generated study unselected: altered details/58168normalized alpha differences.
No new manifests or runtime binding. Five guides updated with scoped findings.

## Verification
All290inputs unchanged; paired141frames and6000ms inspection confirmed.
139interiors per gear have green residue; maxima325/283pixels, mainly partial
alpha. Opaque median close to master, not proof of whole-body perceptual match.
No native/profile/context/continuous playback/owner/full-set acceptance claim.
Generation tool terminal, no process running from this turn.

## Next action
Full source-preserving key spill and tablet material correction, both gears.
Keep geometry/endpoints/wrench/shell/clocks; entire revised cycle review and native
selection/context checks before admission. Remaining James family motion and
cross-family polish remain. Do not mistake this folder name for installed v3.
''')
print('Recorded full282source review and rejected generated study;290inputs unchanged.')
