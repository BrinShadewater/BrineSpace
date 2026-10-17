from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,re,base64
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'full-gait-review-v280';board=Image.new('RGBA',(1120,1372),(47,59,63,255));draw=ImageDraw.Draw(board);m=json.loads((out/'bare-manifest.json').read_bytes())
for i,f in enumerate(m['states'][0]['frameFiles']):
 im=Image.open(r/f.removeprefix('res://')).convert('RGBA').crop((100,136,172,208)).resize((160,160),Image.Resampling.NEAREST);x=(i%7)*160;y=(i//7)*196;board.alpha_composite(im,(x,y+23));draw.text((x+4,y+4),f'phase{i}',fill='white')
board.save(out/'all-thigh-review.png')
html=(out/'playback-review.html').read_text(encoding='utf-8');match=re.search(r'const sources=(.*),durations=',html);data=json.loads(match.group(1));verified=0
for gear in ['bare','helmet']:
 manifest=json.loads((out/f'{gear}-manifest.json').read_bytes())
 for url,f in zip(data[gear],manifest['states'][0]['frameFiles']):assert base64.b64decode(url.split(',',1)[1])==(r/f.removeprefix('res://')).read_bytes();verified+=1
(out/'playback-source-verification.json').write_text(json.dumps(dict(verifiedEmbeddedSources=verified,exactToFrozenManifests=True,cycleMs=1680,continuousVisualAcceptance=False),indent=2)+'\n',encoding='utf-8');print(f'{verified} HTML sources exact to frozen manifests; all49 thigh board prepared.')
