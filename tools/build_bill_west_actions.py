"""Rebuild independently authored west action surfaces with planted contact."""
from pathlib import Path
import hashlib
import numpy as np
from PIL import Image,ImageDraw
from build_bill_south_actions import extract

SOURCE=Path('character/major-bill-v3/sources/west-actions-2026-09-21')


def build(root,read,image,helmet,tilted):
    source=root/SOURCE
    spec=read(source/'registration.json');work=read(source/'repair-registration.json')
    for name,metadata in [('generated-source.png',spec),('repair-source.png',work)]:
        if hashlib.sha256((source/name).read_bytes()).hexdigest()!=metadata['source_sha256']:
            raise ValueError('Bill west source changed: '+name)
    kneel=extract(image(source/'generated-source.png'),spec)
    contact=read(source/'contact-registration.json')
    for i,pose in enumerate(contact['frames']):
        registered=Image.new('RGBA',(256,256));registered.alpha_composite(kneel[i],(pose['x_offset'],0));kneel[i]=registered
    mask=Image.new('L',(256,256));ImageDraw.Draw(mask).polygon([tuple(p) for p in work['replacement_polygon']],fill=255)
    repair=[]
    for i,frame in enumerate(extract(image(source/'repair-source.png'),work)):
        pixels=np.array(frame);y,x=np.where(pixels[218:224,:,3]>0)
        aligned=Image.new('RGBA',frame.size);aligned.alpha_composite(frame,(work['contact_toe']-int(x.min()),0))
        pose=kneel[-1].copy()
        if i not in [0,5]:pose.paste(aligned,(0,0),mask)
        repair.append(pose)
    bare={'kneel-west':kneel,'repair-west':repair,'stand-west':list(reversed(kneel))}
    fit=read(source/'helmet-registration.json')
    anchors={(r['folder'],r['frame']):np.array(r['head']) for r in fit['head_anchors']}
    overlay=helmet.overlay('west',tuple(fit['overlay_size']));equipped={}
    for action,folder in [('kneel-west','contact-candidate'),('repair-west','repair-candidate')]:
        equipped[action]=[]
        for i,body in enumerate(bare[action]):
            head=anchors[folder,i]
            equipped[action].append(tilted(body,overlay,head-np.array(fit['overlay_anchor_offset']),0,[*(head-[14,20]),28,34],'west'))
    equipped['stand-west']=list(reversed(equipped['kneel-west']))
    return bare,equipped
