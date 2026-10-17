"""Register the accepted James south study and fit the selected common shell."""
from pathlib import Path
import math,json,hashlib
import numpy as np
from scipy import ndimage
from scipy.signal import savgol_filter
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
SOURCE=ROOT/'character/james-interact-south-direct-v1'
BARE=ROOT/'character/james-interact-south-matched-v1'
SHELL=ROOT/'character/james-shared-helmet-south-v1/helmet.png'

def idle(path):
    m=json.loads(path.read_text());s=next(s for s in m['states'] if s['id']=='idle-south')
    return Image.open(path.parent/s['frameFiles'][0]).convert('RGBA')

def face(image):
    a=np.array(image);r,g,b=a[:,:,:3].astype(float).transpose(2,0,1);yy,xx=np.indices(a.shape[:2]);top=np.where(a[:,:,3]>192)[0].min()
    mask=(r>g+10)&(r>b+12)&(g>b+2)&(a[:,:,3]>150)&(yy<top+27)&(r+g+b>180)&(~((g>b+15)&(r-g<15)))
    labels,n=ndimage.label(mask);counts=np.bincount(labels.ravel());counts[0]=0
    if counts.max()<60:raise AssertionError('Uncertain head tracking')
    y,x=np.where(labels==counts.argmax());return np.array([x.mean(),y.mean()]),[int(x.min()),int(y.min()),int(x.max()),int(y.max())],int(len(x))

def crown(image):
    a=np.array(image);yy,xx=np.indices(a.shape[:2]);opaque=a[:,:,3]>192
    top=int(yy[opaque].min());mask=opaque&(yy<top+6)
    return np.array([xx[mask].mean(),float(top)])

def rotate_point(point,angle):
    c,s=math.cos(math.radians(angle)),math.sin(math.radians(angle))
    x,y=point;return np.array([c*x+s*y,-s*x+c*y])

