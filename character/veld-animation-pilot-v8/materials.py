"""Deterministic hue mapping to locked material ramps; no geometry changes."""
import json
from pathlib import Path
import numpy as np
from PIL import Image
from brightness import regions

SPEC=Path(__file__).resolve().parent.parent/'crew-turnarounds-v4/palette-reference.json'
palette=json.loads(SPEC.read_text())
weights=np.array([.2126,.7152,.0722])

def ramp(names,collection):
    anchors=[np.array([int(collection[n][i:i+2],16) for i in (1,3,5)])/255 for n in names]
    # Preserve deep occlusion and small specular highlights beyond the three targets.
    return np.array([np.zeros(3),*anchors,np.ones(3)])

ramps={
 'skin':ramp(['Skin shadow','Skin base','Skin light'],palette['character_materials']['veld']),
 'blue':ramp(['Accent shadow','Accent base','Accent light'],palette['character_materials']['veld']),
 'cloth':ramp(['Graphite shadow','Graphite base','Graphite light'],palette['shared_materials']),
 'ivory':ramp(['Ivory shadow','Ivory base','Ivory light'],palette['shared_materials']),
 'steel':ramp(['Steel shadow','Steel base','Steel light'],palette['shared_materials']),
 'silver':ramp(['Hair light'],palette['character_materials']['veld']),
 'hair':ramp(['Hair shadow','Hair base'],palette['character_materials']['veld'])
}
# Brown hair highlights retain the base hue; the silver anchor belongs only to
# the streak. Avoid turning every lighter brown strand into silver/white.
hair_base=ramps['hair'][-2]
ramps['hair'][-1]=hair_base/hair_base.max()

def apply(im, facing='east'):
    rgb,l,masks=regions(im,facing)
    if facing=='north':
        masks['skin'][:]=False
        y=np.indices(l.shape)[0]/im.height
        fx=np.array([im.width/2])
    else:
        # Exclude crown/bun: skin selection requires the facial vertical band.
        y=np.indices(l.shape)[0]/im.height
        masks['skin'] &= (y>.045)&(y<.175)&(l>.24)
        # Warm hair also passes an RGB threshold. Keep the face component and nearby
        # ear/jaw islands, excluding the disconnected crown and bun highlights.
        from scipy import ndimage
        labels,_=ndimage.label(masks['skin'])
        sizes=np.bincount(labels.ravel());sizes[0]=0
        face=int(sizes.argmax());fy,fx=np.nonzero(labels==face)
        assert len(fx)>20,'Face region not detected; do not silently remap hair.'
        allowed=labels==face
        for label in range(1,len(sizes)):
            if label==face or sizes[label]<4:continue
            yy,xx=np.nonzero(labels==label)
            if (yy.mean()>fy.min()+.25*(fy.max()-fy.min()) and
                (xx.mean()<fx.max()+.5*(fx.max()-fx.min()) if facing=='west' else xx.mean()>fx.min()-.5*(fx.max()-fx.min()))):
                allowed |= labels==label
        masks['skin'] &= allowed
    valid=np.array(im)[:,:,3]>127
    red,green,blue=rgb.transpose(2,0,1)
    hi=rgb.max(2);lo=rgb.min(2);sat=(hi-lo)/np.maximum(hi,.001)
    xx=np.indices(l.shape)[1]
    back=xx>fx.max() if facing=='west' else xx<fx.min()
    head=(y<.145) if facing=='north' else (y<.065)|(back&(y<.155))
    head &= valid & ~masks['skin']
    masks['silver']=head & (sat<.20)&(l>.28)
    masks['hair']=head & ~masks['silver'] & (red>blue*1.08)&(l>.035)
    # Chest modules occupy a constrained band around the head/torso centre;
    # this excludes the raised scanner and the silver canisters below the belt.
    chest=(y>.235)&(y<.365)&(np.abs(xx-np.median(fx))<im.height*.13)
    masks['ivory']=valid & chest & (red>blue*1.12)&(red<green*1.28)&(sat>.09)&(sat<.38)&(l>.32)
    # Conservative bright steel selection. Shadowed cloth is deliberately not
    # classified as metal solely because it lies over a knee or boot.
    if facing=='north': masks['ivory'][:]=False
    masks['steel']=valid & (y>.17)&(sat<.22)&(l>.43)&~masks['ivory']&~masks['blue']
    masks['cloth'] &= ~masks['steel'] & ~masks['ivory']
    out=rgb.copy(); reports={}
    diagnostic=np.zeros((*l.shape,4),dtype='uint8')
    colours={'skin':[255,180,80,255],'blue':[80,140,255,255],'cloth':[100,100,100,255],
             'hair':[170,85,40,255],'silver':[230,230,255,255],
             'ivory':[255,240,140,255],'steel':[100,240,200,255]}
    for name,mask in masks.items():
        anchors=ramps[name]; levels=anchors@weights
        for c in range(3):
            out[:,:,c][mask]=np.interp(l[mask],levels,anchors[:,c])
        diagnostic[mask]=colours[name]
        reports[name]={'pixels':int(mask.sum()),'luminance_max_error':float(np.max(np.abs((out@weights)[mask]-l[mask]))) if mask.any() else 0}
    data=np.array(im)
    data[:,:,:3]=np.clip(out*255,0,255).round().astype('uint8')
    return Image.fromarray(data),Image.fromarray(diagnostic),reports
