"""Work reach/stow and single-shot collection jobs from preserved raster parts.

The empty claw master contributes only four masked grippers. Its altered east
tool is deliberately excluded. Existing chassis, tools and propellers are kept.
Cargo ownership and root travel are explicit per-frame metadata, not baked jumps.
"""
from pathlib import Path
import json,math,hashlib
import numpy as np
from scipy import ndimage
from PIL import Image,ImageDraw,ImageChops
from build_cardinal_work import setup
from build_rotor_review import spin,clean
from build_work_loops import smooth
ROOT=Path(__file__).resolve().parent
SIZE=256;FPS=30
DIRS=['north','east','south','west']
def save_png(im,path):
    temp=path.with_name(path.stem+'.tmp.png');im.save(temp);temp.replace(path)
FORWARD={'north':(0,-1),'east':(1,0),'south':(0,1),'west':(-1,0)}
# Native coordinates, on the registered original collection pose.
HANDS={
 'north':{'crop':(340,72,457,201),'sourcePivot':(399,180),'scale':.32,'wrist':(163,74),'joint':(162,88),'cut':[(137,20),(191,20),(191,78),(140,78)],'ore':[(159,31),(167,30),(175,39),(170,52),(163,60),(156,51),(156,40)],'arm':[(143,73),(183,73),(181,96),(144,96)]},
 'east':{'crop':(1090,369,1209,484),'sourcePivot':(1105,414),'scale':.34,'wrist':(198,165),'joint':(188,166),'cut':[(195,147),(245,147),(245,199),(196,196)],'ore':[(216,162),(228,164),(232,171),(230,181),(218,182),(213,173)],'arm':[(181,149),(201,149),(202,182),(181,182)]},
 'south':{'crop':(121,1080,240,1215),'sourcePivot':(177,1101),'scale':.32,'wrist':(72,194),'joint':(74,180),'cut':[(48,190),(99,190),(99,244),(47,244)],'ore':[(71,205),(77,207),(80,215),(77,226),(71,229),(66,218)],'arm':[(55,172),(94,172),(91,196),(54,196)]},
 'west':{'crop':(660,850,793,969),'sourcePivot':(763,896),'scale':.33,'wrist':(53,113),'joint':(65,110),'cut':[(8,89),(57,89),(58,137),(8,137)],'ore':[(23,111),(32,109),(40,114),(37,121),(25,126),(19,120)],'arm':[(51,93),(72,93),(73,128),(50,128)]},
}
GRIPPERS={
 'north': ([(122,29),(189,29),(186,107),(154,107),(152,73),(122,73)],(165,95)),
 'east': ([(183,155),(251,155),(251,211),(183,211)],(188,174)),
 'south': ([(30,178),(105,178),(117,210),(152,210),(152,242),(30,242)],(72,182)),
 'west': ([(1,79),(76,79),(76,123),(35,141),(1,141)],(67,100)),
}
TOOL_ONLY={
 'north':{'weld':[(80,43),(125,43),(125,58),(106,77),(106,95),(81,95)],'repair':[(80,52),(130,52),(130,64),(120,76),(106,96),(80,96)]},
 'east':{'weld':[(182,104),(220,104),(238,146),(238,152),(229,152),(202,134),(182,137)],'repair':[(182,104),(220,104),(225,137),(223,149),(216,149),(202,135),(182,137)]},
 'south':{'weld':[(149,173),(201,176),(188,212),(145,224),(142,218),(144,196)],'repair':[(138,173),(192,176),(171,215),(124,219),(122,205),(128,194)]},
 'west':{'weld':[(31,130),(56,140),(65,143),(65,166),(54,166),(31,147)],'repair':[(34,138),(65,141),(65,162),(46,160),(34,151)]},
}

def mask_polygon(poly):
    m=Image.new('L',(SIZE,SIZE));ImageDraw.Draw(m).polygon(poly,fill=255);return m

