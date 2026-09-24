"""Reconstruct Bill's independently authored north action repair."""
from pathlib import Path
import hashlib
import numpy as np
from PIL import Image
from build_bill_south_actions import extract

SOURCE=Path('character/major-bill-v3/sources/north-actions-2026-09-21')


def build(root,read,image,helmet,tilted):
    source=root/SOURCE
    spec=read(source/'registration.json');work=read(source/'repair-registration.json')
    for name,metadata in [('generated-source.png',spec),('repair-source.png',work)]:
        if hashlib.sha256((source/name).read_bytes()).hexdigest()!=metadata['source_sha256']:
            raise ValueError('Bill north source changed: '+name)
    kneel=extract(image(source/'generated-source.png'),spec)
    correction=read(source/'footlock-registration.json')
    x0,y0,x1,y1=correction['region'];start,end=correction['ramp_y']
    for i,shift in enumerate(correction['offsets']):
        a=np.array(kneel[i]);b=a.copy()
        for y in range(y0,y1):
            dx=round(shift*min(1,max(0,(y-start)/(end-start))))
            if not dx:continue
            row=a[y,x0:x1].copy();b[y,x0:x1]=0
            dest=b[y,x0+dx:x1+dx]
            visible=(row[:,3]>0)&(dest[:,3]==0)
            dest[visible]=row[visible]
        kneel[i]=Image.fromarray(b)
    repair=[]
    for i,registered in enumerate(extract(image(source/'repair-source.png'),work)):
        frame=kneel[-1].copy()
        if i not in [0,5]:
            for rect in work['replacement_regions']:
                rect=tuple(rect);frame.paste(registered.crop(rect),rect)
        repair.append(frame)
    bare={'kneel-north':kneel,'repair-north':repair,'stand-north':list(reversed(kneel))}
    fit=read(source/'helmet-registration.json')
    anchors={(r['folder'],r['frame']):np.array(r['head']) for r in fit['head_anchors']}
    overlay=helmet.overlay('north',tuple(fit['overlay_size']));equipped={}
    for action,folder in [('kneel-north','footlock-candidate'),('repair-north','repair-footlock-candidate')]:
        equipped[action]=[]
        for i,body in enumerate(bare[action]):
            head=anchors[folder,i]
            equipped[action].append(tilted(body,overlay,head-np.array(fit['overlay_anchor_offset']),0,[*(head-[14,20]),28,34],'north'))
    equipped['stand-north']=list(reversed(equipped['kneel-north']))
    return bare,equipped
