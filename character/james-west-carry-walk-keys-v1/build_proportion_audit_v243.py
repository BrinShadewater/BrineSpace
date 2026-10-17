from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'proportion-audit-v243';out.mkdir(exist_ok=True)
manifest=json.loads((r/'character/james-cargo-material-joined-v1/bare-manifest.json').read_bytes());state=next(s for s in manifest['states'] if s['id']=='carry-west');ledger=json.loads((p/'material-repair-progress.json').read_bytes())
items=[('Original master',r/'character/james-west-master-carry-v1/registered-original-master.png'),('Normal carry0',r/'character/james-cargo-material-joined-v1'/state['frameFiles'][0])]+[(f'New carry{i}',r/ledger['states'][i]['candidateSources']['bare']['file']) for i in [0,12,24,30,37,48]]
board=Image.new('RGBA',(len(items)*192,700),(47,58,63,255));draw=ImageDraw.Draw(board);rows=[]
for col,(label,f) in enumerate(items):
 im=Image.open(f).convert('RGBA');assert im.size==(256,256)
 x=col*192;draw.text((x+5,6),label,fill='white');board.alpha_composite(im.crop((80,65,176,235)).resize((192,340),Image.Resampling.NEAREST),(x,26))
 for label2,y in [('Head base',102),('Shoulder',117),('Hip band',151),('Knee region',171),('Floor pivot',224)]:
  yy=26+(y-65)*2;draw.line((x,yy,x+192,yy),fill=(100,125,130,255),width=1)
 draw.text((x+5,382),'Torso / hip detail',fill='white');board.alpha_composite(im.crop((96,104,160,168)).resize((192,192),Image.Resampling.NEAREST),(x,404))
 rows.append(dict(label=label,file=f.relative_to(r).as_posix(),sha256=hashlib.sha256(f.read_bytes()).hexdigest(),alphaBounds=im.getchannel('A').point(lambda a:255 if a>=128 else 0).getbbox()))
board.convert('RGB').save(out/'master-normal-carry-comparison.png')
(out/'inputs.json').write_text(json.dumps(dict(sources=rows,scope='Fixed coordinates and nearest enlargement; anatomy guides are shared image rows, not measured anatomical joint landmarks. No pose normalization, warping or grading.'),indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(comparedPoses=len(items),canvas=list(board.size))))
