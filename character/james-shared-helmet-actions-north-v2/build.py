"""Register the revised James north torch study and fit the selected common shell."""
from pathlib import Path
import math,json,hashlib
import numpy as np
from scipy import ndimage
from scipy.signal import savgol_filter
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
SOURCE=ROOT/'character/james-repair-north-direct-v2'
BARE=ROOT/'character/james-action-north-matched-v2'
SHELL=HERE/'selected-shell.png'

def idle(path):
    m=json.loads(path.read_text());s=next(s for s in m['states'] if s['id']=='idle-north')
    return Image.open(path.parent/s['frameFiles'][0]).convert('RGBA')

def face(image):
    a=np.array(image);yy,xx=np.indices(a.shape[:2]);top=np.where(a[:,:,3]>160)[0].min()
    mask=(a[:,:,3]>160)&(yy<top+7)
    y,x=np.where(mask)
    return np.array([x.mean(),float(top+10)]),[int(x.min()),int(top),int(x.max()),int(top+20)],int(len(x))

def rotate_point(point,angle):
    c,s=math.cos(math.radians(angle)),math.sin(math.radians(angle))
    x,y=point;return np.array([c*x+s*y,-s*x+c*y])

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
    for index,image in enumerate(original):
        a=np.array(image);y,x=np.where(a[:,:,3]>160)
        anchor=np.array([92,int(y.max())]);shift=np.array([92,171])-anchor
        if np.any(np.abs(shift)>6):raise AssertionError('Ground contact drift exceeds tolerance')
        body=Image.new('RGBA',(184,184));body.alpha_composite(image,tuple(map(int,shift)))
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
    # One authored descent. Rising reverses those registered poses, preserving
    # planted contact and exact joins rather than using the drifting source rise.
    descent=list(range(0,34))+list(range(35,74,2));work=[73,74,75,74,73];rise=list(reversed(descent))
    clips={'kneel-north':descent,'repair-north':work,'stand-north':rise};packs=[]
    for dest,rows,eidle in [(BARE,registered,bare_idle),(HERE,equipped,worn_idle)]:
        manifest=dict(name='James north repair chain '+('shared helmet' if dest==HERE else 'bare'),frameWidth=184,frameHeight=184,pivot=[92,172],standingHeight=148,precomposed=True,textureFilter='linear',status='staged_north_repair',states=[])
        for key,indices in clips.items():
            folder=dest/'frames'/key;folder.mkdir(parents=True,exist_ok=True);files=[]
            total=1000 if key!='repair-north' else 1167
            durations=[round((i+1)*total/len(indices))-round(i*total/len(indices)) for i in range(len(indices))]
            for i,source_index in enumerate(indices):
                image=rows[source_index].copy()
                if (key=='kneel-north' and i==0) or (key=='stand-north' and i==len(indices)-1):image=eidle.copy()
                filename=folder/f'{i:03}.png';image.save(filename);files.append(filename.relative_to(dest).as_posix())
            manifest['states'].append(dict(id=key,frameCount=len(files),frameFiles=files,frameDurationsMs=durations,loop=key=='repair-north',provenance=dict(sourceFrames=indices,source=SOURCE.relative_to(ROOT).as_posix(),derivation='Rise reverses descent and torch draw; repair uses compact flame onset poses; exact installed idle endpoints',colour='Neutral material correction reused from accepted east neutral-v3')))
        (dest/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');packs.append(manifest)
    report=dict(sourceSha256=hashlib.sha256((SOURCE/'source.mp4').read_bytes()).hexdigest(),helmetSha256=hashlib.sha256(SHELL.read_bytes()).hexdigest(),standingEndpoint='Exact installed idle',groundBaseline=171,helmetMotion='13-source-frame quadratic path smoothing; 20 percent lateral motion; rear shell held upright during descent',tracking=tracking,limits=['North-v2 revised after owner rejected body self-overlap and missing blowtorch.','Stand is derived by reversing descent.','Repair shows right-hand blowtorch and short blue flame; oversized later flare is omitted. Other actions retain original art.'])
    (HERE/'registration.json').write_text(json.dumps(report,indent=2)+'\n')
    previews=[];times=[]
    for key,repeats in [('kneel-north',1),('repair-north',2),('stand-north',1)]:
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
    sheet.save(HERE/'contact.png');(HERE/'index.html').write_text('<!doctype html><style>body{background:#303b40;color:white;font:18px system-ui;max-width:1104px;margin:auto}img{max-width:100%}</style><h1>James north torch repair chain v2</h1><p>Bare and shared helmet. Exact installed idle endpoints and action joins. Upright torso and visible torch. Rise reverses descent/tool draw. Repair uses only short flame onset, excluding later oversized flare. Staged north chain: restrained head movement.</p><img src="review.gif"><img src="contact.png">')
    print('Staged bare/equipped chain: '+str(sum(len(v) for v in clips.values()))+' frames per mode; boot contact and head tracked.')
if __name__=='__main__':main()
