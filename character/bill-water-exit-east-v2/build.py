"""Insert authored lower midpoint without changing six original poses/timeline."""
from pathlib import Path
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
import numpy as np,json,hashlib,copy
P=Path(__file__).resolve().parent;OLD=P.parent/'bill-water-exit-east-v1';R=P.parent.parent
SOURCE=P/'sources/lower-midpoint.png';HEAD=(891,233);TARGET=(184,145);SCALE=.24
def main():
 raw=np.array(Image.open(SOURCE).convert('RGBA'));labs,_=label(raw[:,:,3]>250);counts=np.bincount(labs.ravel());ids=np.argsort(counts[1:])[-4:]+1
 ids=sorted(ids,key=lambda n:(int(np.where(labs==n)[0].min())//768,int(np.where(labs==n)[1].min())))
 n=ids[1];mask=binary_dilation(labs==n,iterations=3)&(raw[:,:,3]>0);ys,xs=np.where(mask);box=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]
 grade=json.loads((R/'character/bill-land-water-east-v2/material-grade.json').read_text());rgb=raw[:,:,:3].astype(float);mapped=np.interp(rgb.mean(2),grade['input'],grade['output']);w=np.clip((22-np.ptp(rgb,axis=2))/14,0,1)*(raw[:,:,3]>0)
 a=raw.copy();a[:,:,:3]=np.clip(rgb*(1-w[:,:,None])+mapped[:,:,None]*w[:,:,None],0,255).astype('uint8');a[~mask]=0
 im=Image.fromarray(a).crop(box);im=im.resize((round(im.width*SCALE),round(im.height*SCALE)),Image.Resampling.LANCZOS);pos=[round(TARGET[j]-(HEAD[j]-box[j])*SCALE) for j in range(2)]
 mid=Image.new('RGBA',(320,320));mid.alpha_composite(im,pos)
 old=[Image.open(OLD/f'frames/swim-land-east/{i:03}.png').convert('RGBA') for i in range(6)];frames=old[:2]+[mid]+old[2:];times=[60,45,45,100,100,90,60]
 mapping=[0,1,3,4,5,6]
 for i,newindex in enumerate(mapping):assert frames[newindex].tobytes()==old[i].tobytes()
 m=copy.deepcopy(json.loads((OLD/'manifest.json').read_text()));m['name']='Bill separate East water exit with authored lower midpoint';st=m['states'][0];st['frameFiles']=[];st['frameDurationsMs']=times;st['facings']=['east']*7;st['provenance']='Six exact V1 poses; one inserted lower articulated midpoint at same .24body scale/frozen grade. Original500ms by splitting first interior90ms into45+45. Not reversed entry; runtime unselected.'
 for i,im in enumerate(frames):
  f=P/f'frames/swim-land-east/{i:03}.png';f.parent.mkdir(parents=True,exist_ok=True);im.save(f);st['frameFiles'].append(f.relative_to(P).as_posix())
 frames[0].save(P/'source-leave.png',save_all=True,append_images=frames[1:],duration=times,loop=0,disposal=0,blend=0)
 with Image.open(P/'source-leave.png') as apng:
  assert apng.n_frames==7
  for i,im in enumerate(frames):apng.seek(i);assert apng.convert('RGBA').tobytes()==im.tobytes()
  assert sum(apng.seek(i) or apng.info['duration'] for i in range(7))==500
 (P/'manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
 e=dict(generation='exec-4917f326-8e05-4ec5-97e3-25183538d15e',sourceSHA256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),sourceBox=box,sourceCrown=HEAD,targetCrown=TARGET,position=pos,scale=SCALE,alphaCoreThresholdExclusive=250,fringePixels=3,preservedV1ToV2Indices=mapping,sixOriginalPosesRGBAExact=True,APNGDecodeExact=True,timelineMs=500,grade='Frozen entryV2 neutral curve once on new midpoint only.',rejectedSource='sources/rejected-large-midpoints.png violates shared anatomical scale; unused.',normalSelected=False,nativeMotionAccepted=False,crownTrajectory=[181,145,108,98,76],trajectoryScope='Initial73px rise split36/37; not full anatomical/world support or smoothness acceptance.')
 (P/'registration.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
 master=Image.open(OLD/'master-review.png').crop((0,25,320,345));board=Image.new('RGB',(2560,350),'#182932');d=ImageDraw.Draw(board);board.paste(master,(0,25));d.text((4,4),'Original master',fill='white')
 for i,im in enumerate(frames):board.paste(im,((i+1)*320,25),im);d.text(((i+1)*320+4,4),'New lower midpoint' if i==2 else f'Preserved exit {i}',fill='white')
 board.save(P/'master-review.png')
 game=Image.new('RGB',(1344,460),'#182932');d=ImageDraw.Draw(game)
 for j,h in enumerate([82,54,27]):
  for i,im in enumerate(frames):
   small=im.resize((round(320*h/148),round(320*h/148)),Image.Resampling.LANCZOS);game.paste(small,(i*192+(192-small.width)//2,j*150+20),small)
  d.text((5,j*150+3),f'{h}px standing ruler',fill='white')
 game.save(P/'gameplay-review.png')
 (P/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Bill lower water exit</title><style>body{background:#182932;color:#ddd;font:16px sans-serif;margin:24px}img{max-width:100%}</style><h1>Bill East — lower articulated exit midpoint</h1><p>Source-only draft. Six original poses unchanged; one new midpoint with shared scale/grade.500ms original timeline. Master/material/contact/continuous motion still under review; no normal selection.</p><img src="master-review.png"><img src="gameplay-review.png"><img src="source-leave.png">',encoding='utf-8')
 print('Seven authored exit poses/500ms; six original RGBA exact; new midpoint .24scale/frozen grade; APNG7decoded frames exact.')
if __name__=='__main__':main()
