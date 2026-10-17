from pathlib import Path
from PIL import Image,ImageDraw
import json,numpy as np,hashlib
P=Path(__file__).resolve().parent;R=P.parents[2]
roll=json.loads((P/'boot-roll-diagnostic.json').read_text(encoding='utf-8'));frames=[np.array(Image.open(P/f'full-clip-frames/{n:03}.png').convert('RGBA')) for n in range(142)]
results=[]
for role in roll['roles']:
 rows=[]
 for match in role['rows']:
  n=match['frame'];cx=match['center'][0];left,right=max(0,cx-22),min(256,cx+23)
  a=frames[n];y,x=np.where(a[194:233,left:right,3]>200);bottom=int(y.max()+194)
  yy,xx=np.where(a[bottom:bottom+1,left:right,3]>200);bounds=[int(xx.min()+left),int(xx.max()+left)]
  root=(n-16)*2.8
  rows.append({'frame':n,'opaqueGroundY':bottom,'lowestRowSourceXBounds':bounds,'rootPlusLowestRowXBounds':[bounds[0]+root,bounds[1]+root],'bootIdentityWindowCenterX':cx,'rigidAppearanceNCC':match['NCC']})
 base=next(r for r in rows if r['frame']==role['templateFrame']);flat=base['rootPlusLowestRowXBounds'];floor=base['opaqueGroundY']
 for row in rows:
  wx=row['rootPlusLowestRowXBounds'];row['outsideFlatFootprintPixels']=max(0,flat[0]-wx[0],wx[1]-flat[1]);row['projectedFloorDelta']=row['opaqueGroundY']-floor
 board=Image.new('RGB',(1500,900),(32,43,49));d=ImageDraw.Draw(board)
 for j,row in enumerate(rows):
  n=row['frame'];image=Image.fromarray(frames[n]).copy();md=ImageDraw.Draw(image);x0,x1=row['lowestRowSourceXBounds'];y=row['opaqueGroundY'];md.line((x0,y,x1,y),fill=(116,218,155),width=1)
  crop=image.crop((65,185,190,233)).resize((250,96),Image.Resampling.NEAREST);xy=((j%6)*250,(j//6)*220+30);board.paste(crop,xy,crop)
  d.text((xy[0]+3,xy[1]-20),f"{role['role']} raw{n} floor{y}",fill='white');d.text((xy[0]+3,xy[1]+105),f"footprint extra{row['outsideFlatFootprintPixels']:.1f}px",fill='white')
 board.save(P/f"{role['role']}-ground-outline-review.png")
 results.append({'role':role['role'],'templateFrame':role['templateFrame'],'flatRootPlusSourceFootprint':flat,'referenceProjectedFloorY':floor,'rows':rows,'maxOutsideFlatFootprintPixels':max(r['outsideFlatFootprintPixels'] for r in rows),'projectedFloorDeltaRange':[min(r['projectedFloorDelta'] for r in rows),max(r['projectedFloorDelta'] for r in rows)]})
before=json.loads((R/'output/veld-east-native-stride-probe-v1/inputs-after.json').read_text(encoding='utf-8'));assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==sha for p,sha in before.items())
report={'roles':results,'nativeInputsStillStable':len(before),'scope':'Independent opaque lowest-row outline inside boot-identity windows, without treating material correspondence as physical points. Presumed root2.8px/rawframe; lowest-alpha outline is quantized artwork extent, not collision/ground geometry or literal anatomical sole. Window identity inherited from inspected roll fit: overlaps or hidden sole may invalidate it. Footprint envelope can diagnose contact shifts but cannot prove rigid heel/toe contact. No source/world/player edits.'}
(P/'ground-outline-diagnostic.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps({'roles':[{'role':r['role'],'maxOutsideFlatFootprintPixels':r['maxOutsideFlatFootprintPixels'],'projectedFloorDeltaRange':r['projectedFloorDeltaRange']} for r in results],'inputsStillStable':len(before)}))
