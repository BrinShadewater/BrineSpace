from repair_sources import *
import math,copy
O=R/'character/krusher-continuity-bank-v1';(O/'frames').mkdir(parents=True,exist_ok=True);(O/'edit-masks').mkdir(exist_ok=True)
base=R/'character/krusher-animation-package-v9';package=read(base/'package.json');replacements={};reports=[];findings=[];presets={}
def add(ids,name,delta,cleanup=0,closed=False):
 for cid in ids:presets[idx['crops'][cid]['sourceDrawing']]={'cropId':cid,'name':name+('-closed' if closed else ''),'delta':delta,'cleanup':cleanup}
add(range(1355,1358),'pickup-east',[3,4]);add(list(range(1395,1400))+list(range(1415,1420)),'meal-west',[-1,-1]);add(range(1428,1437),'prone-south',[-1,0],38);add(range(1504,1506),'collapse-south',[-1,0],38);add(range(1524,1529),'prone-south',[0,0],38);add(range(1543,1548),'collapse-south',[0,4],0,True);add(range(1565,1571),'collapse-south',[0,0],46,True)
rear_sources={idx['crops'][i]['sourceDrawing'] for i in rear};portrait_sources={idx['crops'][i]['sourceDrawing']:i for i in polygons}
# Additional views of the same bent-visor family use translated observed visor contours.
for cid in [3110,3111,3206]:
 q=records[idx['crops'][cid]['sourceDrawing']];reference=3109 if cid<3200 else 3207;refq=records[idx['crops'][reference]['sourceDrawing']];delta=np.array(q['newPaste'])-np.array(refq['newPaste']);polygons[cid]=(np.array(polygons[reference])+delta).tolist();portrait_sources[q['source']]=cid