def split(im,mask,pivot=None):
    part=im.copy();part.putalpha(ImageChops.multiply(im.getchannel('A'),mask))
    erase=mask.copy()
    if pivot:
        # Keep the fixed hinge under the rotating member to avoid a transparent seam.
        x,y=pivot;ImageDraw.Draw(erase).ellipse((x-4,y-4,x+4,y+4),fill=0)
    base=im.copy();base.putalpha(ImageChops.multiply(im.getchannel('A'),ImageChops.invert(erase)))
    return base,part

def rotate_point(point,pivot,angle):
    t=math.radians(angle);x=point[0]-pivot[0];y=point[1]-pivot[1]
    return (pivot[0]+x*math.cos(t)+y*math.sin(t),pivot[1]-x*math.sin(t)+y*math.cos(t))

def rotate(im,angle,pivot):
    return im if abs(angle)<1e-8 else im.rotate(angle,Image.Resampling.BICUBIC,center=pivot)

def rotors(im,reference,rigs,n):
    # Always sample blades from the original source, never a previously spun frame.
    out=np.array(im)
    for r in rigs:
        spun,mask=spin(reference,r,n/51,1)
        out[mask>0]=np.array(spun)[mask>0]
    return Image.fromarray(out)

def collection_setup(direction):
    spec=HANDS[direction];source=Image.open(ROOT/'poses'/f'collect-{direction}.png').convert('RGBA')
    master=Image.open(ROOT/'sources/collection-empty-claws-v4.png').convert('RGBA')
    box=spec['crop'];part=master.crop(box);s=spec['scale']
    part=part.convert('RGBa').resize((round(part.width*s),round(part.height*s)),Image.Resampling.LANCZOS).convert('RGBA')
    hand=Image.new('RGBA',source.size)
    at=(round(spec['wrist'][0]-(spec['sourcePivot'][0]-box[0])*s),round(spec['wrist'][1]-(spec['sourcePivot'][1]-box[1])*s))
    hand.alpha_composite(part,at)
    body,_=split(source,mask_polygon(spec['cut']))
    # The forearm and replacement hand rotate together about the original elbow.
    body,arm=split(body,mask_polygon(spec['arm']),spec['joint'])
    ore=source.copy();ore.putalpha(ImageChops.multiply(source.getchannel('A'),mask_polygon(spec['ore'])))
    save_png(ore,ROOT/'poses'/f'cargo-ore-{direction}.png')
    fx,fy=FORWARD[direction];sx,sy=-fy,fx
    yy,xx=np.indices((SIZE,SIZE));dx=xx-spec['wrist'][0];dy=yy-spec['wrist'][1]
    forward=dx*fx+dy*fy;side=dx*sx+dy*sy
    jaw_masks=[Image.fromarray(np.uint8((forward>7)&(side*sign>0))*255) for sign in [-1,1]]
    palm=hand.copy();jaws=[]
    for sign,mask in zip([-1,1],jaw_masks):
        palm,jaw=split(palm,mask)
        pivot=(spec['wrist'][0]+fx*7+sx*sign*8,spec['wrist'][1]+fy*7+sy*sign*8)
        jaws.append((jaw,pivot,sign))
    if direction=='south':
        rigs=[{'center':(44,138),'u':(9,-1),'v':(3,15),'sign':1},{'center':(215,138),'u':(9,1),'v':(-3,15),'sign':-1}]
    else:rigs=setup(direction,1)[3]
    return source,body,arm,palm,jaws,ore,rigs

def collect_frame(direction,prepared,q,closed,n):
    source,body,arm,palm,jaws,ore,rigs=prepared;spec=HANDS[direction]
    hand=palm.copy()
    for jaw,pivot,sign in jaws:hand.alpha_composite(rotate(jaw,sign*closed*10,pivot))
    limb=arm.copy();limb.alpha_composite(hand)
    angle=q*24;im=body.copy();im.alpha_composite(rotate(limb,angle,spec['joint']))
    return rotors(im,source,rigs,n),rotate(ore,angle,spec['joint'])

