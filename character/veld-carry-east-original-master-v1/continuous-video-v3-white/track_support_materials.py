"""Read-only rigid-material patch diagnostics, not contact acceptance."""
from pathlib import Path
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import json
import numpy as np
from PIL import Image,ImageDraw
from scipy.signal import correlate2d

P=Path(__file__).resolve().parent
scale=159/768
frames=[np.asarray(Image.open(P/'raw-review'/f'raw-{i+1:03d}.png').convert('RGB'),dtype=float).mean(axis=2) for i in range(141)]

def track(anchor,bounds,start,end):
    # Bounds refer to native figure; convert using the unchanged whole plate mapping.
    x0,y0,x1,y1=bounds
    x0,x1=round((x0-53)/scale),round((x1-53)/scale)
    y0,y1=round((y0-46)/(212/1024)),round((y1-46)/(212/1024))
    template=frames[anchor][y0:y1,x0:x1]
    centered=template-template.mean(); energy=float((centered*centered).sum())
    rows=[]
    for i in range(start,end+1):
        left=max(0,x0-100);top=max(0,y0-12)
        search=frames[i][top:y1+13,left:x1+101]
        ones=np.ones(template.shape)
        sums=correlate2d(search,ones,mode='valid')
        squared=correlate2d(search*search,ones,mode='valid')
        covariance=correlate2d(search,centered,mode='valid')
        denominator=np.sqrt(np.maximum(1e-6,squared-sums*sums/template.size)*energy)
        scores=covariance/denominator
        yy,xx=np.unravel_index(np.argmax(scores),scores.shape)
        # Parabolic refinement on the sampled correlation peak only.
        dx=0.0
        if 0<xx<scores.shape[1]-1:
            a,b,c=scores[yy,xx-1:xx+2]
            denom=a-2*b+c
            if abs(denom)>1e-8:dx=float(np.clip(.5*(a-c)/denom,-.5,.5))
        rows.append({'frame':i,'rawX':float(left+xx+dx),'rawY':int(top+yy),'correlation':float(scores[yy,xx]),'nativeX':float((left+xx+dx)*scale+53)})
    t=np.array([r['frame'] for r in rows]);x=np.array([r['nativeX'] for r in rows])
    slope,intercept=np.polyfit(t,x,1);res=x-(slope*t+intercept)
    return {'templateNativeBounds':bounds,'anchorFrame':anchor,'rows':rows,'nativeBackwardPixelsPerFrame':float(-slope),'suggested37FrameTravelPixels':float(-slope*37),'linearResidualSpanNativePixels':float(np.ptp(res)),'minimumCorrelation':min(r['correlation'] for r in rows)}

windows=[]
for start,end,anchor,toe,heel in [
    (19,25,21,(136,212,146,218),(125,211,131,218)),
    (38,44,40,(143,211,153,217),(131,210,137,217)),
    (56,62,58,(135,212,145,218),(124,211,130,218))]:
    pair={'frames':[start,end],'toeCap':track(anchor,toe,start,end),'heelStrap':track(anchor,heel,start,end)}
    pair['toeHeelImpliedStrideDifferencePixels']=abs(pair['toeCap']['suggested37FrameTravelPixels']-pair['heelStrap']['suggested37FrameTravelPixels'])
    windows.append(pair)
report={'scope':'Three visually inspected flat-support windows only. Independent toe-cap and heel-strap luminance template matching on raw source at fixed scale. Material patches may deform or match another boot: inspect overlays and correlation. No full heel/toe roll, near/far continuity, floor contact or accepted stride.', 'candidatePeriodFrames':37,'windows':windows,'strideAccepted':False}
(P/'support-material-diagnostic.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
board=Image.new('RGB',(1400,900),'#202a30');draw=ImageDraw.Draw(board)
for w,pair in enumerate(windows):
    for k,i in enumerate(range(pair['frames'][0],pair['frames'][1]+1)):
        im=Image.open(P/'full-clip-frames'/f'{i:03d}.png').convert('RGBA').crop((95,195,170,230)).resize((180,84),Image.Resampling.NEAREST)
        xy=(k*200,w*290+35);board.paste(im,xy,im)
        draw.text((xy[0],xy[1]-20),f'raw{i}',fill='white')
        for key,col in [('toeCap','#70d7e0'),('heelStrap','#f4cb75')]:
            row=pair[key]['rows'][k];bounds=pair[key]['templateNativeBounds']
            nx=row['nativeX']+(bounds[2]-bounds[0])/2
            ny=row['rawY']*(212/1024)+46+(bounds[3]-bounds[1])/2
            cx=xy[0]+(nx-95)*2.4;cy=xy[1]+(ny-195)*2.4
            draw.ellipse((cx-3,cy-3,cx+3,cy+3),outline=col,width=2)
        draw.text((xy[0],xy[1]+96),f"toe {pair['toeCap']['rows'][k]['correlation']:.2f}",fill='#70d7e0')
        draw.text((xy[0],xy[1]+115),f"heel {pair['heelStrap']['rows'][k]['correlation']:.2f}",fill='#f4cb75')
board.save(P/'support-material-tracking-review.png')
print(json.dumps({'windows':[{'frames':w['frames'],'toeStride':w['toeCap']['suggested37FrameTravelPixels'],'heelStride':w['heelStrap']['suggested37FrameTravelPixels'],'difference':w['toeHeelImpliedStrideDifferencePixels'],'toeResidual':w['toeCap']['linearResidualSpanNativePixels'],'heelResidual':w['heelStrap']['linearResidualSpanNativePixels'],'minimumToeCorrelation':w['toeCap']['minimumCorrelation'],'minimumHeelCorrelation':w['heelStrap']['minimumCorrelation']} for w in windows],'strideAccepted':False}))
