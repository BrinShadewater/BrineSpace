"""Fixed anatomical-density extraction of freshly articulated North exit poses."""
from pathlib import Path
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent;R=P.parent;S=P/'sources';F=P/'bare/frames/swim-land-north';F.mkdir(parents=True,exist_ok=True)
raw=Image.open(S/'exit-atlas-v1.png').convert('RGBA');assert raw.size==(1536,1024)
SCALE=.25;TIMES=[40,60,65,65,65,65,65,75];assert sum(TIMES)==500
frames=[Image.open(R/'bill-land-water-north-v3/bare/frames/land-swim-north/008.png').convert('RGBA')];records=[]
yy,xx=np.indices((512,512))
for i in range(4):
 col=i%3;row=i//3;box=(col*512,row*512,(col+1)*512,(row+1)*512)
 a=np.array(raw.crop(box));labs,count=label(a[:,:,3]>250);sizes=np.bincount(labs.ravel());assert count>0 and sizes[1:].max()>5000
 component=labs==np.argmax(sizes[1:])+1
 keep=binary_dilation(component,iterations=3)&(a[:,:,3]>0);a[~keep]=0
 rgb=a[:,:,:3].astype(float)
 # Head region excludes warm cuff/belt highlights; validate observed crown later.
 hair=(a[:,:,3]>180)&(xx>180)&(xx<330)&(yy<240)&(rgb[:,:,0]>rgb[:,:,1]*1.12)&(rgb[:,:,1]>rgb[:,:,2]*1.2)&(rgb[:,:,0]>35)
 ys,xs=np.where(hair);assert len(ys)>80,(i,'semantic hair region')
 crown=int(ys.min());axis=int(np.median(xs[ys<crown+6]))
 native=Image.fromarray(a).resize((128,128),Image.Resampling.LANCZOS)
 opaque=np.array(native)[:,:,3]>180;ny,nx=np.where(opaque)
 contact=int(ny.max())+1
 shift=(160-round(axis*SCALE),[180,155][i]-round(crown*SCALE)) if i<2 else (160-round(axis*SCALE),224-contact)
 out=Image.new('RGBA',(320,352));out.paste(native,shift)
 assert np.count_nonzero(np.array(out)[:,:,3])==np.count_nonzero(np.array(native)[:,:,3]),'No clipped source alpha'
 frames.append(out)
 records.append(dict(pose=i+1,source='res://character/bill-water-exit-north-v1/sources/exit-atlas-v1.png',sourceCell=box,sourceHairCrown=[axis+col*512,crown+row*512],scale=SCALE,wholeFigureTranslation=shift,headAnchor=[round(axis*SCALE)+shift[0],round(crown*SCALE)+shift[1]],opaqueSole=contact+shift[1],alphaBounds=out.getchannel('A').getbbox(),phase=['elbow retract','palm push','knee tuck/plant','half kneel','rising squat','near standing'][i]))
for name in ['rise','near-stand']:
 version=2 if name=='rise' else 3
 path=S/f'{name}-canvas-v{version}.png';single=Image.open(path).convert('RGBA');assert single.size==(1254,1254)
 a=np.array(single);sy,sx=np.indices(a.shape[:2]);labs,count=label(a[:,:,3]>250);sizes=np.bincount(labs.ravel());assert count>0 and sizes[1:].max()>10000
 keep=binary_dilation(labs==np.argmax(sizes[1:])+1,iterations=3)&(a[:,:,3]>0);a[~keep]=0
 rgb=a[:,:,:3].astype(float)
 hair=(a[:,:,3]>180)&(sx>500)&(sx<750)&(sy>100)&(sy<470)&(rgb[:,:,0]>rgb[:,:,1]*1.12)&(rgb[:,:,1]>rgb[:,:,2]*1.2)&(rgb[:,:,0]>35)
 ys,xs=np.where(hair);assert len(ys)>500;top=int(ys.min());axis=int(np.median(xs[ys<top+6]))
 scale=148/976;size=round(1254*scale);native=Image.fromarray(a).resize((size,size),Image.Resampling.LANCZOS)
 ny,nx=np.where(np.array(native)[:,:,3]>180);contact=int(ny.max())+1
 shift=(160-round(axis*scale),224-contact);out=Image.new('RGBA',(320,352));out.paste(native,shift)
 assert np.count_nonzero(np.array(out)[:,:,3])==np.count_nonzero(np.array(native)[:,:,3]),'No clipped single source alpha'
 frames.append(out);records.append(dict(pose=len(frames)-1,source='res://character/bill-water-exit-north-v1/sources/'+path.name,sourceHairCrown=[axis,top],scale=scale,resampledCanvasSize=[size,size],wholeFigureTranslation=shift,headAnchor=[round(axis*scale)+shift[0],round(top*scale)+shift[1]],opaqueSole=224,alphaBounds=out.getchannel('A').getbbox(),phase='rising squat' if name=='rise' else 'near standing',rawSHA256=hashlib.sha256(path.read_bytes()).hexdigest()))
