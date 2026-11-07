"""Isolated shared-edge limb-mesh study; preserves selected joint trajectories."""
from pathlib import Path
import hashlib
import json
import math
import numpy as np
from PIL import Image
from scipy.interpolate import RBFInterpolator
from repair_bill_walk import build, place, knee as solve_knee

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/bill-pixel-layer-2026-09-21/smooth-limbs'
SOURCES = ROOT / 'output/bill-body-motion-2026-09-20'
ANCHORS = {
    'east': {'far': ((78,119),(65,140),(50,158)), 'near': ((90,114),(104,132),(109,158))},
    'west': {'far': ((83,117),(73,135),(63,159)), 'near': ((99,116),(105,137),(125,158))},
}


def cage(points):
    a,b,c=map(lambda p:np.array(p,dtype=float),points)
    u=(b-a)/np.linalg.norm(b-a);v=(c-b)/np.linalg.norm(c-b)
    n0=np.array([-u[1],u[0]]);n2=np.array([-v[1],v[0]])
    n1=n0+n2;n1/=np.linalg.norm(n1)
    return np.array([a+n0*16,b+n1*16,c+n2*12,a-n0*16,b-n1*16,c-n2*12])


def isolate_legs(source,direction):
    pixels=np.array(source)
    yy,xx=np.mgrid[:source.height,:source.width]
    # Split the visible source at the inter-leg boundary, retaining every pixel
    # exactly once. This does not invent the far leg's hidden surfaces.
    boundary=np.interp(yy,[0,119,136,184],[84,84,82,82] if direction=='east' else [92,92,94,94])
    near=xx>=boundary
    layers={}
    for name,mask in [('near',near),('far',~near)]:
        data=pixels.copy();data[(yy<112)|~mask]=0
        layers[name]=Image.fromarray(data)
    combined=Image.new('RGBA',source.size)
    combined.alpha_composite(layers['far']);combined.alpha_composite(layers['near'])
    expected=pixels.copy();expected[:112]=0
    if not np.array_equal(np.array(combined),expected):
        raise ValueError('Source layer split lost or changed pixels')
    return layers


def mesh_limb(source, original, target):
    src=cage(original);dst=cage(target)
    pixels=np.array(source);result=np.zeros_like(pixels)
    yy,xx=np.mgrid[:source.height,:source.width]
    samples=np.stack((xx+.5,yy+.5,np.ones_like(xx)),axis=-1)
    for ids in [(0,1,3),(1,4,3),(1,2,4),(2,5,4)]:
        si=src[list(ids)];di=dst[list(ids)]
        matrix=np.vstack((di.T,np.ones(3)))
        weights=samples @ np.linalg.inv(matrix).T
        inside=(weights>=-1e-7).all(axis=-1)
        coords=weights @ si
        sx=np.floor(coords[:,:,0]).astype(int);sy=np.floor(coords[:,:,1]).astype(int)
        inside &= (sx>=0)&(sy>=0)&(sx<source.width)&(sy<source.height)
        result[inside]=pixels[sy[inside],sx[inside]]
    return Image.fromarray(result)


