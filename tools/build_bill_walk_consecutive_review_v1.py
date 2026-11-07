"""Register whole sequential source trials losslessly; expose failures, never fit."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[1];P=R/'character/bill-east-walk-master-pilot-v1';D=P/'consecutive-review-v1';D.mkdir(exist_ok=False);F=D/'frames';F.mkdir()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def bounds(a):
 y,x=np.where(a[:,:,3]>127);return [int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
records=[];images={};originals={};inputs={}
for slot in range(13):
 oldpath=R/f'character/bill-walk-east-material-v1/frames/bare/walk-east/{slot:03}.png';old=Image.open(oldpath).convert('RGBA');originals[slot]=old;inputs[str(oldpath)]=sha(oldpath);ob=bounds(np.asarray(old))
 if slot in [0,12]:
  src=P/f'keypose-review-v1/frames/{slot:03}.png';im=Image.open(src).convert('RGBA');shift=0;receiptPath=P/f'stride-{slot:03}-v1/provenance.json'
 else:
  S=P/f'sequence-individual-{slot:03}-v1';src=S/f'candidate-{slot:03}.png';assert src.exists(),slot;im=Image.open(src).convert('RGBA');a=np.asarray(im).copy();nb=bounds(a);shift=ob[3]-nb[3]
  dst=np.zeros_like(a)
  if shift>0:
   assert not a[-shift:,:,3].any(),slot;dst[shift:]=a[:-shift];assert np.array_equal(dst[shift:],a[:-shift])
  elif shift<0:
   assert not a[:-shift,:,3].any(),slot;dst[:shift]=a[-shift:];assert np.array_equal(dst[:shift],a[-shift:])
  else:dst=a.copy()
  assert np.count_nonzero(dst[:,:,3])==np.count_nonzero(a[:,:,3]);im=Image.fromarray(dst);receiptPath=S/'provenance.json'
  receipt=json.loads(receiptPath.read_text(encoding='utf-8'));assert sha(Path(receipt['savedPath']))==receipt['rawSha256'];assert sha(S/'prompt.txt')==receipt['promptSha256']
  for ref in receipt['references']:assert sha(Path(ref['path']))==ref['sha256'] and sha(Path(ref['source']))==ref['sourceSha256']
 inputs[str(src)]=sha(src);inputs[str(receiptPath)]=sha(receiptPath);nb=bounds(np.asarray(im));images[slot]=im;out=F/f'{slot:03}.png';im.save(out)
 heightDelta=(nb[3]-nb[1])-(ob[3]-ob[1]);records.append(dict(slot=slot,source=str(src),wholeShiftY=shift,bounds=nb,selectedBounds=ob,heightDelta=heightDelta,soleDelta=nb[3]-ob[3],frameSha256=sha(out),geometryFlag=abs(heightDelta)>2,visualAcceptance=False))
for page,start in enumerate([0,6,12]):
 slots=list(range(start,min(start+6,13)));board=Image.new('RGB',(1920,1000),'#17252d');draw=ImageDraw.Draw(board)
 for col,slot in enumerate(slots):
  rec=records[slot];x=col*320;draw.text((x+8,10),f'Phase{slot}: height {rec["heightDelta"]:+} yShift{rec["wholeShiftY"]:+}',fill='white')
  for row,im in enumerate([originals[slot],images[slot]]):
   y=30+row*360;body=im.resize((320,320),Image.Resampling.NEAREST);board.paste(body,(x,y),body);draw.text((x+8,y+8),'Selected' if row==0 else 'Whole registered trial',fill='white')
  for n,h in enumerate([82,54,27]):
   sc=h/148;im=images[slot].resize((round(256*sc),round(256*sc)),Image.Resampling.LANCZOS);center=x+56+n*98;y=950;board.paste(im,(round(center-128*sc),round(y-224*sc)),im)
 board.save(D/f'comparison-{page}.png')
selected=json.loads((P/'keypose-review-v1/review.json').read_text(encoding='utf-8'))['selectedInputs'];assert all(sha(Path(p))==h for p,h in selected.items())
report=dict(status='pending_consecutive_visual_review',slots=13,completeWalkSlots=48,completeWalk=False,records=records,inputs=inputs,selectedProtectedInputs=selected,normalAdmission=False,nativeTested=False,wholeTranslationOnly=True,scope='Thirteen consecutive source drawings for comparison. No loop/manifest, anatomy fitting, per-part splicing, recoloring or partial installation. All surviving whole RGBA exact under registration; occupied pose height varies naturally and flags require visual diagnosis.')
(D/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(slots=13,heightDeltas=[r['heightDelta'] for r in records],soleDeltas=[r['soleDelta'] for r in records],geometryFlags=[r['slot'] for r in records if r['geometryFlag']],selectedProtected=len(selected))))
