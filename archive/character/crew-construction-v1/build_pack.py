"""Package generated sources; chroma removal and foot registration only, no invented poses."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent
DIRECTIONS=['east','south','west','north']
def bands(values):
    groups=[]
    for i in np.flatnonzero(values):
        if not groups or i>groups[-1][-1]+1: groups.append([])
        groups[-1].append(int(i))
    return [(g[0],g[-1]+1) for g in groups if len(g)>30]
def clean(source):
    im=Image.open(source).convert('RGBA')
    a=np.array(im)
    key=(a[:,:,0]>40)&(a[:,:,2]>35)&(a[:,:,1]<135)&(a[:,:,0]>a[:,:,1]*1.4)&(a[:,:,2]>a[:,:,1]*1.4)
    a[key]=0
    im=Image.fromarray(a)
    rows=bands((a[:,:,3]>0).sum(axis=1)>12)
    assert len(rows)==4,(str(source),rows)
    return im,rows
def build(actor):
    source=ROOT/'source'/f'{actor}.png'
    im,rows=clean(source)
    out=ROOT/actor
    out.mkdir(exist_ok=True)
    states=[]; contact=Image.new('RGBA',(6*92,4*92),(25,34,37,255))
    all_frames=[]
    for row,(top,bottom) in enumerate(rows):
        row_image=im
        if actor=='bill' and row in [1,3]:
            row_image,revised_rows=clean(ROOT/'source'/'bill-direction-v2.png')
            top,bottom=revised_rows[row]
        direction=DIRECTIONS[row]; images=[]; anchors=[]
        for col in range(6):
            crop=row_image.crop((col*row_image.width//6,top,(col+1)*row_image.width//6,bottom))
            pix=np.array(crop)
            feet=np.argwhere(pix[int(crop.height*.88):,:,3]>0)
            assert len(feet)>0
            anchor=((float(feet[:,1].min())+float(feet[:,1].max())+1)/2,crop.height)
            images.append(crop); anchors.append(anchor)
        # Shared scale per row retains arm motion; feet are the sole registration anchor.
        body_heights=[]
        for crop in images:
            pix=np.array(crop)
            body=np.argwhere((pix[:,:,3]>0)&(pix[:,:,:3].max(axis=2)<185))
            body_heights.append(crop.height-int(body[:,0].min()))
        factor=74/float(np.median(body_heights))
        files=[]
        for col,(crop,anchor) in enumerate(zip(images,anchors)):
            resized=crop.resize((round(crop.width*factor),round(crop.height*factor)),Image.Resampling.NEAREST)
            frame=Image.new('RGBA',(92,92))
            frame.alpha_composite(resized,(round(46-anchor[0]*factor),round(86-anchor[1]*factor)))
            assert frame.getbbox() and frame.getbbox()[0]>0 and frame.getbbox()[2]<92
            dest=f'weld-{direction}-{col:03d}.png';frame.save(out/dest);files.append(dest)
            contact.alpha_composite(frame,(col*92,row*92))
            images[col]=frame
        states.append(dict(id=f'weld-{direction}',frameFiles=files,frameDurationsMs=[160]*6,loop=True))
        all_frames.append(images)
    manifest=dict(character=actor,frameWidth=92,frameHeight=92,standingHeight=74,background='transparent',pivot=[46,86],states=states,source=str(source.relative_to(ROOT)),sourceSha256=hashlib.sha256(source.read_bytes()).hexdigest(),authoring='Generated four-direction source; no mirrored views; chroma removed; nearest resize; feet registered',rowBounds=rows)
    if actor=='bill':
        revision=ROOT/'source'/'bill-direction-v2.png'
        manifest['directionRevision']={'source':str(revision.relative_to(ROOT)),'sha256':hashlib.sha256(revision.read_bytes()).hexdigest(),'rows':['south','north'],'reason':'Original forward/backward poses incorrectly aimed the torch sideways; original east/west rows retained.'}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    contact.save(out/'contact-sheet.png')
    preview=[]
    for phase in range(6):
        tile=Image.new('RGBA',(4*92,92),(25,34,37,255))
        for d in range(4): tile.alpha_composite(all_frames[d][phase],(d*92,0))
        preview.append(tile.convert('RGB').resize((4*184,184),Image.Resampling.NEAREST))
    preview[0].save(out/'preview.gif',save_all=True,append_images=preview[1:],duration=160,loop=0,disposal=2)
    print(actor,len(states),'clips',sum(len(s['frameFiles']) for s in states),'frames; alpha, canvas and bounds pass')
if __name__=='__main__':
    import sys
    for actor in sys.argv[1:] or ['bill','veld','branforth']: build(actor)
