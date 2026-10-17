from pathlib import Path
import json,math,sys
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
O=R/'output'/sys.argv[1];D=P/(sys.argv[1]+'-review');D.mkdir(exist_ok=True)
j=json.loads((O/'journeys.json').read_text());summaries=[]
for x in j['journeys']:
    tag=('staged' if x['candidate'] else 'normal')+('-helmet' if x['helmet'] else '-bare')
    records=x['records'];turns=[];group=[]
    for r in records+[{'motion':{},'key':''}]:
        clip=r['key'] if r['key'].startswith('carry-turn-') else ''
        if group and clip!=group[-1]['key']:
            a,b=group[0],group[-1]
            turns.append({'clip':a['key'],'firstStep':a['step'],'lastStep':b['step'],'tickCount':len(group),'travelWorldUnits':math.dist(a['foot'],b['foot']),'foot':a['foot']});group=[]
        if clip:group.append(r)
    captured=[r for r in records if 'capture' in r];first={}
    for r in captured:first.setdefault((r['stage'],r['key'],r['slot']),r)
    rows=list(first.values());pages=[]
    if x['candidate']:
        for page in range(math.ceil(len(rows)/18)):
            selection=rows[page*18:page*18+18]
            board=Image.new('RGB',(1260,60+330*math.ceil(len(selection)/3)),'#202a30');d=ImageDraw.Draw(board)
            d.text((12,12),tag+f' / page {page+1}: first occurrence of each actual displayed state/slot',fill='white')
            d.text((12,32),'Left source at master ruler; right native room crop. Simulation held at each captured pose; not continuous video.',fill='#bccbd0')
            for n,r in enumerate(selection):
                bx=(n%3)*420;by=60+(n//3)*330
                d.text((bx+5,by+5),f"{r['step']} {r['key']} / {r['slot']}",fill='white')
                d.text((bx+5,by+24),r['stage'],fill='#bccbd0')
                src=Image.open(O/(r['capture']+'-source.png')).convert('RGBA')
                if src.size==(92,92):src=src.resize((184,184),Image.Resampling.NEAREST)
                board.paste(src,(bx+5,by+50),src)
                native=Image.open(O/(r['capture']+'-native.png')).convert('RGB').crop((250,220,655,695));native.thumbnail((150,230),Image.Resampling.LANCZOS)
                board.paste(native,(bx+265,by+50))
            name=tag+f'-{page+1}.png';board.save(D/name);pages.append(name)
    summaries.append({'tag':tag,'ticks':len(records),'nativeCaptureCount':len(captured),'uniqueCapturedRows':len(rows),'reviewPages':pages,'turns':turns,'stageBoundaries':[r for i,r in enumerate(records) if i==0 or r['stage']!=records[i-1]['stage']]})
(D/'summary.json').write_text(json.dumps({'scope':j['scope'],'checks':j['checks'],'failures':j['failures'],'journeys':summaries},indent=2)+'\n',encoding='utf-8')
print(json.dumps([{k:s[k] for k in ['tag','ticks','nativeCaptureCount','uniqueCapturedRows','reviewPages','turns']} for s in summaries],indent=2))
