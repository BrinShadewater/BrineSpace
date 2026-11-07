"""Rebuild selected human cargo directions from preserved character-specific sources."""
from pathlib import Path
import contextlib,io,re
import numpy as np
from PIL import Image
import rebuild_bill_art as shared

_frames={}
SELECTED={('veld','east'):76,('branforth','east'):76,('veld','west'):64,('branforth','west'):64,('veld','south'):72,('branforth','south'):72,('veld','north'):72,('branforth','north'):72}

def matches(actor,path):
    path=Path(path)
    clip=path.parent.name
    state,_,direction=clip.rpartition('-')
    return (actor,direction) in SELECTED and path.parent.parent.name==actor and state in ['pickup','unload','carry'] and 'crew-actions-v1' in path.parts

def replacement(actor,path):
    global _frames
    if not matches(actor,path):return None
    direction=Path(path).parent.name.rsplit('-',1)[-1];key=(actor,direction)
    if key not in _frames:
        from extract_veld_cargo_study import main as pickup_build
        from repair_veld_carry import main as carry_build
        if direction in ['south','north']:
            from repair_front_cargo import main as front_build
        with contextlib.redirect_stdout(io.StringIO()):
            pickup=pickup_build(actor,direction=direction)
            carry=front_build(actor,direction) if direction in ['south','north'] else carry_build(actor,direction)
        padded=[]
        for pose in carry:
            canvas=Image.new('RGBA',(256,256));canvas.alpha_composite(pose,(36,52));padded.append(canvas)
        _frames[key]={'pickup-'+direction:pickup,'unload-'+direction:pickup[::-1],'carry-'+direction:padded}
    index=int(re.search(r'(\d+)\.png$',Path(path).name)[1])
    pickup_revision='03' if key==('veld','east') else '01'
    carry_name='veld-carry-east-candidate-01.png' if key==('veld','east') else f'{actor}-carry-{direction}-donor-01.png'
    if direction in ['south','north']:carry_name=f'{actor}-pickup-{direction}-candidate-{pickup_revision}.png'
    shared.OPS[actor+'/cargo-'+direction+'/revision']={'sources':[f'character/crew-action-detail-v2/sources/{actor}-pickup-{direction}-candidate-{pickup_revision}.png','character/crew-action-detail-v2/sources/'+carry_name],
        'method':'Uniform source-scale pickup, exact reverse unload, source-specific carry rig; original timing retained',
        'carryStrideDistanceCells':SELECTED[key]*65.28/148/384}
    return _frames[key][Path(path).parent.name][index].copy()

def fitted(body,overlay):
    pixels=np.array(body);ys,_=np.where(pixels[:,:,3]>0);crown=int(ys.min())
    _,xs=np.where(pixels[crown:crown+12,:,3]>0)
    center=float(xs.min()+xs.max()+1)/2
    out=body.copy();out.alpha_composite(overlay,(round(center-overlay.width/2),crown-4))
    return out
