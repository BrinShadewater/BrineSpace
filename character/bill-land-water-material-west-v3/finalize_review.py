from pathlib import Path
from PIL import Image, ImageDraw
import json, hashlib, shutil
P=Path(__file__).resolve().parent;R=P.parent.parent;O=R/'output/bill-land-water-material-west-v3'
e=json.loads((P/'review.json').read_text(encoding='utf-8'));assert e['validation']['passed'] and not e['validation']['realProfileChanges']
data=json.loads((O/'records.json').read_text(encoding='utf-8'));guards=[x for x in data['records'] if '-guard-' in x['name']];assert len(guards)==28
board=Image.new('RGB',(1400,1700),'#182932');d=ImageDraw.Draw(board);hashes={};inventory=json.loads((P/'source-inventory.json').read_text(encoding='utf-8'));guard_sources={}
for line,(gear,phase) in enumerate([('bare','entry'),('helmet','entry'),('bare','exit'),('helmet','exit')]):
    group=[x for x in guards if x['name'].startswith(gear+'-'+phase+'-')];assert len(group)==7
    for col,row in enumerate(group):
        name=row['name'];x=255+(row['foot'][0]-7680)*398/384;y=287+(row['foot'][1]-8064)*398/384
        for kind in ['source','room']:
            f=O/f'{name}-{kind}.png';shutil.copy2(f,P/'captures'/f.name);hashes[f.name]=hashlib.sha256(f.read_bytes()).hexdigest()
        room=Image.open(P/'captures'/f'{name}-room.png').crop((round(x)-100,round(y)-130,round(x)+100,round(y)+70));board.paste(room,(col*200,line*425+20))
        source=Image.open(P/'captures'/f'{name}-source.png').convert('RGBA');key=hashlib.sha256(source.tobytes()).hexdigest();assert key in inventory,(name,key)
        guard_sources[name]=inventory[key]
        source.thumbnail((180,180),Image.Resampling.LANCZOS);board.paste(source,(col*200+(200-source.width)//2,line*425+230),source)
        d.text((col*200+3,line*425+3),f"{gear} {phase} {name.split('-guard-')[1].split('-candidate')[0]}",fill='white');d.text((col*200+3,line*425+410),f"material {row['materialWeight']:.3f}; raw source",fill='white')
board.save(P/'native-guards.png')
before=json.loads((P/'targeted-inputs.json').read_text(encoding='utf-8'));post={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in before}
changes=[f for f in before if before[f]!=post[f]];assert not changes,changes
e.update(nativeGuardPresentations=guards,nativeGuardCaptureSHA256=hashes,nativeGuardSourceRegistration=guard_sources,targetedPostSHA256=post,targetedChanges=changes,frozenInputCount=len(before),visualReview='Pending review of four advancing boards and28guard pairs. Full motion/master consistency and physical contact remain separate; no checkpoint/Continue or normal admission.')
(P/'review.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
html=(P/'index.html').read_text(encoding='utf-8')
if 'native-guards.png' not in html:html+='<h2>Entry and exit interruption captures</h2><p>Synthetic active/takeover snapshots. Natural priority/death completion remains pending.</p><img src="native-guards.png">'
(P/'index.html').write_text(html,encoding='utf-8')
print(json.dumps(dict(guardPairs=len(guards),guardSourcesRGBAExact=len(guard_sources),frozenInputsStable=len(before),targetedChanges=changes)))
