from pathlib import Path
import json,math
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-cardinal-actions-shared-original-helmet-v1'
records=json.loads((O/'records.json').read_text());actions=list(dict.fromkeys(r['action'] for r in records))
s=(R/'character/veld-south-shared-original-helmet-v1/review_native.py').read_text()
s=s.replace('output/veld-south-shared-original-helmet-v2','output/veld-cardinal-actions-shared-original-helmet-v1').replace('282','558')
s=s.replace("['unload-south','pickup-south','carry-south','carry-start-south','carry-stop-south','idle-south']",repr(actions)).replace('12 chronological boards','30 chronological boards').replace('Standalone South shared helmet on original-master bodies','Standalone N/E/W shared helmet action families')
(P/'review_native.py').write_text(s)
overview=[]
for gear in ['bare','helmet']:
    for direction in ['north','east','west']:
        selected=[]
        for action in [a for a in actions if a.endswith('-'+direction)]:
            seen=set()
            for row in records:
                if row['gear']==gear and row['action']==action and row['sourceIndex'] not in seen:
                    seen.add(row['sourceIndex']);selected.append(row)
        board=Image.new('RGB',(1280,240*math.ceil(len(selected)/4)),'#202a30');draw=ImageDraw.Draw(board)
        for i,row in enumerate(selected):
            x=i%4*320;y=i//4*240
            native=Image.open(O/(row['name']+'-native.png')).convert('RGB');source=Image.open(O/(row['name']+'-source.png')).convert('RGBA').resize((96,96),Image.Resampling.LANCZOS)
            draw.text((x+4,y+3),row['action']+' '+str(row['sourceIndex']),fill='white');board.paste(source,(x+110,y+16),source)
            board.paste(native.crop((0,455,140,585)),(x,y+110));board.paste(native.crop((160,455,340,585)),(x+140,y+110))
        name=gear+'-'+direction+'-all-source-native.png';board.save(P/name);overview.append({'board':name,'stateSourcePoses':len(selected),'records':[r['name'] for r in selected]})
(P/'overview-review.json').write_text(json.dumps({'scope':'Each distinct state source slot, actual native47/93 candidates plus source thumbnail; repeated chronological samples remain separately recorded.', 'boards':overview,'visualReview':'pending'},indent=2)+'\n')
clips={}
for gear in ['bare','helmet']:
    data=json.loads((P/f'{gear}-manifest.json').read_text());clips[gear]={s['id']:{'frames':['/'+f[6:] for f in s['frameFiles']],'durations':s['frameDurationsMs']} for s in data['states']}
page=(R/'character/veld-south-shared-original-helmet-v1/index.html').read_text()
a=page.index('const clips=');b=page.index(',action=document',a);page=page[:a]+'const clips='+json.dumps(clips)+page[b:]
page=page.replace('Veld South shared original helmet','Veld cardinal shared original helmet').replace('Veld South - shared original helmet','Veld North, East and West - shared original helmet')
page=page.replace('South idle, pickup, unload, carrying and start/stop now share the whole original-master helmet used in the turns. Existing corrected body colours and exact action joins are preserved. Other directions, turn body grading and gameplay integration remain in progress.','North, East and West pickup, unload, carrying and start/stop share the original-master turn helmets. Held-case and turn endpoints match exactly. Whole bodies and action clocks are preserved. Master grading, full idle and gameplay integration remain in progress.')
a=page.index('<select id="action">');b=page.index('</select>',a);page=page[:a]+'<select id="action">'+''.join(f'<option value="{k}">{k.replace("-"," ").title()}</option>' for k in clips['helmet'])+page[b:]
page=page.replace('Carry and idle loop in the engine','Carry loops in the engine').replace('unload-south-comparison.png','unload-west-comparison.png')
a=page.index('<h2>Engine comparisons</h2>');b=page.index('<script>',a);gallery='<h2>Engine comparisons</h2><p>Every distinct source pose, at two native sizes, with source thumbnails. Complete recorded previews follow.</p>'
for entry in overview:
    label=' '.join(entry['board'].split('-')[:2]).title()
    gallery+=f'<h3>{label}</h3><img src="{entry["board"]}">'
for gear in clips:
    for action in clips[gear]:gallery+=f'<h3>{gear.title()} {action}</h3><img src="{gear}-{action}-native-review.apng">'
page=page[:a]+gallery+page[b:];(P/'index.html').write_text(page)
print(f'Six overviews cover {sum(r["stateSourcePoses"] for r in overview)} state-source poses.')
