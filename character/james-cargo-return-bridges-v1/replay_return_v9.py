from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent;r=p.parents[1]
data=json.loads((p/'actor-return-v9-evidence.json').read_bytes())
cases=[next(c for c in data['results'] if c.get('mode')==mode and c.get('target')=='workshop_carry' and 'trace' in c) for mode in ['bare','helmet']]
rows=cases[0]['plan']['rows'];assert rows==cases[1]['plan']['rows']
maps=[{(t['key'],t['index']):t for t in c['trace']} for c in cases]
frames=[]
for row in rows:
    frame=Image.new('RGB',(512,286),'#303b40');draw=ImageDraw.Draw(frame)
    for i,mode in enumerate(['bare','helmet']):
        pose=maps[i][row['key'],row['index']]
        source=Image.open(r/pose['source'].removeprefix('res://')).convert('RGBA')
        assert source.size==(256,256)
        frame.paste(source,(i*256,26),source)
        draw.text((i*256+8,8),'James / '+mode,fill='white')
    frames.append(frame)
strip=Image.new('RGB',(512,286*len(frames)))
for i,f in enumerate(frames):strip.paste(f,(0,i*286))
palette=strip.quantize(colors=255)
encoded=[f.quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
durations=[round(float(row['seconds'])*1000) for row in rows]
native_duration=sum(durations);durations[-1]+=700
encoded[0].save(p/'actual-return-v9-source-replay.gif',save_all=True,append_images=encoded[1:],duration=durations,loop=0,disposal=2)
(p/'actual-return-v9-source-replay.json').write_text(json.dumps({'selected':False,'rows':rows,'nativePlanDurationMs':native_duration,'terminalViewerHoldMs':700,'scope':'Exact native captured source Texture drawings reconstructed at their plan durations, common review palette. This is not a continuous native world movie; repeat and terminal hold are viewer behavior, not authored loop. Floor case after idle/departure still unresolved.'},indent=2)+'\n')
print(len(rows),'paired native source slots,',native_duration,'ms source plan plus700ms viewer hold; reconstruction only.')
