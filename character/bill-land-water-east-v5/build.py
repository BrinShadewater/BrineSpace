from pathlib import Path
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
import numpy as np,json,hashlib,copy
P=Path(__file__).resolve().parent;R=P.parent;OLD=R/'bill-land-water-east-v4'
SOURCE=P/'sources/lift-canvas-v3.png';CROWN=(180,124);TIMES=[60,90,50,50,100,90,60]
DONOR=R/'bill-equipped-east-selected-v1/frames/interact-east/000.png'
POLYGON=[(72,20),(114,20),(114,51),(110,55),(101,58),(90,55),(82,51),(75,48),(72,43)]
def helmet(bare):
 donor=Image.open(DONOR).convert('RGBA');mask=Image.new('L',donor.size);ImageDraw.Draw(mask).polygon(POLYGON,fill=255)
 a=np.array(donor);a[:,:,3]=np.minimum(a[:,:,3],np.array(mask));a[a[:,:,3]==0]=0;component=Image.fromarray(a)
 b=np.array(bare);x,y=CROWN;ox,oy=x-93,y-27;chin=49+oy
 erase=Image.new('L',(320,320));ImageDraw.Draw(erase).polygon([(x-17,y-3),(x+16,y-3),(x+16,y+23),(x-2,y+27),(x-18,y+17)],fill=255)
 e=np.array(erase)>0;out=b.copy();out[e]=0;result=Image.fromarray(out);result.alpha_composite(component,(ox,oy));out=np.array(result)
 yy,xx=np.indices((320,320));fg=((yy>=chin+3)&(xx>=x+6)|(yy>=y+18)&(xx<=x-5))&(b[:,:,3]>0);out[fg]=b[fg]
 region=Image.new('L',(320,320));region.paste(mask,(ox,oy));allowed=e|(np.array(region)>0)
 assert np.array_equal(out[~allowed],b[~allowed]) and np.array_equal(out[fg],b[fg]) and np.array_equal(out[yy>=oy+59],b[yy>=oy+59])
 component.save(P/'sources/canonical-helmet-component.png')
 return Image.fromarray(out)
