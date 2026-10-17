"""Package independent headings and work contacts into a layered review pack.

Sources remain immutable. Raster blade rotation uses corrected local rigs;
status and work effects are evaluated independently by the review player.
"""
from pathlib import Path
import json,hashlib,math
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from build_rotor_review import clean,spin

ROOT=Path(__file__).resolve().parent
SIZE=256
FONT=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',15)
SOURCE=ROOT/'sources'

def cell(name,index=None):
    im=Image.open(SOURCE/name).convert('RGBA')
    if index is not None:
        x,y=index%2,index//2
        im=im.crop((round(x*im.width/2),round(y*im.height/2),round((x+1)*im.width/2),round((y+1)*im.height/2)))
    return clean(im)

def centered(im,anchor,scale):
    new=im.convert('RGBa').resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS).convert('RGBA')
    result=Image.new('RGBA',(SIZE,SIZE))
    result.alpha_composite(new,(round(128-anchor[0]*scale),round(128-anchor[1]*scale)))
    return result

def rig(c,u,v,sign=1):return {'center':c,'u':u,'v':v,'sign':sign}
def transformed(r,anchor,scale):
    return rig((128+(r['center'][0]-anchor[0])*scale,128+(r['center'][1]-anchor[1])*scale),
               tuple(x*scale for x in r['u']),tuple(x*scale for x in r['v']),r['sign'])

# Origins are chassis landmarks, not changing whole-sprite bounding-box centers.
# Common sheet scale retained; single-view source scales match the chassis family.
views={
 'south':{'file':'south-reference.png','cell':None,'anchor':(350,236),'scale':203.294/634,
          'rotors':[rig((88,249),(30,-5),(10,50)),rig((612,249),(30,5),(-10,50),-1)]},
 'east':{'file':'cardinal-v2-partial-north-rejected.png','cell':1,'anchor':(292,298),'scale':.305,
         'rotors':[rig((354,157),(36,0),(0,42)),rig((351,516),(36,0),(0,42),-1)]},
 'west':{'file':'cardinal-v2-partial-north-rejected.png','cell':3,'anchor':(394,291),'scale':.305,
         'rotors':[rig((339,116),(37,0),(0,40)),rig((341,467),(37,0),(0,40),-1)]},
 'north':{'file':'north-v1.png','cell':None,'anchor':(684,580),'scale':.163,
          'rotors':[rig((165,704),(60,-10),(20,98)),rig((1212,704),(60,10),(-20,98),-1)]},
 'southeast':{'file':'diagonal-v1-partial.png','cell':1,'anchor':(333,230),'scale':.32,
              'rotors':[rig((86,360),(35,0),(0,34)),rig((548,190),(26,0),(0,44),-1)]},
 'northwest':{'file':'northwest-curve-v4.png','cell':None,'anchor':(700,550),'scale':.16,
              'rotors':[rig((199,785),(53,-3),(5,76)),rig((1228,520),(59,0),(0,81),-1)]},
}

def camera_anchor(im):
    a=np.array(im);y,x=np.indices(a.shape[:2])
    mask=(a[:,:,0]<140)&(a[:,:,1]>170)&(a[:,:,2]>170)&(x>275)&(x<420)&(y>170)&(y<380)
    yy,xx=np.argwhere(mask).mean(axis=0)
    return (float(xx),float(yy)-90)