def work_setup(direction,action,data):
    source=Image.open(ROOT/'poses'/f'{action}-{direction}.png').convert('RGBA')
    if direction=='south':
        poly,pivot={
          'mine': ([(180,203),(240,203),(240,255),(180,255)],(197,207)),
          'weld': ([(158,173),(205,177),(185,227),(126,230)],(180,177)),
          'repair': ([(148,175),(210,178),(185,227),(113,227)],(181,177)),
        }[action]
        rigs=[{'center':(44,138 if action=='mine' else 132),'u':(9,-1),'v':(3,15),'sign':1},{'center':(215,138 if action=='mine' else 132),'u':(9,1),'v':(-3,15),'sign':-1}]
    else:
        from build_cardinal_work import SPECS,mapped
        spec=SPECS[direction];i=['mine','collect','weld','repair'].index(action)
        pivot=mapped(spec['pivots'][i],spec,i);poly=[mapped(p,spec,i) for p in spec['polys'][i]]
        if direction=='east':
            poly=[(181,99),(254,99),(254,156 if action=='weld' else 165),(181,156 if action=='weld' else 165)] if action!='mine' else [(181,98),(255,98),(255,140),(181,140)]
        elif direction=='west' and action=='mine':poly=[(1,136),(69,136),(69,180),(1,180)]
        rigs=setup(direction,i)[3]
    if action in TOOL_ONLY[direction]:poly=TOOL_ONLY[direction][action]
    if direction=='west' and action!='mine':pivot=(61,152)
    body,tool=split(source,mask_polygon(poly),pivot)
    tool=clean(tool)
    if action=='mine':
        h=HANDS[direction];gpoly=h['cut']+[];gpivot=h['joint']
        # Mining's free claw remains relaxed; stow/reach actuates the boring arm.
        grip=Image.new('RGBA',source.size)
    else:
        gpoly,gpivot=GRIPPERS[direction]
        body,grip=split(body,mask_polygon(gpoly),gpivot)
    return source,body,tool,pivot,grip,gpivot,(-22 if action=='mine' else 22),rigs

def work_transition(prepared,q,n):
    source,body,tool,pivot,grip,gpivot,fold_angle,rigs=prepared
    if q==0:im=source.copy()
    else:
        # Stabilize the held workpiece; withdraw the tool clear of its edge.
        im=body.copy();im.alpha_composite(grip)
        pixels=np.array(im);labels,_=ndimage.label(pixels[:,:,3]>24)
        counts=np.bincount(labels.ravel());counts[0]=0
        keep=ndimage.binary_dilation(counts[labels]>100,iterations=2)
        pixels[:,:,3]=np.where(keep,pixels[:,:,3],0);im=Image.fromarray(pixels)
        im.alpha_composite(rotate(tool,fold_angle*q,pivot))
    return rotors(im,source,rigs,n)

def save_clip(data,key,bodies,effects,cargo,metadata):
    previous=next((s for s in data['states'] if s['id']==key and s['frameCount']==len(bodies)),{})
    atlases={k:previous[k] for k in ['atlas','effectAtlas','cargoAtlas'] if k in previous}
    folders={name:ROOT/name/key for name in ['frames','effects','cargo']}
    for path in folders.values():path.mkdir(parents=True,exist_ok=True)
    paths={name:[] for name in folders}
    for name,frames in [('frames',bodies),('effects',effects),('cargo',cargo)]:
        for i,im in enumerate(frames):
            p=folders[name]/f'{i:03}.png';save_png(im,p);paths[name].append(p.relative_to(ROOT).as_posix())
    data['states']=[s for s in data['states'] if s['id']!=key]
    data['states'].append({'id':key,'frameFiles':paths['frames'],'effectFiles':paths['effects'],'cargoFiles':paths['cargo'],
     'frameCount':len(bodies),'fps':FPS,'loop':False,'holdStart':metadata['phases'].index('Complete'),'statusLayer':'independent',**atlases,**metadata})

