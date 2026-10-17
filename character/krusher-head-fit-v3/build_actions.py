from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from scipy.ndimage import distance_transform_edt,binary_dilation,label
import numpy as np,json,hashlib,sys
R=Path.cwd();H=R/'character/krusher-head-fit-v3';C=R/'character/krusher-james-canonical-v6'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def arr(p):return np.array(Image.open(p).convert('RGBA'))
def read(p):return json.loads(p.read_text())
idle={(g,d):arr(C/next(s for s in read(C/(g+'-manifest.json'))['states'] if s['id']=='idle-'+d)['frameFiles'][0]) for g in ['bare','helmet'] for d in ['east','west','south','north']}
for family in sys.argv[1:] or ['repair','torch','seated']:
 old=R/f'character/krusher-{family}-family-v1';P=R/f'character/krusher-{family}-family-v3';P.mkdir(exist_ok=True);records=[]
 for q in read(old/'provenance.json')['records']:
  g=q['gear'];d=q['state'].rsplit('-',1)[1];a=arr(old/q['output']);out=a.copy();hh,ww=a.shape[:2];yy,xx=np.indices((hh,ww));mask=np.zeros((hh,ww),bool);details={};protected=150
  if q['method'].startswith('Exact complete'):
   out=np.zeros_like(a);out[:184,:184]=idle[g,d];mask=np.any(a!=out,axis=2);details={'canonicalEndpoint':d}
  elif d!='north':
   bowed=('side-heads' in q['headSource'] or 'bow-heads' in q['headSource']);kind='bare' if g=='bare' else 'visor';hp=H/'sources'/f'{kind}-{d}{"-bowed" if bowed else ""}-native.png'
   head=Image.open(hp).convert('RGBA');details={'headSource':'res://'+hp.relative_to(R).as_posix(),'headHash':sha(hp),'bowed':bowed}
   if g=='bare':
    oldhead=Image.open(R/q['headSource']).convert('RGBA');ax,ay=q['headPaste'];x0,y0,x1,y1=q['headBox'];oldlayer=Image.new('RGBA',(ww,hh));oldlayer.paste(oldhead,(ax,ay));oldalpha=np.array(oldlayer)[:,:,3]>0
    # Original insertion was clipped at the body collar; remove only its actual
    # edited alpha. Never cut a broad ellipse through the real neck hardware.
    allowed=np.array(Image.open(old/q['allowedMask']))>0;oldalpha&=allowed;out[oldalpha]=0
    if bowed:newpaste=[ax-(head.width-oldhead.width)//2,ay+oldhead.height-head.height]
    else:newpaste=[ax-4 if d=='east' else ax+2 if d=='west' else ax-(head.width-oldhead.width)//2,ay]
    layer=Image.new('RGBA',(ww,hh));layer.paste(head,tuple(newpaste));ha=np.array(layer);opaque=ha[:,:,3]>0;out[opaque]=ha[opaque];mask=oldalpha|opaque;details.update(paste=newpaste,oldPaste=[ax,ay],oldHeadSource='res://'+q['headSource'],oldHeadHash=sha(R/q['headSource']))
   else:
    x0,y0,x1,y1=q['headBox'];orig=arr(R/q['source']);rgb=orig[:,:,:3].astype(float)
    # The original face is explicitly clipped to the helmet. Expand upward to
    # include the identity's hair/skull while retaining its glass/metal rim.
    warm=(orig[:,:,3]>180)&(rgb[:,:,0]>rgb[:,:,1]*1.1)&(rgb[:,:,0]>rgb[:,:,2]*1.12)&(xx>=x0)&(xx<x1)&(yy>=y0)&(yy<y1)
    base=warm;mask=binary_dilation(base,iterations=2)
    for dy in range(1,5):mask[:-dy]|=base[dy:]
    glass=(rgb[:,:,2]>rgb[:,:,0]*1.2)&(rgb[:,:,1]>rgb[:,:,0]*1.2);metal=(rgb.max(2)-rgb.min(2)<12)&(rgb.mean(2)>75)&(yy<y0)
    mask&=(xx>=x0-1)&(xx<x1+1)&(yy>=y0-4)&(yy<y1+1)&~glass&~metal&(a[:,:,3]>180)
    sy,sx=np.where(mask);box=[int(sx.min()),int(sy.min()),int(sx.max()+1),int(sy.max()+1)];part=np.array(head);nearest=distance_transform_edt(part[:,:,3]==0,return_distances=False,return_indices=True);part[:,:,:3]=part[nearest[0],nearest[1],:3];part[:,:,3]=255;im=Image.fromarray(part).resize((box[2]-box[0],box[3]-box[1]),Image.Resampling.NEAREST);layer=Image.new('RGBA',(ww,hh));layer.paste(im,(box[0],box[1]));out[mask,:3]=np.array(layer)[mask,:3];details.update(visorBox=box,glassAndUpperMetalProtected=True)
  assert np.array_equal(a[~mask],out[~mask]);assert np.array_equal(a[protected:],out[protected:])
  if g=='helmet':assert np.array_equal(a[:,:,3],out[:,:,3])
  target=P/q['output'];target.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(out).save(target);mr='head-masks/'+g+'/'+Path(q['output']).name;(P/mr).parent.mkdir(parents=True,exist_ok=True);Image.fromarray(mask.astype('uint8')*255).save(P/mr)
  records.append({'gear':g,'state':q['state'],'frame':q['frame'],'source':'res://'+(old/q['output']).relative_to(R).as_posix(),'sourceHash':sha(old/q['output']),'output':q['output'],'outputHash':sha(target),'mask':mr,'protectedFromRow':protected,'changedPixels':int(np.any(a!=out,2).sum()),'details':details})
 for g in ['bare','helmet']:(P/(g+'-manifest.json')).write_bytes((old/(g+'-manifest.json')).read_bytes())
 (P/'revision.json').write_text(json.dumps({'records':records,'scope':'Complete head/neck and full visor identity on original action bodies; root/state/manifest bytes exact. Rear retained. Staged partial full-library correction.'},indent=2)+'\n')
 (P/'pack-index.json').write_text(json.dumps({'candidatePacks':{g:['res://'+(P/(g+'-manifest.json')).relative_to(R).as_posix()] for g in ['bare','helmet']}},indent=2)+'\n')
 native=P/'native';native.mkdir(exist_ok=True);previous=R/f'character/krusher-{family}-family-v2'
 for name in ['verify.gd','review.gd']:(native/name).write_text((previous/'native'/name).read_text().replace(previous.name,P.name))
 for name in ['run_native_verify.py','run_native_review.py']:(P/name).write_text((previous/name).read_text().replace(previous.name,P.name))
 print(json.dumps({'family':family,'unique':len(records),'changed':sum(q['changedPixels']>0 for q in records)}))
