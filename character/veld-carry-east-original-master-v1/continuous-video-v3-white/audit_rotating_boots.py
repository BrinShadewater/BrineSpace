"""Read-only native rigid rotation fit; annotated sole points remain diagnostic."""
from pathlib import Path
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import json,math
import numpy as np
from PIL import Image,ImageDraw
from scipy.signal import correlate2d
from scipy.ndimage import rotate
P=Path(__file__).resolve().parent;R=P.parents[2];N=R/'output/veld-east-phase-probe-v1'
records=json.loads((N/'records.json').read_text(encoding='utf-8'))['records']
comparisons=[];paired_checks=0
for trial,label in enumerate(['uniform','paced']):
    rows=[r for r in records if r['trial']==trial and r['gear']=='bare' and 1<=r['sample']<=37]
    images={r['rawSlot']:np.asarray(Image.open(N/(r['name']+'-native.png')).convert('RGB'),dtype=float) for r in rows}
    for r in rows:
        helmet=next(h for h in records if h['trial']==trial and h['gear']=='helmet' and h['sample']==r['sample'])
        hi=np.asarray(Image.open(N/(helmet['name']+'-native.png')).convert('RGB'),dtype=float)
        assert np.array_equal(hi[510:575],images[r['rawSlot']][510:575]);paired_checks+=1
    groups=[]
    for anchor,start,end,bounds,heel,toe in [
        (21,18,29,(128,203,155,225),(129,223),(153,223)),
        (40,34,48,(134,200,162,225),(135,223),(160,223))]:
        ar=next(r for r in rows if r['rawSlot']==anchor);root=120+ar['travelWorld']*148/65.28
        bx0,bx1=[round(root+x-128) for x in [bounds[0],bounds[2]]]
        by0,by1=[round(565+y-224) for y in [bounds[1],bounds[3]]]
        raw=images[anchor][by0:by1,bx0:bx1]
        template=raw.mean(axis=2);mask=((raw[:,:,0]>=raw[:,:,1])&(raw[:,:,0]>50)).astype(float)
        base_center=np.array([(template.shape[1]-1)/2,(template.shape[0]-1)/2])
        landmarks={'heel':np.array([root+heel[0]-128-bx0,565+heel[1]-224-by0])-base_center,
                   'toe':np.array([root+toe[0]-128-bx0,565+toe[1]-224-by0])-base_center}
        variants=[]
        for angle in range(-60,41,5):
            t=rotate(template,float(angle),reshape=True,order=1,mode='constant',cval=0,prefilter=False)
            m=rotate(mask,float(angle),reshape=True,order=0,mode='constant',cval=0,prefilter=False)
            count=float(m.sum());mean=float((t*m).sum()/count);centered=(t-mean)*m;energy=float((centered*centered).sum())
            rad=math.radians(angle);matrix=np.array([[math.cos(rad),math.sin(rad)],[-math.sin(rad),math.cos(rad)]])
            variants.append((angle,t,m,count,centered,energy,matrix))
        output=[]
        for slot in range(start,end+1):
            left=bx0-30;top=by0-25;search=images[slot][top:by1+26,left:bx1+31].mean(axis=2)
            best=None
            for angle,t,m,count,centered,energy,matrix in variants:
                sums=correlate2d(search,m,mode='valid');squared=correlate2d(search*search,m,mode='valid')
                cov=correlate2d(search,centered,mode='valid');score=cov/np.sqrt(np.maximum(1e-6,squared-sums*sums/count)*energy)
                yy,xx=np.unravel_index(np.argmax(score),score.shape);value=float(score[yy,xx])
                if best is None or value>best['correlation']:
                    dx=0.0
                    if 0<xx<score.shape[1]-1:
                        a,b,c=score[yy,xx-1:xx+2];denom=a-2*b+c
                        if abs(denom)>1e-8:dx=float(np.clip(.5*(a-c)/denom,-.5,.5))
                    center=np.array([left+xx+dx+(t.shape[1]-1)/2,top+yy+(t.shape[0]-1)/2])
                    best={'rawSlot':slot,'angleDegrees':angle,'correlation':value,'centerScreen':center.tolist(),
                          'heelScreen':(center+matrix@landmarks['heel']).tolist(),'toeScreen':(center+matrix@landmarks['toe']).tolist(),
                          'searchEdge':bool(xx in [0,score.shape[1]-1] or yy in [0,score.shape[0]-1]),'angleLimit':angle in [-60,40]}
            output.append(best)
        groups.append({'anchor':anchor,'rows':output,'heelAtAnchorSource':heel,'toeAtAnchorSource':toe,'scope':'Manually annotated heel/toe points transferred by best native rigid rotation fit. Rotation/shape deformation/occlusion can invalidate sole position. Not accepted physical contact.'})
    comparisons.append({'timing':label,'height':148,'boots':groups})
    board=Image.new('RGB',(1300,740),'#202a30');d=ImageDraw.Draw(board)
    for j,slot in enumerate(list(range(18,30))+list(range(34,49))):
        crop=(95,510,360,573);xy=((j%4)*325,(j//4)*100+28)
        board.paste(Image.fromarray(images[slot].astype('uint8')).crop(crop),xy)
        d.text((xy[0],xy[1]-18),f'{label} raw{slot} native148px',fill='white')
        for group in groups:
            for row in group['rows']:
                if row['rawSlot']!=slot:continue
                for key,col in [('heelScreen','#f4cb75'),('toeScreen','#70d7e0')]:
                    x=xy[0]+row[key][0]-crop[0];y=xy[1]+row[key][1]-crop[1]
                    d.ellipse((x-2,y-2,x+2,y+2),outline=col)
                d.text((xy[0]+175,xy[1]+35),f"{row['angleDegrees']}deg",fill='white')
                d.text((xy[0]+175,xy[1]+50),f"NCC {row['correlation']:.2f}",fill='white')
    board.save(P/f'rotating-boot-{label}-review.png')
report={'scope':'Independent native148px rigid rotation plus translation, first-cycle boot regions18..29 and34..48. Gear lower-body native equality verified74 comparisons; no repeat Godot run or altered source. Fitted sole points are not independently tracked physical landmarks: annotated sole geometry, redraw/deformation, occlusion and wrong-boot matches require visual inspection. Rotation confidence alone cannot certify contact.','pairedLowerBodyPixelChecks':paired_checks,'pairedLowerBodyFailures':0,'comparisons':comparisons,'visualReview':'Pending angle/sole overlay inspection.','fullContactAccepted':False}
(P/'rotating-boot-audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'pairedChecks':paired_checks,'comparisons':[{'timing':r['timing'],'angleRanges':[[min(x['angleDegrees'] for x in b['rows']),max(x['angleDegrees'] for x in b['rows'])] for b in r['boots']],'minimumConfidence':[min(x['correlation'] for x in b['rows']) for b in r['boots']]} for r in comparisons],'fullContactAccepted':False}))
