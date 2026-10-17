"""Register independent directional work sources; retain native density and handedness.

No view is mirrored. Motion reprojects authored distal arm pixels about a joint;
the chassis, other arm and casings remain stationary outside the rotor masks.
"""
from pathlib import Path
import json, math, hashlib
import numpy as np
from scipy import ndimage
from PIL import Image, ImageDraw, ImageChops, ImageFont
from build_motion_pack import centered, transformed, rig
from build_rotor_review import clean, spin
from build_work_loops import lamp_layer, smooth

ROOT=Path(__file__).resolve().parent
N=102; FPS=30; ACTIONS=['mine','collect','weld','repair']
# Source-space chassis registration and measured fan hubs, never whole-pose bounds.
SPECS={
 'north':{'scale':.344,'anchors':[(344,366),(341,366),(344,329),(341,329)],
  'hubs':[[(95,425),(591,425)],[(96,425),(591,425)],[(95,388),(591,388)],[(96,388),(591,388)]],
  'axes':[(27,-4),(8,49)],
  'tools':[(241,58),(435,96),(337,94),(374,130)],
  'pivots':[(247,244),(436,229),(245,219),(238,219)],
  'polys':[[(205,40),(276,40),(279,249),(209,249)],[(378,63),(515,63),(502,236),(397,236)],[(191,46),(347,46),(347,140),(280,221),(202,221)],[(193,104),(375,104),(375,155),(282,221),(200,221)]]},
 'east':{'scale':.300,'anchors':[(289,282),(289,282),(289,247),(289,247)],
  'hubs':[[(348,137),(341,501)],[(348,137),(341,501)],[(348,104),(341,475)],[(348,104),(341,475)]],
  'axes':[(36,0),(0,43)],
  'tools':[(684,260),(598,421),(635,325),(614,354)],
  'pivots':[(483,263),(483,407),(483,232),(483,232)],
  'polys':[[(480,211),(705,211),(705,310),(480,310)],[(480,350),(681,350),(681,517),(480,517)],[(480,180),(645,210),(662,328),(610,328),(558,284),(480,280)],[(480,179),(616,202),(641,305),(632,360),(597,360),(573,291),(480,280)]]},
 'west':{'scale':.312,'anchors':[(469,311),(414,311),(469,280),(414,280)],
  'hubs':[[(414,141),(414,484)],[(359,141),(359,484)],[(414,113),(414,450)],[(359,113),(359,450)]],
  'axes':[(34,0),(0,42)],
  'tools':[(72,413),(95,279),(156,303),(111,320)],
  'pivots':[(272,406),(239,266),(265,359),(210,359)],
  'polys':[[(55,354),(275,354),(275,459),(55,459)],[(39,193),(240,193),(240,343),(39,343)],[(139,275),(209,293),(271,324),(272,407),(219,407),(139,333)],[(93,294),(153,300),(217,325),(217,400),(167,389),(93,342)]]},
}

def mapped(point,spec,index):
    a=spec['anchors'][index];s=spec['scale']
    return (128+(point[0]-a[0])*s,128+(point[1]-a[1])*s)

