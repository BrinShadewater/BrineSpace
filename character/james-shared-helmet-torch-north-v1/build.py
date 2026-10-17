"""Register the revised James north torch study and fit the selected common shell."""
from pathlib import Path
import math,json,hashlib
import numpy as np
from scipy import ndimage
from scipy.signal import savgol_filter
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
SOURCE=ROOT/'character/james-torch-north-direct-v2'
BARE=ROOT/'character/james-torch-north-matched-v1'
SHELL=ROOT/'character/james-shared-helmet-actions-north-v5/selected-shell.png'

def idle(path):
    m=json.loads(path.read_text());s=next(s for s in m['states'] if s['id']=='idle-north')
    return Image.open(path.parent/s['frameFiles'][0]).convert('RGBA')

def face(image):
    a=np.array(image);r,g,b=a[:,:,:3].astype(float).transpose(2,0,1);yy,xx=np.indices(a.shape[:2])
    cyan=(b>r+15)&(g>r+5);yellow=(r>b+18)&(g>b+10)&(r-g<15)
    # Central dark rear-head silhouette ignores the raised torch and blue flare.
    mask=(a[:,:,3]>160)&(xx>80)&(xx<94)&(yy<130)&((r+g+b)/3<110)&(~cyan)&(~yellow)
    top=int(np.where(mask)[0].min())
    head=(a[:,:,3]>160)&(yy>=top)&(yy<top+6)&(xx>75)&(xx<103)&(~cyan)
    y,x=np.where(head)
    return np.array([x.mean(),float(top+10)]),[int(x.min()),top,int(x.max()),top+20],int(len(x))

def rotate_point(point,angle):
    c,s=math.cos(math.radians(angle)),math.sin(math.radians(angle))
    x,y=point;return np.array([c*x+s*y,-s*x+c*y])

def correct_tool(body,index):
    # Motion is authored; only its misgenerated held wrench/nozzle is replaced.
    if index<36:return body
    edit=Image.open(HERE/'forward-torch-pose.png').convert('RGBA')
    a=np.array(edit);r,g,b=a[:,:,:3].astype(float).transpose(2,0,1)
    a[(g>r+50)&(g>b+50)]=0
    # Preserve body and glove outside the bounded tool outline.
    mask=Image.new('L',(184,184));d=ImageDraw.Draw(mask)
    d.polygon([(98,0),(126,0),(126,39),(112,39),(108,27),(98,25)],fill=255)
    local=np.array(mask)>0
    a[~local]=0;edit=Image.fromarray(a)
    # Hand rises toward the shoulder in the original draw.
    dx=int(round(np.interp(index,[36,40,44,48,83,96],[7,1,0,0,0,0])))
    dy=int(round(np.interp(index,[36,40,44,48,83,96],[40,25,8,0,0,0])))
    moved=Image.new('RGBA',(184,184));moved.alpha_composite(edit,(dx,dy))
    clear=Image.new('L',(184,184));clear.paste(mask,(dx,dy))
    return Image.composite(moved,body,clear)