def smooth_limb(source,original,target,angle):
    hip,knee,ankle=map(lambda x:np.array(x,float),original)
    th,tk,ta=map(lambda x:np.array(x,float),target)
    controls=[];dest=[]
    for p,q,axis,taxis in [(hip,th,knee-hip,tk-th),(knee,tk,ankle-hip,ta-th)]:
        n=np.array([-axis[1],axis[0]])/np.linalg.norm(axis)
        tn=np.array([-taxis[1],taxis[0]])/np.linalg.norm(taxis)
        for side in [-8,0,8]:controls.append(p+n*side);dest.append(q+tn*side)
    rotation=np.array([[math.cos(angle),-math.sin(angle)],[math.sin(angle),math.cos(angle)]])
    for offset in [[0,0],[-10,2],[10,2],[-10,14],[14,14]]:
        controls.append(ankle+offset);dest.append(ta+rotation@offset)
    warp=RBFInterpolator(np.array(dest),np.array(controls),kernel='thin_plate_spline',smoothing=0)
    yy,xx=np.mgrid[:source.height,:source.width]
    points=np.stack([xx.ravel()+.5,yy.ravel()+.5],axis=1)
    uv=np.floor(warp(points)).astype(int);sx,sy=uv.T
    inside=(sx>=0)&(sy>=0)&(sx<source.width)&(sy<source.height)
    out=np.zeros((len(points),4),np.uint8);pixels=np.array(source)
    out[inside]=pixels[sy[inside],sx[inside]]
    return Image.fromarray(out.reshape(source.height,source.width,4))


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    audit = {}
    for direction, anchors in ANCHORS.items():
        source_path = SOURCES / f'{direction}-preserved-0.png'
        source = Image.open(source_path).convert('RGBA')
        baseline,layers,torso,trajectory = build(source,direction)
        isolated=isolate_legs(source,direction)
        for name,layer in isolated.items():layer.save(OUT/f'{direction}-source-{name}.png')
        frames=[]
        for phase,poses in enumerate(trajectory):
            frame=Image.new('RGBA',source.size)
            bob=-1 if phase in (1,4) else 0
            for leg in ('far','near'):
                hip,knee,ankle=map(np.array,anchors[leg])
                target=poses[leg]
                th,tk,ta=map(np.array,(target['hip'],target['knee'],target['ankle']))
                l1=np.linalg.norm(knee-hip);l2=np.linalg.norm(ankle-knee)
                if np.linalg.norm(ta-th)<l1+l2:
                    tk=solve_knee(th,ta,l1,l2,1 if direction=='east' else -1)
                target['knee']=tk.tolist()
                target['source_lengths']=[float(l1),float(l2)]
                target['reachable']=bool(np.linalg.norm(ta-th)<=l1+l2)
                step=target['phase']
                angle=([-.25,-.25,-.25,-.1,-.3,-.25] if leg=='far' else [.25,.25,.25,.1,-.05,.1])[step]
                limb=smooth_limb(isolated[leg],(hip,knee,ankle),(th,tk,ta),angle)
                shift=round(target['soleTarget']-limb.getbbox()[3])
                translated=Image.new('RGBA',source.size)
                translated.alpha_composite(limb,(0,shift))
                translated.paste((0,0,0,0),(0,0,184,116+bob))
                frame.alpha_composite(translated)
                target['whole_leg_y_shift']=shift
            # Preserved poses provide local arm/shoulder movement; keep the head.
            body_index=[0,1,5,5,2,1][phase]
            body=Image.open(SOURCES/f'{direction}-preserved-{body_index}.png').convert('RGBA')
            shift=source.getbbox()[1]-body.getbbox()[1]+bob
            frame.alpha_composite(torso,(0,bob))
            frame.paste((0,0,0,0),(0,0,184,119+bob))
            frame.alpha_composite(body.crop((0,0,184,119-shift)),(0,shift))
            frame.paste(source.crop((0,0,184,60)),(0,bob))
            frame.save(OUT/f'{direction}-{phase:02}.png')
            frames.append(frame)
        sheet=Image.new('RGBA',(184*6,184*2),'#26383c')
        for i,(before,after) in enumerate(zip(baseline,frames)):
            sheet.alpha_composite(before,(184*i,0));sheet.alpha_composite(after,(184*i,184))
        sheet.resize((2208,736),Image.Resampling.NEAREST).save(OUT/f'{direction}-comparison.png')
        audit[direction]={'source_sha256':hashlib.sha256(source_path.read_bytes()).hexdigest(),
                          'trajectory':trajectory,'source_anchors':anchors,'scope':'Thin-plate spline with independent boot orientation, nearest source sampling and sole-height correction. Preserved upper-body poses with fixed head; no runtime selection change.'}
    (OUT/'provenance.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8')
    print('Twelve isolated joint-study frames written; production unchanged.')


if __name__=='__main__': main()
