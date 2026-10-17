from pathlib import Path
from PIL import Image,ImageDraw
from scipy import ndimage
import json,numpy as np,hashlib
P=Path(__file__).resolve().parent;R=P.parents[2]
roll=json.loads((P/'boot-roll-diagnostic.json').read_text(encoding='utf-8'));frames=[np.array(Image.open(P/f'full-clip-frames/{n:03}.png').convert('RGBA')) for n in range(142)]
results=[]
for role in roll['roles']:
 rows=[]
 for match in role['rows']:
  n=match['frame'];cx=match['center'][0];a=frames[n]
  labels,k=ndimage.label(a[201:233,:,3]>200);parts=[]
  for index in range(1,k+1):
   y,x=np.where(labels==index)
   if len(x)>15:parts.append((abs(float(x.mean())-cx),index,int(x.min()),int(x.max()),len(x)))
  assert parts
  error,index,left,right,count=min(parts);assert error<18,'Boot component identity ambiguous'
  selected=labels==index;y,x=np.where(selected);bottom=int(y.max()+201)
  # A two-pixel sole band covers the rounded heel and toe in a flat pose.
  yy,xx=np.where(selected[max(0,bottom-1-201):bottom+1-201,:]);bounds=[int(xx.min()),int(xx.max())]
  root=(n-16)*2.8
  rows.append({'frame':n,'opaqueGroundY':bottom,'lowestTwoRowSourceXBounds':bounds,'rootPlusSoleBandXBounds':[bounds[0]+root,bounds[1]+root],'componentBoundsX':[left,right],'componentMergedWidthRisk':right-left>45,'componentIdentityCenterError':round(error,3),'rigidAppearanceNCC':match['NCC']})
 base=next(r for r in rows if r['frame']==role['templateFrame']);flat=base['rootPlusSoleBandXBounds'];floor=base['opaqueGroundY']
 for row in rows:
  wx=row['rootPlusSoleBandXBounds'];row['outsideFlatFootprintPixels']=max(0,flat[0]-wx[0],wx[1]-flat[1]);row['projectedFloorDelta']=row['opaqueGroundY']-floor
  row['onReferencePlaneWithinOnePixel']=abs(row['projectedFloorDelta'])<=1
 board=Image.new('RGB',(1500,900),(32,43,49));d=ImageDraw.Draw(board)
 for j,row in enumerate(rows):
  n=row['frame'];image=Image.fromarray(frames[n]).copy();md=ImageDraw.Draw(image);x0,x1=row['lowestTwoRowSourceXBounds'];y=row['opaqueGroundY'];md.line((x0,y,x1,y),fill=(116,218,155),width=1)
  crop=image.crop((65,185,190,233)).resize((250,96),Image.Resampling.NEAREST);xy=((j%6)*250,(j//6)*220+30);board.paste(crop,xy,crop)
  d.text((xy[0]+3,xy[1]-20),f"{role['role']} raw{n} floor{y}",fill='white');d.text((xy[0]+3,xy[1]+105),f"extra{row['outsideFlatFootprintPixels']:.1f}px {'plane' if row['onReferencePlaneWithinOnePixel'] else 'AIRBORNE'}",fill='white')
 board.save(P/f"{role['role']}-ground-outline-review-v2.png")
 contact=[r for r in rows if r['onReferencePlaneWithinOnePixel']]
 results.append({'role':role['role'],'templateFrame':role['templateFrame'],'flatRootPlusSourceFootprint':flat,'referenceProjectedFloorY':floor,'rows':rows,'maxOutsideFlatFootprintPixelsOnReferencePlane':max(r['outsideFlatFootprintPixels'] for r in contact),'projectedFloorDeltaRange':[min(r['projectedFloorDelta'] for r in rows),max(r['projectedFloorDelta'] for r in rows)],'offPlaneFrames':[r['frame'] for r in rows if not r['onReferencePlaneWithinOnePixel']]})
before=json.loads((R/'output/veld-east-native-stride-probe-v1/inputs-after.json').read_text(encoding='utf-8'));assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==sha for p,sha in before.items())
report={'roles':results,'nativeInputsStillStable':len(before),'supersedes':'ground-outline-diagnostic.json: rectangle overlapped the other boot at near32 and a single lowest row made the flat reference footprint too narrow. Its11.6px excess must not be treated as source-contact proof. Original evidence retained.','scope':'Connected opaque boot component nearest the inspected role center, two-row sole silhouette envelope. Merger/occlusion still limit leg identity; projected floor±1 tolerates quantization and is not literal physics. Presumed root2.8px/rawframe; footprint evidence diagnoses source shape/contact but cannot certify full rigid contact. No source/world/player/manifest edits.'}
(P/'ground-outline-diagnostic-v2.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps({'roles':[{'role':r['role'],'maxOutsideFootprintOnPlane':r['maxOutsideFlatFootprintPixelsOnReferencePlane'],'projectedFloorDeltaRange':r['projectedFloorDeltaRange'],'offPlaneFrames':r['offPlaneFrames']} for r in results],'inputsStillStable':len(before)}))
