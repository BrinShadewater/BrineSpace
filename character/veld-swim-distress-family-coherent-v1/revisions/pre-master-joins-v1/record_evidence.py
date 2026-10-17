"""Bind the staged cardinal proof and record the measured clearance lesson."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;R=P.parents[1];S=R/'character/veld-swim-distress-south-coherent-v1';O=R/'output/veld-swim-distress-south-candidate-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
native=json.loads((O/'validation.json').read_text());assert native['passed'] and not native['realProfileChanges']
assert '121 checks,0 failures' in (O/'native.log').read_text()
audit=json.loads((P/'clearance-audit.json').read_text());assert all(r['coveredByCurrentConsumedExtent'] for r in audit['rows'])
assert json.loads((P/'rebuild-checks.json').read_text())['passed']
for folder in [S,P]:
 files=[f for f in folder.rglob('*') if f.is_file() and f.name!='candidate-evidence.json' and '__pycache__' not in f.parts]
 evidence={'status':'staged_candidate_not_selected','boundFiles':{f.relative_to(R).as_posix():sha(f) for f in files},'runtimeOrSelectedClearanceChanged':False,'remaining':'furnished gates,wet interruptions/reentry,disk restore,continuous motion/handoffs,normal selection; remaining full-set death/rest/life/polish'}
 if folder==S:
  evidence.update(nativeChecks=121,nativeResult=native,providerResults=['C:/Users/Alex/.codex/generated_images/01a0ef89-9984-7e73-99c2-84cdd8b28b14/exec-c9da34ba-5798-4508-aa0a-ff7e353d3f55.png'])
  evidence['boundFiles'].update({f.relative_to(R).as_posix():sha(f) for f in O.iterdir() if f.is_file()})
 else:evidence.update(states=8,references=48,effectiveClearanceCoveredStates=8,sourceChecks=64)
 if (P/'furnished-evidence.json').exists():
  evidence['familyFurnishedEvidence']={'file':'character/veld-swim-distress-family-coherent-v1/furnished-evidence.json','sha256':sha(P/'furnished-evidence.json')}
  evidence['remaining']='continuous motion/handoffs,normal selection,actual low-air escape journeys; remaining full-set death/rest/life/polish'
 (folder/'candidate-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
lesson='''

## Veld cardinal swimming distress consolidation — September 30, 2026

South independent prone source stages two gear states/12refs, fixed face ruler
.23529411764705882, pooled matte materials and selected native south helmet.
Source glove masks restore original gray glove pixels over the rim in poses1–3.
21 fit/48 package/121 native checks PASS36.1s; two manifests/12frames rebuild
byte-exact. Scratch APPDATA preserved2914 owner non-logfiles. South native82 and
cardinal master contacts reviewed; continuous motion acceptance remains open.

Cardinal family consolidates8states/48refs without another grade/resample;
64 source checks and actual two-manifest/48frame/binding rebuild pass. All eight
candidate envelopes fit the existing effective base-swim plus life-distress
union. Additional-only reports for east/west/south are not effective navigation
failures. Measure the actual consumed union before proposing profile expansion;
do not enlarge gates to satisfy a report reading only one constituent field.
No runtime/profile change. Furnished clearance,wet interruptions/reentry,disk
restore,full-speed joins and normal-loader selection remain. Death/rest/life and
whole-set polish remain. Handoff:character/veld-swim-distress-family-coherent-v1/HANDOFF.md.
'''
for name in ['docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','docs/VELD_ANIMATION_CONTINUATION_2026-09-29.md','skills/brinespace-character-pipeline/references/crew-consistency.md','C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md']:
 f=Path(name) if Path(name).is_absolute() else R/name
 if b'## Veld cardinal swimming distress consolidation' not in f.read_bytes():
  with f.open('ab') as stream:stream.write(lesson.encode('utf-8'))
f=R/'docs/CURRENT_STATUS.md';current=f.read_bytes()
if b'## Veld cardinal swimming distress family staged' not in current:
 f.write_bytes('''## Veld cardinal swimming distress family staged — September 30, 2026

South source completes cardinal candidate coverage:8gear states/48refs,64 exact
consolidation checks and byte-exact two-manifest/48frame rebuild. South21fit/
48package/121native PASS36.1s,2914 owner non-logfiles unchanged. Native82 and
cardinal master boards reviewed. Effective base-swim/life union covers all8
states; no clearance expansion needed. Runtime/profile unchanged. Furnished
clearance,wet interruption/reentry,diskrestore,continuous motion/handoffs and
normal-loader selection remain; death/rest/life/full-set polish goal active.
[Handoff](../character/veld-swim-distress-family-coherent-v1/HANDOFF.md).

'''.encode('utf-8')+current)
print('Bound south/cardinal evidence; recorded milestone in status,pipeline,bible and both skill copies')
