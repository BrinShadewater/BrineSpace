from pathlib import Path
from PIL import Image,ImageDraw
import json,numpy as np,hashlib
P=Path(__file__).resolve().parent;R=P.parents[2];O=R/'output/veld-east-grounded-flat-probe-v1'
records=json.loads((O/'records.json').read_text())['records'];roles=json.loads((P/'refined-flat-sole-diagnostic.json').read_text())['roles'];results=[]
board=Image.new('RGB',(1200,1280),(32,43,49));d=ImageDraw.Draw(board)
for trial in [0,1]:
 for ri,role in enumerate(roles):
  rawrows=role['rows'];rows=[r for r in records if r['trial']==trial and r['gear']=='bare' and 1<=r['sample']<=21 and r['rawSlot'] in [x['frame'] for x in rawrows]]
  anchor=next(r for r in rows if r['rawSlot']==rawrows[1]['frame']);ax=120+anchor['travelWorld']*148/65.28;matches=[]
  for j,record in enumerate(rows):
   source=next(x for x in rawrows if x['frame']==record['rawSlot']);root=120+record['travelWorld']*148/65.28;left,right=source['soleEnvelopeXBounds'];bottom=source['opaqueBottomY'];sx=root+left-128;ex=root+right-128;sy=565+bottom-224
   im=Image.open(O/(record['name']+'-native.png')).convert('RGB');a=np.array(im).astype(float)
   # A frozen two-screen-row band at the predicted source silhouette plane.
   # Colour-distance extraction measures rendered outline independently, while
   # source geometry only supplies the small search region; floor grid excluded.
   y0=int(np.floor(sy))-1;y1=int(np.floor(sy))+1;x0=int(np.floor(sx))-4;x1=int(np.ceil(ex))+5
   region=a[y0:y1,x0:x1];mask=np.max(np.abs(region-np.array([32,42,48])),axis=2)>15
   for colour in [[114,135,146],[83,101,111]]:mask &= np.max(np.abs(region-np.array(colour)),axis=2)>4
   yy,xx=np.where(mask);assert len(xx)>3
   bounds=[int(x0+xx.min()),int(x0+xx.max())];matches.append({'rawSlot':record['rawSlot'],'screenEnvelopeBounds':bounds,'predictedBottomY':sy,'maskPixels':len(xx)})
   md=ImageDraw.Draw(im);md.line((bounds[0],sy,bounds[1],sy),fill=(110,220,155),width=1)
   crop=im.crop((round(ax-70),520,round(ax+30),580)).resize((300,180),Image.Resampling.NEAREST);xy=(j*300,(trial*2+ri)*320+35);board.paste(crop,xy)
   d.text((xy[0]+3,xy[1]-25),f"trial{trial} {role['role'].split()[0]} raw{record['rawSlot']}",fill='white');d.text((xy[0]+3,xy[1]+190),f"screen outline {bounds}",fill='white')
  results.append({'trial':trial,'role':role['role'],'height':148,'cycle':0,'matches':matches,'rearScreenSpan':max(m['screenEnvelopeBounds'][0] for m in matches)-min(m['screenEnvelopeBounds'][0] for m in matches),'frontScreenSpan':max(m['screenEnvelopeBounds'][1] for m in matches)-min(m['screenEnvelopeBounds'][1] for m in matches)})
board.save(P/'rendered-flat-outline-review.png')
frozen=json.loads((O/'inputs-after.json').read_text());assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in frozen.items())
report={'windows':results,'nativeInputsUnchanged':len(frozen),'scope':'Four-frame first-cycle bare148px native outline regions. Actual screenshot colour-distance foreground; search region from frozen source silhouette projection. Two-row outline bands are not anatomical toe/heel/contact proof; rounded silhouette/pitch and antialiasing change rear edge. No source/root edits or final admission.'}
(P/'rendered-flat-outline-diagnostic.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps([{'trial':r['trial'],'role':r['role'],'frontSpan':r['frontScreenSpan'],'rearSpan':r['rearScreenSpan']} for r in results]))
