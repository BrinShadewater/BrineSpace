"""Retain a frozen whole cargo generation and its original without altering pixels."""
from pathlib import Path
import argparse,hashlib,json,shutil
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'character/marsh-cargo-held-material-v1/sources'
ap=argparse.ArgumentParser();ap.add_argument('--source',required=True);ap.add_argument('--generation-id',required=True);args=ap.parse_args()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((S/f'{args.source}.request.json').read_text());assert sha(S/f'{args.source}.prompt.txt')==r['promptSha256']
for q in r['orderedReferences']+r['sourceFrames']+r['guideDependencies']:assert sha(ROOT/q['path'])==q['sha256']
original=Path('C:/Users/Alex/.codex/generated_images/01a0fbf5-ac74-7c72-98e7-34736a220c96')/(args.generation_id+'.png');raw=S/f'{args.source}.raw.png'
if raw.exists():assert sha(raw)==sha(original)
else:shutil.copy2(original,raw)
r.update(generationId=args.generation_id,originalGeneratedPath=str(original),rawSha256=sha(raw),status='generated; original retained; whole packing and review pending')
(S/f'{args.source}.request.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'generationId':args.generation_id,'originalRetained':original.exists(),'rawSha256':sha(raw)}))
