from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'thigh-audit-v253';out.mkdir(exist_ok=True);ledger=json.loads((p/'material-repair-progress.json').read_bytes())
board=Image.new('RGBA',(1120,1260),(47,58,63,255));draw=ImageDraw.Draw(board);sources=[]
for i in range(49):
 f=r/ledger['states'][i]['candidateSources']['bare']['file'];im=Image.open(f).convert('RGBA');x=(i%7)*160;y=(i//7)*180;draw.text((x+4,y+4),f'phase{i}',fill='white');board.alpha_composite(im.crop((104,136,144,176)).resize((160,160),Image.Resampling.NEAREST),(x,y+20));sources.append(dict(phase=i,file=f.relative_to(r).as_posix(),sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
board.convert('RGB').save(out/'all-selected-thighs.png')
(out/'inputs.json').write_text(json.dumps(dict(sources=sources,cropBox=[104,136,144,176],scope='Current selected49 same-coordinate thigh crops, nearest4x. Some walking thighs leave this fixed crop; absence of seam here does not prove missing seam on whole leg.'),indent=2)+'\n',encoding='utf-8')
print('Prepared current49 selected thigh construction audit.')