def main():
    extra=ROOT/'additional-views.json'
    if extra.exists():views.update(json.loads(extra.read_text(encoding='utf-8')))
    order=['north','northeast','east','southeast','south','southwest','west','northwest']
    metadata={'id':'construction-motion-v2','frameWidth':SIZE,'frameHeight':SIZE,'pivot':[128,128],
              'worldUnitsPerPixel':.34,'nominalSouthHullWidthWorld':69.12,'fps':30,
              'lamp':{'periodSeconds':.85,'operational':'#309bff','stopped':'#ff302e','charging':'#ffcd2d','layer':'separate; continuous across action changes'},
              'headings':{},'actions':{},'states':[],
              'scope':'Review assets; no runtime role changes. Eight-heading travel and south-facing work contacts.',
              'sourceFiles':[]}
    (ROOT/'poses').mkdir(exist_ok=True)
    review=Image.new('RGB',(1024,600),'#17272e');d=ImageDraw.Draw(review)
    for index,name in enumerate(order):
        if name not in views:continue
        spec=views[name];im=cell(spec['file'],spec.get('cell'));anchor=spec['anchor'];scale=spec['scale']
        base=centered(im,anchor,scale)
        base.save(ROOT/'poses'/f'{name}.png')
        rigs=[transformed(r,anchor,scale) for r in spec['rotors']]
        lamp_offsets={'south':(0,-7),'north':(0,7),'east':(-7,0),'west':(7,0),'southeast':(-5,-5),'southwest':(5,-5),'northeast':(-5,5),'northwest':(5,5)}
        offset=lamp_offsets[name];lamp=[128+offset[0],128+offset[1]]
        metadata['headings'][name]={'pose':f'poses/{name}.png','lamp':lamp,'rotors':rigs,'source':spec}
        for state,turns in [('idle',1),('move',6)]:
            folder=ROOT/'frames'/f'{state}-{name}';folder.mkdir(parents=True,exist_ok=True)
            paths=[]
            for n in range(51):
                frame=base.copy();combined=np.zeros((SIZE,SIZE),bool)
                for r in rigs:
                    frame,mask=spin(frame,r,n/51,turns)
                    combined|=mask>0
                changed=np.any(np.asarray(base)!=np.asarray(frame),axis=2)
                assert not np.any(changed & ~combined)
                p=folder/f'{n:03}.png';frame.save(p);paths.append(p.relative_to(ROOT).as_posix())
            metadata['states'].append({'id':f'{state}-{name}','frameFiles':paths,'frameCount':51,'fps':30,'loop':True,'statusLayer':'independent'})
        x=(index%4)*256;y=(index//4)*300
        review.paste(base,(x,y+30),base);d.text((x+15,y+8),name.upper(),font=FONT,fill='#cadce5')
        # Diagnostic markers stay in a separate review artifact, never exports.
        for r in rigs:
            cx,cy=r['center'];d.ellipse((x+cx-2,y+30+cy-2,x+cx+2,y+30+cy+2),fill='#ee6e58')
    review.save(ROOT/'review/direction-registration.png')
    contact=Image.new('RGB',(1024,310),'#17272e');cd=ImageDraw.Draw(contact)
    for index,name in enumerate(['mine','collect','weld','repair']):
        im=cell('work-contacts-v1.png',index);anchor=camera_anchor(im);scale=.335
        pose=centered(im,anchor,scale);pose.save(ROOT/'poses'/f'{name}-south.png')
        # Work tools and targets are authored separately for each action.
        metadata['actions'][name]={'pose':f'poses/{name}-south.png','direction':'south','lamp':[128,121],
            'anchorSource':anchor,'sourceCell':index,'scale':scale,
            'phaseChain':['approach','engage','work','release'],'durationSeconds':3.4,
            'effect':{'mine':'boring bit + sediment','collect':'grip and retract ore','weld':'localized arc along plate edge','repair':'short tool pulses at bracket fastener'}[name]}
        contact.paste(pose,(index*256,28),pose);cd.text((index*256+15,7),name.upper(),font=FONT,fill='#cadce5')
    contact.save(ROOT/'review/work-contacts.png')
    for p in sorted(SOURCE.glob('*.png')):metadata['sourceFiles'].append({'path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    (ROOT/'manifest.json').write_text(json.dumps(metadata,indent=2),encoding='utf-8')
    print(json.dumps({'headings':len(metadata['headings']),'clips':len(metadata['states']),'workContacts':len(metadata['actions']),'housingInvariance':'pass'}))

if __name__=='__main__':main()
