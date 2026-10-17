from pathlib import Path
import json,hashlib
from PIL import Image
H=Path(__file__).resolve().parent;R=H.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
source=H/'body-source-v1.png';prompt=H/'body-prompt-v1.txt';refs=[R/'character/veld-swim-turn-south-west-coherent-v1/bare-source-v1.png',R/'character/veld-swim-carry-west-coherent-v1/source-v1.png',R/'character/veld-swim-carry-south-coherent-v1/source-v3.png']
sources=[dict(path=source.relative_to(R).as_posix(),sha256=sha(source),dimensions=list(Image.open(source).size),prompt=prompt.relative_to(R).as_posix(),promptSha256=sha(prompt),providerOriginal='C:/Users/Alex/.codex/generated_images/01a0ef89-9984-7e73-99c2-84cdd8b28b14/exec-88da6ffd-d39e-4134-8370-6a10a4386119.png',references=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in refs],selection='All4 authored intermediate cells')]
helmets=[]
for version,cells,scale in [(2,[0,1],.083),(1,[2,3],.095)]:
 p=R/f'character/veld-swim-turn-south-west-coherent-v1/helmet-source-v{version}.png';helmets.append(dict(path=p.relative_to(R).as_posix(),sha256=sha(p),cells=cells,scale=scale))
(H/'source-provenance.json').write_text(json.dumps(dict(installed=False,method='Built-in imagegen cargo body; retained independently authored ordinary-turn helmet sources',bodySources=sources,helmetSources=helmets,scaleRule='Uniform.21 atlas physical ruler; measured fitted endpoint face anchors; no per-frame size normalization'),indent=2)+'\n',encoding='utf-8')
