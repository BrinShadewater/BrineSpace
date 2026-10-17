from pathlib import Path
import json,hashlib,uuid,os
p=Path(__file__).resolve().parent;r=p.parents[1]
reference=json.loads((p/'reference-evidence.json').read_bytes())
assert hashlib.sha256((r/reference['source']).read_bytes()).hexdigest()==reference['sha256']
def atomic(path,new):
    old=path.read_bytes();temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp')
    temp.write_bytes(new);assert path.read_bytes()==old;os.replace(temp,path)
for version in [5,6]:
    name='release_v'+str(version)
    evidence=json.loads((p/(name+'-evidence.json')).read_bytes())
    guard=json.loads((p/(name+'-validation.json')).read_bytes())
    inputs=json.loads((p/(name+'-inputs.json')).read_bytes())
    registration=json.loads((p/(name+'-registration-evidence.json')).read_bytes())
    assert evidence['checks']==220 and evidence['failures']==0 and len(evidence['results'])==14
    assert guard['exitCode']==0 and not guard['timedOut'] and guard['realProfileUnchanged']
    assert len(inputs)==14 and all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in inputs.items())
    assert len(registration['matches'])==14
    package=json.loads((p/('package-v'+str(version)+'-evidence.json')).read_bytes())
    assert package['caseFloorBaseline']==222 and package['crewStandingHeight']==148
    review=json.loads((p/(name+'-review.json')).read_bytes())
    review.update(visualReviewPending=False,reviewed='All14 registered source/prop and native room before/release/terminal/idle/departure presentations inspected for both gears. Body/head/helmet unchanged; smaller matte case hardware improves separate-prop comparison. V6 closer center/corner hardware than V5. Original partly hidden edge and layering differ; continuous exact join not yet certified.',continuousMotionAcceptance=False,ordinaryContinueAcceptance=False)
    atomic(p/(name+'-review.json'),(json.dumps(review,indent=2)+'\n').encode())
raws={str(path.relative_to(r)):hashlib.sha256(path.read_bytes()).hexdigest() for path in [p/('floor-case-generated-v'+str(i)+'.png') for i in [4,5,6]]}
verdict={'selected':False,'fullGoalComplete':False,'preferredStagedVisualVariant':'v6','authoring':'Built-in image_gen edits; raw v4/v5/v6 and exact prompts preserved.','rawHashes':raws,'originalReferenceHashUnchanged':True,'sourceCompared':'Original terminal unload/occluded boot, old v3 separate sprite, v5 and v6 registered source composites.','versions':{'v4':'Duller/smaller hardware, but1.83 silhouette too shallow; not packaged.','v5':'44x26 native alpha footprint, matte improvement; center/corners insufficiently differentiated.','v6':'44x25 native alpha footprint, closer center clasp versus narrow corners. One native pixel shallower than26target; visible hardware/material closer in reviewed source/room presentations.'},'nativeReleaseChecksPerVersion':220,'nativeSourceWorldPairsReviewed':28,'targetedInputsPerVersionUnchanged':14,'ownerProfileUnchanged':True,'remaining':['Continuous native join/playback and original precomposed boot versus sorted-prop occlusion.','Floor sprite version/hash binding in paired checkpoint: current floor3 contract evidence predates new visual variant.','V9 collar/head-turn/body polish and normal paired Continue admission.','Other cardinals, natural world scheduling and full James/master/cross-family set.']}
(p/'case-polish-acceptance.json').write_text(json.dumps(verdict,indent=2)+'\n')
section='''## James West case matte/hardware polish v4–v6 — October 2, 2026

Three built-in raw edits/exact prompts preserved. V4 reduced white sheen/pad size
but silhouette1.83too shallow. V5 corrected44x26native footprint; V6 differentiated
larger center shield clasp from narrower corner guards, closer to original unload
case than six repeated buttons. Preferred staged visual auditionV6,44x25alpha
footprint (one native pixel shallower than26target), uniform aspect-preserving
native packaging/p128224/H148/left75/floor222, no separate-axis warp/grade edit.
Original terminal reference/source hash unchanged; hidden edge remains inferred.

V5/V6 each220native release checks0fail/two actual carry power-loss returns/both
gears. All28source/world presentations reviewed across four boards, plus original/
v3/v5/v6 registered contact comparisons. Matte finish/visible hardware improved;
body/head/helmet untouched. Case stays fixed while next activity departs48.769.
Each14targeted prelaunch hashes unchanged/engine0/whole owner profile unchanged.
Current original source RGBA/pivots/H148 bindings are post-run, not full freeze.
First V5 package45x27rounding interval retained; shared uniform scale correction
yields actual44x26alpha footprint. Neither axis was independently stretched.

Lesson: match distinct center versus corner hardware and alpha footprint after
resampling, not only raw aspect or generic matte instructions. Reference case is
partly occluded and precomposed with boots; sorted separate prop exposes a different
occlusion boundary. Source comparison improves material but does not certify
continuous native handoff. Next continuous join/boot contact, sprite-version/hash
binding in paired checkpoint (existing floor3 evidence predates new art), V9
collar/head-turn polish and normal paired Continue admission. Other cardinals and
full James/master/cross-family goal remain active/incomplete. Candidate unselected.
Evidence:character/james-floor-case-west-v1/case-polish-acceptance.json,
case-v6-comparison.png,release_v5-review.json,release_v6-review.json.
No normal actor/renderer/art selection changed; no commit/export.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() not in old:
        atomic(path,section.encode()+b'\n'+old if path.name=='CURRENT_STATUS.md' else old+b'\n\n'+section.encode())
handoff='''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James West case visual polish

## Objective and acceptance
Full James set matching directional masters/style/perspective/size/proportions/
matte grade, then cross-family polish. Incomplete; candidate unselected.

## Accepted decisions and constraints
Preserve selected art/room geometry/owner profile. Built-in authored sources,
uniform native packaging, shared p128224/H148/floor222. No grade/axis warp repair.

## Current state
New raw v4/v5/v6/exact prompts. V5/V6 native sibling sprites/packagers and separate
audition renderers/release fixtures. Preferred V6 center/corner hardware and dull
matte44x25footprint. Existing floor3 lifecycle/checkpoint untouched. Original/v3/
v5/v6 contact comparison, four native review boards and acceptance recorded.

## Verification
V5/V6 each220checks0fail/two actual carry returns/both gears/14reviewed pairs.
Each14targeted hashes/owner unchanged/engine0. Original reference hash unchanged.
Native package guards clean; first V5 rounding45x27 interval retained before uniform
correction44x26. V6 one native pixel shallower than26target; hardware/matte closer.
No continuous join/full master/normal Continue acceptance. Five guides updated.
Prior220/88/434floor and210staged disk gates retain original floor3 artwork scope.

## Next action
Continuous native source-to-prop/boot occlusion review; bind actual selected floor
sprite revision/hash to checkpoint rather than reusing floor3 acceptance. V9
collar/head-turn/body polish; then normal paired Save/title/new-process Continue,
other cardinals/natural world/master and full cross-family review. No commit/export.
'''
atomic(p/'HANDOFF.md',handoff.encode())
print('V5/V6 material/hardware audition:28reviewed native pairs;five guides/handoff updated;full goal incomplete.')
