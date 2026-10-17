"""Replace only final authored pitch interior; freeze all earlier v2 pixels/grade."""
from pathlib import Path
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent;OLD=P.parent/'bill-land-water-east-v2'
SOURCE=P/'sources/interiors-v3.png';SCALE=.27;HEAD=(1298,668);TARGET=(187,188)
def main():
 frames=[Image.open(OLD/f'frames/land-swim-east/{i:03}.png').convert('RGBA') for i in range(6)]
 raw=np.array(Image.open(SOURCE).convert('RGBA'));labs,_=label(raw[:,:,3]>250);counts=np.bincount(labs.ravel());ids=np.argsort(counts[1:])[-4:]+1
 ids=sorted(ids,key=lambda n:(int(np.where(labs==n)[0].min())//512,int(np.where(labs==n)[1].min())))
 grade=json.loads((OLD/'material-grade.json').read_text());rgb=raw[:,:,:3].astype(float)
 mapped=np.interp(rgb.mean(2),grade['input'],grade['output']);weight=np.clip((22-np.ptp(rgb,axis=2))/14,0,1)*(raw[:,:,3]>0)
 pixels=raw.copy();pixels[:,:,:3]=np.clip(rgb*(1-weight[:,:,None])+mapped[:,:,None]*weight[:,:,None],0,255).astype('uint8')
 mask=binary_dilation(labs==ids[-1],iterations=3)&(raw[:,:,3]>0);ys,xs=np.where(mask);box=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]
 pixels[~mask]=0;pose=Image.fromarray(pixels).crop(box);pose=pose.resize((round(pose.width*SCALE),round(pose.height*SCALE)),Image.Resampling.LANCZOS)
 pos=(round(TARGET[0]-(HEAD[0]-box[0])*SCALE),round(TARGET[1]-(HEAD[1]-box[1])*SCALE))
 frames[4]=Image.new('RGBA',(320,320));frames[4].alpha_composite(pose,pos)
 manifest=json.loads((OLD/'manifest.json').read_text());manifest['name']='Bill staged East compact leg land/water source bridge'
 for state in manifest['states']:
  forward=state['id']=='land-swim-east';poses=frames if forward else list(reversed(frames))
  state['provenance']='Original exact endpoints and first three v2 interiors retained; final interior generated compact-knee correction. Reverse exit derived; runtime unselected.'
  for file,im in zip(state['frameFiles'],poses):
   target=P/file;target.parent.mkdir(parents=True,exist_ok=True);im.save(target)
 for i in [0,1,2,3,5]:assert frames[i].tobytes()==Image.open(OLD/f'frames/land-swim-east/{i:03}.png').convert('RGBA').tobytes()
 (P/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
 (P/'material-grade.json').write_text(json.dumps(grade,indent=2)+'\n',encoding='utf-8')
 (P/'registration.json').write_text(json.dumps({'generation':'exec-24e6b4e9-2338-4bc1-817c-e1a2d901c75f','sourceSHA256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'component':int(ids[-1]),'sourceBox':box,'sourceCrown':HEAD,'targetCrown':TARGET,'position':pos,'scale':SCALE,'alphaCoreThresholdExclusive':250,'connectedFringePixels':3,'rejectedAlphaAttempt':'sources/alpha-attempt-v1.png shifted/enlarged figure; not used','preservedFrameIndices':[0,1,2,3,5],'grade':'Exact frozen v2 neutral curve; applied once to final replacement only.'},indent=2)+'\n',encoding='utf-8')
 times=manifest['states'][0]['frameDurationsMs']
 for filename,poses in [('source-enter.png',frames),('source-leave.png',list(reversed(frames)))]:poses[0].save(P/filename,save_all=True,append_images=poses[1:],duration=times,loop=0,disposal=0,blend=0)
 board=Image.new('RGB',(960,340),'#182932');d=ImageDraw.Draw(board)
 for i,(name,im) in enumerate([('Old extended-leg interior',Image.open(OLD/'frames/land-swim-east/004.png').convert('RGBA')),('New compact-knee interior',frames[4]),('Original swim endpoint',frames[5])]):
  board.paste(im,(i*320,20),im);d.text((i*320+5,3),name,fill='white')
 board.save(P/'leg-join-review.png')
 (P/'source-evidence.json').write_text(json.dumps({'fivePreservedFramesRGBAExact':True,'allInteriorScale':SCALE,'sourceOnly':True,'normalProductionSelected':False,'frameSHA256':{f.relative_to(P).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in (P/'frames').rglob('*.png')}},indent=2)+'\n',encoding='utf-8')
 print('One compact-knee interior replaced; five other frames byte-exact; frozen v2 grade retained.')
if __name__=='__main__':main()
