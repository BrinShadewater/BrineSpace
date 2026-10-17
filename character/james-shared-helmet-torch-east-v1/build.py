"""Register the accepted James east study and fit the selected common shell."""
from pathlib import Path
import math,json,hashlib
import numpy as np
from scipy import ndimage
from scipy.signal import savgol_filter
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
SOURCE=ROOT/'character/james-torch-east-direct-v1'
BARE=ROOT/'character/james-torch-east-matched-v1'
SHELL=ROOT/'character/james-shared-helmet-east-v1/helmet.png'

def idle(path):
    m=json.loads(path.read_text());s=next(s for s in m['states'] if s['id']=='idle-east')
    return Image.open(path.parent/s['frameFiles'][0]).convert('RGBA')

def face(image):
    a=np.array(image);r,g,b=a[:,:,:3].astype(float).transpose(2,0,1);yy,xx=np.indices(a.shape[:2]);top=np.where(a[:,:,3]>192)[0].min()
    mask=(r>g+10)&(r>b+12)&(g>b+2)&(a[:,:,3]>150)&(yy<top+27)&(r+g+b>180)&(~((g>b+15)&(r-g<15)))
    labels,n=ndimage.label(mask);counts=np.bincount(labels.ravel());counts[0]=0
    if counts.max()<60:raise AssertionError('Uncertain head tracking')
    y,x=np.where(labels==counts.argmax());return np.array([x.mean(),y.mean()]),[int(x.min()),int(y.min()),int(x.max()),int(y.max())],int(len(x))

def rotate_point(point,angle):
    c,s=math.cos(math.radians(angle)),math.sin(math.radians(angle))
    x,y=point;return np.array([c*x+s*y,-s*x+c*y])

