"""Frozen material calibration against selected idle, shared by both source sheets."""
import numpy as np
from scipy.ndimage import gaussian_filter,binary_erosion

def calibrate(raw,body,idle,authority='crew-runtime-matte-v1/bill/frames/idle-east-breathing-v1/000.png',facing='east'):
    rgb=raw[:,:,:3].astype(float);yy,xx=np.indices(body.shape);y,x=np.where(body)
    # Exclude the head and detached case from neutral suit calibration.
    valid=body&(raw[:,:,3]>200)&(yy>y.min()+85)&((rgb.max(2)-rgb.min(2))<25)
    a=np.asarray(idle);ar=a[:,:,:3].astype(float);ay,ax=np.indices(a.shape[:2]);top=ay[a[:,:,3]>200].min()
    authority_mask=(a[:,:,3]>200)&(ay>top+35)&((ar.max(2)-ar.min(2))<25)
    quantiles=[0,.05,.15,.35,.5,.7,.85,.95,.98,1]
    src=np.quantile(rgb.mean(2)[valid],quantiles);target=np.quantile(ar.mean(2)[authority_mask],quantiles)
    unique,idx=np.unique(src,return_index=True)
    return {'quantiles':quantiles,'neutralInput':unique.tolist(),'neutralOutput':target[idx].tolist(),
            'hair':[.60,.64,.70],'skin':[.84,.90,.96],'burgundy':[.52,.60,.74],
            'clothDetail':{'radiusSourcePixels':2.2,'gain':1.1,'residualLimit':18},
            'authority':authority,'facing':facing}

def grade(raw,body,settings):
    rgb=raw[:,:,:3].astype(float);r,g,b=rgb.transpose(2,0,1);luma=rgb.mean(2)
    yy,xx=np.indices(body.shape);by,bx=np.where(body);valid=raw[:,:,3]>0
    hy,hx=np.where(body&(yy<by.min()+18))
    head=(yy<by.min()+95)&(xx>=hx.min()-(14 if settings.get('facing') in ['west','south','north'] else 0))&(xx<=hx.max()+(0 if settings.get('facing')=='west' else 14))
    warm=np.clip((r-g-7)/18,0,1)*np.clip((r-b-10)/18,0,1)
    hair=head&((yy<by.min()+20)|((yy<by.min()+39)&(luma<110)))
    skin=head&(~hair)&(luma>65)
    patch=(r>g*1.6)&(r>b*1.6)&(~head)&valid
    neutral=np.clip(1-(rgb.max(2)-rgb.min(2)-8)/18,0,1)*valid
    silver=(rgb.min(2)>95)&((rgb.max(2)-rgb.min(2))<60)&(~head)&valid
    neutral=np.maximum(neutral,silver.astype(float))
    mapped=np.interp(luma,settings['neutralInput'],settings['neutralOutput'])
    target=np.stack((mapped+.7,mapped,mapped-.5),2)
    result=rgb*(1-neutral[:,:,None])+target*neutral[:,:,None]
    # Recover the raw source's small seams and panel shading after tonal
    # compression. Only interior cloth midtones: no silhouette sharpening,
    # bright metal enhancement, or new painted details.
    detail=settings['clothDetail'];weights=(raw[:,:,3]/255).astype(float)
    smooth=gaussian_filter(luma*weights,detail['radiusSourcePixels'])/np.maximum(gaussian_filter(weights,detail['radiusSourcePixels']),.001)
    residual=np.clip(luma-smooth,-detail['residualLimit'],detail['residualLimit'])
    cloth=neutral*(~head)*(~silver)*binary_erosion(raw[:,:,3]>180,iterations=3)
    cloth*=np.clip((luma-20)/15,0,1)*np.clip((145-luma)/30,0,1)
    result+=residual[:,:,None]*detail['gain']*cloth[:,:,None]
    for weight,key in [(hair*warm,'hair'),(skin*warm,'skin'),(patch.astype(float),'burgundy')]:
        result=result*(1-weight[:,:,None])+rgb*np.array(settings[key])*weight[:,:,None]
    output=raw.copy();output[:,:,:3]=np.clip(result,0,255).astype('uint8');output[~valid]=0
    diagnostic=np.zeros_like(raw);diagnostic[:,:,0]=np.clip(patch*255+hair*warm*120,0,255);diagnostic[:,:,1]=np.clip(skin*warm*255,0,255);diagnostic[:,:,2]=np.clip(neutral*255,0,255);diagnostic[:,:,3]=raw[:,:,3]
    return output,diagnostic
