"""Compare current staged idle/reach with unchanged full-closure selected sources."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
R=Path(__file__).resolve().parents[1];P=R/'character/bill-east-reach-adjacent-motion-v2';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
audit_path=R/'character/bill-east-interact-master-consistency-v1/native/corrected-source-audit.json';audit=json.loads(audit_path.read_text(encoding='utf-8'))
historic=json.loads((R/'character/bill-full-family-consistency-2026-10-03-v1/review.json').read_text(encoding='utf-8'))
block=(R/'scripts/grid_canvas.gd').read_text(encoding='utf-8').split('func _load_major_bill_animations()',1)[1].split('\nfunc ',1)[0]
assert hashlib.sha256(block.encode()).hexdigest()==historic['loaderBlockSha256']
assert sha(R/'character/major-bill-v3/catalog.json')==audit['catalogSha256']
bindings={**audit['manifestBindings'],**audit['candidateClosureBindings']};assert all(sha(R/path)==digest for path,digest in bindings.items())
inputs={};records=[]
def read(path):
 inputs[path.relative_to(R).as_posix()]=sha(path);return Image.open(path).convert('RGBA')
def register(im,pivot,height):
 scale=148/height
 if scale!=1:im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
 out=Image.new('RGBA',(320,320));out.alpha_composite(im,(round(160-pivot[0]*scale),round(224-pivot[1]*scale)));return out
master_path=R/'character/bill-east-idle-interact-joined-v1/head-consistency-pilot-v3/original-master.png'
master=read(master_path).resize((352,352),Image.Resampling.LANCZOS).crop((68,52,252,236))
tiles=[('Original master reference',register(master,[92,172],148))]
for label,key,slot in [('Staged idle','idle-east',0),('Staged reach peak','interact-east',3)]:
 manifest=json.loads((P/'manifest.json').read_text(encoding='utf-8'));s=next(s for s in manifest['states'] if s['id']==key);path=R/s['frameFiles'][slot].removeprefix('res://');tiles.append((label,register(read(path),manifest['pivot'],manifest['standingHeight'])))
for key in ['idle-east','walk-east','run-east','carry-east','weld-east']:
 state=audit['selected']['bare'][key];slot=0 if key=='idle-east' else len(state['files'])//2;path=R/state['files'][slot]
 tiles.append((f'Selected {key} [{slot}]',register(read(path),state['pivot'],state['standingHeight'])));records.append(dict(key=key,slot=slot,source=path.relative_to(R).as_posix(),manifest=state['manifest'],pivot=state['pivot'],standingHeight=state['standingHeight'],precomposed=state['precomposed']))
board=Image.new('RGBA',(1280,1000),(23,37,45,255));draw=ImageDraw.Draw(board)
for n,(label,im) in enumerate(tiles):
 x=n%4*320;y=n//4*500;draw.text((x+8,y+8),label,fill='white');board.alpha_composite(im,(x,y+28));draw.line((x+70,y+252,x+250,y+252),fill=(90,145,155));head=im.crop((125,55,195,125)).resize((140,140),Image.Resampling.NEAREST);board.alpha_composite(head,(x+90,y+350))
board.save(P/'master-cross-family.png')
report=dict(status='pending_visual_review',scope='Eight representative source figures at declared common H148/p160224; original master reference and staged idle/reach versus full-closure selected context. No per-pose fitting/recoloring. Fixed head window may omit low poses; whole figures authoritative. Static representative samples do not certify full sequences/equipment or native context actions.',inputs=inputs,selectionBindings=bindings,loaderBlockSha256=hashlib.sha256(block.encode()).hexdigest(),auditSha256=sha(audit_path),samples=records,normalAdmission=False,visualReviewed=False)
(P/'master-cross-family.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print('Eight full figures; full literal/closure binding hashes and loader block exact; current carry-east gait-v3 context.')
