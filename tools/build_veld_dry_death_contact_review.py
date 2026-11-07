"""Native screenshot crops only; leave artwork and room pixels intact."""
from pathlib import Path
import json,re
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent.parent;O=R/'output/veld-dry-death-station-candidate-v1'
data=json.loads((O/'contacts.json').read_text());phases=['before-kneel','entry','first-interior','terminal']
for contact in ['counter','aisle']:
    board=Image.new('RGB',(840,8*180),'#202a30');draw=ImageDraw.Draw(board)
    records=[r for r in data['records'] if r['contact']==contact]
    for r in records:
        im=Image.open(O/r['screenshot']).convert('RGB');sx,sy=map(float,re.findall(r'-?\d+(?:\.\d+)?',r['screen']))
        # Renderer records design-space coordinates; actual capture is1280px
        # across the1920px expanded design viewport, uniformly scaled.
        factor=im.width/1920;x,y=sx*factor,sy*factor
        crop=im.crop((round(x-105),round(y-115),round(x+105),round(y+45)))
        row=['east','west','north','south'].index(r['direction'])*2+int(r['helmet']);col=phases.index(r['phase'])
        board.paste(crop,(col*210,row*180+20));draw.text((col*210+3,row*180+3),f"{r['direction']} {'helmet' if r['helmet'] else 'bare'} / {r['phase']}",fill='white')
    board.save(O/f'{contact}-contact-review.png')
print(json.dumps({'nativeCaptures':len(data['records']),'reviewBoards':2,'terminalProjectionOverlaps':sum(bool(r['projectionProxyOverlaps']) for r in data['records'] if r['phase']=='terminal'),'scope':'native screenshot crops, conservative overlap proxy; no physical footprint certification'}))
