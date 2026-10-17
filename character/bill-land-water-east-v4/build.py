"""Register early grounded poses by semantic boot contacts, never body-height fitting."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,copy
P=Path(__file__).resolve().parent;R=P.parent
B=R/'bill-land-water-east-v3';H=R/'bill-land-water-helmet-east-v1'
REGIONS={0:(150,216,180,229),1:(150,216,180,234),2:(130,236,150,255)}
def contact(im,box):
 a=np.array(im);x0,y0,x1,y1=box;ys,xs=np.where(a[y0:y1,x0:x1,3]>180)
 assert len(ys)>0
 return int(ys.max()+y0+1)
def shifted(im,dy):
 out=Image.new('RGBA',im.size);out.paste(im,(0,dy))
 old=np.array(im);new=np.array(out)
 assert np.count_nonzero(old[:abs(dy)])==0 and np.count_nonzero(old[-abs(dy):])==0
 assert np.array_equal(new[:320+dy],old[-dy:])
 assert np.count_nonzero(old[:,:,3])==np.count_nonzero(new[:,:,3])
 return out
def main():
 P.mkdir(exist_ok=True)
 oldbare=[Image.open(B/f'frames/land-swim-east/{i:03}.png').convert('RGBA') for i in range(6)]
 oldhelmet=[Image.open(H/f'frames/land-swim-east/{i:03}.png').convert('RGBA') for i in range(6)]
 floor=contact(oldbare[0],REGIONS[0]);assert floor==224
 offsets={i:floor-contact(oldbare[i],REGIONS[i]) for i in [1,2]};assert offsets=={1:-6,2:-27}
 banks={};hashes={}
 for gear,old,origin in [('bare',oldbare,B),('helmet',oldhelmet,H)]:
  frames=[shifted(im,offsets[i]) if i in offsets else im.copy() for i,im in enumerate(old)]
  for i in [0,3,4,5]:assert frames[i].tobytes()==old[i].tobytes()
  if gear=='bare':
   for i in [1,2]:
    x0,y0,x1,y1=REGIONS[i];dy=offsets[i]
    assert contact(frames[i],(x0,y0+dy,x1,y1+dy))==floor
  manifest=copy.deepcopy(json.loads((origin/'manifest.json').read_text()));manifest['name']='Bill East early grounded contact registration — '+gear
  manifest['status']='source_contact_trial_unselected'
  manifest['states']=[s for s in manifest['states'] if s['id']=='land-swim-east'];state=manifest['states'][0]
  # Earlier source-study flags labelled every pose wet; they are not admission data.
  state.pop('waterPoses',None);state.pop('waterKinds',None)
  state['frameFiles']=[];state['provenance']='Two whole-figure Y translations using explicit front-boot sole regions and canonical idle contact224; scale1, no paint/grade/head fitting. Four other source poses exact. Not native contact/motion acceptance.'
  for i,im in enumerate(frames):
   target=P/gear/'frames/land-swim-east'/f'{i:03}.png';target.parent.mkdir(parents=True,exist_ok=True);im.save(target)
   state['frameFiles'].append(f'frames/land-swim-east/{i:03}.png');hashes[target.relative_to(P).as_posix()]=hashlib.sha256(target.read_bytes()).hexdigest()
  m=P/gear/'manifest.json';m.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
  apng=P/gear/'source-enter.png';times=state['frameDurationsMs'];assert sum(times)==500
  frames[0].save(apng,save_all=True,append_images=frames[1:],duration=times,loop=0,disposal=0,blend=0)
  with Image.open(apng) as im:
   assert im.n_frames==6
   for i,frame in enumerate(frames):im.seek(i);assert im.convert('RGBA').tobytes()==frame.tobytes() and im.info['duration']==times[i]
  banks[gear]=frames
 # Original master panel stays at original common standing ruler/pivot.
 master=Image.open(B/'master-relative-review.png').crop((0,20,320,340))
 board=Image.new('RGB',(2240,720),'#182932');draw=ImageDraw.Draw(board)
 for row,gear in enumerate(['bare','helmet']):
  y=row*360+25;board.paste(master,(0,y));draw.text((4,row*360+3),'Original master / common148 standing ruler',fill='white')
  for i,im in enumerate(banks[gear]):
   x=(i+1)*320;board.paste(im,(x,y),im);draw.text((x+4,row*360+3),gear+' '+str(i)+(' contact shift '+str(offsets[i]) if i in offsets else ' exact'),fill='white')
   if i<3:draw.line((x,y+floor,x+319,y+floor),fill='#6aa39e',width=1)
 board.save(P/'master-contact-review.png')
 detail=Image.new('RGB',(1280,720),'#182932');d=ImageDraw.Draw(detail)
 for row,i in enumerate([1,2]):
  for col,(gear,label,im) in enumerate([('bare','before',oldbare[i]),('bare','registered',banks['bare'][i]),('helmet','before',oldhelmet[i]),('helmet','registered',banks['helmet'][i])]):
   x=col*320;y=row*360+25;detail.paste(im,(x,y),im);d.line((x,y+224,x+319,y+224),fill='#6aa39e',width=1);d.text((x+4,row*360+3),gear+' '+label+' pose'+str(i),fill='white')
 detail.save(P/'before-after-contact.png')
 e={'floorContactY':floor,'semanticFrontBootRegions':REGIONS,'alphaThresholdExclusive':180,'wholePoseTranslations':{i:[0,dy] for i,dy in offsets.items()},'scale':1,'standingHeight':148,'pivot':[160,224],
  'preservedIndicesPerGear':[0,3,4,5],'translatedOpaquePixelsAndRGBAExact':True,'noClipping':True,'APNGDecodedFramesExact':12,'durationMsPerGear':500,'frameSHA256':hashes,
  'sourceBankPaths':['character/bill-land-water-east-v3/manifest.json','character/bill-land-water-helmet-east-v1/manifest.json'],
  'crownRegistrationForNextRuntime':[ [171,82],[177,91],[183,157],[187,188] ],'newSpacingGapPx':66,
  'runtimeWaterMetadataPending':True,'scope':'Deterministic source contact registration trial only. Two original whole figures shifted vertically without pixel/scale/grade/helmet/body changes. Contacts use explicit semantic sole regions, not full-body bounding-box normalization. Corrected early dry-support line exposes66px crown gap to first buoyant pose; authored intermediate still needed. Earlier all-wet source-study flags omitted, actual runtime classification still pending. Not world contact/collision/continuous native/master-motion acceptance; normal and staged runtime selectors unchanged.'}
 (P/'review.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
 (P/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Bill grounded entry contact</title><style>body{background:#182932;color:#eef;font:16px sans-serif}img{max-width:100%}</style><h1>Bill East — early boot contact registration trial</h1><p>'+e['scope']+'</p><img src="before-after-contact.png"><img src="master-contact-review.png"><p>Bare / helmet500ms source trials</p><img src="bare/source-enter.png"><img src="helmet/source-enter.png">',encoding='utf-8')
 print(json.dumps({'wholePoseOffsets':offsets,'preservedPoses':8,'translatedPoses':4,'exactAPNGFrames':12,'floorContact':floor,'remainingAuthoredGap':66}))
if __name__=='__main__':main()
