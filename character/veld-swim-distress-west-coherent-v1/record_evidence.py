"""Record staged source/native proof and append the foreground-occlusion lesson."""
from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];OUT=R/'output/veld-swim-distress-west-candidate-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
result=json.loads((OUT/'validation.json').read_text());assert result['passed'] and not result['realProfileChanges']
files=[P/f for f in ['sources/distress-v1.png','sources/prompt-v1.txt','sources/selected-swim-reference.png','bare-manifest.json','helmet-manifest.json','build.py','validate.py','validation.json','build-evidence.json','rebuild-checks.json','foreground-occlusion-audit.json','paired-contact.png','station-scale-contact.png','collar-glove-detail.png','HANDOFF.md']]
files+=sorted((P/'frames').rglob('*.png'))+sorted((P/'sources/crops').glob('glove-mask-*.png'))
files += [OUT/f for f in ['native.log','validation.json','profile-before.json','profile-after.json','native-contact.png']]
files += [R/f for f in ['tests/test_veld_swim_distress_west_candidate.gd','tools/run_veld_swim_distress_west_candidate.py','character/veld-water-west-coherent-v1/swim-source-v1.png']]
e={'status':'staged_west_candidate','authoring':'built-in imagegen independent six-pose transparent source; exact prompt and both input references retained',
   'providerResult':'C:/Users/Alex/.codex/generated_images/01a0ef89-9984-7e73-99c2-84cdd8b28b14/exec-fcc6160a-4d51-43b3-b17c-8356ae59689a.png',
   'nativeChecks':121,'nativeResult':result,'boundFiles':{f.relative_to(R).as_posix():sha(f) for f in files},
   'runtimeOrSelectedClearanceChanged':False,'remaining':'north/south authoring; cardinal family; real furnished clearance; wet re-entry/interruption/disk restoration; complete motion/handoff review before selection; remaining full-set work'}
(P/'candidate-evidence.json').write_text(json.dumps(e,indent=2)+'\n')
title='## Veld west swimming distress staged — September 30, 2026'
lesson='''

'''+title+'''

Independent west source stages two gear states/12 refs against selected prone
swimming, with the near-side instrument pouch and far-side vial tips retained.
One .228571 anatomical ruler; pooled skin/hair/cloth/patch grade; native west
helmet at16degrees.21 fit,48 package/envelope and121 corrected-art native checks
pass;2 manifests/12 frames rebuild byte-exact. Native82 contact and glove/collar
detail reviewed. All2914 owner non-logfiles unchanged; clean passing log. Runtime
and selected clearance unchanged. Handoff:
character/veld-swim-distress-west-coherent-v1/HANDOFF.md.

Protected-body and clock tests can pass while the helmet collar hides the working
fingertips. Compare bare/equipped authored gesture details before promotion.
Use documented source foreground masks to restore original glove pixels in front
of the shell; do not repaint anatomy. Poses1–3 restore6/55/47 changed native pixels;
masked original-pixel equality and corrected-art native checks pass. The earlier
technically passing unmasked interval is historical, not visual acceptance.
Neither gear candidate fits current life.swim-distress-west bounds; retain a
conservative union and test the consumed gate, then real furnished geometry.
Synthetic gate injection does not select the disk profile or prove room safety.
North/south authoring,life interruption/restore and complete motion/handoffs
remain before family selection. Full-set death/rest/life/polish work stays active.
'''
for name in ['docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','docs/VELD_ANIMATION_CONTINUATION_2026-09-29.md','skills/brinespace-character-pipeline/references/crew-consistency.md','C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md']:
 f=Path(name) if Path(name).is_absolute() else R/name
 if b'## Veld west swimming distress staged' not in f.read_bytes():
  with f.open('ab') as stream:stream.write(lesson.encode('utf-8'))
f=R/'docs/CURRENT_STATUS.md';old=f.read_bytes()
if b'## Veld west swimming distress candidate staged' not in old:
 f.write_bytes('''## Veld west swimming distress candidate staged — September 30, 2026

Independent west source stages two gear states/12 refs, matched to selected prone
camera, one anatomical ruler, pooled four-material matte grade and native helmet.
West instrument pouch/vial sides preserved. Foreground masks restore collar-touch
fingertips;21 fit/48 package/121 corrected-art native checks pass32.78s.2 manifests/
12 frames rebuild byte-exact. Native82/detail reviewed;all2914 owner non-logfiles
unchanged. Runtime/profile unchanged; conservative life-distress union staged.
North/south,furnished clearance,wet interruption/diskrestore,full motion/handoffs,
family selection and remaining death/life/rest/full-set polish remain. Goal active.
[Handoff](../character/veld-swim-distress-west-coherent-v1/HANDOFF.md).

'''.encode('utf-8')+old)
print('Bound west candidate evidence; updated current status, pipeline, bible and both skill copies')