for source,q in records.items():
 oldrel='frames/'+q['outputHash']+'.png';a=Image.open(base/oldrel).convert('RGBA');before=np.array(a);b=before.copy();mask=np.zeros(before.shape[:2],bool);meta=maps[source];info={'source':oldrel,'sourceRaw':source,'example':q['example'],'exampleFrame':q['exampleFrame'],'gear':q['gear'],'canvas':q['canvas'],'pivot':q['pivot'],'mode':'Unchanged V9 drawing'}
 if source in presets or source in rear_sources or source in portrait_sources:
  original=pad(Image.open(R/meta['originalBody']).convert('RGBA'),q);maskpath=meta.get('mask') if source in rear_sources else meta['details'].get('portraitMask') or meta.get('mask');mi=Image.open(R/maskpath.removeprefix('res://')).convert('L');mask=np.array(mi)>0
  if mask.shape!=b.shape[:2]:
   expanded=Image.new('L',a.size);expanded.paste(mi,(36,52));mask=np.array(expanded)>0
  if source in rear_sources or source in portrait_sources:
   restored=cyan(np.array(original));b[mask]=restored[mask];info['mode']='Original helmet/body restored; false portrait on shoulder/back removed'
   if source in portrait_sources:
    cid=portrait_sources[source];pm=Image.new('L',a.size);ImageDraw.Draw(pm).polygon([tuple(v) for v in polygons[cid]],fill=255);ap=np.array(pm)>0;head=Image.open(R/q['newHead']).convert('RGBA')
    if cid==3379:head=Image.open(R/'character/krusher-style-neck-v1/sources/style-east-native.png').convert('RGBA')
    ha=np.array(head);r,g,bl=[ha[:,:,i].astype(float) for i in range(3)];skin=(ha[:,:,3]>150)&(r>g*1.09)&(r>bl*1.15)&(r>65);ys,xs=np.where(skin);center=np.array([xs.mean(),ys.mean()]);ys,xs=np.where(ap);target=np.array([xs.mean(),ys.mean()]);at=np.rint(target-center).astype(int);b[ap,:3]=[29,33,34];layer=Image.new('RGBA',a.size);layer.alpha_composite(head,tuple(at));merged=np.array(Image.alpha_composite(Image.fromarray(b),layer));b[ap,:3]=merged[ap,:3];mask|=ap;info.update({'mode':'Full observed visor aperture, rim preserved; no cyan face remnants','portraitPolygon':polygons[cid],'newPaste':at.tolist(),'newHead':q['newHead'] if cid!=3379 else 'character/krusher-style-neck-v1/sources/style-east-native.png'})
  else:
   spec=presets[source];raw=np.array(original);rr,gg,bb=[raw[:,:,k].astype(float) for k in range(3)];yy,xx=np.indices(mask.shape);x0,y0=q['newPaste'];oldhead=Image.open(R/q['newHead']).convert('RGBA');cx=x0+oldhead.width/2
   if spec['cleanup']:
    skin=(raw[:,:,3]>120)&(rr>gg*1.06)&(rr>bb*1.1)&((rr-gg)>(gg-bb)*.75)&(rr>30)&(abs(xx-cx)<11)&(yy>=y0+8)&(yy<y0+spec['cleanup']);sy,sx=np.where(skin)
    if len(sx)>4:
     pts=np.array(list(zip(sx,sy)));hull=ConvexHull(pts);extra=Image.new('L',a.size);ImageDraw.Draw(extra).polygon([tuple(pts[k]) for k in hull.vertices],fill=255);mask|=ndimage.binary_dilation(np.array(extra)>0,iterations=1)
   head=Image.open(H/('integrated-'+spec['name']+'-native.png')).convert('RGBA');angle=q.get('rotationDegrees',0);t=math.radians(angle);rot=np.array([[math.cos(t),math.sin(t)],[-math.sin(t),math.cos(t)]]);oldrot=oldhead.rotate(angle,expand=True);vector=np.array(head.size)/2+spec['delta']-np.array(oldhead.size)/2;center=np.array(q['newPaste'])+np.array(oldrot.size)/2;head=head.rotate(angle,resample=Image.Resampling.BICUBIC,expand=True) if angle else head;at=np.rint(center+rot@vector-np.array(head.size)/2).astype(int);b[mask]=0;layer=Image.new('RGBA',a.size);layer.alpha_composite(head,tuple(at));b=np.array(Image.alpha_composite(Image.fromarray(b),layer));mask|=np.array(layer)[:,:,3]>0
   if spec['cleanup']:
    warm=(rr>gg*1.06)&(rr>bb*1.1);restore=mask&(raw[:,:,3]>0)&(b[:,:,3]==0)&~warm;restored=cyan(raw);b[restore]=restored[restore]
   # Test the authored head's visible skin against the whole opaque body, not just a nominal anchor.
   ha=np.array(layer);hr,hg,hb=[ha[:,:,k].astype(float) for k in range(3)];hm=(ha[:,:,3]>220)&(hr>hg*1.09)&(hr>hb*1.15)&(hr>65);labels,_=ndimage.label(b[:,:,3]>180);areas=np.bincount(labels.ravel());areas[0]=0;attached=bool(hm.any() and np.all(labels[hm]==areas.argmax()))
   if not attached:findings.append({'source':source,'example':q['example'],'cropId':spec['cropId'],'kind':'Head skin attachment'})
   info.update({'mode':'Authored integrated head/neck/collar repair','newHead':(H/('integrated-'+spec['name']+'-native.png')).relative_to(R).as_posix(),'newPaste':at.tolist(),'rotationDegrees':angle,'attached':attached,'cleanup':spec['cleanup']})
 # Remove observed gold flashes in turns/distress and west reclining collars with the existing material mapping.
 if '-turn-' in q['example'] or q['example'].endswith(':swim-distress-south') or q['example'].endswith(':sleep-west') or q['example'].endswith(':lie-down-west'):
  protected=np.array(Image.open(B/q['mask']).convert('L'))>0
  if source in presets or source in portrait_sources:protected|=mask
  converted=cyan(b);paint=np.any(converted!=b,2)&~protected;mask|=paint;b[paint]=converted[paint];info['accentPixels']=int(paint.sum())
 assert np.array_equal(before[~mask],b[~mask]),q['example'];changed=int(np.any(before!=b,2).sum())
 if changed:
  digest=hashlib.sha256(b.tobytes()+str(b.shape).encode()).hexdigest();dest=O/'frames'/(digest+'.png');Image.fromarray(b).save(dest);mp=O/'edit-masks'/(Path(oldrel).stem+'.png');Image.fromarray(mask.astype('uint8')*255).save(mp);replacements[oldrel]='res://'+dest.relative_to(R).as_posix();info.update({'output':dest.relative_to(O).as_posix(),'mask':mp.relative_to(O).as_posix(),'outputHash':hashlib.sha256(dest.read_bytes()).hexdigest()})
 else:replacements[oldrel]='res://'+(base/oldrel).relative_to(R).as_posix();info['outputUnchanged']=oldrel
 info.update({'changedPixels':changed,'outsideRepairMaskExact':True});reports.append(info)
index={'candidatePacks':{'bare':[],'helmet':[]}}
for gear,paths in package['candidatePacks'].items():
 for number,path in enumerate(paths):
  mp=R/path[6:];m=read(mp)
  for state in m['states']:state['frameFiles']=[replacements[(mp.parent/f).resolve().relative_to(base.resolve()).as_posix()] for f in state['frameFiles']]
  dest=O/'packs'/f'{gear}-{number:02d}.json';dest.parent.mkdir(exist_ok=True);dest.write_text(json.dumps(m,indent=2)+'\n');index['candidatePacks'][gear].append('res://'+dest.relative_to(R).as_posix())
(O/'candidate-bank-index.json').write_text(json.dumps(index,indent=2)+'\n');(O/'revision.json').write_text(json.dumps({'baseline':'V9','status':'Full continuity repair candidate; final review pending','records':reports,'findings':findings},indent=2)+'\n');(H/'candidate-bank-index.json').write_text(json.dumps(index,indent=2)+'\n');print(json.dumps({'drawings':len(reports),'changed':sum(q['changedPixels']>0 for q in reports),'authoredBareRepairs':len(presets),'correctedHelmetPortraits':len(portrait_sources),'rearHelmetRepairs':len(rear_sources),'findings':findings}))