def main():
    data=json.loads((ROOT/'manifest.json').read_text());data['jobs']={};blank=Image.new('RGBA',(SIZE,SIZE))
    for direction in DIRS:
        lamp=data['headings'][direction]['lamp']
        for action in ['mine','weld','repair']:
            prepared=work_setup(direction,action,data);original=next(s for s in data['states'] if s['id']==f'work-{action}-{direction}')
            bodies=[];effects=[];phases=[]
            for i in range(30):
                im=work_transition(prepared,1-smooth(i/29),len(bodies))
                if i==29:im=rotors(Image.open(ROOT/original['frameFiles'][0]).convert('RGBA'),prepared[0],prepared[-1],len(bodies))
                bodies.append(im);effects.append(blank);phases.append('Reach')
            for i in range(102):
                im=Image.open(ROOT/original['frameFiles'][i]).convert('RGBA')
                bodies.append(rotors(im,prepared[0],prepared[-1],len(bodies)));effects.append(Image.open(ROOT/original['effectFiles'][i]).convert('RGBA'));phases.append('Work')
            for i in range(30):
                im=work_transition(prepared,smooth(i/29),len(bodies))
                if i==0:im=rotors(Image.open(ROOT/original['frameFiles'][-1]).convert('RGBA'),prepared[0],prepared[-1],len(bodies))
                bodies.append(im);effects.append(blank);phases.append('Stow')
            for i in range(51):
                bodies.append(work_transition(prepared,1,len(bodies)));effects.append(blank);phases.append('Complete')
            key=f'job-{action}-{direction}';save_clip(data,key,bodies,effects,[blank]*len(bodies),{'lamp':lamp,'phases':phases,'rootOffsets':[[0,0]]*len(bodies),'endpoint':'job-ready folded tool pose; work contact shares the existing source','method':'local raster articulation of authored arms; continuous blade clock'})
            data['jobs'][f'{action}-{direction}']=key
        prepared=collection_setup(direction);bodies=[];effects=[];cargo=[];phases=[];roots=[];ownership=[];events=[]
        fx,fy=FORWARD[direction];destination=[-fy*48,fx*34]
        stages=[('Ready',15,1,1,0,0,0,0),('Reach',30,1,0,0,0,0,0),('Grip',18,0,0,0,1,0,0),('Lift',24,0,.8,1,1,0,0),('Carry',60,.8,.8,1,1,0,1),('Lower',24,.8,0,1,1,1,1),('Release',18,0,0,1,0,1,1),('Withdraw',30,0,1,0,0,1,1),('Complete',51,1,1,0,0,1,1)]
        held=False;deposited=False
        for phase,count,q0,q1,c0,c1,r0,r1 in stages:
            for i in range(count):
                f=smooth(i/(count-1));n=len(bodies)
                if phase=='Grip' and i==count-1:held=True;events.append({'frame':n,'event':'attach-cargo'})
                if phase=='Release' and i==count//2:held=False;deposited=True;events.append({'frame':n,'event':'detach-cargo'})
                body,item=collect_frame(direction,prepared,q0+(q1-q0)*f,c0+(c1-c0)*f,n)
                bodies.append(body);effects.append(blank);cargo.append(item if held else blank);phases.append(phase)
                back=18 if phase=='Ready' else (18*(1-f) if phase=='Reach' else (24*f if phase=='Withdraw' else (24 if phase=='Complete' else 0)))
                roots.append([round(destination[0]*(r0+(r1-r0)*f)-fx*back,4),round(destination[1]*(r0+(r1-r0)*f)-fy*back,4)])
                ownership.append('held' if held else ('deposited' if deposited else 'pickup'))
        key=f'job-collect-{direction}';save_clip(data,key,bodies,effects,cargo,{'lamp':lamp,'phases':phases,'rootOffsets':roots,'cargoState':ownership,'cargoEvents':events,
         'groundCargo':f'poses/cargo-ore-{direction}.png','depositOffset':destination,'endpoint':'empty gripper; deposited cargo persists until explicit replay','method':'generated empty jaw pixels articulated at hinges; separate ore and root trajectory'})
        data['jobs'][f'collect-{direction}']=key
        print(direction,'job sequences built',flush=True)
    data['sourceFiles']=[{'path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted((ROOT/'sources').glob('*.png'))]
    temp=ROOT/'manifest.tmp.json';temp.write_text(json.dumps(data,indent=2));temp.replace(ROOT/'manifest.json')

if __name__=='__main__':main()
