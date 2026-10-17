from pathlib import Path
import json,hashlib,shutil,sys
P=Path(__file__).resolve().parent;slot=int(sys.argv[1]);original=Path(sys.argv[2]);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();q=json.loads((P/f'job-{slot:03}.json').read_text());assert q['status']=='prepared'
for path,h in q['frozenInputs'].items():assert sha(Path(path))==h,path
for ref in q['references']:assert sha(Path(ref['path']))==ref['sha256']
assert sha(Path(q['promptFile']))==q['promptSha256']==q['submittedPromptSha256']
saved=P/f'sources/raw-{slot:03}.png';assert not saved.exists();shutil.copy2(original,saved);assert sha(original)==sha(saved)
q.update(status='completed',originalPath=str(original),savedPath=str(saved),sha256=sha(saved),generationId=original.stem);t=json.dumps(q,indent=2)+'\n';(P/f'job-{slot:03}.json').write_text(t);(P/f'provenance-{slot:03}.json').write_text(t);print(f'Pose {slot}: raw copied and exact source/prompt/reference/output hashes verified.')
