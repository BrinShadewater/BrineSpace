from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[2];O=R/'output/veld-east-original-motion-probe-v2'
records=json.loads((O/'records.json').read_text(encoding='utf-8'))['records']
boards=[]
for trial in range(3):
    # Separate boards by gear; preserve full47/93/148 capture panels.
    for gear in ['bare','helmet']:
        selected=[r for r in records if r['trial']==trial and r['gear']==gear and r['sample'] in [0,8,16,24,32,40]]
        board=Image.new('RGB',(2700,1280),'#202a30')
        for j,r in enumerate(selected):board.paste(Image.open(O/(r['name']+'-native.png')).convert('RGB'),((j%3)*900,(j//3)*640))
        dest=P/f'native-trial{trial}-{gear}-review.png';board.save(dest);boards.append(dest.name)
        timeline=[r for r in records if r['trial']==trial and r['gear']==gear and (O/(r['name']+'-native.png')).exists()]
        frames=[Image.open(O/(r['name']+'-native.png')).convert('RGBA') for r in timeline]
        durations=[max(1,round((timeline[i+1]['time']-row['time'])*1000)) if i+1<len(timeline) else 100 for i,row in enumerate(timeline)]
        frames[0].save(P/f'native-trial{trial}-{gear}-review.png.apng',save_all=True,append_images=frames[1:],duration=durations,loop=0,disposal=0,blend=0)
        # Exact sparse native review, not an interpolated continuous recording.
traces=[]
for trial in range(3):
    for start,end in [(34,38),(50,54)]:
        rows=[]
        for raw in range(start,end+1):
            slot=raw-32;r=next(r for r in records if r['trial']==trial and r['gear']=='bare' and r['sample']==slot+1)
            a=np.array(Image.open(O/(r['name']+'-source.png')).convert('RGBA'))[:,:,3]>200
            y=int(np.where(a)[0].max());xs=np.where(a[y-3:y+1].any(axis=0))[0]
            toe=int(xs.max());travel_pixels=r['travelWorld']*148/65.28
            rows.append({'rawFrame':raw,'slot':slot,'toeOutlineX':toe,'floor':y,'rootTravelSourcePixels':travel_pixels,'worldToeSourcePixelEquivalent':toe+travel_pixels})
        values=[r['worldToeSourcePixelEquivalent'] for r in rows]
        traces.append({'trial':trial,'rawFrames':[start,end],'toeOutlineDriftSourcePixels':max(values)-min(values),'toeOutlineDriftAt93px':(max(values)-min(values))*93/148,'rows':rows})
report={'boards':boards,'supportTraces':traces,'scope':'Native actual-distance stride sweep and sparse capture playback. Toe outline in visually inspected early flat-support windows only; outline is a diagnostic proxy, not rigid material landmark tracking. Contact/stride acceptance unresolved; no source or player edits.'}
(P/'native-motion-review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'boards':boards,'supportDrift':[ {k:v for k,v in t.items() if k!='rows'} for t in traces]}))
