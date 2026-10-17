"""Deterministic packaging of four generated tool keys and raster rotor motion.

No generation calls. South-facing review pilot only; no runtime bindings.
"""
from pathlib import Path
import hashlib
import json
import math
import numpy as np
from scipy import ndimage
from PIL import Image, ImageDraw, ImageFont, ImageChops

ROOT = Path(__file__).resolve().parent
SIZE = 256
SCALE = (69.12 / .34) / 634
PIVOT = (128, 128)
LENS = (128, 137)
FONT = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 17)
SMALL = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 13)

def clean(im):
    a = np.array(im)
    labels, count = ndimage.label(a[:, :, 3] > 24)
    sizes = np.bincount(labels.ravel())
    sizes[0] = 0
    keep = ndimage.binary_dilation(labels == sizes.argmax(), iterations=2)
    a[:, :, 3] = np.where(keep, a[:, :, 3], 0)
    return Image.fromarray(a)

def lens(im):
    a = np.array(im)
    yy, xx = np.indices(a.shape[:2])
    selection = ((a[:,:,0] < 140) & (a[:,:,1] > 170) & (a[:,:,2] > 170)
                 & (xx > 300) & (xx < 385) & (yy > 270) & (yy < 360))
    points = np.argwhere(selection)
    assert len(points) > 15, 'Front lens registration landmark missing'
    y, x = points.mean(axis=0)
    return (float(x), float(y))

def registered(im, anchor):
    im = im.convert('RGBa').resize((round(im.width*SCALE), round(im.height*SCALE)), Image.Resampling.LANCZOS).convert('RGBA')
    out = Image.new('RGBA', (SIZE,SIZE))
    out.alpha_composite(im, (round(LENS[0]-anchor[0]*SCALE), round(LENS[1]-anchor[1]*SCALE)))
    return out

sheet = Image.open(ROOT/'sources/construction-tool-poses-v2.png').convert('RGBA')
poses, anchors = [], []
for i in range(4):
    col,row=i%2,i//2
    cell=clean(sheet.crop((round(col*sheet.width/2),round(row*sheet.height/2),round((col+1)*sheet.width/2),round((row+1)*sheet.height/2))))
    anchor=lens(cell)
    anchors.append(anchor)
    poses.append(registered(cell,anchor))

lamp=Image.open(ROOT/'sources/drone-status-light.png').convert('RGBA')
lamp=lamp.crop(lamp.getchannel('A').point(lambda a:255 if a>64 else 0).getbbox())
lamp=lamp.resize((12,12),Image.Resampling.LANCZOS)

def rotor(im, center, radii, angle):
    """Rotate only existing propeller disk pixels in its projected ellipse."""
    a=np.array(im).astype(float)
    yy,xx=np.indices(a.shape[:2])
    dx=(xx-center[0])/radii[0]; dy=(yy-center[1])/radii[1]
    radius=np.sqrt(dx*dx+dy*dy)
    sx=center[0]+radii[0]*(dx*math.cos(angle)+dy*math.sin(angle))
    sy=center[1]+radii[1]*(-dx*math.sin(angle)+dy*math.cos(angle))
    rotated=np.stack([ndimage.map_coordinates(a[:,:,c],[sy,sx],order=1,mode='nearest') for c in range(4)],axis=2)
    weight=np.clip((.92-radius)/.12,0,1)[:,:,None]
    return Image.fromarray(np.uint8(np.clip(a*(1-weight)+rotated*weight,0,255)))

def led(im,t):
    out=im.copy()
    bright=lamp.convert('L').point(lambda v:max(0,min(255,(v-90)*3)))
    pulse=.25+.75*(.5+.5*math.cos(t*math.tau/.85))**3
    colored=Image.new('RGBA',lamp.size,(48,155,255,255))
    colored.putalpha(ImageChops.multiply(bright,lamp.getchannel('A')).point(lambda v:round(v*pulse)))
    lit=lamp.copy();lit.alpha_composite(colored)
    # Accepted v10 hull placement: centered X, 17% above hull bounding-box center.
    # Fixed to registered neutral hull, never to moving tool bounds.
    bbox=poses[0].getbbox()
    y=round((bbox[1]+bbox[3])/2-(bbox[3]-bbox[1])*.17)
    out.alpha_composite(lit,(122,y-6))
    return out

