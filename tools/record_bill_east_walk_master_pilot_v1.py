"""Bind source pilot limitations and retain the reference-density lesson."""
from pathlib import Path
import json,hashlib,ast,subprocess
R=Path(__file__).resolve().parents[1];P=R/'character/bill-east-walk-master-pilot-v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
receipt=json.loads((P/'provenance.json').read_text(encoding='utf-8'));assert sha(P/'raw-024.png')==receipt['rawSha256'] and sha(P/'prompt.txt')==receipt['promptSha256']
assert all(sha(Path(r['source']))==r['sourceSha256'] and sha(Path(r['path']))==r['sha256'] for r in receipt['references'])
neighbors=json.loads((P/'neighbor-inputs.json').read_text(encoding='utf-8'));assert all(sha(Path(p))==h for p,h in neighbors.items())
report=json.loads((P/'review.json').read_text(encoding='utf-8'));report.update(status='provisional_master_detail_geometry_open',visualReviewed=True,visualFindings='Raw and full master/donor and neighbor23/24/25 boards inspected. Warmer angular face and quilt/weathered hardware improve original fidelity. Crown3px higher/sole1px lower/height4px greater than target; material/head jump against unchanged neighbors. No complete loop or normal acceptance.',comparisonSha256=sha(P/'comparison.png'),neighborComparisonSha256=sha(P/'neighbor-comparison.png'));(P/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
tools=['prepare_bill_east_walk_master_pilot_v1.py','register_bill_walk_pilot_references_v1.py','register_bill_walk_pilot_references_v2.py','review_bill_east_walk_master_pilot_v1.py','build_bill_walk_pilot_neighbors_v1.py','record_bill_east_walk_master_pilot_v1.py']
for name in tools:ast.parse((R/'tools'/name).read_text(encoding='utf-8'))
pngs=list(P.rglob('*.png'));result=subprocess.run(['git','check-attr','filter','--']+[p.relative_to(R).as_posix() for p in pngs],cwd=R,capture_output=True,text=True,check=True);assert len(result.stdout.splitlines())==len(pngs) and all(x.endswith(': filter: lfs') for x in result.stdout.splitlines())
note=f'''

Bill East walk master pilot (October3): one full stride24 of48, built-in
exec-73ef655c-2404-4bca-905d-d17ea95e929f. Exact raw/prompt/three refs saved.
Master/detailed support refs use same physicalH148/p128224 fourfold profile as
whole target while preserving high source density. Archive first whole-square
density mismatch and second low-res packed/upscaled preparation before generation.
Use1408common (4x352), crop736 (4x184), translate144,208 onto1024; no bbox fitting.
Matching canvas sizes alone does not match physical scale. Packing to low-res then
upscaling discards reference detail; perform fixed profile operations directly at
high density for generation refs and reduce once for actual compatibility output.

Whole raw/master/donor and neighbor23/24/25 boards inspected. Warm face/quilt/
worn hardware closer, but bounds85,78,181,224 versus85,81,180,223: crown-3,
sole+1,height+4,IoU.930729. Single revised pose would create a head/material seam
against unchanged neighbors. Keep provisional geometry/temporal issue, no normal
manifest/admission/native run. Do not falsely count this as full48source coverage.
Provenance/neighbor hashes stable;6Python syntax/{len(pngs)}PNG LFS checks pass.
Next restrained full-pose stature/contact correction and representative other
stride phases before full48 expansion. All other Bill family/polish scope remains
active; no live generation handles. Handoff:character/bill-east-walk-master-pilot-v1/HANDOFF.md.
'''
paths=[R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']
for root in [R/'skills/brinespace-character-pipeline',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline')]:paths += [root/'references/crew-consistency.md',root/'references/source-density.md']
for p in paths:
 with p.open('a',encoding='utf-8') as f:f.write(note)
with (R/'character/bill-east-reach-adjacent-motion-v2/HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\nWalking job640 terminal, preserved in bill-east-walk-master-pilot-v1; full raw/master/neighbors reviewed. Master detail improves but head/height4px difference and neighbor grade seam remain, no full48 expansion/admission. See its HANDOFF. Current goal remains full library; no live job/session.\n')
print(f'Recorded one-of48 source pilot, geometry/temporal findings and reference-density lesson;6AST/{len(pngs)}PNG LFS; eight maintained records updated.')