def setup(direction,index):
    spec=SPECS[direction]
    raw=Image.open(ROOT/'sources'/f'work-{direction}-v3.png').convert('RGBA')
    x=round((index%2)*raw.width/2);y=round((index//2)*raw.height/2)
    # East mining bit extends just beyond the nominal half-sheet separator.
    right=raw.width if index%2 else min(raw.width,round(raw.width/2)+(17 if direction=='east' else 0))
    source=raw.crop((x,y,right,round((index//2+1)*raw.height/2)))
    # Preserve held ore even when a tiny alpha gap separates it from the claw.
    pixels=np.array(source);labels,_=ndimage.label(pixels[:,:,3]>24)
    counts=np.bincount(labels.ravel());counts[0]=0
    keep=ndimage.binary_dilation(counts[labels]>=80,iterations=2)
    pixels[:,:,3]=np.where(keep,pixels[:,:,3],0);source=Image.fromarray(pixels)
    im=centered(source,spec['anchors'][index],spec['scale'])
    rigs=[transformed(rig(h,*spec['axes'],1 if j==0 else -1),spec['anchors'][index],spec['scale']) for j,h in enumerate(spec['hubs'][index])]
    poly=[mapped(p,spec,index) for p in spec['polys'][index]]
    mask=Image.new('L',im.size);ImageDraw.Draw(mask).polygon(poly,fill=255)
    part=im.copy();part.putalpha(ImageChops.multiply(im.getchannel('A'),mask))
    base=im.copy();base.putalpha(ImageChops.multiply(im.getchannel('A'),ImageChops.invert(mask)))
    return im,base,part,rigs,mapped(spec['pivots'][index],spec,index),mapped(spec['tools'][index],spec,index)

def render(action,direction,n,prepared):
    source,base,part,rigs,pivot,contact=prepared
    t=n/FPS;phase=n/(N-1);envelope=smooth(phase/.16)*(1-smooth((phase-.8)/.2))
    amplitude={'mine':1.4,'collect':4.0,'weld':1.3,'repair':1.1}[action]
    frequency={'mine':6,'collect':1/3.4,'weld':1/3.4,'repair':2}[action]
    angle=amplitude*math.sin(t*math.tau*frequency)*envelope
    im=base.copy();im.alpha_composite(part.rotate(angle,resample=Image.Resampling.BICUBIC,center=pivot))
    for r in rigs:im,_=spin(im,r,n/51,1)
    theta=-math.radians(angle);dx=contact[0]-pivot[0];dy=contact[1]-pivot[1]
    cx=pivot[0]+dx*math.cos(theta)-dy*math.sin(theta);cy=pivot[1]+dx*math.sin(theta)+dy*math.cos(theta)
    fx=Image.new('RGBA',im.size);d=ImageDraw.Draw(fx)
    if action=='mine' and envelope>.1:
        for j in range(12):
            p=(t*.9+j/12)%1;x=cx+math.sin(j*12.7)*p*15;y=cy-p*16
            d.ellipse((x-1,y-1,x+1,y+1),fill=(136,130,104,round(130*(1-p)*envelope)))
    elif action=='weld' and envelope>.03:
        pulse=(.6+.4*math.sin(t*83)**2)*envelope
        d.ellipse((cx-4,cy-4,cx+4,cy+4),fill=(55,157,236,round(85*pulse)))
        d.ellipse((cx-1.5,cy-1.5,cx+1.5,cy+1.5),fill=(216,243,255,round(250*pulse)))
        for j in range(5):
            p=(t*1.4+j/5)%1;x=cx+math.sin(j*4.1)*p*10;y=cy-p*18
            d.ellipse((x-1,y-1,x+1,y+1),outline=(162,210,225,round((1-p)*150*envelope)))
    elif action=='repair' and envelope>.2 and math.sin(t*math.tau*2)>.5:
        d.ellipse((cx-1,cy-1,cx+1,cy+1),fill=(151,214,227,round(150*envelope)))
    return im,fx

def main():
    data=json.loads((ROOT/'manifest.json').read_text())
    for direction,spec in SPECS.items():
        for i,action in enumerate(ACTIONS):
            prepared=setup(direction,i);pose=prepared[0]
            pose_path=f'poses/{action}-{direction}.png';pose.save(ROOT/pose_path)
            clip_id=f'work-{action}-{direction}';body_dir=ROOT/'frames'/clip_id;fx_dir=ROOT/'effects'/f'{action}-{direction}'
            body_dir.mkdir(exist_ok=True);fx_dir.mkdir(exist_ok=True)
            bodies=[];effects=[]
            for n in range(N):
                im,fx=render(action,direction,n,prepared)
                box=im.getbbox();assert box and min(box[:2])>0 and max(box[2:])<256,(clip_id,n,box)
                p=body_dir/f'{n:03}.png';im.save(p);bodies.append(p.relative_to(ROOT).as_posix())
                p=fx_dir/f'{n:03}.png';fx.save(p);effects.append(p.relative_to(ROOT).as_posix())
            lamp=data['headings'][direction]['lamp']
            entry={'id':clip_id,'frameFiles':bodies,'effectFiles':effects,'frameCount':N,'fps':FPS,'loop':True,'statusLayer':'independent','lamp':lamp,
             'contact':list(prepared[-1]),'pose':pose_path,'method':'independent directional source; joint articulation; no mirroring'}
            data['states']=[s for s in data['states'] if s['id']!=clip_id];data['states'].append(entry)
            data['actions'][action].setdefault('directions',{})[direction]={'pose':pose_path,'lamp':lamp,'source':f'sources/work-{direction}-v3.png','cell':i,'scale':spec['scale'],'anchor':spec['anchors'][i]}
    for action in ACTIONS:
        data['actions'][action]['directions']['south']={'pose':data['actions'][action]['pose'],'lamp':data['actions'][action]['lamp']}
        data['actions'][action]['limits']='Cardinal work contact loops. Full approach, acquire and release transitions are not included.'
        entry=next(s for s in data['states'] if s['id']==f'work-{action}-south');entry['lamp']=data['actions'][action]['lamp']
    data['scope']='Review assets: eight travel headings; four work actions in N/E/S/W; separate status lights. No runtime role changes.'
    data['sourceFiles']=[{'path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted((ROOT/'sources').glob('*.png'))]
    (ROOT/'manifest.json').write_text(json.dumps(data,indent=2))
    (ROOT/'review/cardinal-registration.json').write_text(json.dumps(SPECS,indent=2))
    print('Added 12 directional work clips: 1224 body frames and 1224 effect layers.')

if __name__=='__main__':main()