def main():
    BARE.mkdir(exist_ok=True);bare_idle=idle(ROOT/'character/crew-runtime-matte-v1/branforth/manifest.json');worn_idle=idle(ROOT/'character/james-shared-helmet-runtime-v1/manifest.json')
    original=[Image.open(SOURCE/f'graded/{i:03}.png').convert('RGBA') for i in range(141)]
    reference,_box,_count=face(original[0]);shell=Image.open(SHELL).convert('RGBA')
    baseline=np.array([76,22]);center=np.array([shell.width/2,shell.height/2]);registered=[];equipped=[];tracking=[]
    # Lock the helmet/face to a smooth head path instead of noisy per-frame
    # skin-mask centroids. Preserve vertical descent, restrain forward reach.
    raw_faces=np.array([face(image)[0] for image in original])
    smooth_faces=savgol_filter(raw_faces,13,2,axis=0,mode='interp')
    # Planted front boot matches installed idle at (97,171). Search only its
    # local footprint; hands and the rear boot cannot influence registration.
    belt_mask=Image.new('L',(184,184));bd=ImageDraw.Draw(belt_mask)
    bd.polygon([(106,72),(111,72),(113,78),(112,93),(113,105),(112,116),(107,116),(106,105)],fill=255)
    for index,image in enumerate(original):
        a=np.array(image);y,x=np.where(a[:,:,3]>160)
        anchor=np.array([92,int(y.max())]);shift=np.array([92,171])-anchor
        if np.any(np.abs(shift)>6):raise AssertionError('Ground contact drift exceeds tolerance')
        body=Image.new('RGBA',(184,184));body.alpha_composite(image,tuple(map(int,shift)))
        body=correct_tool(body,index)
        body=Image.composite(bare_idle,body,belt_mask)
        raw_target,box,count=face(body)
        source_angle=0.0
        lowered=float(np.clip((smooth_faces[index,1]-reference[1])/35,0,1))
        target=smooth_faces[index]+shift
        target[0]=reference[0]+(target[0]-reference[0])*.2
        angle=source_angle*.45
        rotated=shell.rotate(angle,resample=Image.Resampling.BICUBIC,expand=True)
        # Rotate about the reference face so helmet motion follows the head.
        face_shell=reference-baseline
        face_rotated=rotate_point(face_shell-center,angle)+np.array([rotated.width/2,rotated.height/2])
        at=np.rint(target-face_rotated).astype(int)
        out=body.copy();draw=ImageDraw.Draw(out)
        local=[(-12,-11),(12,-11),(14,8),(8,12),(-8,12),(-14,8)]
        clear=[tuple(raw_target+rotate_point(point,source_angle)) for point in local]
        draw.polygon(clear,fill=(0,0,0,0))
        out.alpha_composite(rotated,tuple(map(int,at)))
        registered.append(body);equipped.append(out)
        tracking.append(dict(sourceFrame=index,boot=anchor.tolist(),translation=shift.tolist(),face=target.round(3).tolist(),rawFace=raw_target.round(3).tolist(),facePixels=count,angle=angle,sourceAngle=source_angle,helmetPosition=at.tolist(),helmetBounds=at.tolist()+(at+rotated.size).tolist()))
    work=list(range(83,97))+list(range(95,82,-1))
    clips={'torch-draw-north':[0,8,16,24,36,40,44,48,83],'weld-north':work,'torch-stow-north':[83,48,44,40,36,24,16,8,0]};packs=[]
    for dest,rows,eidle in [(BARE,registered,bare_idle),(HERE,equipped,worn_idle)]:
        manifest=dict(name='James north standing construction blowtorch '+('shared helmet' if dest==HERE else 'bare'),frameWidth=184,frameHeight=184,pivot=[92,172],standingHeight=148,precomposed=True,textureFilter='linear',status='installed_owner_accepted_north_construction_torch',states=[])
        for key,indices in clips.items():
            folder=dest/'frames'/key;folder.mkdir(parents=True,exist_ok=True);files=[]
            total=1200 if key=='weld-north' else 520
            durations=[round((i+1)*total/len(indices))-round(i*total/len(indices)) for i in range(len(indices))]
            if key=='torch-draw-north':durations=[20,25,30,35,40,40,45,45,240]
            for i,source_index in enumerate(indices):
                image=rows[source_index].copy()
                if (key=='torch-draw-north' and i==0) or (key=='torch-stow-north' and i==len(indices)-1):image=eidle.copy()
                # Ignite only once raised; shut down immediately on stow.
                if (key=='torch-stow-north' and i>0) or (key=='torch-draw-north' and i<7):
                    aa=np.array(image);rr,gg,bb=aa[:,:,:3].astype(int).transpose(2,0,1);yy,xx=np.indices(aa.shape[:2])
                    blue=(bb>rr+25)&(gg>rr+15)&(yy<85)&(xx>96)
                    aa[blue]=0;image=Image.fromarray(aa)
                filename=folder/f'{i:03}.png';image.save(filename);files.append(filename.relative_to(dest).as_posix())
            manifest['states'].append(dict(id=key,frameCount=len(files),frameFiles=files,frameDurationsMs=durations,loop=key=='weld-north',provenance=dict(sourceFrames=indices,source=SOURCE.relative_to(ROOT).as_posix(),derivation='Draw0/8/16/24/36/40/44/48/83; work83-96 then95-83 reverse; reverse selected draw to stow; oversized-flare sections excluded; exact joins',colour='Owner accepted neutral-v3',beltEquipment='Selected rear idle wrench restored in fixed local mask',toolAim='Generated local forward/upward blowtorch replaces source held-wrench artifact')))
        (dest/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');packs.append(manifest)
    report=dict(sourceSha256=hashlib.sha256((SOURCE/'source.mp4').read_bytes()).hexdigest(),helmetSha256=hashlib.sha256(SHELL.read_bytes()).hexdigest(),standingEndpoint='Exact installed idle',groundBaseline=171,helmetTracking='Rear head silhouette path, Savitzky-Golay13/order2, upright selected shell',tracking=tracking,limits=['Owner accepted north construction blowtorch installed.','Stow reverses authored draw; raw source does not complete a useful clean stow.','Other states remain installed/retained.'])
    (HERE/'registration.json').write_text(json.dumps(report,indent=2)+'\n')
    previews=[];times=[]
    for key,repeats in [('torch-draw-north',1),('weld-north',2),('torch-stow-north',1)]:
        states=[next(s for s in m['states'] if s['id']==key) for m in packs]
        for repeat in range(repeats):
            for i in range(states[0]['frameCount']):
                board=Image.new('RGB',(920,255),'#303b40');d=ImageDraw.Draw(board);d.text((8,6),'James north - '+key+' / bare / shared helmet / 82px / 54px / 27px',fill='white')
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
    previews[0].save(HERE/'review.gif',save_all=True,append_images=previews[1:],duration=times,loop=0)
    sheet.save(HERE/'contact.png');(HERE/'index.html').write_text('<!doctype html><style>body{background:#303b40;color:white;font:18px system-ui;max-width:1104px;margin:auto}img{max-width:100%}</style><h1>James north standing blowtorch</h1><p>Bare and shared helmet. Exact installed idle endpoints; standing forward blowtorch draw/work/stow. Staged for owner review.</p><img src="review.gif"><img src="contact.png">')
    print('Staged bare/equipped chain: '+str(sum(len(v) for v in clips.values()))+' frames per mode; boot contact and head tracked.')
if __name__=='__main__':main()
