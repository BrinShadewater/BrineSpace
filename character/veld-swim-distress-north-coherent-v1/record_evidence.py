"""Record north source/native evidence and append measured production lessons."""
from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-swim-distress-north-candidate-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
result=json.loads((O/'validation.json').read_text());assert result['passed'] and not result['realProfileChanges']
files=[P/f for f in ['sources/distress-v1.png','sources/distress-arm-edit-v2.png','sources/prompt-v1.txt','sources/prompt-arm-edit-v2.txt','sources/selected-swim-reference.png','bare-manifest.json','helmet-manifest.json','build.py','validate.py','validation.json','build-evidence.json','rebuild-checks.json','paired-contact.png','station-scale-contact.png','head-arm-detail.png','revisions/landmark-trials-v1.json','HANDOFF.md']]
files+=sorted((P/'frames').rglob('*.png'))
files += [O/f for f in ['native.log','validation.json','profile-before.json','profile-after.json','native-contact.png']]
files += [R/f for f in ['tests/test_veld_swim_distress_north_candidate.gd','tools/run_veld_swim_distress_north_candidate.py','character/veld-water-north-coherent-v1/swim-source-v1.png']]
e={'status':'staged_north_candidate','nativeChecks':123,'nativeResult':result,
 'authoring':'built-in imagegen independent six-pose source plus local arm correction; five original cells and corrected edit cell5 mapped to slot3',
 'providerResults':['C:/Users/Alex/.codex/generated_images/01a0ef89-9984-7e73-99c2-84cdd8b28b14/exec-ffa131f7-4eb4-4bb4-8bef-e1d53b7f9aae.png','C:/Users/Alex/.codex/generated_images/01a0ef89-9984-7e73-99c2-84cdd8b28b14/exec-df49fa44-7fee-4f06-b730-f554a9e2f698.png'],
 'boundFiles':{f.relative_to(R).as_posix():sha(f) for f in files},'runtimeOrSelectedClearanceChanged':False,
 'remaining':'south authoring/cardinal family; actual furnished clearance; wet re-entry/interruption/disk restore; continuous motion/handoff review before normal-loader selection; remaining full-set work'}
(P/'candidate-evidence.json').write_text(json.dumps(e,indent=2)+'\n')
lesson='''

## Veld north swimming distress staged — September 30, 2026

Independent rear/overhead source plus local arm correction stages two gear states/
12refs against selected prone swim. Same screen-right working arm,screen-left support;
pouch/vials keep rear sides. Five original poses plus edited cell5 mapped to slot3.
Primary scalp21/74 and edited21/93 rulers,crown104/center128,pooled four-material
matte grade,native rear helmet.24 fit/60 package/123 native checks pass30.85s;
2manifests/12frames rebuild byte-exact. Native82/head-arm contacts reviewed;
all2914 owner non-logfiles unchanged,clean passing log. Runtime/profile unchanged.
Handoff:character/veld-swim-distress-north-coherent-v1/HANDOFF.md. South,furnished
clearance,wet interruption/diskrestore,full motion/handoffs/family selection remain;
remaining death/rest/life/cross-family polish goal stays active.

Inspect source edits before selecting: provider changed2column/3row atlas into
3column/2row and changed source density. Select only corrected cell,retain original
unaffected cells,record actual source grid and separate anatomical edit ruler.
Dark hair strands fragment colour landmarks; nearby warm support can group them,
but a nearby glove cuff may join the edited head. Bound the actual scalp region
and name the row/ruler; inspect anatomy at station scale before native promotion.
Historical31px fragment/111px cuff-contaminated calibrations are rejected;
current74/93px source scalp widths both map21native pixels. Do not height-normalize.

CrewLife.clear's additional distress extent is unioned with base swimming by the
actor. An outside-additional blocker can still touch that wider base. Test the
effective union and independently prove an additional life reach outside base
swim; use actual consumed code,not the nearest JSON field alone. Initial outside
blocker fixture failure retained; production navigation unchanged. Synthetic
gates remain separate from real furnished clearance and selected runtime proof.
'''
for name in ['docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','docs/VELD_ANIMATION_CONTINUATION_2026-09-29.md','skills/brinespace-character-pipeline/references/crew-consistency.md','C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md']:
 f=Path(name) if Path(name).is_absolute() else R/name
 if b'## Veld north swimming distress staged' not in f.read_bytes():
  with f.open('ab') as stream:stream.write(lesson.encode('utf-8'))
f=R/'docs/CURRENT_STATUS.md';current=f.read_bytes()
if b'## Veld north swimming distress candidate staged' not in current:
 f.write_bytes('''## Veld north swimming distress candidate staged — September 30, 2026

Independent rear prone source plus local same-arm correction stages2gear states/
12refs. Five original cells plus corrected edit cell5→slot3;21px anatomical scalp
rulers74/93,crown104,matte pooled grade,native rear helmet.24 fit/60 package/123
native checks PASS30.85s;2manifests/12frames rebuild byte-exact. Native82/head-arm
contacts reviewed;2914 owner non-logfiles unchanged. Rejected fragmented/cuff
landmarks and fixture union assumption retained. Effective gate unions base swim
with life-distress. Runtime/profile unchanged. South/cardinal family,furnished
clearance,wet interruption/diskrestore,full motion/handoffs and full-set death/rest/
life/polish remain. Goal active.
[Handoff](../character/veld-swim-distress-north-coherent-v1/HANDOFF.md).

'''.encode('utf-8')+current)
print('Bound north evidence; updated current status,pipeline,bible and both skill copies')