frames={}
for state, duration, rotations in [('idle-south',2.0,.5),('swim-south',1.0,2.0)]:
    clip=[]
    for f in range(24):
        t=duration*f/24
        im=poses[0].copy()
        for center,sign in [((85,240),1),((604,236),-1)]:
            at=(LENS[0]+(center[0]-anchors[0][0])*SCALE,LENS[1]+(center[1]-anchors[0][1])*SCALE)
            im=rotor(im,at,(29*SCALE,55*SCALE),sign*t*math.tau*rotations)
        clip.append((led(im,t),round(duration*1000/24)))
    frames[state]=clip

# Holds are explicit: four authored keys, no invented in-between claims.
sequence=[(0,300),(1,240),(2,500),(3,240),(0,320)]
frames['tool-cycle-south']=[(led(poses[key],sum(d for _,d in sequence[:i])/1000),ms) for i,(key,ms) in enumerate(sequence)]
manifest={
    'id':'construction-drone-pilot-v1','frameWidth':SIZE,'frameHeight':SIZE,
    'pivot':list(PIVOT),'registrationLandmark':{'frontLens':list(LENS)},
    'worldUnitsPerPixel':.34,'nominalHullWidthWorld':69.12,
    'camera':'approved steep overhead south-facing','mirroringAllowed':False,
    'scope':'Review pilot; south only; not installed; four authored tool keys, coarse timing',
    'sourceAnchors':anchors,'states':[],
    'statusSemantics':{'blue':'operational','red':'stopped','yellow':'charging or out of power'},
    'statusCoverage':'blue only in this operational pilot',
    'omitted':['north/east/west','separate build/repair actions','contact targets','launch/recovery integration','pathfinding'],
    'sources':[{ 'file':str(p.relative_to(ROOT)).replace('\\','/'),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted((ROOT/'sources').glob('*.png'))]
}
for state,clip in frames.items():
    folder=ROOT/'frames'/state;folder.mkdir(parents=True,exist_ok=True)
    paths=[]
    for i,(im,ms) in enumerate(clip):
        p=folder/f'{i:03}.png';im.save(p);paths.append(p.relative_to(ROOT).as_posix())
        bbox=im.getbbox()
        assert bbox and min(bbox[:2])>0 and max(bbox[2:])<SIZE, 'Clipped frame'
    manifest['states'].append({'id':state,'frameCount':len(clip),'frameFiles':paths,
        'frameDurationsMs':[ms for _,ms in clip],'loop':True,
        'method':'four generated pose keys with timed neutral/reach/contact/release holds' if state.startswith('tool') else 'registered neutral source; projected raster rotor rotation and status pulse'})
    strip=Image.new('RGBA',(SIZE*len(clip),SIZE))
    for i,(im,_) in enumerate(clip):strip.alpha_composite(im,(i*SIZE,0))
    (ROOT/'strips').mkdir(exist_ok=True);strip.save(ROOT/'strips'/f'{state}.png')
(ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')

def frame_at(clip,ms):
    ms%=sum(duration for _,duration in clip)
    for im,duration in clip:
        if ms<duration:return im
        ms-=duration
    return clip[-1][0]

reviews=[]
for i in range(120):
    canvas=Image.new('RGB',(960,470),'#17272e');d=ImageDraw.Draw(canvas)
    d.text((22,16),'CONSTRUCTION / SOUTH MOTION PILOT',font=FONT,fill='#e6eff2')
    d.text((22,42),'Four tool keys. Provisional scale: 69 world units. No game installation.',font=SMALL,fill='#b4c6ce')
    for j,(state,clip) in enumerate(frames.items()):
        im=frame_at(clip,i*50)
        canvas.paste(im,(32+j*320,81),im)
        d.text((35+j*320,68),state.replace('-south','').upper(),font=SMALL,fill='#88cbd4')
        native=im.resize((87,87),Image.Resampling.LANCZOS)
        canvas.paste(native,(114+j*320,340),native)
    d.text((22,446),'Top: enlarged detail     Bottom: 1 pixel per world unit',font=SMALL,fill='#b4c6ce')
    reviews.append(canvas)
out=ROOT/'review';out.mkdir(exist_ok=True)
reviews[0].save(out/'motion-preview.gif',save_all=True,append_images=reviews[1:],duration=50,loop=0,optimize=False)
board=Image.new('RGB',(1024,310),'#d5dce0');d=ImageDraw.Draw(board)
for i,im in enumerate(poses):
    board.paste(im,(i*256,30),im);d.text((i*256+20,8),['Neutral','Reach','Contact','Release'][i],font=FONT,fill='#20323a')
board.save(out/'tool-contact-sheet.png')
print(json.dumps({'frames':sum(len(c) for c in frames.values()),'states':len(frames),'authoredToolKeys':4,'transparentBorders':'pass','reviewFrames':len(reviews)}))
