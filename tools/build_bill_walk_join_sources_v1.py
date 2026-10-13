"""Whole uniform packing/sole registration and honest source comparison."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[1];D=R/'character/bill-east-walk-joins-v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
receipts=json.loads((D/'receipts.json').read_text(encoding='utf-8'));inputs={};records=[];F=D/'frames';F.mkdir(exist_ok=False)
idle_path=R/'character/bill-east-idle-master-motion-v1/frames/idle-east/000.png';idle=Image.new('RGBA',(256,256));idle.alpha_composite(Image.open(idle_path).convert('RGBA'),(36,52));idle.save(F/'idle.png');inputs[str(idle_path)]=sha(idle_path)
def bounds(a):
 y,x=np.where(a[:,:,3]>127);return [int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
board=Image.new('RGB',(1280,1060),'#17252d');draw=ImageDraw.Draw(board)
for col,receipt in enumerate(receipts):
 slot=receipt['slot'];S=D/f'settle-{slot:03}';raw=S/'raw.png';a=np.asarray(Image.open(raw).convert('RGBA').resize((256,256),Image.Resampling.LANCZOS)).copy();b=bounds(a);dy=224-b[3];packed=np.zeros_like(a)
 if dy>0:assert not a[-dy:,:,3].any();packed[dy:]=a[:-dy]
 elif dy<0:assert not a[:-dy,:,3].any();packed[:dy]=a[-dy:]
 else:packed=a.copy()
 assert np.count_nonzero(a[:,:,3])==np.count_nonzero(packed[:,:,3]);im=Image.fromarray(packed);dst=F/f'settle-{slot:03}.png';im.save(dst)
 refs=json.loads((S/'references.json').read_text(encoding='utf-8'))
 for ref in refs:assert sha(Path(ref['path']))==ref['sha256'] and sha(Path(ref['source']))==ref['sourceSha256']
 for path in [raw,S/'prompt.txt',S/'references.json']:inputs[str(path)]=sha(path)
 prov=dict(receipt,rawSha256=sha(raw),promptSha256=sha(S/'prompt.txt'),references=refs,wholeShiftY=dy,packedSha256=sha(dst));(S/'provenance.json').write_text(json.dumps(prov,indent=2)+'\n',encoding='utf-8')
 old=Image.open(R/f'character/bill-east-walk-master-full-v1/frames/{slot:03}.png').convert('RGBA');bb=bounds(packed);records.append(dict(slot=slot,bounds=bb,height=bb[3]-bb[1],wholeShiftY=dy,frameSha256=sha(dst),rawSha256=sha(raw)))
 for row,(label,img) in enumerate([('Walk source',old),('Whole settling pose',im),('Idle endpoint',idle)]):
  x=col*320;y=row*320;draw.text((x+8,y+8),f'{slot} · {label}',fill='white');q=img.resize((320,320),Image.Resampling.NEAREST);board.paste(q,(x,y+20),q)
 for n,h in enumerate([82,54,27]):
  sc=h/148;q=im.resize((round(256*sc),round(256*sc)),Image.Resampling.LANCZOS);board.paste(q,(round(col*320+50+n*95-128*sc),round(1050-224*sc)),q)
board.save(D/'whole-join-comparison.png')
manifest={'frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'textureFilter':'linear','precomposed':True,'status':'provisional_unselected','states':[{'id':f'walk-settle-{slot:03}-east','frameCount':1,'frameFiles':[f'res://character/bill-east-walk-joins-v1/frames/settle-{slot:03}.png'],'frameDurationsMs':[90],'loop':False} for slot in [0,12,24,36]]}
(D/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
protected=json.loads((R/'character/bill-east-walk-master-full-v1/review.json').read_text(encoding='utf-8'))['inputs'];assert all(sha(Path(p))==h for p,h in protected.items())
(D/'review.json').write_text(json.dumps(dict(records=records,inputs=inputs,sourceWalkInputs=protected,boardSha256=sha(D/'whole-join-comparison.png'),normalAdmission=False,nativeTested=False,visualReviewed=False),indent=2)+'\n',encoding='utf-8')
print(json.dumps(records))
