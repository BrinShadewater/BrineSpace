"""Copy a built-in result immediately and bind it to verified prepared inputs."""
from pathlib import Path
import hashlib,json,shutil,sys
OUT=Path(__file__).resolve().parent
key,original=sys.argv[1:3];original=Path(original)
revision=int(sys.argv[3]) if len(sys.argv)>3 else 1
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
job=OUT/f'generation-job-{key}-v{revision}.json'
q=json.loads(job.read_text(encoding='utf-8'));assert q['status']=='prepared'
assert sha(Path(q['sourcePath']))==q['sourceSha256']
assert sha(Path(q['promptFile']))==q['promptSha256']==q['submittedPromptSha256']
for r in q['references']:assert sha(Path(r['path']))==r['sha256']
saved=OUT/'sources'/f'{key}-edit-v{revision}.png';assert not saved.exists()
shutil.copy2(original,saved);assert sha(original)==sha(saved)
q.update(status='completed',originalPath=str(original),savedPath=str(saved),sha256=sha(saved),generationId=original.stem)
text=json.dumps(q,indent=2)+'\n'
job.write_text(text,encoding='utf-8')
(OUT/f'generation-provenance-{key}-v{revision}.json').write_text(text,encoding='utf-8')
print(key+' copied and verified')
