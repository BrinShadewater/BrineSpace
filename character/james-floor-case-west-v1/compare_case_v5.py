from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent;r=p.parents[1]
reference=json.loads((p/'reference-evidence.json').read_bytes())
assert hashlib.sha256((r/reference['source']).read_bytes()).hexdigest()==reference['sha256']
original=Image.open(r/reference['source']).convert('RGBA')
idle=Image.open(p/'arrival-captures/bare-release-idle-source.png').convert('RGBA')
assert idle.size==(184,184)
board=Image.new('RGB',(1536,760),'#303b40');draw=ImageDraw.Draw(board)
for index,(label,path) in enumerate([('original terminal / boot occludes right edge',None),('previous separate case v3','floor-case-west.png'),('revised separate case v5','floor-case-west-v5.png')]):
    composite=original if path is None else Image.open(p/path).convert('RGBA')
    if path is not None:composite.alpha_composite(idle,(36,52))
    x=index*512;draw.text((x+8,6),label,fill='white')
    enlarged=composite.resize((512,512),Image.Resampling.NEAREST)
    board.paste(enlarged,(x,28),enlarged)
    detail=composite.crop((73,193,124,225)).resize((306,192),Image.Resampling.NEAREST)
    board.paste(detail,(x+103,558),detail)
    draw.text((x+8,540),'registered source composite / enlarged case contact',fill='#b9c2c3')
board.save(p/'case-v5-comparison.png')
print('Original/v3/v5 registered presentation saved;reference hash unchanged. No source retouch.')
