from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'late-thigh-audit-v278';out.mkdir(exist_ok=True);j=json.loads((p/'material-repair-progress.json').read_bytes());board=Image.new('RGBA',(1152,1152),(47,59,63,255));draw=ImageDraw.Draw(board);inputs=[]
for i,phase in enumerate(range(31,47)):
 f=r/j['states'][phase]['candidateSources']['bare']['file'];im=Image.open(f).convert('RGBA').crop((100,128,172,200)).resize((256,256),Image.Resampling.NEAREST);x=(i%4)*288;y=(i//4)*288;board.alpha_composite(im,(x,y+23));draw.text((x+5,y+4),f'phase{phase}',fill='white');inputs.append(dict(phase=phase,file=f.relative_to(r).as_posix(),sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
board.save(out/'late-thigh-source-review.png');(out/'inputs.json').write_text(json.dumps(dict(sources=inputs,cropBox=[100,128,172,200],normalChanged=False),indent=2)+'\n',encoding='utf-8');print('Sixteen late near/far thigh regions prepared from current selected sources, frozen hashes retained.')
