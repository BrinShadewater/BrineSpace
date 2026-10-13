"""Bind inspected pilot evidence and bounded follow-up lessons."""
from pathlib import Path
import ast,hashlib,json
R=Path(__file__).resolve().parents[1]
D=R/'character/bill-east-reach-adjacent-motion-v1/recovery-direct-004-v3'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
report=json.loads((D/'review.json').read_text(encoding='utf-8'))
receipt=json.loads((D/'provenance.json').read_text(encoding='utf-8'))
assert sha(D/'raw-004.png')==receipt['rawSha256']
assert sha(D/'prompt.txt')==receipt['promptSha256']
assert all(sha(Path(x['path']))==x['sha256'] for x in receipt['references'])
assert report['crownDelta']==-1 and report['soleDelta']==0 and report['opaqueOverflow']==0
for tool in ['review_bill_direct_recovery_v3.py','record_bill_adjacent_reach_milestone.py','record_bill_direct_recovery_v3.py']:
    ast.parse((R/'tools'/tool).read_text(encoding='utf-8'))
report.update(status='provisional_source_improvement',visualReviewed=True,visualFindings='Whole raw and complete four-column master/donor/prior/new comparison inspected. More stable stature and forward low forearm, warm face and matte quilt retained. Hair/collar edges still redraw slightly; one-pixel crown rise remains. Recovery arm angle differs from prior and needs complete sequence review.',comparisonSha256=sha(D/'comparison.png'),sourceGeometryValidated=True,normalAdmission=False,nativeTested=False)
(D/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
note='''

Bill East direct recovery follow-up (October 3): built-in edit from successful
first-reach raw001, exec-6a2d312f-0298-47dd-b737-de1423a9a7bf, preserves sole224
without registration and reduces recovery stature excess from3packed pixels to1.
Common bounds138,75,203,224 versus donor138,76,199,224; zeroopaque overflow,
lower-body IoU.960468. Entire raw and four-column whole/master/head board reviewed.
Forward low forearm/material improved, but collar/hair still redraw slightly and
complete sequence/cadence remains untested. Keep provisional source study outside
current six-slot manifest; earlier904native check does not cover this new source.
Three receipt/reference/prompt checks and Python syntax pass;3PNG LFS attributes
checked. No normal selection change. Full goal active; fix extension stature,
then assemble and review complete candidate sequence before runtime validation.
Evidence:character/bill-east-reach-adjacent-motion-v1/recovery-direct-004-v3/review.json.
'''
paths=[R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']
for root in [R/'skills/brinespace-character-pipeline',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline')]:
    paths += [root/'references/crew-consistency.md',root/'references/source-density.md']
for p in paths:
    with p.open('a',encoding='utf-8') as f:f.write(note)
handoff=R/'character/bill-east-reach-adjacent-motion-v1/HANDOFF.md'
with handoff.open('a',encoding='utf-8') as f:f.write('\nDirect recovery job600 is terminal and saved: recovery-direct-004-v3/raw-004.png. Raw and master comparison inspected, source stature excess reduced3→1px, sole unchanged without whole shift, no overflow. Receipt/reference/prompt equality and three Python syntax checks pass;3PNG LFS checked. Not installed into manifest/native test. Next extension stature repair and full revised-sequence comparison. No live generation handles.\n')
print('Preserved terminal pilot and review; provenance, geometry and syntax checks passed; eight records updated.')
