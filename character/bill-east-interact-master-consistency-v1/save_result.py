"""Bind each independent built-in result to exact prepared inputs immediately."""
from pathlib import Path
import hashlib,json,shutil,sys
P=Path(__file__).resolve().parent
index=int(sys.argv[1]);original=Path(sys.argv[2]);sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
job=P/f'generation-job-{index:03}-v1.json';q=json.loads(job.read_text());assert q['status']=='prepared'
for path,digest in q['frozenInputs'].items():assert sha(Path(path))==digest
for r in q['references']:assert sha(Path(r['path']))==r['sha256']
assert sha(Path(q['promptFile']))==q['promptSha256']==q['submittedPromptSha256']
saved=P/f'sources/interact-{index:03}-edit-v1.png';assert not saved.exists();shutil.copy2(original,saved);assert sha(original)==sha(saved)
q.update(status='completed',originalPath=str(original),savedPath=str(saved),sha256=sha(saved),generationId=original.stem)
text=json.dumps(q,indent=2)+'\n';job.write_text(text);(P/f'generation-provenance-{index:03}-v1.json').write_text(text)
print(f'{index:03} raw copied and exact input/output hashes verified')
