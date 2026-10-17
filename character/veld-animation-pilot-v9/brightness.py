"""Conservative material exposure matching, not global palette quantization.

Warm head pixels, blue cloth and low-chroma suit pixels are measured separately.
Ratios operate on luminance, preserving each pixel's hue and local shading.
Targets come from the retained idle's pooled source pixels. No poses are changed.
"""
import numpy as np
from PIL import Image

def regions(im, facing=None):
    a=np.asarray(im).astype(float)
    rgb=a[:,:,:3]/255
    hi=rgb.max(2); lo=rgb.min(2)
    sat=(hi-lo)/np.maximum(hi,.001)
    r,g,b=rgb.transpose(2,0,1)
    y=np.indices(hi.shape)[0]/im.height
    valid=a[:,:,3]>127
    l=rgb @ np.array([.2126,.7152,.0722])
    skin=valid & (y<.20) & (r>g*1.18) & (g>b*1.12) & (l>.20)
    blue=valid & (y>.15) & (b>r*1.15) & (b>g*1.06) & (l>.12)
    cloth=valid & (y>.20) & (sat<.24) & (l>.10) & (l<.43)
    if facing=='north': skin[:]=False
    return rgb,l,{'skin':skin,'blue':blue,'cloth':cloth}

def measure(im, facing=None):
    _,l,masks=regions(im,facing)
    return {k:float(np.median(l[m])) for k,m in masks.items() if m.sum()>30}

def match(im,targets,facing=None):
    rgb,l,masks=regions(im,facing); before=measure(im,facing)
    gains={k:float(np.clip(targets[k]/before[k],.72,1.38)) for k in before}
    # East source fabric exceeds the old 0.43 luminance measurement ceiling.
    # Measure a bounded thigh band with no upper luminance exclusion. The
    # target is the unchanged front-idle thigh median (six source frames).
    if facing=='east':
        y=np.indices(l.shape)[0]/im.height
        hi=rgb.max(2);sat=(hi-rgb.min(2))/np.maximum(hi,.001)
        sample=(y>.51)&(y<.60)&(sat<.24)&(l>.10)&(np.asarray(im)[:,:,3]>127)
        assert sample.sum()>100, 'Insufficient thigh fabric for exposure measurement'
        thigh=float(np.median(l[sample]))
        gains['cloth']=float(np.clip(.272/ thigh,.40,1.38))
    # Global suit exposure; independently controlled skin and blue are retained.
    gain=np.full(l.shape,gains.get('cloth',1.))
    for k in ('skin','blue'):
        if k in gains: gain[masks[k]]=gains[k]
    # Gain masks feather within visible artwork to avoid hard recolour seams.
    from scipy.ndimage import gaussian_filter
    visible=np.asarray(im)[:,:,3]>127
    weighted=gaussian_filter(gain*visible,1.0)
    weight=gaussian_filter(visible.astype(float),1.0)
    gain=np.where(visible,weighted/np.maximum(weight,.001),1.)
    result=np.asarray(im).copy()
    result[:,:,:3]=np.clip(rgb*gain[:,:,None]*255,0,255).round().astype('uint8')
    out=Image.fromarray(result)
    after_l=(result[:,:,:3]/255) @ np.array([.2126,.7152,.0722])
    after={k:float(np.median(after_l[m])) for k,m in masks.items() if k in before}
    return out,{'before':before,'after':after,'gains':gains}