def main():
    BARE.mkdir(exist_ok=True);bare_idle=idle(ROOT/'character/crew-runtime-matte-v1/branforth/manifest.json');worn_idle=idle(ROOT/'character/james-shared-helmet-runtime-v1/manifest.json')
    original=[Image.open(SOURCE/f'graded/{i:03}.png').convert('RGBA') for i in range(141)]
    # Three transient frames inherit a brown/green source lighting flash.
    # Restore neighbouring graphite chroma, retaining each pixel's luminance,
    # alpha and pose. Reference materials exclude skin, hair and yellow patches.
    reference_rgb=np.median(np.array([np.array(original[i])[:,:,:3] for i in list(range(79,85))+list(range(90,96))]),axis=0)
    reference_luma=reference_rgb@np.array([.2126,.7152,.0722])
    ref_chroma=reference_rgb-reference_luma[:,:,None]
    yy=np.indices(reference_luma.shape)[0]
    neutral=(np.ptp(reference_rgb,axis=2)<16)&(yy>59)
    colour_records=[]
    for i in [86,87,88]:
        a=np.array(original[i]);rgb=a[:,:,:3].astype(float)
        mask=neutral&(a[:,:,3]>0)&(np.ptp(rgb,axis=2)<32)
        luma=rgb@np.array([.2126,.7152,.0722])
        corrected=np.clip(np.rint(luma[:,:,None]+ref_chroma),0,255).astype('uint8')
        # The source flash also tints leather, trim and yellow markings.
        # Remove only the measured common cast there, preserving material chroma.
        sample=(a[:,:,3]>240)&(yy>100)&(yy<165)&(rgb.mean(2)>25)&(rgb.mean(2)<100)&(np.ptp(rgb,axis=2)<25)
        sample_rgb=np.median(rgb[sample],axis=0)
        reference_sample=np.median(reference_rgb[sample],axis=0)
        cast=sample_rgb-reference_sample
        cast-=cast@np.array([.2126,.7152,.0722])
        body_mask=(yy>59)&(a[:,:,3]>0)
        b=a.copy();b[:,:,:3][body_mask]=np.clip(np.rint(rgb-cast),0,255).astype('uint8')[body_mask]
        b[:,:,:3][mask]=corrected[mask]
        mask=body_mask
        assert np.array_equal(a[:,:,3],b[:,:,3])
        assert np.array_equal(a[~mask],b[~mask])
        original[i]=Image.fromarray(b)
        colour_records.append(dict(sourceFrame=i,changedPixels=int(np.any(a!=b,axis=2).sum()),alphaExact=True,outsideMaskExact=True))
    (HERE/'colour-flash-v3.json').write_text(json.dumps(dict(method='Transient86-88 graphite chroma from neighbouring79-84/90-95; luminance/alpha/pose preserved, head excluded; coloured materials retain chroma after measured common cast removal',records=colour_records),indent=2)+'\n')
    reference,_box,_count=face(original[0]);shell=Image.open(SHELL).convert('RGBA')
    baseline=np.array([73,17]);center=np.array([shell.width/2,shell.height/2]);registered=[];equipped=[];tracking=[]
    # Crown silhouette stays visible during the nod; skin components do not.
    # Smooth its small authored movement without altering any body pixels.
    crown_reference=crown(original[0])
    crowns=[]
    for image in original:
        a=np.array(image);y,x=np.where(a[162:176,94:134,3]>160)
        shift=np.array([97,171])-np.array([94+x.min(),162+y.max()])
        crowns.append(crown(image)+shift)
    smooth_crowns=savgol_filter(np.array(crowns),13,2,axis=0,mode='interp')
    # Planted front boot matches installed idle at (118,167). Search only its
    # local footprint; hands and the rear boot cannot influence registration.
    for index,image in enumerate(original):
        a=np.array(image);roi=a[162:176,94:134,3]>160;y,x=np.where(roi)
        anchor=np.array([94+x.min(),162+y.max()]);shift=np.array([97,171])-anchor
        if np.any(np.abs(shift)>3):raise AssertionError('Front contact drift exceeds registration tolerance')
        body=Image.new('RGBA',(184,184));body.alpha_composite(image,tuple(map(int,shift)))
        raw_face,box,count=face(body)
        target=reference+smooth_crowns[index]-crown_reference
        angle=0.0
        rotated=shell.rotate(angle,resample=Image.Resampling.BICUBIC,expand=True)
        # Rotate about the reference face so helmet motion follows the head.
        face_shell=reference-baseline
        face_rotated=rotate_point(face_shell-center,angle)+np.array([rotated.width/2,rotated.height/2])
        at=np.rint(target-face_rotated).astype(int)
        out=body.copy();draw=ImageDraw.Draw(out)
        local=[(-13,-20),(13,-20),(16,7),(9,13),(-9,13),(-16,7)]
        clear=[tuple(target+rotate_point(point,angle)) for point in local]
        draw.polygon(clear,fill=(0,0,0,0))
        out.alpha_composite(rotated,tuple(map(int,at)))
        registered.append(body);equipped.append(out)
        tracking.append(dict(sourceFrame=index,boot=anchor.tolist(),translation=shift.tolist(),face=target.round(3).tolist(),rawFace=raw_face.round(3).tolist(),crown=smooth_crowns[index].round(3).tolist(),facePixels=count,angle=angle,helmetPosition=at.tolist(),helmetBounds=at.tolist()+(at+rotated.size).tolist()))
    # Preserve the full authored meter lift/read/tap/holster.
    indices=list(range(141))
    clips={'interact-south':indices};packs=[]
    for dest,rows,eidle in [(BARE,registered,bare_idle),(HERE,equipped,worn_idle)]:
        manifest=dict(name='James standing meter interaction '+('shared helmet' if dest==HERE else 'bare'),frameWidth=184,frameHeight=184,pivot=[92,172],standingHeight=148,precomposed=True,textureFilter='linear',status='staged_south_meter_interaction',states=[])
        for key,indices in clips.items():
            folder=dest/'frames'/key;folder.mkdir(parents=True,exist_ok=True);files=[]
            total=5500
            durations=[round((i+1)*total/len(indices))-round(i*total/len(indices)) for i in range(len(indices))]
            for i,source_index in enumerate(indices):
                image=rows[source_index].copy()
                if i==0 or i==len(indices)-1:image=eidle.copy()
                filename=folder/f'{i:03}.png';image.save(filename);files.append(filename.relative_to(dest).as_posix())
            manifest['states'].append(dict(id=key,frameCount=len(files),frameFiles=files,frameDurationsMs=durations,loop=False,provenance=dict(sourceFrames=indices,source=SOURCE.relative_to(ROOT).as_posix(),derivation='Full front-view source lift/read/tap/holster0-140; exact installed idle endpoints',colour='Owner accepted neutral-v3')))
        (dest/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');packs.append(manifest)
    report=dict(sourceSha256=hashlib.sha256((SOURCE/'source.mp4').read_bytes()).hexdigest(),helmetSha256=hashlib.sha256(SHELL.read_bytes()).hexdigest(),standingEndpoint='Exact installed idle',frontBoot=[97,171],helmetTracking='crown-fit-v2: visible head crown, Savitzky-Golay 13 frames/order2; upright selected shell',tracking=tracking,limits=['Standing meter interaction staged for owner review.','Full south source completes the meter holster.','Other states remain installed/retained.'])
    (HERE/'registration.json').write_text(json.dumps(report,indent=2)+'\n')
    previews=[];times=[]
    for key,repeats in [('interact-south',1)]:
        states=[next(s for s in m['states'] if s['id']==key) for m in packs]
        for repeat in range(repeats):
            for i in range(states[0]['frameCount']):
                board=Image.new('RGB',(920,255),'#303b40');d=ImageDraw.Draw(board);d.text((8,6),'James south - '+key+' / bare / shared helmet / 82px / 54px / 27px',fill='white')
                images=[]
                for dest,state,x in [(BARE,states[0],0),(HERE,states[1],220)]:
                    im=Image.open(dest/state['frameFiles'][i]).convert('RGBA');board.paste(im,(x,40),im);images.append(im)
                for h,x in [(82,460),(54,660),(27,800)]:
                    side=round(184*h/148)
                    for j,im in enumerate(images):
                        small=im.resize((side,side),Image.Resampling.BILINEAR);board.paste(small,(x+j*(side+8),40+172-round(side*172/184)),small)
                previews.append(board);times.append(states[0]['frameDurationsMs'][i])
    previews[0].save(HERE/'review.gif',save_all=True,append_images=previews[1:],duration=times,loop=0)
    sheet=Image.new('RGB',(1104,440),'#303b40');d=ImageDraw.Draw(sheet)
    for row,(dest,statekey) in enumerate([(dest,key) for key in clips for dest in [BARE,HERE]]):
        m=packs[0 if dest==BARE else 1];state=next(s for s in m['states'] if s['id']==statekey)
        for col,i in enumerate(np.linspace(0,state['frameCount']-1,6).astype(int)):
            im=Image.open(dest/state['frameFiles'][i]).convert('RGBA');pos=(col*184,row*220+20);sheet.paste(im,pos,im);d.text((pos[0]+5,pos[1]-15),statekey+' '+str(i),fill='white')
    sheet.save(HERE/'contact.png');(HERE/'index.html').write_text('<!doctype html><style>body{background:#303b40;color:white;font:18px system-ui;max-width:1104px;margin:auto}img{max-width:100%}</style><h1>James south meter interaction</h1><p>Bare and shared helmet. Exact installed idle endpoints; full original south meter lift/read/tap/holster. Staged for owner review.</p><img src="review.gif"><img src="contact.png">')
    print('Staged bare/equipped chain: '+str(sum(len(v) for v in clips.values()))+' frames per mode; boot contact and head tracked.')
if __name__=='__main__':main()
