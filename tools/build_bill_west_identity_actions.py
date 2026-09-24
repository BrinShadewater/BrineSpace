"""Rebuild west work with canonical proportions and an arm-only wrench loop."""
from pathlib import Path
import hashlib
import numpy as np
from PIL import Image,ImageDraw
from build_bill_north_identity_actions import extract

SOURCE=Path('character/major-bill-v3/sources/west-work-identity-2026-09-21')

def build(root,read,image,helmet,tilted):
    source=root/SOURCE
    specs={}
    for family in ('lowering','work'):
        spec=read(source/(family+'-registration.json'))
        path=source/(family+'-source.png')
        if hashlib.sha256(path.read_bytes()).hexdigest()!=spec['source_sha256']:
            raise ValueError('Bill west identity source changed: '+family)
        specs[family]=spec
    kneel=extract(image(source/'lowering-source.png'),specs['lowering'])
    registered=extract(image(source/'work-source.png'),specs['work'])
    mask=Image.new('L',(256,256))
    ImageDraw.Draw(mask).polygon([tuple(p) for p in specs['work']['replacement_polygon']],fill=255)
    repair=[]
    for index,pose in enumerate(registered):
        frame=kneel[-1].copy()
        if index not in (0,5):frame.paste(pose,(0,0),mask)
        repair.append(frame)
    bare={'kneel-west':kneel,'repair-west':repair,'stand-west':list(reversed(kneel))}
    fit=read(source/'helmet-registration.json')
    anchors={(row['folder'],row['frame']):np.array(row['head']) for row in fit['head_anchors']}
    overlay=helmet.overlay('west',tuple(fit['overlay_size']))
    equipped={}
    for key,folder in [('kneel-west','lowering'),('repair-west','repair')]:
        equipped[key]=[]
        for index,frame in enumerate(bare[key]):
            head=anchors[folder,index]
            equipped[key].append(tilted(frame,overlay,head-np.array(fit['overlay_anchor_offset']),0,
                                       [*(head-[14,20]),28,34],'west'))
    equipped['stand-west']=list(reversed(equipped['kneel-west']))
    return bare,equipped
