"""Verify and bind exact selected master joins independently from gesture provenance."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;R=P.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
bindings=json.loads((P/'source-bindings.json').read_text());assert bindings['checks']==80
joins=0;interiors=0
for row in bindings['sourceBindings']:
 for f in row['frames']:
  out=P/f"frames/{row['gear']}/swim-distress-{row['direction']}/{f['slot']:03}.png"
  assert sha(out)==f['sha256']==sha(R/f['file'])
  if f['role']=='selected_swim_exact_join':joins+=1
  else:assert sha(out)==f['authoredSha256'];interiors+=1
assert (joins,interiors)==(16,32)
proofs={}
for name,folder,count in [('candidate','veld-swim-distress-family-candidate-v1',571),('furnished','veld-distress-furnished-v1',1007)]:
 o=R/'output'/folder;v=json.loads((o/'validation.json').read_text());assert v['passed'] and not v['realProfileChanges'];assert f'{count} checks,0 failures' in (o/'native.log').read_text()
 proofs[name]={'checks':count,'result':v,'logSha256':sha(o/'native.log')}
e={'selectedMasterJoins':joins,'authoredInteriorsUnchanged':interiors,'rebuildChecks':json.loads((P/'rebuild-checks.json').read_text()),'nativeProofs':proofs,'frameBindings':bindings,'status':'staged_master_join_revision','rollback':'character/veld-swim-distress-family-coherent-v1/revisions/pre-master-joins-v1','runtimeSelected':False,'remaining':'actual escape journeys,continuous-motion/first-interior joins,normal-loader selection and full-set work'}
(P/'master-join-evidence.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
lesson=f'''

## Veld distress exact selected-swim joins — September 30, 2026

Neutral authored entry/closure replaced4810-ish pixels versus selected master
(measured range3672–5122 across16 comparisons), despite matching nominal scale
and grade. Family slots0/5 now copy exact selected swim0 by direction/gear;
32 authored interior gesture frames remain byte-exact. Original directional
source packs unchanged and pre-join family/evidence archived. source-bindings
explicitly records selected join versus authored gesture donors,including each
original authored input hash.80 donor/metadata/join checks and full two-manifest/
48frame rebuild pass. Fresh571 controller/renderer checks PASS{proofs['candidate']['result']['seconds']}s
and1007 furnished checks/96 restores PASS{proofs['furnished']['result']['seconds']}s. Owner profile unchanged;
current effective clearance still covers8/8. Native family/contact reviewed.

Exact joins establish a stable master body/head/material at the boundary,not
smooth first-interior motion or arbitrary-phase exit acceptance. Keep original
gesture interiors and review neighboring frames rather than inventing tween
pixels or treating whole-clip source identity as exact endpoint continuity.
Timing remains six160ms,original pivot/standing ruler. Family GIFs now preview
the joined output rather than obsolete independent source loops. Runtime
selection unchanged; actual escape and full motion/normal selection still open.
Full-set death/rest/life/consistency goal active.
'''
for name in ['docs/VELD_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md','C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md']:
 f=Path(name) if Path(name).is_absolute() else R/name
 if b'## Veld distress exact selected-swim joins' not in f.read_bytes():
  with f.open('ab') as stream:stream.write(lesson.encode('utf-8'))
f=P/'HANDOFF.md';s=f.read_text(encoding='utf-8')
if 'Master join follow-up:' not in s:
 s=s.replace('## Next action',f"Master join follow-up:16 exact selected swim0 entry/closure donors and32 unchanged authored interiors.80 packaging/source checks; fresh571 renderer checks PASS{proofs['candidate']['result']['seconds']}s and1007 furnished/96restore checks PASS{proofs['furnished']['result']['seconds']}s. Original pre-join candidate/evidence retained in revisions/pre-master-joins-v1. Current family GIFs/interactive review reflect joined output.\n\n## Next action")
 f.write_text(s,encoding='utf-8')
f=R/'docs/CURRENT_STATUS.md';current=f.read_bytes()
if b'## Veld distress selected-master joins staged' not in current:
 f.write_bytes(f'''## Veld distress selected-master joins staged — September 30, 2026

Family slots0/5 now use16 exact selected swim master donors;32 authored gesture
interiors unchanged. Original source packs/pre-join family/evidence preserved.
80 donor/metadata checks and2manifest/48frame rebuild PASS. Fresh571 renderer
checks PASS{proofs['candidate']['result']['seconds']}s and1007 furnished/96restores PASS{proofs['furnished']['result']['seconds']}s;
owner profile unchanged,current clearance covers8/8. Native/master contacts
reviewed. Output GIFs and interactive motion review now show joined frames.
Exact endpoints do not prove first-interior or arbitrary-phase exits. Actual
escape journeys and full continuous motion/normal selection remain;full-set
death/rest/life/consistency goal active. Runtime selection unchanged.
[Handoff](../character/veld-swim-distress-family-coherent-v1/HANDOFF.md).

'''.encode('utf-8')+current)
print('Bound16 exact master joins/32 preserved interiors and fresh571/1007 native checks')
