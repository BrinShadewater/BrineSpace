from pathlib import Path
import json,hashlib
from PIL import Image
H=Path(__file__).resolve().parent;R=H.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
refs=[R/'character/veld-swim-turn-east-south-coherent-v1/bare-source-v1.png',R/'character/veld-swim-carry-east-coherent-v1/source-v2.png',R/'character/veld-swim-carry-south-coherent-v1/source-v3.png']
rows=[]
for version,provider,rr,selection in [(1,'exec-8e7c67c0-7032-49dd-b659-7b0f6f99ef62.png',refs,'cells0,1,3 selected;cell2 rejected for close yaw'),(2,'exec-df799607-56c3-4936-bba1-6f536ea7e030.png',[H/'body-source-v1.png'],'cell2 only selected; other cells unused')]:
 p=H/f'body-source-v{version}.png';prompt=H/f'body-prompt-v{version}.txt'
 rows.append(dict(source=p.relative_to(R).as_posix(),sourceSha256=sha(p),dimensions=list(Image.open(p).size),prompt=prompt.relative_to(R).as_posix(),promptSha256=sha(prompt),providerOriginal='C:/Users/Alex/.codex/generated_images/01a0ef89-9984-7e73-99c2-84cdd8b28b14/'+provider,references=[dict(path=q.relative_to(R).as_posix(),sha256=sha(q)) for q in rr],selection=selection))
helmet=R/'character/veld-swim-turn-east-south-coherent-v1/helmet-source-v1.png'
(H/'source-provenance.json').write_text(json.dumps(dict(installed=False,method='built-in imagegen body; reused independently authored selected ordinary-turn helmet components',sources=rows,helmetSource=dict(path=helmet.relative_to(R).as_posix(),sha256=sha(helmet)),scaleRule='One .24 source atlas ruler; visual skull/torso/leg/case comparisons required; no per-frame normalization'),indent=2)+'\n',encoding='utf-8')
