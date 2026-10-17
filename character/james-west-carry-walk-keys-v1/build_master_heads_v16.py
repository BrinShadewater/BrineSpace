from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'master-head-review-v16';out.mkdir(exist_ok=True)
rect=(102,62,155,110)
masters=[r/'character/james-carry-headcaps-v1/frames/004.png',r/'character/james-carry-authored-helmet-v1/frames/004.png']
indexfile=p/'contact-v14-prompt-index.json';index=json.loads(indexfile.read_bytes())
files=[indexfile,Path(__file__)]+masters;groups=[];checks=[]
for mode,masterfile in zip(('bare','helmet'),masters):
 master=Image.open(masterfile).convert('RGBA');frames=[]
 for row in index['poses']:
  i=row['phase'];f=p/row['source'];assert hashlib.sha256(f.read_bytes()).hexdigest()==row['sourceSha256']
  body=Image.open(f).convert('RGBA');candidate=body.copy();candidate.paste(master.crop(rect),rect[:2]);files.append(f)
  a=np.array(body);b=np.array(candidate);mask=np.ones((256,256),bool);mask[62:110,102:155]=False
  assert mask.sum()==62992 and np.array_equal(a[mask],b[mask]);assert candidate.crop(rect).tobytes()==master.crop(rect).tobytes()
  candidate.save(out/f'{mode}-{i:03}.png');frames.append(candidate)
  checks.append({'gear':mode,'phase':i,'bodyOutsideHead62992Exact':True,'exactStandingMasterHead':True,'alpha128Bounds':candidate.getchannel('A').point(lambda v:255 if v>=128 else 0).getbbox()})
 groups.append(frames)
 m=json.loads((p/'paired-v14'/(mode+'-manifest.json')).read_bytes());m['name']='James carrying selected standing-master head '+mode+' provisional'
 m['status']='candidate_unselected_master_head_review';m['states'][0]['frameFiles']=['res://'+(out/f'{mode}-{i:03}.png').relative_to(r).as_posix() for i in range(49)]
 (out/(mode+'-manifest.json')).write_text(json.dumps(m,indent=2)+'\n')
for start in range(0,49,7):
 board=Image.new('RGBA',(1120,372),(48,59,63,255));d=ImageDraw.Draw(board)
 for y,bank in enumerate(groups):
  for col,i in enumerate(range(start,min(start+7,49))):
   board.alpha_composite(bank[i].crop((96,56,160,120)).resize((160,160),Image.Resampling.NEAREST),(col*160,y*186+26));d.text((col*160+3,y*186+7),f'{i} '+('helmet' if y else 'bare'),fill='white')
 board.convert('RGB').save(out/f'heads-{start}.png')
preview=[]
for i in range(49):
 board=Image.new('RGBA',(960,270),(48,59,63,255));d=ImageDraw.Draw(board)
 for mode,bank in enumerate(groups):
  for j,h in enumerate((148,82,54,27)):
   scale=h/148;size=round(256*scale);x=mode*480+(80,230,340,430)[j]
   board.alpha_composite(bank[i].resize((size,size),Image.Resampling.LANCZOS),(round(x-128*scale),round(252-224*scale)));d.text((x-35,8),('helmet ' if mode else 'bare ')+str(h),fill='white')
 preview.append(board.convert('RGB'))
durations=[row['durationMs'] for row in index['poses']]
preview[0].save(out/'paired-preview.apng',save_all=True,append_images=preview[1:],duration=durations,loop=0)
decoded=Image.open(out/'paired-preview.apng');assert decoded.n_frames==49
for i in range(49):decoded.seek(i);assert decoded.convert('RGB').tobytes()==preview[i].tobytes() and decoded.info['duration']==durations[i]
report={'inputSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in set(files)},'checks':checks,'headAdmissionRegion':rect,'durationMs':sum(durations),'decodedPreviewFramesExact':49,'standingMasterBare':masters[0].relative_to(r).as_posix(),'standingMasterHelmet':masters[1].relative_to(r).as_posix(),'sourceAcceptance':False,'selected':False,'visualReviewPending':True,'continuousMotionWatched':False,'normalChanged':False,'scope':'Exact fixed-position selected standing-master head/collar reuse over unchanged current49 carrying body sources. Head differs deliberately from original walking donor; all body/legs outside62992 head guard unchanged. Neck seam/material/cadence/room acceptance unproven.'}
(out/'review.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'masterHeadPairs':49,'outsideHeadExact':98,'decodedPreviewFrames':49,'durationMs':sum(durations)}))
