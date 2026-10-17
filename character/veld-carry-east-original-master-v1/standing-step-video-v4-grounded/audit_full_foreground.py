"""Independent complete foreground extent avoids losing a disconnected boot."""
from pathlib import Path
from PIL import Image,ImageDraw
from scipy import ndimage
import numpy as np,json
P=Path(__file__).resolve().parent; rows=[]
for n,file in enumerate(sorted((P/'raw-review').glob('raw-*.png'))):
 a=np.array(Image.open(file).convert('RGB')).astype(int);mask=np.abs(a-np.array([12,18,24])).max(2)>8
 labels,k=ndimage.label(mask);counts=np.bincount(labels.ravel());counts[0]=0
 kept=mask&(counts[labels]>=20);y,x=np.where(kept);bottom=int(y.max());main=np.where(labels==counts.argmax())[0].max()
 rows.append({'frame':n,'allForegroundBottomRaw':bottom,'projectedNativeFloor':(bottom+1)/3-32-1,'largestComponentBottomRaw':int(main),'omittedComponentExtentRaw':int(bottom-main),'componentCountAtLeast20':int((counts>=20).sum())})
indices=sorted(range(len(rows)),key=lambda i:rows[i]['projectedNativeFloor'])[:12]
board=Image.new('RGB',(1536,1040),(32,43,49));d=ImageDraw.Draw(board)
for j,n in enumerate(indices):
 raw=Image.open(P/'raw-review'/f'raw-{n:03}.png').convert('RGB');im=raw.crop((220,550,580,790)).resize((360,240),Image.Resampling.NEAREST)
 board.paste(im,((j%4)*384,(j//4)*340+50));y=round((32+223)*3+2)-550;d.line([(j%4*384,j//4*340+50+y),(j%4*384+360,j//4*340+50+y)],fill='red',width=1)
 d.text((j%4*384+5,j//4*340+10),f'Raw{n} full extent {rows[n]["projectedNativeFloor"]:.1f}',fill='white')
board.save(P/'lowest-full-source-boot-review.png')
report={'rows':rows,'minimumProjectedNativeFloor':min(r['projectedNativeFloor'] for r in rows),'maximumProjectedNativeFloor':max(r['projectedNativeFloor'] for r in rows),'largestComponentOmissionFrames':[r for r in rows if r['omittedComponentExtentRaw']>3],'scope':'Read-only complete raw foreground extent includes disconnected components20pixels or greater. Fixed background rule; no erosion, source resample or RGB/art repair. Projection uses original1/3 and -32. Extent alone is not physical boot identity/contact; lowest12 raw lower-body crops inspected separately. Red line is original near-floor223, far original floor220; this is a diagnostic overlay only.'}
(P/'full-foreground-diagnostic.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ['rows','scope']}))