def main():
 raw=Image.open(SOURCE).convert('RGBA');a=np.array(raw);assert raw.size==(1254,1254)
 labs,_=label(a[:,:,3]>250);counts=np.bincount(labs.ravel());n=int(np.argmax(counts[1:])+1)
 mask=binary_dilation(labs==n,iterations=3)&(a[:,:,3]>0);a[~mask]=0
 scale=320/raw.width;mid=Image.fromarray(a).resize((320,320),Image.Resampling.LANCZOS)
 aligned=Image.new('RGBA',(320,320));aligned.paste(mid,(-2,-1));mid=aligned
 mids={'bare':mid,'helmet':helmet(mid)};banks={};hashes={}
 for gear in ['bare','helmet']:
  original=[Image.open(OLD/gear/f'frames/land-swim-east/{i:03}.png').convert('RGBA') for i in range(6)]
  frames=original[:3]+[mids[gear]]+original[3:];mapping=[0,1,2,4,5,6]
  for old_i,new_i in enumerate(mapping):assert frames[new_i].tobytes()==original[old_i].tobytes()
  manifest=copy.deepcopy(json.loads((OLD/gear/'manifest.json').read_text()));manifest['name']='Bill East articulated lift midpoint — '+gear;manifest['status']='source_lift_trial_unselected'
  s=manifest['states'][0];s['frameFiles']=[];s['frameDurationsMs']=TIMES;s['facings']=['east']*7;s['provenance']='Six V4 poses exact. One new whole-body lift at fixed320/1254 authoring-canvas scale with whole-pose(-2,-1) registration; helmet uses original scale1 native component. Original100ms crouch hold split50+50, total500ms. No normal admission.'
  for i,im in enumerate(frames):
   f=P/gear/'frames/land-swim-east'/f'{i:03}.png';f.parent.mkdir(parents=True,exist_ok=True);im.save(f);s['frameFiles'].append(f'frames/land-swim-east/{i:03}.png');hashes[f.relative_to(P).as_posix()]=hashlib.sha256(f.read_bytes()).hexdigest()
  (P/gear/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
  f=P/gear/'source-enter.png';frames[0].save(f,save_all=True,append_images=frames[1:],duration=TIMES,loop=0,disposal=0,blend=0)
  with Image.open(f) as apng:
   assert apng.n_frames==7
   for i,im in enumerate(frames):apng.seek(i);assert apng.convert('RGBA').tobytes()==im.tobytes() and apng.info['duration']==TIMES[i]
  banks[gear]=frames
 master=Image.open(OLD/'master-contact-review.png').crop((0,25,320,345));board=Image.new('RGB',(2560,720),'#182932');d=ImageDraw.Draw(board)
 for row,gear in enumerate(['bare','helmet']):
  y=row*360+25;board.paste(master,(0,y));d.text((4,row*360+3),'Original master / common148 ruler',fill='white')
  for i,im in enumerate(banks[gear]):
   x=(i+1)*320;board.paste(im,(x,y),im);d.text((x+4,row*360+3),gear+' '+str(i)+(' new articulated lift' if i==3 else ' exact V4'),fill='white')
   if i<3:d.line((x,y+224,x+319,y+224),fill='#6aa39e',width=1)
 board.save(P/'master-lift-review.png')
 detail=Image.new('RGB',(1280,660),'#182932');d=ImageDraw.Draw(detail)
 for row,gear in enumerate(['bare','helmet']):
  for col,i in enumerate([2,3,4]):
   im=banks[gear][i].crop((50,70,250,260)).resize((320,304),Image.Resampling.NEAREST);detail.paste(im,(col*400,row*330+24),im);d.text((col*400+4,row*330+4),gear+' '+str(i),fill='white')
 detail.save(P/'lift-detail-review.png')
 e={'generation':'exec-717e0171-0783-4e10-9f6b-4de5c5b98f84','sourceSHA256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'actualRawSize':list(raw.size),'scale':scale,'scaleRule':'Uniform full authoring canvas to320, reference poses were exact4x1280 canvases; actual tool output1254 accounted for. No per-pose bounding-box/head-size normalization.','wholePoseTranslation':[-2,-1],'logicalCrown':list(CROWN),'alphaCoreThresholdExclusive':250,'fringePixels':3,
  'grade':'Generated against already graded neighboring sources/master; no old unrelated raw neutral curve reapplied. Pending comparative material acceptance.','preservedV4ToV5':[0,1,2,4,5,6],'twelveOriginalPosesRGBAExact':True,'APNGDecodedFramesExact':14,'timelineMs':500,'durations':TIMES,'crownRegistration':[ [171,82],[177,91],[180,124],[183,157],[187,188] ],'crouchToBuoyantGapsPx':[33,33],
  'helmetDonor':DONOR.relative_to(R).as_posix(),'helmetScale':1,'helmetRotation':0,'newHelmetBodyOutsideExplicitHeadRegionExact':True,'foregroundArmShoulderExact':True,'frameSHA256':hashes,
  'rejectedSources':[{'generation':'exec-f2abd627-d734-4a27-b18d-0871c9962c41','file':'sources/rejected-large-lift-v1.png','reason':'Oversized figure/head; requested source scale ignored.'},{'generation':'exec-1eb9dd99-bb25-4fa2-8c02-ab2cdcedfc73','file':'sources/rejected-layout-lift-v2.png','reason':'Still oversized relative to shared source ruler.'}],
  'scope':'Source-only articulated midpoint trial. Native physical support/buoyancy/material/head/collision, moving endpoint phases and interruption/Continue on new source bank not verified. Normal and earlier staged runtime selectors unchanged.'}
 (P/'review.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
 (P/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Bill articulated water lift</title><style>body{background:#182932;color:#eef;font:16px sans-serif}img{max-width:100%}</style><h1>Bill East — authored lift midpoint trial</h1><p>'+e['scope']+'</p><img src="master-lift-review.png"><img src="lift-detail-review.png"><img src="bare/source-enter.png"><img src="helmet/source-enter.png">',encoding='utf-8')
 print(json.dumps({'rawSize':raw.size,'canvasScale':scale,'preservedOriginalPoses':12,'newPairedMidpoints':2,'exactAPNGFrames':14,'durationMs':500,'crownGaps':[33,33]}))
if __name__=='__main__':main()
