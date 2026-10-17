"""Separate articulated exit study with exact captured normal endpoints."""
from pathlib import Path
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent;R=P.parent.parent
SOURCE=P/'sources/interiors-portrait-v3.png';SCALE=.24
HEADS=[(470,190),(886,145),(350,874),(820,799)]
TARGETS=[(189,181),(179,108),(168,98),(165,76)]
TIMES=[60,90,100,100,90,60]
def main():
 phase=json.loads((R/'character/bill-land-water-phase-audit-v1/phase-evidence.json').read_text());plan=next(x for x in phase['plans'] if x['id']=='bare-leave')
 frames=[Image.open(R/'character/bill-land-water-phase-audit-v1'/plan['rows'][0]['file']).convert('RGBA')]
 raw=np.array(Image.open(SOURCE).convert('RGBA'));labs,_=label(raw[:,:,3]>250);counts=np.bincount(labs.ravel());ids=np.argsort(counts[1:])[-4:]+1
 ids=sorted(ids,key=lambda n:(int(np.where(labs==n)[0].min())//768,int(np.where(labs==n)[1].min())))
 grade=json.loads((R/'character/bill-land-water-east-v2/material-grade.json').read_text());rgb=raw[:,:,:3].astype(float);mapped=np.interp(rgb.mean(2),grade['input'],grade['output']);w=np.clip((22-np.ptp(rgb,axis=2))/14,0,1)*(raw[:,:,3]>0)
 pixels=raw.copy();pixels[:,:,:3]=np.clip(rgb*(1-w[:,:,None])+mapped[:,:,None]*w[:,:,None],0,255).astype('uint8');reg=[]
 for i,n in enumerate(ids):
  mask=binary_dilation(labs==n,iterations=3)&(raw[:,:,3]>0);ys,xs=np.where(mask);box=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)];a=pixels.copy();a[~mask]=0
  im=Image.fromarray(a).crop(box);im=im.resize((round(im.width*SCALE),round(im.height*SCALE)),Image.Resampling.LANCZOS)
  pos=[round(TARGETS[i][j]-(HEADS[i][j]-box[j])*SCALE) for j in range(2)];out=Image.new('RGBA',(320,320));out.alpha_composite(im,pos);frames.append(out)
  reg.append(dict(sourceBox=box,sourceCrown=HEADS[i],targetCrown=TARGETS[i],position=pos,scale=SCALE))
 frames.append(Image.open(R/'character/bill-land-water-phase-audit-v1'/plan['rows'][5]['file']).convert('RGBA'))
 files=[]
 for i,im in enumerate(frames):
  f=P/f'frames/swim-land-east/{i:03}.png';f.parent.mkdir(parents=True,exist_ok=True);im.save(f);files.append(f.relative_to(P).as_posix())
 for index in [0,5]:assert frames[index].tobytes()==Image.open(R/'character/bill-land-water-phase-audit-v1'/plan['rows'][index]['file']).convert('RGBA').tobytes()
 frames[0].save(P/'source-leave.png',save_all=True,append_images=frames[1:],duration=TIMES,loop=0,disposal=0,blend=0)
 with Image.open(P/'source-leave.png') as apng:
  assert apng.n_frames==6
  for i,im in enumerate(frames):apng.seek(i);assert apng.convert('RGBA').tobytes()==im.tobytes()
  assert sum(apng.seek(i) or apng.info['duration'] for i in range(6))==500
 m=dict(name='Bill authored tucked-arm East water exit study',status='source_study_unselected',frameWidth=320,frameHeight=320,pivot=[160,224],standingHeight=148,textureFilter='linear',precomposed=True,states=[dict(id='swim-land-east',frameFiles=files,frameDurationsMs=TIMES,loop=False,facings=['east']*6,provenance='New distinct four-pose exit, not reversed entrance. Exact captured normal swim2/walk34 endpoints. Runtime medium/contact classification intentionally unassigned.')])
 (P/'manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
 e=dict(sourceSHA256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),generation='exec-02990fa7-5689-4d75-ac27-0f5cc2a7f04c',alphaCoreThresholdExclusive=250,fringePixels=3,frames=reg,endpointAuthorities=plan['sourceBoundary'],endpointExact=True,APNGDecodeExact=True,timelineMs=500,uniformBodyScale=SCALE,scaleBasis='One approximate near-standing source ruler across all interiors; not per-pose bounding-height normalization. Actual-master proportions remain under visual review.',grade='Frozen entry V2 neutral curve; warm materials not remapped.',rejectedCandidates={'interiors-v1.png':'Oversized heads, compact body proportions in short landscape cells.','head-attempt-v2.png':'Narrow head repair altered bodies; preservation failed.'},normalSelected=False,nativeAcceptance=False)
 (P/'registration.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
 master=Image.open(R/'character/bill-land-water-east-v3/master-relative-review.png').crop((0,20,320,340)).convert('RGB')
 board=Image.new('RGB',(2240,350),'#182932');d=ImageDraw.Draw(board);board.paste(master,(0,25));d.text((4,4),'Original master',fill='white')
 for i,im in enumerate(frames):board.paste(im,((i+1)*320,25),im);d.text(((i+1)*320+4,4),'Captured swim2' if i==0 else 'Captured walk34' if i==5 else f'Authored exit {i}',fill='white')
 board.save(P/'master-review.png')
 (P/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Bill separate water exit</title><style>body{background:#182932;color:#ddd;font:16px sans-serif;margin:24px}img{max-width:100%}</style><h1>Bill East — separate tucked-arm water exit</h1><p>Unselected source study. Four new articulated exit poses; exact sampled swimming/walking endpoints. Shared .24 body scale and frozen matte curve. Master proportions, contact trajectory and initial rise spacing under review. No native bridge playback or collision/medium admission.</p><img src="master-review.png"><img src="source-leave.png">',encoding='utf-8')
 print('Separate four-pose exit packaged; two captured endpoints/6APNGframes exact/500ms; native/proportion/contact acceptance pending.')
if __name__=='__main__':main()
