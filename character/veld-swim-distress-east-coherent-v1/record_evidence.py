"""Bind the staged milestone and append current lessons without resetting shared docs."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;R=P.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
files=[P/'sources/distress-v1.png',P/'sources/prompt-v1.txt',P/'sources/selected-swim-reference.png',P/'bare-manifest.json',P/'helmet-manifest.json',P/'build.py',P/'validate.py',P/'validation.json',P/'rebuild-checks.json',P/'paired-contact.png',P/'station-scale-contact.png',P/'collar-glove-detail.png',R/'tests/test_veld_swim_distress_east_candidate.gd',R/'tools/run_veld_swim_distress_east_candidate.py']
files+=sorted((P/'frames').rglob('*.png'))
out=R/'output/veld-swim-distress-east-candidate-v1'
files += [out/f for f in ['native.log','validation.json','profile-before.json','profile-after.json','native-contact.png']]
report=json.loads((out/'validation.json').read_text());assert report['passed'] and not report['realProfileChanges']
evidence={'status':'staged_east_candidate','nativeChecks':121,'nativeResult':report,'authoring':'built-in imagegen independent six-pose transparent atlas; exact prompt retained',
 'providerResult':'C:/Users/Alex/.codex/generated_images/01a0ef89-9984-7e73-99c2-84cdd8b28b14/exec-8b222fc8-d21e-429c-8b93-a6db5ad4a2eb.png',
 'boundFiles':{f.relative_to(R).as_posix():sha(f) for f in files},'runtimeOrClearanceSelectionChanged':False,
 'remaining':'other directions; actual furnished clearance; wet interruption/diskrestore; continuous-motion/handoff review; family promotion and remaining full-set work'}
(P/'candidate-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
lesson='''

## Veld east swimming distress staged — September 30, 2026

Independent six-pose prone collar-touch/weak-scull source stages two gear states/
12refs at the selected swim camera/ruler. One .234483 anatomical scale; pooled
skin/hair/cloth/blue-patch curves preserve frame consistency; native16degree
master helmet and glove/collar detail reviewed.18 fit,45 package/envelope and121
native checks pass; actual2manifest/12frame rebuild byte-exact. Native82 contact
reviewed,all2914 owner non-logfiles unchanged,clean passing engine log. Selected
runtime/profile unchanged; other directions,real furnished clearance,diskrestore
and full motion/handoffs remain before family promotion. Evidence/handoff:
character/veld-swim-distress-east-coherent-v1/HANDOFF.md.

Wet CrewLife.elapsed=-1 does not imply arbitrary global-phase entry: inspect
CrewSpritePlayer.frame's key-change phase reset. Here actual renderer entry resets
to frame0 at two clock offsets,then advances cosmetic time. Threshold-crossing
presentation and historical low-air flags have different sampling order:
step_crew records the flag before consuming oxygen. Test the crossing and next
unsafe tick separately; preserve production behavior. Initial flag-assumption
failure is retained. Prone distress calls the consumed life.swim-distress profile;
measure every candidate and retain a conservative union with prior bounds. A
candidate static-profile injection with synthetic blockers is not selected-world
or furnished-room clearance proof. Inspect foreground gloves after helmet fitting.
'''
targets=['docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','docs/VELD_ANIMATION_CONTINUATION_2026-09-29.md','skills/brinespace-character-pipeline/references/crew-consistency.md','C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md']
for name in targets:
 f=Path(name) if Path(name).is_absolute() else R/name
 if b'## Veld east swimming distress staged' not in f.read_bytes():
  # Some maintained historical documents contain mixed encodings. Append UTF8
  # without decoding/re-encoding their existing bytes.
  with f.open('ab') as stream:stream.write(lesson.encode('utf-8'))
f=R/'docs/CURRENT_STATUS.md';current=f.read_bytes()
title='## Veld east swimming distress candidate staged — September 30, 2026'
if b'## Veld east swimming distress candidate staged' not in current:
 f.write_bytes((title+'''

Independent source stages2gear states/12refs using selected prone camera,
fixed anatomical ruler,pooled four-material matte grade and native master helmet.
18fit/45package-envelope/121native checks pass;2manifests/12frames rebuild byte-exact.
Native82/contact/collar reviewed;2914 owner non-logfiles unchanged. Renderer entry
resets frame0,then uses cosmetic time. Candidate clearance exceeds current bounds;
conservative union tested only by injected synthetic gate. Runtime/profile unchanged.
Other directions,real furnished clearance,wet interruption/diskrestore,full motion/
handoffs and remaining distress/death/life/rest/polish remain. Full goal active.
[Handoff](../character/veld-swim-distress-east-coherent-v1/HANDOFF.md).

''').encode('utf-8')+current)
print('Bound staged evidence; updated current status, pipeline, bible and both skill copies')
