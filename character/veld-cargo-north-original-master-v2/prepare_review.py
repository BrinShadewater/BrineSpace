from pathlib import Path
import json,math
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];B=R/'character/veld-idle-north-original-master-v1';O=R/'output/veld-cargo-north-original-master-v2'
s=(B/'review_native.py').read_text().replace('veld-idle-north-original-master-v1','veld-cargo-north-original-master-v2').replace('282','172').replace('12 chronological boards','6 chronological boards').replace("['unload-north', 'pickup-north', 'carry-start-north', 'carry-stop-north', 'carry-north', 'idle-north']","['unload-north','pickup-north','idle-north']")
(P/'review_native.py').write_text(s);exec(compile(s,str(P/'review_native.py'),'exec'),{'__file__':str(P/'review_native.py')})
records=json.loads((O/'records.json').read_text());overviews=[]
for gear in ['bare','helmet']:
    selected=[];seen=set()
    for rec in records:
        key=(rec['action'],rec['sourceIndex'])
        if rec['gear']==gear and key not in seen:selected.append(rec);seen.add(key)
    board=Image.new('RGB',(1280,260*math.ceil(len(selected)/4)),'#202a30');d=ImageDraw.Draw(board)
    for i,rec in enumerate(selected):
        x=i%4*320;y=i//4*260;d.text((x+4,y+4),rec['action']+' '+str(rec['sourceIndex']),fill='white')
        native=Image.open(O/(rec['name']+'-native.png')).convert('RGB');source=Image.open(O/(rec['name']+'-source.png')).convert('RGBA').resize((96,96),Image.Resampling.LANCZOS)
        board.paste(source,(x+110,y+18),source);board.paste(native.crop((0,455,320,585)),(x,y+120))
    name=gear+'-north-all-source-native.png';board.save(P/name);overviews.append({'board':name,'stateSourcePoses':len(selected),'records':[s['name'] for s in selected]})
(P/'overview-review.json').write_text(json.dumps({'boards':overviews,'visualReview':'pending'},indent=2)+'\n')
clips={g:{s['id']:{'frames':['/'+ref[6:] for ref in s['frameFiles']],'durations':s['frameDurationsMs']} for s in json.loads((P/f'{g}-manifest.json').read_text())['states']} for g in ['bare','helmet']}
html=(B/'index.html').read_text();start=html.index('const clips=');end=html.index(',action=document',start);html=html[:start]+'const clips='+json.dumps(clips)+html[end:]
html=html.replace('Veld North original master idle','Veld North original cargo repair').replace('Veld North - original master idle','Veld North - original cargo repair')
html=html.replace('Quiet North breathing follows the prepared original rear master, with planted boots and a fixed shared helmet. Pickup and unload share its exact resting endpoint. Broader body grading and gameplay transitions remain in progress.','Whole-source North cargo repair restores quilt detail and wider standing legs against the original master. Shared helmet and exact resting endpoint retained. Suit shading and older held/gait/turn joins still need refinement; staged only.')
html=html.replace('<option value="carry-start-north">Carry Start North</option><option value="carry-stop-north">Carry Stop North</option><option value="carry-north">Carry North</option>','').replace('paired-original-idle.png','paired-unload.png')
for gear in ['Bare','Helmet']:
    for action in ['carry-start-north','carry-stop-north','carry-north']:
        html=html.replace(f'<h3>{gear} {action}</h3><img src="{gear.lower()}-{action}-native-review.apng">','')
(P/'index.html').write_text(html)
(P/'PROMPTS.md').write_text('# Exact built-in image generation prompts\n\n'+''.join('\n## '+f.name+'\n\n'+f.read_text() for f in sorted(P.glob('prompt-unload-*.txt'))))
(P/'EXECUTIONS.json').write_text(json.dumps({'tool':'built-in image_gen','executions':{'v1':'fa799a72-c7c2-472f-8870-79818ee11453','v2':'aa005083-e5f7-49b7-b545-76912ebcfb2d','v3':'5de5480b-aded-47f1-9616-14ce202626d4','v4':'5d301d42-cd54-491d-83e0-70104e7f8590'},'selection':'v4 whole-source candidate; remaining grade/joins unaccepted','rejections':{'v1':'Narrow legs/smooth dark suit remain','v2':'Heads24–25 rather than22; standing overshoot1–2px','v3':'Head correction overshot to19px; detached debris'},'references':['character/veld-cargo-north-master-family-v1/raw-unload-v1.png','character/veld-idle-north-original-master-v1/raw-clean-master-v1.png']},indent=2)+'\n')
print('Two all-pose native overviews /32 distinct poses, six source controls, exact prompts saved.')
