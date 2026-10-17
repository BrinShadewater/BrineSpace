from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
P=Path(__file__).resolve().parent;R=P.parents[1]
font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),20)
states={}
for bank in ['krusher-james-canonical-v8','krusher-james-canonical-v9']:
    root=R/'character'/bank;m=json.loads((root/'bare-manifest.json').read_text())
    for s in m['states']:
        if s['id'].startswith('walk-'):states[bank,s['id']]=(s,[Image.open(root/f).convert('RGBA') for f in s['frameFiles']])
frames=[]
for step in range(90):
    board=Image.new('RGBA',(900,580),'#252b2e');draw=ImageDraw.Draw(board)
    for row,bank in enumerate(['krusher-james-canonical-v8','krusher-james-canonical-v9']):
        draw.text((12,row*290+5),'BEFORE' if row==0 else 'UPDATED / COLLAR-REGISTERED NECK',font=font,fill='white')
        for col,d in enumerate(['south','east','north','west']):
            state,imgs=states[bank,'walk-'+d];clock=step*50%sum(state['frameDurationsMs']);index=0
            while index<len(imgs)-1 and clock>=state['frameDurationsMs'][index]:clock-=state['frameDurationsMs'][index];index+=1
            crop=imgs[index].crop((63,14,119,69)).resize((224,220),Image.Resampling.NEAREST);x=col*225;y=row*290+35
            board.alpha_composite(crop,(x,y));draw.text((x+10,y+224),d.upper(),font=font,fill='#bfd2d4')
    frames.append(board.convert('RGB'))
frames[0].save(P/'bare-connection-review.gif',save_all=True,append_images=frames[1:],duration=50,loop=0,disposal=2,optimize=True)
for index in [0,30,60]:frames[index].save(P/f'bare-connection-phase-{index:02d}.png')
print('90 exact-clock comparison samples at 4x nearest; 4.5 seconds, four bare walk facings.')
