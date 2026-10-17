"""Equal-pivot east/west comparison; no mirroring, retinting or pose normalization."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];bound={}
board=Image.new('RGBA',(1536,1024),'#202a30');draw=ImageDraw.Draw(board)
for row,(direction,gear) in enumerate([('east','bare'),('west','bare'),('east','helmet'),('west','helmet')]):
 folder=R/f'character/veld-death-water-tread-{direction}-coherent-v1';m=json.loads((folder/f'{gear}-manifest.json').read_text(encoding='utf-8'))
 assert m['pivot']==[128,128] and m['standingHeight']==148
 for i,name in enumerate(m['states'][0]['frameFiles']):
  f=folder/name;board.alpha_composite(Image.open(f).convert('RGBA'),(i*256,row*256));draw.text((i*256+4,row*256+4),f'{direction}/{gear}/{i}',fill='white');bound[f.relative_to(R).as_posix()]=hashlib.sha256(f.read_bytes()).hexdigest()
board.save(P/'east-west-comparison.png');board.resize((852,568),Image.Resampling.LANCZOS).save(P/'east-west-station-comparison.png')
(P/'cross-review-bindings.json').write_text(json.dumps({'frames':bound,'scope':'equal pivot/H148 physical ruler comparison; independent camera and source phase/pitch remain for motion review'},indent=2)+'\n',encoding='utf-8')
print('Built source-bound east/west cross-family comparison at shared pivot and scale')
