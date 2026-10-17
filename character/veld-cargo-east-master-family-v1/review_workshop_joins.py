"""Build review boards from recorded production-stage boundaries, without changing sources."""
from pathlib import Path
import json
from PIL import Image, ImageDraw
R=Path(__file__).resolve().parents[2]
O=R/'output/veld-workshop-source-joins-v2'
P=Path(__file__).resolve().parent/'workshop-join-review-v1'
P.mkdir(exist_ok=True)
data=json.loads((O/'journeys.json').read_text())
summaries=[]
for j in data['journeys']:
    records=j['records'];tag=('staged' if j['candidate'] else 'normal')+('-helmet' if j['helmet'] else '-bare')
    captured=[r for r in records if 'capture' in r]
    picks=[]
    for stage in ['workshop_pickup','workshop_carry','workshop_unload']:
        rows=[r for r in captured if r['stage']==stage]
        if rows:
            picks.extend([rows[0],rows[-1]])
    picks.append(captured[-1]);picks=list({r['step']:r for r in picks}.values())
    board=Image.new('RGB',(880,310*len(picks)+60),'#202a30');d=ImageDraw.Draw(board)
    d.text((14,10),tag+' / actual production stage boundaries',fill='white')
    d.text((14,30),'Left: displayed source; right: native workshop crop. Prescribed service entry; stages untouched.',fill='white')
    for i,r in enumerate(picks):
        y=60+i*310
        source=Image.open(O/(r['capture']+'-source.png')).convert('RGBA')
        # Common physical master ruler, never fit each pose to its bounds.
        scale=2.0 if source.size==(92,92) else 1.0
        source=source.resize((round(source.width*scale),round(source.height*scale)),Image.Resampling.NEAREST)
        board.paste(source,(80,y+55),source)
        native=Image.open(O/(r['capture']+'-native.png')).convert('RGB')
        crop=native.crop((250,220,655,695));crop.thumbnail((400,210),Image.Resampling.LANCZOS)
        board.paste(crop,(460,y+25))
        d.text((12,y+5),f"step {r['step']} / {r['stage']} / {r['key']} / slot {r['slot']}",fill='white')
        d.text((12,y+25),f"action elapsed {r['actionElapsed']:.3f}s / timer {r['timer']:.3f}s",fill='#bccbd0')
    board.save(P/(tag+'.png'))
    stages=[]
    for r in records:
        if not stages or stages[-1]['stage']!=r['stage']:
            stages.append({'stage':r['stage'],'key':r['key'],'step':r['step'],'foot':r['foot'],'elapsed':r['actionElapsed']})
    summaries.append({'tag':tag,'stationFacing':j['stationFacing'],'stageBoundaries':stages,'boundaryCaptures':picks,'simulationTicks':len(records),'nativeCaptureCount':len(captured)})
(P/'summary.json').write_text(json.dumps({'checks':data['checks'],'failures':data['failures'],'scope':data['scope'],'journeys':summaries},indent=2)+'\n',encoding='utf-8')
print(json.dumps([{'tag':j['tag'],'stages':j['stageBoundaries'],'captures':j['nativeCaptureCount']} for j in summaries],indent=2))
