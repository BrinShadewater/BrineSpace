"""Independent native boot-material tracking and complete ground chronology."""
from pathlib import Path
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import json
import numpy as np
from scipy.signal import correlate2d
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[2];N=R/'output/veld-east-phase-probe-v1'
records=json.loads((N/'records.json').read_text(encoding='utf-8'))['records']
reports=[]

def point_track(images,rows,anchor,bounds,start,end,height):
    scale=height/148;floor=565 if height==148 else 330
    ar=next(r for r in rows if r['rawSlot']==anchor)
    root=120+ar['travelWorld']*height/65.28
    x0,y0,x1,y1=bounds
    bx0=round(root+(x0-128)*scale);bx1=round(root+(x1-128)*scale)
    by0=round(floor+(y0-224)*scale);by1=round(floor+(y1-224)*scale)
    template=images[anchor][by0:by1,bx0:bx1].mean(axis=2)
    t=template-template.mean();energy=float((t*t).sum())
    output=[]
    for slot in range(start,end+1):
        data=images[slot].mean(axis=2)
        left=bx0-18;top=by0-8
        search=data[top:by1+9,left:bx1+19]
        one=np.ones(template.shape)
        sums=correlate2d(search,one,mode='valid');squared=correlate2d(search*search,one,mode='valid')
        cov=correlate2d(search,t,mode='valid')
        score=cov/np.sqrt(np.maximum(1e-6,squared-sums*sums/template.size)*energy)
        yy,xx=np.unravel_index(np.argmax(score),score.shape)
        dx=0.0
        if 0<xx<score.shape[1]-1:
            a,b,c=score[yy,xx-1:xx+2];denom=a-2*b+c
            if abs(denom)>1e-8:dx=float(np.clip(.5*(a-c)/denom,-.5,.5))
        output.append({'rawSlot':slot,'screenX':float(left+xx+dx+template.shape[1]/2),'screenY':float(top+yy+template.shape[0]/2),'correlation':float(score[yy,xx]),'atSearchBorder':bool(xx in [0,score.shape[1]-1] or yy in [0,score.shape[0]-1])})
    flat=[r for r in output if (19<=r['rawSlot']<=25) or (38<=r['rawSlot']<=44)]
    return {'anchorRawSlot':anchor,'nativeBoundsAtAnchor':[bx0,by0,bx1,by1],'rows':output,'shortFlatWindowSpanScreenPixels':max(r['screenX'] for r in flat)-min(r['screenX'] for r in flat),'shortFlatMinimumCorrelation':min(r['correlation'] for r in flat),'extendedMinimumCorrelation':min(r['correlation'] for r in output),'extendedPointSpanScreenPixels':max(r['screenX'] for r in output)-min(r['screenX'] for r in output)}

