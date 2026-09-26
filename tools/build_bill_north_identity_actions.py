"""Rebuild north work from canonical-identity art with stationary tool-loop anatomy."""
from pathlib import Path
import hashlib
import numpy as np
from PIL import Image
from build_bill_west_style_actions import solid

SOURCE=Path('character/major-bill-v3/sources/north-work-identity-2026-09-21')

def extract(source, spec):
    frames=[]
    source=solid(source)
    for row in spec['frames']:
        crop=source.crop(row['cell']).crop(row['box'])
        crop=solid(crop.resize(tuple(row['size']),Image.Resampling.LANCZOS))
        frame=Image.new('RGBA',(256,256))
        frame.alpha_composite(crop,tuple(row['paste']))
        frames.append(frame)
    return frames

def build(root,read,image,helmet,tilted):
    source=root/SOURCE
    specs={}
    for family in ('lowering','work'):
        spec=read(source/(family+'-registration.json'))
        path=source/(family+'-source.png')
        if hashlib.sha256(path.read_bytes()).hexdigest()!=spec['source_sha256']:
            raise ValueError('Bill north identity source changed: '+family)
        specs[family]=spec
    kneel=extract(image(source/'lowering-source.png'),specs['lowering'])
    registered=extract(image(source/'work-source.png'),specs['work'])
    repair=[]
    for index,pose in enumerate(registered):
        frame=kneel[-1].copy()
        if index not in (0,5):
            for rect in specs['work']['replacement_rectangles']:
                rect=tuple(rect)
                frame.paste(pose.crop(rect),rect)
        repair.append(frame)
    bare={'kneel-north':kneel,'repair-north':repair,'stand-north':list(reversed(kneel))}
    fit=read(source/'helmet-registration.json')
    anchors={(row['folder'],row['frame']):np.array(row['head']) for row in fit['head_anchors']}
    overlay=helmet.overlay('north',tuple(fit['overlay_size']))
    equipped={}
    for key,folder in [('kneel-north','lowering'),('repair-north','repair')]:
        equipped[key]=[]
        for index,frame in enumerate(bare[key]):
            head=anchors[folder,index]
            equipped[key].append(tilted(frame,overlay,head-np.array(fit['overlay_anchor_offset']),0,
                                       [*(head-[14,20]),28,34],'north'))
    equipped['stand-north']=list(reversed(equipped['kneel-north']))
    return bare,equipped