def main():
    BARE.mkdir(exist_ok=True);bare_idle=idle(ROOT/'character/crew-runtime-matte-v1/branforth/manifest.json');worn_idle=idle(ROOT/'character/james-shared-helmet-runtime-v1/manifest.json')
    original=[Image.open(SOURCE/f'graded/{i:03}.png').convert('RGBA') for i in range(141)]
    reference,_box,_count=face(original[0]);shell=Image.open(SHELL).convert('RGBA')
    baseline=np.array([73,16]);center=np.array([shell.width/2,shell.height/2]);registered=[];equipped=[];tracking=[]
    smooth_faces=savgol_filter(np.array([face(im)[0] for im in original]),13,2,axis=0,mode='interp')
    # Planted front boot matches installed idle at (118,167). Search only its
    # local footprint; hands and the rear boot cannot influence registration.
    for index,image in enumerate(original):
        a=np.array(image);roi=a[156:177,100:121,3]>160;y,x=np.where(roi)
        anchor=np.array([100+x.max(),156+y.max()]);shift=np.array([118,167])-anchor
        if np.any(np.abs(shift)>3):raise AssertionError('Front contact drift exceeds registration tolerance')
        body=Image.new('RGBA',(184,184));body.alpha_composite(image,tuple(map(int,shift)))
        raw_target,box,count=face(body)
        target=smooth_faces[index]+shift
        angle=0.0
        rotated=shell.rotate(angle,resample=Image.Resampling.BICUBIC,expand=True)
        # Rotate about the reference face so helmet motion follows the head.
        face_shell=reference-baseline
        face_rotated=rotate_point(face_shell-center,angle)+np.array([rotated.width/2,rotated.height/2])
        at=np.rint(target-face_rotated).astype(int)
        out=body.copy();draw=ImageDraw.Draw(out)
        local=[(-11,-14),(10,-14),(14,8),(6,15),(-10,10)]
        clear=[tuple(target+rotate_point(point,angle)) for point in local]
        draw.polygon(clear,fill=(0,0,0,0))
        out.alpha_composite(rotated,tuple(map(int,at)))
        registered.append(body);equipped.append(out)
        tracking.append(dict(sourceFrame=index,boot=anchor.tolist(),translation=shift.tolist(),face=target.round(3).tolist(),facePixels=count,angle=angle,helmetPosition=at.tolist(),helmetBounds=at.tolist()+(at+rotated.size).tolist()))
    work=list(range(18,75))+list(range(73,17,-1))
    clips={'torch-draw-east':list(range(19)),'weld-east':work,'torch-stow-east':[18]+list(range(75,100))};packs=[]
    for dest,rows,eidle in [(BARE,registered,bare_idle),(HERE,equipped,worn_idle)]:
        manifest=dict(name='James standing construction blowtorch '+('shared helmet' if dest==HERE else 'bare'),frameWidth=184,frameHeight=184,pivot=[92,172],standingHeight=148,precomposed=True,textureFilter='linear',status='installed_owner_accepted_east_construction_torch',states=[])
        for key,indices in clips.items():
            folder=dest/'frames'/key;folder.mkdir(parents=True,exist_ok=True);files=[]
            total=round(len(indices)*1000/24) if key=='weld-east' else 520
            durations=[round((i+1)*total/len(indices))-round(i*total/len(indices)) for i in range(len(indices))]
            for i,source_index in enumerate(indices):
                image=rows[source_index].copy()
                if (key=='torch-draw-east' and i==0) or (key=='torch-stow-east' and i==len(indices)-1):image=eidle.copy()
                filename=folder/f'{i:03}.png';image.save(filename);files.append(filename.relative_to(dest).as_posix())
            manifest['states'].append(dict(id=key,frameCount=len(files),frameFiles=files,frameDurationsMs=durations,loop=key=='weld-east',provenance=dict(sourceFrames=indices,source=SOURCE.relative_to(ROOT).as_posix(),derivation='Draw0-18; weld18-74 then reverse73-18 for exact loop/joins; flame-off/stow75-99 from original source, prefixed work join18; exact idle endpoints',colour='Owner accepted neutral-v3')))
        (dest/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');packs.append(manifest)
    report=dict(sourceSha256=hashlib.sha256((SOURCE/'source.mp4').read_bytes()).hexdigest(),helmetSha256=hashlib.sha256(SHELL.read_bytes()).hexdigest(),standingEndpoint='Exact installed idle',frontBoot=[118,167],tracking=tracking,limits=['Standing construction blowtorch staged for owner review.','Weld uses forward/reverse source for exact loop joins; stow uses actual flame-off/stow.','Other states remain installed/retained.'])
    (HERE/'registration.json').write_text(json.dumps(report,indent=2)+'\n')
    previews=[];times=[]
    for key,repeats in [('torch-draw-east',1),('weld-east',1),('torch-stow-east',1)]:
        states=[next(s for s in m['states'] if s['id']==key) for m in packs]
        for repeat in range(repeats):
            for i in range(states[0]['frameCount']):
                board=Image.new('RGB',(920,255),'#303b40');d=ImageDraw.Draw(board);d.text((8,6),'James east - '+key+' / bare / shared helmet / 82px / 54px / 27px',fill='white')
                images=[]
                for dest,state,x in [(BARE,states[0],0),(HERE,states[1],220)]:
                    im=Image.open(dest/state['frameFiles'][i]).convert('RGBA');board.paste(im,(x,40),im);images.append(im)
                for h,x in [(82,460),(54,660),(27,800)]:
                    side=round(184*h/148)
                    for j,im in enumerate(images):
                        small=im.resize((side,side),Image.Resampling.BILINEAR);board.paste(small,(x+j*(side+8),40+172-round(side*172/184)),small)
                previews.append(board);times.append(states[0]['frameDurationsMs'][i])
    previews[0].save(HERE/'review.gif',save_all=True,append_images=previews[1:],duration=times,loop=0)
    sheet=Image.new('RGB',(1104,1320),'#303b40');d=ImageDraw.Draw(sheet)
    for row,(dest,statekey) in enumerate([(dest,key) for key in clips for dest in [BARE,HERE]]):
        m=packs[0 if dest==BARE else 1];state=next(s for s in m['states'] if s['id']==statekey)
        for col,i in enumerate(np.linspace(0,state['frameCount']-1,6).astype(int)):
            im=Image.open(dest/state['frameFiles'][i]).convert('RGBA');pos=(col*184,row*220+20);sheet.paste(im,pos,im);d.text((pos[0]+5,pos[1]-15),statekey+' '+str(i),fill='white')
    sheet.save(HERE/'contact.png');(HERE/'index.html').write_text('<!doctype html><style>body{background:#303b40;color:white;font:18px system-ui;max-width:1104px;margin:auto}img{max-width:100%}</style><h1>James east standing blowtorch</h1><p>Bare and shared helmet. Exact installed idle endpoints; forward torch draw/work/flame-off/stow. Staged for owner review.</p><img src="review.gif"><img src="contact.png">')
    print('Staged bare/equipped chain: '+str(sum(len(v) for v in clips.values()))+' frames per mode; boot contact and head tracked.')
if __name__=='__main__':main()
