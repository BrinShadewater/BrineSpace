from pathlib import Path
import json,hashlib,copy
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from scipy.ndimage import label,binary_dilation

R=Path(__file__).resolve().parents[2];H=Path(__file__).resolve().parent
P=R/'character/krusher-animation-package-v2';O=R/'character/krusher-animation-package-v3'
for name in ['frames','packs','references','palette-masks']:(O/name).mkdir(parents=True,exist_ok=True)
read=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rows=read(H/'shoulder-palette-proposals.json');groups=read(H/'shoulder-palette-review-groups.json');selection=read(H/'shoulder-palette-selection.json');byfile={}
for gid in selection['selectedGroups']:
 for rid in groups[gid]['members']:byfile.setdefault(rows[rid]['file'],[]).append((gid,rows[rid]))
index=read(P/'package.json');mapping={};files={};records=[]
for rel in index['files']:
 src=P/rel;assert sha(src)==index['files'][rel]['sha256']
 a=np.array(Image.open(src).convert('RGBA'));b=a.copy();mask=np.zeros(a.shape[:2],bool)
 r,g,blue=[a[:,:,i].astype(float) for i in range(3)]
 gold=(r>g*1.06)&(r<g*1.55)&(g>blue*1.6)&(g>48)&(a[:,:,3]>180)
 bbox=Image.fromarray(a).getbbox();yy=np.indices(gold.shape)[0]
 gold&=(yy>bbox[1]+(bbox[3]-bbox[1])*.16)&(yy<bbox[1]+(bbox[3]-bbox[1])*.42)
 labels,count=label(gold,np.ones((3,3)))
 cyan=(r<g*.86)&(abs(g-blue)<25)&(g>50)&(a[:,:,3]>180)
 cyanlabels,cyancount=label(cyan,np.ones((3,3)))
 for gid,q in byfile.get(rel,[]):
  x0,y0,x1,y1=q['box'];matches=[]
  for component in set(labels[y0:y1,x0:x1].ravel())-{0}:
   local=labels==component;y,x=np.where(local)
   if int(local.sum())==q['area'] and [int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]==q['box']:matches.append(local)
  assert len(matches)==1,(rel,gid,'reviewed component changed')
  mask|=matches[0]
  # The reviewed patch includes pale gold edging which the conservative
  # discovery threshold omitted. Keep this extension within one pixel of
  # its inspected bounding rectangle; never expand across the whole sprite.
  rect=np.zeros_like(mask);rect[max(0,y0-1):min(mask.shape[0],y1+1),max(0,x0-1):min(mask.shape[1],x1+1)]=True
  # The same inspected shoulder panel can have disconnected gold badge
  # edging. Include the bounded adjacent cyan panel, never a body-wide hue.
  near=binary_dilation(matches[0],iterations=2);panels=[]
  for component in set(cyanlabels[near].ravel())-{0}:
   panel=cyanlabels==component;py,px=np.where(panel);score=int((panel&near).sum())
   if panel.sum()>=12 and px.max()-px.min()<32 and py.max()-py.min()<40:panels.append((score,int(px.min()),int(py.min()),int(px.max()+1),int(py.max()+1)))
  if panels:
   score,cx0,cy0,cx1,cy1=max(panels)
   rect[max(0,min(y0,cy0)-1):min(mask.shape[0],max(y1,cy1)+1),max(0,min(x0,cx0)-1):min(mask.shape[1],max(x1,cx1)+1)]=True
  warm=(r>g*1.015)&(r<g*1.8)&(g>blue*1.08)&(g>35)&(a[:,:,3]>180)
  mask|=rect&warm
 if mask.any():
  luminance=(r*.2126+g*.7152+blue*.0722)/145.0
  mapped=np.clip(luminance[:,:,None]*np.array([82,124,128]),0,177).astype('uint8')
  b[mask,:3]=mapped[mask]
  assert np.array_equal(a[~mask],b[~mask]) and np.array_equal(a[:,:,3],b[:,:,3])
  temp=O/'frames'/'palette-output.tmp.png';Image.fromarray(b).save(temp);digest=sha(temp);dst=O/'frames'/(digest+'.png');temp.replace(dst)
  maskrel='palette-masks/'+src.name;Image.fromarray(mask.astype('uint8')*255).save(O/maskrel)
  records.append({'source':rel,'sourceHash':sha(src),'output':'frames/'+dst.name,'outputHash':digest,'mask':maskrel,'pixels':int(mask.sum()),'groups':[gid for gid,q in byfile[rel]]})
 else:
  digest=sha(src);dst=O/'frames'/(digest+'.png');dst.write_bytes(src.read_bytes())
 mapping[rel]='frames/'+dst.name;files['frames/'+dst.name]={'sha256':digest,'bytes':dst.stat().st_size}