frames.append(Image.open(R/'bill-land-water-north-v3/bare/frames/land-swim-north/000.png').convert('RGBA'))
for i,im in enumerate(frames):im.save(F/f'{i:03}.png')
manifest=dict(name='Bill independently articulated North water exit candidate',frameWidth=320,frameHeight=352,pivot=[160,224],standingHeight=148,precomposed=True,status='source_visual_review_pending',states=[dict(id='swim-land-north',frameFiles=[f'frames/swim-land-north/{i:03}.png' for i in range(8)],frameDurationsMs=TIMES,loop=False,facings=['north']*8,provenance='Six new whole-figure exit poses: four atlas poses at common.25 anatomical density and two original-master-density rising poses at148/976. Exact padded selected North swim/idle contexts. No reverse entry, normal admission or native acceptance.')])
(P/'bare/manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
frames[0].save(P/'bare/source-leave.png',save_all=True,append_images=frames[1:],duration=TIMES,loop=0,disposal=0,blend=0)
with Image.open(P/'bare/source-leave.png') as ap:
 assert ap.n_frames==8
 for i,im in enumerate(frames):ap.seek(i);assert ap.convert('RGBA').tobytes()==im.tobytes() and ap.info['duration']==TIMES[i]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
review=dict(registrations=records,sharedAtlasDrawingScale=SCALE,singlePoseMasterDensity=148/976,scaleReason='First four new atlas poses share established North atlas anatomical density.25; two fresh original-master single poses share master148/976 density. No per-pose bounding-box normalization. Canvas sizes alone do not determine density.',sourceSHA256=sha(S/'exit-atlas-v1.png'),promptSHA256=sha(S/'exit-atlas-prompt-v1.txt'),timelineMs=500,pairedFrames=16,endpointExactToSelectedSources=True,rejectedAtlasCells=[dict(cell=4,reason='Rising stature too short at common head/hardware density; replaced by original-master single pose.'),dict(cell=5,reason='Near-standing stature too short at common head/hardware density; replaced by original-master single pose.')],visualReview='Pending full source sequence/master/temporal review.',nativeAcceptance=False,normalSelected=False)
(P/'exit-review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
helmet=(R/'bill-land-water-north-v1/build_helmet.py').read_text(encoding='utf-8')
helmet=helmet.replace('entry-review.json','exit-review.json').replace('land-swim-north','swim-land-north').replace('source-enter','source-leave').replace('range(9)','range(8)').replace('[0,8]','[0,7]').replace('i==0 else','i==7 else')
# Endpoint order is swimming first, standing last; original padding and exact pixels.
helmet=helmet.replace("'bill-shared-helmet-runtime-v2/frames/idle-north/000.png' if i==7 else 'bill-swim-helmet-north-coherent-v1/frames/swim-north/000.png'","'bill-swim-helmet-north-coherent-v1/frames/swim-north/000.png' if i==0 else 'bill-shared-helmet-runtime-v2/frames/idle-north/000.png'")
helmet=helmet.replace('shift=(68,52) if i==7 else (56,152)','shift=(56,152) if i==0 else (68,52)')
helmet=helmet.replace('((184,184) if i==7 else (208,224))','((208,224) if i==0 else (184,184))')
helmet=helmet.replace('ap.n_frames==9','ap.n_frames==8').replace('(2880,810)','(2560,810)').replace('(1960,660)','(1680,660)').replace('paired-entry-contact.png','paired-exit-contact.png').replace('canonical rear helmet candidate','exit canonical rear helmet candidate').replace('decodedPairedAPNGFramesExact=18','decodedPairedAPNGFramesExact=16').replace('pairedFrames=18','pairedFrames=16')
helmet=helmet.replace("'pairedFrames':18","'pairedFrames':16").replace("'decodedAPNGExact':18","'decodedAPNGExact':16").replace("'protectedFittings':7","'protectedFittings':6")
(P/'build_helmet.py').write_text(helmet,encoding='utf-8')
board=Image.new('RGB',(2560,405),'#182932');d=ImageDraw.Draw(board)
names=['selected swim']+[r['phase'] for r in records]+['selected idle']
for i,im in enumerate(frames):
 board.paste(im,(i*320,25),im);d.text((i*320+5,5),names[i],fill='white')
 if i>=3:d.line((i*320,249,i*320+319,249),fill='#6aa39e')
board.save(P/'exit-contact.png')
print(json.dumps(dict(frames=8,decodedAPNGExact=8,registrations=records)))
