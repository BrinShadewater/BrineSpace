from pathlib import Path
from PIL import Image,ImageDraw
import json
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'late-thigh-audit-v278';out.mkdir(exist_ok=True);j=json.loads((p/'material-repair-progress.json').read_bytes());board=Image.new('RGBA',(1440,960),(47,59,63,255));draw=ImageDraw.Draw(board)
for i,phase in enumerate([41,42,43,44,45,46]):
 im=Image.open(r/j['states'][phase]['candidateSources']['bare']['file']).convert('RGBA').crop((104,136,168,200)).resize((384,384),Image.Resampling.NEAREST);x=(i%3)*480;y=(i//3)*480;board.alpha_composite(im,(x+36,y+32));draw.text((x+36,y+5),f'Original phase{phase}; x104..167 y136..199',fill='white')
 for n in range(0,64,8):
  xx=x+36+n*6;yy=y+32+n*6;draw.line((xx,y+32,xx,y+416),fill=(115,150,150,110));draw.line((x+36,yy,x+420,yy),fill=(115,150,150,110));draw.text((xx,y+420),str(104+n),fill='white');draw.text((x+4,yy),str(136+n),fill='white')
board.save(out/'coordinate-source-review.png');print('Six original return-leg crops prepared with native coordinates for component review.')
