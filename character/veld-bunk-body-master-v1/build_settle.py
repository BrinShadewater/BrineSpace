from pathlib import Path
import json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent
for gear in ['bare','helmet']:
    path=P/f'{gear}-manifest.json';data=json.loads(path.read_text())
    data['supportedBunkDeathMode']='settle-v1'
    source=next(s for s in data['states'] if s['id']=='bunk-enter-east')
    death=next(s for s in data['states'] if s['id']=='death-bunk-east')
    row={'id':'death-bunk-settle-east','frameFiles':source['frameFiles'][2:]+death['frameFiles'][1:],'frameDurationsMs':source['frameDurationsMs'][2:]+death['frameDurationsMs'][1:],'loop':False,'furnitureFrames':source['furnitureFrames'][2:]+death['furnitureFrames'][1:],'depthOffsets':source['depthOffsets'][2:]+death['depthOffsets'][1:]}
    data['states']=[s for s in data['states'] if s['id']!=row['id']]+[row]
    path.write_text(json.dumps(data,indent=2)+'\n')
    board=Image.new('RGB',(7*256,300),'#202a30');draw=ImageDraw.Draw(board)
    for i,relative in enumerate(row['frameFiles']):
        im=Image.open(P.parents[1]/relative.removeprefix('res://')).convert('RGBA');board.paste(im,(i*256,20),im);draw.text((i*256+8,4),f'{gear}: settle {i}',fill='white')
    board.save(P/f'settle-source-{gear}.png')
print('Paired finite settling rows reuse five exact descent poses and two relaxed terminal poses; no new or modified PNGs')
