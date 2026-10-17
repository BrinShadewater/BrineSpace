"""Reproject accepted blade pixels about corrected hubs; keep housings fixed.

Small raster animation rig, not a redraw of the drone. The axle highlight is
stationary. Motion samples are averaged before reduction to library density.
"""
from pathlib import Path
import json, math
import numpy as np
from scipy import ndimage
from PIL import Image, ImageDraw, ImageFont, ImageChops

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'sources/south-reference.png'
PERIOD=1.7
FPS=30
COUNT=51
RIG=[{'center':(88,249),'u':(30,-5),'v':(10,50),'sign':1},
     {'center':(612,249),'u':(30,5),'v':(-10,50),'sign':-1}]

def clean(im):
    a=np.array(im)
    labels,_=ndimage.label(a[:,:,3]>24)
    counts=np.bincount(labels.ravel());counts[0]=0
    keep=ndimage.binary_dilation(labels==counts.argmax(),iterations=2)
    a[:,:,3]=np.where(keep,a[:,:,3],0)
    return Image.fromarray(a)

def rotor_setup(im, rig):
    a=np.asarray(im).astype(float)
    yy,xx=np.indices(a.shape[:2]);cx,cy=rig['center']
    basis=np.array([rig['u'],rig['v']],dtype=float).T
    inverse=np.linalg.inv(basis)
    uv=np.einsum('ij,jhw->ihw',inverse,np.array([xx-cx,yy-cy]))
    radius=np.sqrt((uv**2).sum(axis=0))
    # Inner feather preserves the axle; outer feather preserves intake/rim.
    mask=np.clip((radius-.44)/.10,0,1)*np.clip((.94-radius)/.12,0,1)
    return a,uv,basis,mask

def _spin_patch(im, rig, phase, turns, blur=True):
    a,uv,basis,mask=rotor_setup(im,rig)
    if phase==0 and not blur:return im.copy(),mask
    cx,cy=rig['center'];samples=[]
    # 180-degree shutter; source pixels sampled at five times during exposure.
    shutter=(turns/PERIOD)*math.tau/(FPS*2) if blur else 0
    for step in [-.5,-.25,0,.25,.5] if blur else [0]:
        angle=rig['sign']*(phase*turns*math.tau+step*shutter)
        rot=np.array([[math.cos(angle),math.sin(angle)],[-math.sin(angle),math.cos(angle)]])
        source=np.einsum('ij,jhw->ihw',basis@rot,uv)
        source[0]+=cx;source[1]+=cy
        samples.append(np.stack([ndimage.map_coordinates(a[:,:,c],[source[1],source[0]],order=1,mode='nearest') for c in range(4)],axis=2))
    blurred=np.mean(samples,axis=0)
    result=np.rint(a*(1-mask[:,:,None])+blurred*mask[:,:,None]).clip(0,255).astype(np.uint8)
    return Image.fromarray(result),mask

def spin(im,rig,phase,turns,blur=True):
    cx,cy=rig['center']
    rx=abs(rig['u'][0])+abs(rig['v'][0])+3
    ry=abs(rig['u'][1])+abs(rig['v'][1])+3
    box=(max(0,int(cx-rx)),max(0,int(cy-ry)),min(im.width,int(cx+rx+1)),min(im.height,int(cy+ry+1)))
    local=dict(rig,center=(cx-box[0],cy-box[1]))
    patch,mask=_spin_patch(im.crop(box),local,phase,turns,blur)
    out=im.copy();out.paste(patch,box[:2])
    full=np.zeros((im.height,im.width));full[box[1]:box[3],box[0]:box[2]]=mask
    return out,full

def add_lamp(im,t,color=(48,155,255)):
    out=im.copy()
    lamp_path=ROOT/'sources/drone-status-light.png'
    lamp=Image.open(lamp_path).convert('RGBA')
    lamp=lamp.crop(lamp.getchannel('A').point(lambda a:255 if a>64 else 0).getbbox()).resize((30,30),Image.Resampling.LANCZOS)
    pulse=.18+.82*(.5+.5*math.cos(t*math.tau/.85))
    bright=lamp.convert('L').point(lambda v:max(0,min(255,(v-90)*3)))
    dark=Image.new('RGBA',lamp.size,(9,20,29,255))
    dark.putalpha(ImageChops.multiply(bright,lamp.getchannel('A')))
    lamp.alpha_composite(dark)
    light=Image.new('RGBA',lamp.size,color+(255,))
    light.putalpha(ImageChops.multiply(bright,lamp.getchannel('A')).point(lambda v:round(v*pulse)))
    lamp.alpha_composite(light)
    # Centered on dorsal steel, at the accepted neutral-hull offset.
    out.alpha_composite(lamp,(334,198))
    return out

def main():
    source=clean(Image.open(SOURCE).convert('RGBA'))
    out=ROOT/'review';out.mkdir(exist_ok=True)
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
    small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14)
    frames=[];checks=[]
    for n in range(COUNT):
        canvas=Image.new('RGB',(1080,650),'#18272f');draw=ImageDraw.Draw(canvas)
        draw.text((24,16),'PROPELLER REVISION / fixed housings + corrected centers + continuous top light',font=font,fill='#deebef')
        for column,(name,turns) in enumerate([('Idle',1),('Travel',6)]):
            im=source.copy();combined=np.zeros((source.height,source.width),bool)
            for rig in RIG:
                im,mask=spin(im,rig,n/COUNT,turns)
                combined|=mask>0
            delta=np.any(np.asarray(source)!=np.asarray(im),axis=2)
            assert not np.any(delta & ~combined),'Stationary housing or hub modified'
            checks.append(int(delta.sum()))
            im=add_lamp(im,n/FPS)
            im=im.resize((480,400),Image.Resampling.LANCZOS)
            canvas.paste(im,(column*540+30,70),im)
            draw.text((column*540+30,50),name,font=font,fill='#cbdde5')
            native=im.resize((75,63),Image.Resampling.LANCZOS)
            canvas.paste(native,(column*540+234,522),native)
        draw.text((24,610),'Upper: enlarged inspection. Lower: approximate game size. Blue = operational.',font=small,fill='#b3c6cf')
        frames.append(canvas)
    frames[0].save(out/'propeller-revision.gif',save_all=True,append_images=frames[1:],duration=[33,33,34]*17,loop=0,optimize=False)
    for n in [0,6,13,25,38]:frames[n].save(out/f'propeller-phase-{n:02}.png')
    report={'frames':COUNT,'fps':FPS,'durationSeconds':PERIOD,'rig':RIG,'staticHousingAndHubInvariant':'pass','changedRotorPixelRange':[min(checks),max(checks)],'lampPeriodSeconds':.85,'method':'five shutter samples; annular blade masks; fixed hub/rim; corrected affine projected axes'}
    (out/'propeller-checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report))

if __name__=='__main__':main()