for gear,paths in index['candidatePacks'].items():
 index['candidatePacks'][gear]=[q.replace('krusher-animation-package-v2','krusher-animation-package-v3') for q in paths]
for rel in sorted(set(q['manifest'] for q in index['states'].values())):
 m=read(P/rel)
 for s in m['states']:s['frameFiles']=['../'+mapping['frames/'+Path(q).name] for q in s['frameFiles']]
 (O/rel).write_text(json.dumps(m,indent=2)+'\n')
for key,q in index['states'].items():
 q['paletteSourceManifest']='character/krusher-animation-package-v2/'+q['manifest']
for q in index['references']:q['frame']=mapping[q['frame']]
index['files']=files;index['status']='complete head-fit and reviewed shoulder palette candidate; final station review pending'
index['paletteRevision']={'sourcePackage':'res://character/krusher-animation-package-v2/package.json','report':'palette-revision.json','accent':'#527C80','method':'Explicit visually reviewed shoulder component masks; luminance preserves matte shading. No other pixels changed.'}
(O/'package.json').write_text(json.dumps(index,indent=2)+'\n');(O/'palette-revision.json').write_text(json.dumps({'records':records,'selection':selection,'scope':'Reviewed shoulder components only; all other RGBA pixels exact v2.'},indent=2)+'\n')
library=(P/'library.js').read_text()
for before,after in mapping.items():library=library.replace(before,after)
(O/'library.js').write_text(library);(O/'index.html').write_text((P/'index.html').read_text().replace('palette and station review remain','reviewed shoulder palette applied; final station review remains'))
(O/'README.md').write_text('# Krusher Dom complete animation candidate\n\nSystem Administrator / AI & Robotics. James utility suit; muted matte cyan #527C80. All586states and8058source slots preserve original render profiles and clocks. Corrected complete heads and explicitly reviewed shoulder recolouring. Open index.html. This candidate does not install a normal playable crew member; final station/Continue review remains. Rebuild with ../krusher-head-fit-v3/build_palette_package.py.\n')
font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),24);sheet=Image.new('RGBA',(1600,1030),'#252b2e');draw=ImageDraw.Draw(sheet)
draw.text((28,18),'KRUSHER DOM / SYSTEM ADMINISTRATOR',font=font,fill='white');draw.text((28,54),'AI & Robotics / James utility suit / matte muted cyan #527C80',font=font,fill='#b9d0d2')
for row,gear in enumerate(['bare','helmet']):
 for col,direction in enumerate(['south','east','north','west']):
  q=index['states'][gear+':idle-'+direction];m=read(O/q['manifest']);s=next(s for s in m['states'] if s['id']=='idle-'+direction);im=Image.open((O/q['manifest']).parent/s['frameFiles'][0]).convert('RGBA');x=col*400+16;y=row*445+118;sheet.alpha_composite(im.resize((im.width*2,im.height*2),Image.Resampling.NEAREST),(x,y));draw.text((x+10,y-30),direction.upper()+' / '+gear.upper(),font=font,fill='white')
sheet.save(O/'references/character-sheet.png')
print(json.dumps({'states':len(index['states']),'uniquePNG':len(files),'recolouredFrames':len(records),'recolouredPixels':sum(q['pixels'] for q in records)}))
