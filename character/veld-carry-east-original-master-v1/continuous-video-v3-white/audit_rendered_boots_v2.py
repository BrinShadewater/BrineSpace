"""Broader masked native boot registration; retain failed tiny-patch diagnostic."""
from pathlib import Path
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import numpy as np
from scipy.signal import correlate2d
from PIL import Image,ImageDraw
import json
P=Path(__file__).resolve().parent;R=P.parents[2];N=R/'output/veld-east-phase-probe-v1'
records=json.loads((N/'records.json').read_text(encoding='utf-8'))['records']
results=[]
for trial,label in enumerate(['uniform','paced']):
    for gear in ['bare','helmet']:
        rows=[r for r in records if r['trial']==trial and r['gear']==gear and 1<=r['sample']<=37]
        images={r['rawSlot']:np.asarray(Image.open(N/(r['name']+'-native.png')).convert('RGB'),dtype=float) for r in rows}
        for height in [93,148]:
            groups=[]
            for anchor,start,end,bounds in [(21,18,29,(128,203,155,225)),(40,34,48,(134,200,162,225))]:
                scale=height/148;floor=565 if height==148 else 330
                ar=next(r for r in rows if r['rawSlot']==anchor);root=120+ar['travelWorld']*height/65.28
                bx0,bx1=[round(root+(x-128)*scale) for x in [bounds[0],bounds[2]]]
                by0,by1=[round(floor+(y-224)*scale) for y in [bounds[1],bounds[3]]]
                raw=images[anchor][by0:by1,bx0:bx1]
                mask=((raw[:,:,0]>=raw[:,:,1])&(raw[:,:,0]>50)).astype(float)
                assert mask.sum()>20
                template=raw.mean(axis=2);count=mask.sum();mean=(template*mask).sum()/count
                centered=(template-mean)*mask;energy=float((centered*centered).sum())
                output=[]
                for slot in range(start,end+1):
                    left=bx0-16;top=by0-7;search=images[slot][top:by1+8,left:bx1+17].mean(axis=2)
                    sums=correlate2d(search,mask,mode='valid');squared=correlate2d(search*search,mask,mode='valid')
                    cov=correlate2d(search,centered,mode='valid');score=cov/np.sqrt(np.maximum(1e-6,squared-sums*sums/count)*energy)
                    yy,xx=np.unravel_index(np.argmax(score),score.shape);dx=0.0
                    if 0<xx<score.shape[1]-1:
                        a,b,c=score[yy,xx-1:xx+2];denom=a-2*b+c
                        if abs(denom)>1e-8:dx=float(np.clip(.5*(a-c)/denom,-.5,.5))
                    output.append({'rawSlot':slot,'screenX':float(left+xx+dx),'screenY':float(top+yy),'correlation':float(score[yy,xx]),'searchEdge':bool(xx in [0,score.shape[1]-1] or yy in [0,score.shape[0]-1])})
                flat=[r for r in output if (19<=r['rawSlot']<=25) or (38<=r['rawSlot']<=44)]
                groups.append({'anchor':anchor,'boundsAtAnchor':[bx0,by0,bx1,by1],'bootMaterialPixels':int(count),'rows':output,'flatSpanScreenPixels':max(r['screenX'] for r in flat)-min(r['screenX'] for r in flat),'flatMinimumCorrelation':min(r['correlation'] for r in flat),'extendedMinimumCorrelation':min(r['correlation'] for r in output)})
            results.append({'timing':label,'gear':gear,'height':height,'boots':groups})
            board=Image.new('RGB',(1300,740),'#202a30');d=ImageDraw.Draw(board)
            for k,slot in enumerate(list(range(18,30))+list(range(34,49))):
                floor=565 if height==148 else 330;crop=(95,floor-42,360,floor+7)
                im=Image.fromarray(images[slot].astype('uint8')).crop(crop)
                xy=((k%4)*325,(k//4)*100+28);board.paste(im,xy);d.text((xy[0],xy[1]-18),f'{label} {gear} {height}px raw{slot}',fill='white')
                for group in groups:
                    for row in group['rows']:
                        if row['rawSlot']!=slot:continue
                        width=group['boundsAtAnchor'][2]-group['boundsAtAnchor'][0];h=group['boundsAtAnchor'][3]-group['boundsAtAnchor'][1]
                        x=xy[0]+row['screenX']-crop[0];y=xy[1]+row['screenY']-crop[1]
                        d.rectangle((x,y,x+width,y+h),outline='#70d7e0')
                        d.text((xy[0]+170,xy[1]+55),f"NCC {row['correlation']:.2f}",fill='white')
            board.save(P/f'rendered-boot-v2-{gear}-{label}-{height}.png')
report={'scope':'Independent masked native full-boot luminance registration; original tiny-detail failures retained. Template uses warm neutral material pixels excluding grid/background. Whole-boot translation is a proxy, not a rigid sole landmark. Rotation, deformation, occlusion and near/far swaps can invalidate matching; inspect overlays and confidence before using results.','comparisons':results,'visualReview':'Pending broad boot overlays.','fullContactAccepted':False}
(P/'rendered-boot-audit-v2.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'comparisons':[{'timing':r['timing'],'gear':r['gear'],'height':r['height'],'flatSpans':[b['flatSpanScreenPixels'] for b in r['boots']],'flatConfidence':[b['flatMinimumCorrelation'] for b in r['boots']],'extendedConfidence':[b['extendedMinimumCorrelation'] for b in r['boots']]} for r in results],'fullContactAccepted':False}))
