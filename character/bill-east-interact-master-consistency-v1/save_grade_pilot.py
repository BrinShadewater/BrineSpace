from pathlib import Path
import json,hashlib,shutil
P=Path('character/bill-east-interact-master-consistency-v1/grade-pilot-v1');q=json.loads((P/'job.json').read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for path,h in q['frozenInputs'].items():assert sha(Path(path))==h
for r in q['references']:assert sha(Path(r['path']))==r['sha256']
assert sha(Path(q['promptFile']))==q['promptSha256']==q['submittedPromptSha256']
original=Path('C:/Users/Alex/.codex/generated_images/01a0ef89-cf35-77f0-9b57-2a08e6ea987f/exec-7ffa3fae-d16e-43da-b5ed-f15c3841970b.png');saved=P/'raw.png';assert not saved.exists();shutil.copy2(original,saved);assert sha(original)==sha(saved)
q.update(status='completed',originalPath=str(original),savedPath=str(saved.resolve()),sha256=sha(saved),generationId=original.stem);(P/'provenance.json').write_text(json.dumps(q,indent=2)+'\n');print('Generated raw copied; all frozen inputs, exact prompt and output hashes match.')
