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
 'cloth':ramp(['Graphite shadow','Graphite base','Graphite light'],palette['shared_materials'])
}

def apply(im):
    rgb,l,masks=regions(im)
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
            xx.mean()>fx.min()-.5*(fx.max()-fx.min())):
            allowed |= labels==label
    masks['skin'] &= allowed
    out=rgb.copy(); reports={}
    diagnostic=np.zeros((*l.shape,4),dtype='uint8')
    colours={'skin':[255,180,80,255],'blue':[80,140,255,255],'cloth':[160,160,160,255]}
    for name,mask in masks.items():
        anchors=ramps[name]; levels=anchors@weights
        for c in range(3):
            out[:,:,c][mask]=np.interp(l[mask],levels,anchors[:,c])
        diagnostic[mask]=colours[name]
        reports[name]={'pixels':int(mask.sum()),'luminance_max_error':float(np.max(np.abs((out@weights)[mask]-l[mask]))) if mask.any() else 0}
    data=np.array(im)
    data[:,:,:3]=np.clip(out*255,0,255).round().astype('uint8')
    return Image.fromarray(data),Image.fromarray(diagnostic),reports
