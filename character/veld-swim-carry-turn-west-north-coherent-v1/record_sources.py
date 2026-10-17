from pathlib import Path
import json,hashlib
from PIL import Image
H=Path(__file__).resolve().parent;R=H.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
refs=[R/'character/veld-swim-turn-west-north-coherent-v1/bare-source-v1.png',R/'character/veld-swim-carry-west-coherent-v1/source-v1.png',R/'character/veld-swim-carry-north-coherent-v1/source-v3.png']
sources=[]
for v,provider,selection,rr in [(1,'exec-96aff425-11cd-47a2-b39a-358510091f65.png','Rejected: early yaw repeated, last cell cardinal north',refs),(2,'exec-b05fca40-20c3-40ca-887a-f0e916eabc5a.png','Selected all four revised yaws',[H/'body-source-v1.png'])]:
 p=H/f'body-source-v{v}.png';prompt=H/f'body-prompt-v{v}.txt';sources.append(dict(path=p.relative_to(R).as_posix(),sha256=sha(p),dimensions=list(Image.open(p).size),prompt=prompt.relative_to(R).as_posix(),promptSha256=sha(prompt),providerOriginal='C:/Users/Alex/.codex/generated_images/01a0ef89-9984-7e73-99c2-84cdd8b28b14/'+provider,selection=selection,references=[dict(path=x.relative_to(R).as_posix(),sha256=sha(x)) for x in rr]))
p=R/'character/veld-swim-turn-west-north-coherent-v1/helmet-source-v2.png'
(H/'source-provenance.json').write_text(json.dumps(dict(installed=False,method='Built-in imagegen authored cargo body with revised yaw; retained independently authored ordinary prone helmet heads',bodySources=sources,helmetSources=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p),cells=[0,1,2,3],scale=.07)],scaleRule='Uniform .22 body/.07 helmet atlas rulers; explicit full-head centers and case ownership; no pose-size normalization',semanticLandmarksSha256=sha(H/'semantic-landmarks.json')),indent=2)+'\n',encoding='utf-8')
