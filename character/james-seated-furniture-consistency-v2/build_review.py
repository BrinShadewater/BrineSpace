from pathlib import Path
import json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent
e=json.loads((P/'validate-evidence.json').read_text());assert e['failures']==0
for room in ['crew_lounge','observation_room']:
    roi=(330,235,435,390) if room=='crew_lounge' else (630,230,790,390)
    for mode in [0,1]:
        records=[r for r in e['records'] if r['room']==room and r['mode']==mode]
        b=Image.new('RGB',(6*320,3*344),'#202a30');d=ImageDraw.Draw(b);frames=[];durations=[]
        for n,r in enumerate(records):
            im=Image.open(P/'native-rooms'/Path(r['capture']).name).convert('RGB').crop(roi)
            # Integer nearest enlargement only for inspection; full captures retained.
            im=im.resize((im.width*2,im.height*2),Image.Resampling.NEAREST)
            x=n%6*320;y=n//6*344;b.paste(im,(x,y+24));d.text((x+4,y+4),r['key']+' '+str(r['index']),fill='white')
            frames.append(im)
        b.save(P/(room+'-'+str(mode)+'-all-poses.png'))
print('All72 native furniture poses in four complete review boards; no image/art changes.')
