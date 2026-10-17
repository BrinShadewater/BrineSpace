"""Record a bounded candidate milestone without promoting the death family."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-death-water-east-candidate-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
v=json.loads((O/'validation.json').read_text(encoding='utf-8'))
assert v['passed'] and v['candidateOnly'] and not v['realProfileChanges']
assert '133 checks,0 failures' in (O/'native.log').read_text(encoding='utf-8')
package=json.loads((P/'validation.json').read_text(encoding='utf-8'));assert package['passed'] and package['checks']==66
assert json.loads((P/'rebuild-checks.json').read_text(encoding='utf-8'))['passed']
files=[f for f in P.rglob('*') if f.is_file() and f.name!='candidate-evidence.json' and '__pycache__' not in f.parts]
files+=[f for f in O.iterdir() if f.is_file()]
files+=[R/n for n in ['tests/test_veld_death_water_east_candidate.gd','tests/test_veld_death_water_east_candidate.gd.uid','tools/run_veld_death_water_east_candidate.py','character/dr-veld-v2/clearance.json','character/veld-life-death-audit-v1/build_review.py','character/veld-life-death-audit-v1/coverage.json','character/veld-life-death-audit-v1/death-ground-masters.png','character/veld-life-death-audit-v1/death-water-masters.png']]
e={'status':'staged_east_prone_water_death_candidate','states':2,'references':12,'fitChecks':15,'packageChecks':66,'nativeChecks':133,'actualOxygenDeathCases':4,'nativeResult':v,'runtimeSelected':False,'profileChanged':False,'boundFiles':{f.relative_to(R).as_posix():sha(f) for f in files},'scope':'actual oxygen death/controller/source renderer, finite timing/terminal hold, in-memory playback snapshot restoration; not normal selection, room draw/clearance, fresh-scene disk Continue or upright-tread death entry','remaining':'independent west/north/south water death, upright tread entrance, full-world/clearance/interruptions/checkpoint/normal selection; ground death,rest/life and full cross-family motion polish'}
(P/'candidate-evidence.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
lesson=f'''

## Veld east prone water death staged — September 30, 2026

Current literal catalog/loader audit inventories96 life/death states;16 paired
ground/water death/master rows show inherited green-gray suits, dark/desaturated
hair and old gold/orange or incomplete helmet hardware. Audit is selected-source
diagnosis, not complete-motion or normal rendered selection proof.

East prone replacement stages2gear states/12refs. Source
exec-251cb1a1-aca9-4677-b315-8f818654620f, exact prompt/reference and all6 crops
retained. Source pose0 retained/excluded; slot0 copies exact selected swim master,
slots1..5 are independently authored weak kick/relaxed arms/closed-eye terminal.
One fixed anatomical ruler .3148148148148148 and three-vial-cap belt anchor
(106,141). Final measured anchor within1px in every pose; no per-pose height
normalization. Pooled material mapping keeps each bare skin/hair/cloth/patch
median within12RGB of its own selected master. Native graphite/silver helmet
uses recorded -16..-27deg pitches, with source closing face fitted only to its
native skin window. Body outside head/clear regions remains identical by gear.

15fit/66package checks and actual2manifest/12frame local rebuild PASS.133native
checks PASS{v['seconds']}s: four actual Flood oxygen deaths by gear/visual offset,
all6 source renderer slots, in-memory playback snapshot validation/restoration,
paused pixels, finite1560ms terminal hold and no revival/change of death kind as
room dries.2914 owner non-logfiles unchanged in scratch APPDATA. Full-size
paired/master and native82 boards reviewed. No runtime/profile changes.

Use a stable belt/equipment landmark when a head legitimately lowers: registering
each pose by its face would cancel or displace the intended body motion. Measure
the final rendered anchor after grading/resampling rather than trusting source
coordinates alone. A death preview must demonstrate a held terminal; infinite
GIF repetition can obscure finite runtime semantics. New index uses one finite
sequence and explicit Replay, with bound frame hashes to avoid stale previews.

Prone entrance does not cover upright tread. Candidate is deliberately unselected
until directional body/helmet coverage, upright entrance, actual room clearance,
full checkpoint Continue and normal-loader selection are established. Player
snapshot restoration above is not fresh-scene disk restore. Other directions,
ground death, rest/life and whole-set consistency/motion remain. Full goal active.
'''
for name in ['docs/VELD_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md','C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md']:
 f=Path(name) if Path(name).is_absolute() else R/name
 if b'## Veld east prone water death staged' not in f.read_bytes():
  with f.open('ab') as stream:stream.write(lesson.encode('utf-8'))
f=R/'docs/CURRENT_STATUS.md';current=f.read_bytes()
if b'## Veld east prone water death candidate staged' not in current:
 f.write_bytes(f'''## Veld east prone water death candidate staged — September 30, 2026

2gear states/12refs, exact selected swim entrance plus5 authored relaxed poses.
Fixed .3148148 ruler and vial/belt anchor within1px; master skin/hair/cloth/patch
medians within12RGB, native matte graphite/silver helmet and authored closed eyes.
Original1560ms finite timing/terminal hold retained.15fit/66package and exact
2manifest/12frame rebuild PASS.133native checks PASS{v['seconds']}s: actual oxygen
death at four gear/clock cases, all6poses, paused/in-memory playback restoration
and terminal hold; owner2914 non-logfiles unchanged. Native82/master boards reviewed.
Source/prompt/crops retained. Selected-source96state life/death audit locates old
material/helmet drift; does not establish complete motion or normal selection.
Candidate unselected. Next independent west/north/south prone death, upright
tread entrance, actual room/clearance/checkpoint/normal selection; ground death,
rest/life and full-set cross-family polish remain. Full goal active.
[Handoff](../character/veld-death-water-east-coherent-v1/HANDOFF.md).

'''.encode('utf-8')+current)
print('Bound15fit/66package/133native candidate evidence; updated status,pipeline,bible and both skills')
