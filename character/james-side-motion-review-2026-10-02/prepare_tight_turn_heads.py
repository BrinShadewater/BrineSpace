from pathlib import Path
from PIL import Image
import json
P=Path(__file__).resolve().parent;R=P.parents[1];rows=json.loads((P/'turn-head-layout.json').read_bytes());target=Image.new('RGBA',(864,512))
for row in rows:
    n=row['cell'];im=Image.open(R/row['source']).convert('RGBA').crop((128,71,164,103)).resize((288,256),Image.Resampling.NEAREST);target.alpha_composite(im,((n%3)*288,(n//3)*256))
target.save(P/'turn-head-only-target.png')
path=R/'character/crew-runtime-matte-v1/branforth/manifest.json';pack=json.loads(path.read_bytes());masters=Image.new('RGBA',(864,272))
for n,d in enumerate(['east','north','south']):
    s=next(s for s in pack['states'] if s['id']=='idle-'+d);im=Image.open(path.parent/s['frameFiles'][0]).convert('RGBA').crop((76,18,112,52)).resize((288,272),Image.Resampling.NEAREST);masters.alpha_composite(im,(n*288,0))
masters.save(P/'turn-head-only-masters.png')
Image.open(P/'east-family-v2/carry-east-000.png').crop((128,71,164,103)).resize((288,256),Image.Resampling.NEAREST).save(P/'turn-head-only-anchor.png')
