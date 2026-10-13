"""Static same-physical-scale review of staged walking against selected activities."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
R=Path(__file__).resolve().parents[1];D=R/'character/bill-east-walk-joins-v1/context-review-v1';D.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
A=R/'character/bill-east-interact-master-consistency-v1/native/corrected-source-audit.json';audit=json.loads(A.read_text(encoding='utf-8'))
bindings={**audit['manifestBindings'],**audit['candidateClosureBindings']}
assert all(sha(R/p)==s for p,s in bindings.items())
historic=json.loads((R/'character/bill-full-family-consistency-2026-10-03-v1/review.json').read_text(encoding='utf-8'))
block=(R/'scripts/grid_canvas.gd').read_text(encoding='utf-8').split('func _load_major_bill_animations()',1)[1].split('\nfunc ',1)[0]
assert hashlib.sha256(block.encode()).hexdigest()==historic['loaderBlockSha256']
tiles=[];records=[];inputs={}
def add(label,path,pivot,height,slot):
 im=Image.open(path).convert('RGBA');inputs[path.relative_to(R).as_posix()]=sha(path)
 scale=148/height
 if scale!=1:im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
 out=Image.new('RGBA',(320,300));out.alpha_composite(im,(round(160-pivot[0]*scale),round(224-pivot[1]*scale)))
 tiles.append((label,out));records.append(dict(label=label,file=path.relative_to(R).as_posix(),pivot=pivot,standingHeight=height,slot=slot))
for label,folder,key,slot in [('Current master idle','bill-east-idle-master-motion-v1','idle-east',0),('Current walk 012','bill-east-walk-master-full-v1','walk-east',12),('Whole settle 012','bill-east-walk-joins-v1','walk-settle-012-east',0),('Current reach peak','bill-east-reach-adjacent-motion-v2','interact-east',3)]:
 p=R/'character'/folder/'manifest.json';m=json.loads(p.read_text(encoding='utf-8'));inputs[p.relative_to(R).as_posix()]=sha(p);s=next(s for s in m['states'] if s['id']==key)
 add(label,R/s['frameFiles'][slot].removeprefix('res://'),m['pivot'],m['standingHeight'],slot)
for key in ['run-east','carry-east','weld-east']:
 s=audit['selected']['bare'][key]
 for slot in [0,len(s['files'])//2]:add(f'Selected {key} / {slot}',R/s['files'][slot],s['pivot'],s['standingHeight'],slot)
board=Image.new('RGBA',(1280,990),(23,37,45,255));draw=ImageDraw.Draw(board)
for n,(label,im) in enumerate(tiles):
 x=n%4*320;y=n//4*330;draw.text((x+10,y+10),label,fill='white');board.alpha_composite(im,(x,y+30));draw.line((x+70,y+254,x+250,y+254),fill=(90,145,155))
board.save(D/'family-comparison.png')
report=dict(scope='Ten full source samples at common H148 and foot pivot160224. Two samples each selected run/carry/weld; not full-sequence acceptance. Whole uniform registration only; no fitting/recoloring.',samples=records,inputs=inputs,bindings=bindings,loaderBlockSha256=hashlib.sha256(block.encode()).hexdigest(),visualReviewed=False,normalAdmission=False)
(D/'family-review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('Ten same-scale source samples saved; current selected closure bindings and loader unchanged.')