for trial,label in enumerate(['uniform','paced']):
    for gear in ['bare','helmet']:
        rows=[r for r in records if r['trial']==trial and r['gear']==gear and 1<=r['sample']<=37]
        images={r['rawSlot']:np.asarray(Image.open(N/(r['name']+'-native.png')).convert('RGB'),dtype=float) for r in rows}
        for height in [93,148]:
            tracks=[]
            for anchor,start,end,toe,ankle in [(21,18,29,(136,212,146,218),(131,207,137,214)),(40,34,48,(143,211,153,217),(138,205,144,212))]:
                for name,bounds in [('toeCap',toe),('ankleStrap',ankle)]:
                    track=point_track(images,rows,anchor,bounds,start,end,height);track['material']=name;tracks.append(track)
            reports.append({'timing':label,'gear':gear,'height':height,'tracks':tracks})
            board=Image.new('RGB',(1300,740),'#202a30');draw=ImageDraw.Draw(board)
            for j,slot in enumerate(list(range(18,30))+list(range(34,49))):
                row=next(r for r in rows if r['rawSlot']==slot);root=120+row['travelWorld']*height/65.28;floor=565 if height==148 else 330
                # Common screen X crop for every source: preserves ground-relative motion.
                crop=(95,floor-42,360,floor+7)
                im=Image.fromarray(images[slot].astype('uint8')).crop(crop)
                xy=((j%4)*325,(j//4)*100+28);board.paste(im,xy)
                draw.text((xy[0],xy[1]-18),f'{label} {gear} {height}px raw{slot}',fill='white')
                for track in tracks:
                    for point in track['rows']:
                        if point['rawSlot']!=slot:continue
                        col='#70d7e0' if track['material']=='toeCap' else '#f4cb75'
                        cx=xy[0]+point['screenX']-crop[0];cy=xy[1]+point['screenY']-crop[1]
                        draw.ellipse((cx-2,cy-2,cx+2,cy+2),outline=col)
            board.save(P/f'rendered-{gear}-{label}-{height}-contact-review.png')

# Full37-phase ground timeline, larger gameplay scale, source clock unchanged.
rows=[r for r in records if r['trial']==1 and r['gear']=='bare' and 1<=r['sample']<=37]
ground=[]
for b in range(3):
    board=Image.new('RGB',(960,840),'#202a30');d=ImageDraw.Draw(board)
    for k,r in enumerate(rows[b*13:(b+1)*13]):
        im=Image.open(N/(r['name']+'-native.png')).convert('RGB')
        root=120+r['travelWorld']*148/65.28
        # A conservative warm boot-material mask excludes blue-grey grid/floor.
        data=np.asarray(im);x0=round(root-70);x1=round(root+80)
        patch=data[530:573,x0:x1].astype(int)
        mask=(patch[:,:,0]>patch[:,:,1]+1)&(patch[:,:,0]>patch[:,:,2]+1)&(patch[:,:,0]>50)
        ys=np.where(mask)[0];bottom=int(ys.max()+530) if len(ys) else None
        ground.append({'rawSlot':r['rawSlot'],'lowestWarmBootMaterialScreenY':bottom,'floorScreenY':565,'gapMaterialToFloorPixels':None if bottom is None else 565-bottom,'scope':'Warm material sample, not full alpha silhouette or an identified heel/toe contact.'})
        strip=im.crop((80,520,400,575)).resize((960,165),Image.Resampling.NEAREST)
        # Diagnostic nearest-neighbour enlargement only, not runtime artwork.
        y=(k%4)*205+25
        if k<4:
            board.paste(strip,(0,y));d.text((5,y-19),f"raw{r['rawSlot']} warm-material floor gap {565-bottom if bottom is not None else 'unknown'}px",fill='white')
    # All13 phases require separate compact strips, preserve actual screen X.
    board=Image.new('RGB',(960,13*80+35),'#202a30');d=ImageDraw.Draw(board)
    for k,r in enumerate(rows[b*13:(b+1)*13]):
        im=Image.open(N/(r['name']+'-native.png')).crop((80,520,400,575))
        board.paste(im,(10,k*80+25));d.text((350,k*80+30),f"raw{r['rawSlot']} / native148px / actual ground-relative X",fill='white')
    board.save(P/f'rendered-full-ground-chronology-{b:02d}.png')

report={'scope':'Independent luminance matching on captured native pixels, first complete cycle, both gears at93/148. Raw-source positions initialize anchor template only; all other measurements use rendered screenshots. Larger windows include rotation/occlusion: point motion is not automatically sliding. Correlation alone cannot prove near/far identity or heel/toe contact. Warm-material floor diagnostic cannot certify full sole geometry.','nativeInputs':'output/veld-east-phase-probe-v1/records.json','tracking':reports,'full37PhaseWarmMaterialFloor':ground,'visualReview':'Pending overlay, ground chronology and occlusion assessment.','fullContactAccepted':False}
(P/'rendered-contact-audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'comparisons':[{'timing':r['timing'],'gear':r['gear'],'height':r['height'],'maxFlatSpan':max(t['shortFlatWindowSpanScreenPixels'] for t in r['tracks']),'minimumFlatCorrelation':min(t['shortFlatMinimumCorrelation'] for t in r['tracks']),'minimumExtendedCorrelation':min(t['extendedMinimumCorrelation'] for t in r['tracks'])} for r in reports],'floorMaterialGapRange':[min(r['gapMaterialToFloorPixels'] for r in ground if r['gapMaterialToFloorPixels'] is not None),max(r['gapMaterialToFloorPixels'] for r in ground if r['gapMaterialToFloorPixels'] is not None)],'fullContactAccepted':False}))
