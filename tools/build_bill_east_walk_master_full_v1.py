"""Package all48 whole authored phases with original timing; keep runtime untouched."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,copy,ast,subprocess
R=Path(__file__).resolve().parents[1];P=R/'character/bill-east-walk-master-pilot-v1';D=R/'character/bill-east-walk-master-full-v1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def bounds(a):
 y,x=np.where(a[:,:,3]>127);return [int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
sources=[]
for slot in range(48):
 if slot in [0,12,24,36]:
  S=P/(f'stride-{slot:03}-v2' if slot==24 else f'stride-{slot:03}-v1');frame=P/f'keypose-review-v1/frames/{slot:03}.png'
 else:
  S=P/f'sequence-individual-{slot:03}-v2'
  if not (S/f'raw-{slot:03}.png').exists():S=P/f'sequence-individual-{slot:03}-v1'
  frame=S/f'candidate-{slot:03}.png'
 assert frame.exists(),f'Missing phase{slot}; no partial manifest'
 sources.append((S,frame))
D.mkdir(exist_ok=False);F=D/'frames';F.mkdir();inputs={};records=[];images=[];oldImages=[];rawImages=[]
protected=json.loads((P/'keypose-review-v1/review.json').read_text(encoding='utf-8'))['selectedInputs'];assert all(sha(Path(p))==h for p,h in protected.items())
for slot,(S,frame) in enumerate(sources):
 receipt=json.loads((S/'provenance.json').read_text(encoding='utf-8'));raw=Path(receipt['savedPath']);assert sha(raw)==receipt['rawSha256'] and sha(S/'prompt.txt')==receipt['promptSha256']
 for ref in receipt['references']:assert sha(Path(ref['path']))==ref['sha256'] and sha(Path(ref['source']))==ref['sourceSha256']
 for path in [raw,S/'provenance.json',S/'prompt.txt',frame]:inputs[str(path)]=sha(path)
 old=Image.open(R/f'character/bill-walk-east-material-v1/frames/bare/walk-east/{slot:03}.png').convert('RGBA');oldImages.append(old);ob=bounds(np.asarray(old));a=np.asarray(Image.open(frame).convert('RGBA')).copy();nb=bounds(a);shift=ob[3]-nb[3];b=np.zeros_like(a)
 if shift>0:
  assert not a[-shift:,:,3].any();b[shift:]=a[:-shift];assert np.array_equal(b[shift:],a[:-shift])
 elif shift<0:
  assert not a[:-shift,:,3].any();b[:shift]=a[-shift:];assert np.array_equal(b[:shift],a[-shift:])
 else:b=a.copy()
 assert np.count_nonzero(b[:,:,3])==np.count_nonzero(a[:,:,3]);im=Image.fromarray(b);out=F/f'{slot:03}.png';im.save(out);images.append(im);rawImages.append(Image.open(raw).convert('RGBA'));nb=bounds(b)
 mask=b[:,:,3]>127;oldmask=np.asarray(old)[:,:,3]>127
 records.append(dict(slot=slot,generationId=receipt['generationId'],source=str(frame),raw=str(raw),wholeShiftY=shift,keyposePriorShiftY=-1 if slot==24 else 0,bounds=nb,selectedBounds=ob,heightDelta=(nb[3]-nb[1])-(ob[3]-ob[1]),soleDelta=nb[3]-ob[3],silhouetteIoU=float((mask&oldmask).sum()/(mask|oldmask).sum()),frameSha256=sha(out)))
manifest=copy.deepcopy(json.loads((R/'character/bill-walk-east-material-v1/manifest.json').read_text(encoding='utf-8')));manifest.update(name='Bill East whole master walking candidate',status='staged_visual_review_pending');state=manifest['states'][0];state['frameFiles']=[f'res://character/bill-east-walk-master-full-v1/frames/{s:03}.png' for s in range(48)];state['provenance']=dict(method='Full whole-source authoring; original48phase/timing preserved; uniform packing and lossless whole Yregistration only',review='res://character/bill-east-walk-master-full-v1/review.json',normalAdmission=False)
assert sum(state['frameDurationsMs'])==2000 and len(state['frameFiles'])==48
(D/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
decoded=[]
for speed in [1,4]:
 dst=D/('walk-normal.png' if speed==1 else 'walk-quarter.png');images[0].save(dst,save_all=True,append_images=images[1:],duration=[t*speed for t in state['frameDurationsMs']],loop=0,disposal=0,blend=0)
 with Image.open(dst) as animation:
  assert animation.n_frames==48;duration=0
  for slot in range(48):animation.seek(slot);assert np.array_equal(np.asarray(animation.convert('RGBA')),np.asarray(images[slot]));duration+=animation.info['duration']
  assert duration==2000*speed;decoded.append(dict(path=str(dst),frames=48,durationMs=duration))
master=Image.open(P/'original-master.png').convert('RGBA').resize((256,256),Image.Resampling.LANCZOS);master.save(D/'master.png')
boards=[]
for page,start in enumerate(range(0,48,6)):
 board=Image.new('RGB',(2240,1050),'#17252d');draw=ImageDraw.Draw(board);rawboard=Image.new('RGB',(2400,700),'#17252d');rd=ImageDraw.Draw(rawboard)
 for col,slot in enumerate(range(start,start+6)):
  rec=records[slot];x=col*320;draw.text((x+8,10),f'Phase{slot}: height{rec["heightDelta"]:+} shift{rec["wholeShiftY"]:+}',fill='white')
  for row,im in enumerate([oldImages[slot],images[slot]]):
   y=30+row*350;draw.text((x+8,y+8),'Current' if row==0 else 'Whole registered candidate',fill='white');body=im.resize((320,320),Image.Resampling.NEAREST);board.paste(body,(x,y+20),body)
  head=images[slot].crop((100,65,160,120)).resize((180,165),Image.Resampling.NEAREST);board.paste(head,(x+70,730),head)
  for n,h in enumerate([82,54,27]):
   sc=h/148;im=images[slot].resize((round(256*sc),round(256*sc)),Image.Resampling.LANCZOS);board.paste(im,(round(x+54+n*98-128*sc),round(1030-224*sc)),im)
  rd.text((col*400+8,10),f'Raw whole phase{slot}',fill='white');rawview=rawImages[slot].resize((400,400),Image.Resampling.LANCZOS);rawboard.paste(rawview,(col*400,35),rawview)
  w,h=rawImages[slot].size;crop=rawImages[slot].crop((round(w*100/256),round(h*60/256),round(w*160/256),round(h*120/256))).resize((240,240),Image.Resampling.LANCZOS);rawboard.paste(crop,(col*400+80,450),crop)
 for row in [0,1]:view=master.resize((320,320),Image.Resampling.NEAREST);board.paste(view,(1920,50+row*350),view)
 draw.text((1928,10),'Original master authority',fill='white');head=master.crop((100,65,160,120)).resize((180,165),Image.Resampling.NEAREST);board.paste(head,(1990,730),head)
 board.save(D/f'comparison-{page}.png');rawboard.save(D/f'raw-review-{page}.png');boards += [f'comparison-{page}.png',f'raw-review-{page}.png']
report=dict(status='complete48_source_candidate_pending_visual_motion_native',completeSourceSlots=48,records=records,inputs=inputs,selectedProtectedInputs=protected,originalTimingMs=state['frameDurationsMs'],decodedAPNG=decoded,normalAdmission=False,nativeTested=False,visualReviewed=False,fullVisualAcceptance=False,geometryFlags=[r['slot'] for r in records if abs(r['heightDelta'])>2],boards={n:sha(D/n) for n in boards},scope='Complete original48phase 2000ms cycle. Full-source edits, no invented interpolation, limb/head splice, local grade or per-pose bbox fitting. Whole Ytranslations retain surviving RGBA/alpha counts exactly. All occupied source soles match original phase-specific soles; not physical2Dplanted-foot proof. Complete sources and APNG decoding do not establish visual cadence/native/full-library acceptance.')
(D/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
validation=dict(passed=True,sourceSlots=48,uniqueFrameHashes=len(set(r['frameSha256'] for r in records)),selectedProtected=len(protected),sourceHeightDeltaRange=[min(r['heightDelta'] for r in records),max(r['heightDelta'] for r in records)],soleDeltas=sorted(set(r['soleDelta'] for r in records)),geometryFlags=report['geometryFlags'],apngDecodedFrames=96,normalAdmission=False,nativeTested=False)
(D/'validation.json').write_text(json.dumps(validation,indent=2)+'\n',encoding='utf-8');print(json.dumps(validation))
