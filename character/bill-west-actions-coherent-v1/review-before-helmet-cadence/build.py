"""Package independent west whole figures to the retained west state profile."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import binary_dilation, label

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCE = HERE/'sources/actions.png'
IDLE = ROOT/'bill-shared-helmet-runtime-v2/frames/idle-west/000.png'


def main():
    raw = np.asarray(Image.open(SOURCE).convert('RGBA'))
    labs,_ = label(raw[:,:,3]>180)
    counts = np.bincount(labs.ravel())
    poses = []
    for ident in range(1,len(counts)):
        if counts[ident]>10000:
            yy,xx = np.where(labs==ident)
            poses.append((int(yy.min()),int(xx.min()),ident))
    assert len(poses)==18,len(poses)
    poses.sort()
    ordered = []
    for row in range(3):
        ordered.extend(sorted(poses[row*6:(row+1)*6],key=lambda a:a[1]))
    idle = Image.open(IDLE).convert('RGBA')
    a = np.asarray(idle)
    iy,ix = np.where(a[:,:,3]>180)
    sy,sx = np.where(labs==ordered[0][2])
    scale_y = (iy.max()-iy.min()+1)/(sy.max()-sy.min()+1)
    hy,hx = np.where((a[:,:,3]>180)&(np.indices(a.shape[:2])[0]<iy.min()+25))
    shy,shx = np.where((labs==ordered[0][2])&(np.indices(labs.shape)[0]<sy.min()+50))
    scale_x = (hx.max()-hx.min()+1)/(shx.max()-shx.min()+1)
    boot = float(np.median(ix[(iy>=iy.max()-6)&(ix<np.median(ix))]))
    spec = importlib.util.spec_from_file_location('east_grade',ROOT/'bill-east-actions-coherent-v5/build.py')
    grade = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(grade)
    frames = []
    records = []
    polish = json.loads((HERE/'polish-settings.json').read_text())
    for n,(_,_,ident) in enumerate(ordered):
        mask = labs==ident
        ys,xs = np.where(mask)
        edge = binary_dilation(mask,iterations=2)
        p = raw.copy()
        p[~edge]=0
        # Reflect mask coordinates only to reuse face/patch material separation.
        # Rendered art and anatomical equipment ownership are never mirrored.
        reflected,diagnostic = grade.grade_materials(p[:,::-1],mask[:,::-1],int(ys.min()))
        mapped = reflected[:,::-1]
        p[:,:,:3] = np.clip(p[:,:,:3]*0.2+mapped[:,:,:3]*0.8,0,255).astype('uint8')
        # West-specific fixed material calibration after the preliminary grade,
        # always starting from the untouched source rather than prior exports.
        diagnostic = diagnostic[:,::-1].astype(float)
        red,green,blue = diagnostic[:,:,:3].transpose(2,0,1)
        skin = np.clip((green-red)/255,0,1)
        patch = np.clip((red-green)/255,0,1)
        metal = np.clip((blue-np.minimum(red,green))/210,0,1)
        neutral = np.clip(np.minimum.reduce([red,green,blue])/45,0,1)
        yy = np.indices(mask.shape)[0]
        lamp = (yy<int(ys.min())+25)&(p[:,:,:3].mean(2)>175)
        metal *= ~lamp
        shell = neutral*(yy<int(ys.min())+76)*(1-metal)
        shell *= ~lamp
        cloth = neutral*(yy>=int(ys.min())+76)*(1-metal)
        rgb = p[:,:,:3].astype(float)
        graded = rgb.copy()
        for weight,target in [
            (cloth,rgb+np.array([1,4,4])),
            (shell,rgb+np.array([-1,0,1])),
            (metal,rgb*0.93+np.array([2,0,-1])),
            (patch,rgb+np.array([7,1,-4])),
            (skin,rgb*np.array([0.94,0.99,1.03])),
        ]:
            graded = graded*(1-weight[:,:,None])+target*weight[:,:,None]
        p[:,:,:3] = np.clip(graded,0,255).astype('uint8')
        if n >= 1:
            # Apply the same idle-calibrated material correction across actions;
            # preserve pose lighting instead of matching exposure per frame.
            rgb = p[:,:,:3].astype(float)
            rgb += cloth[:,:,None]*np.array([4,2,1])
            rgb += patch[:,:,None]*np.array([4,4,3])
            rgb += skin[:,:,None]*np.array([18,8,7])
            p[:,:,:3] = np.clip(rgb,0,255).astype('uint8')
        if str(n) in polish['duplicateHandCleanup']:
            cleanup = polish['duplicateHandCleanup'][str(n)]
            start,end = cleanup['yRange']
            left,right = cleanup['edgeX']
            # Trim only the third glove outside the trouser contour. The two
            # real hands and underlying leg pixels remain original artwork.
            for row in range(start,end):
                boundary = left+(right-left)*(row-start)/(end-start-1)
                columns = np.arange(int(xs.min())-3,int(boundary)+2)
                weight = np.clip(columns-boundary+1,0,1)
                p[row,columns,3] = np.round(p[row,columns,3]*weight).astype('uint8')
                p[row,columns[p[row,columns,3]==0],:3] = 0
        if n in (0,1,7,12):
            mask_dir = HERE/'review-masks'
            mask_dir.mkdir(exist_ok=True)
            Image.fromarray(diagnostic.astype('uint8')).crop((int(xs.min()-3),int(ys.min()-3),int(xs.max()+4),int(ys.max()+4))).save(mask_dir/f'{n:02d}.png')
        x0,y0,x1,y1 = int(xs.min()-3),int(ys.min()-3),int(xs.max()+4),int(ys.max()+4)
        source_boot = float(np.median(xs[(ys>=ys.max()-10)&(xs<np.median(xs))]))
        im = Image.fromarray(p).crop((x0,y0,x1,y1))
        im = im.resize((round(im.width*scale_x),round(im.height*scale_y)),Image.Resampling.LANCZOS)
        position = (round(boot-(source_boot-x0)*scale_x),round(iy.max()-(ys.max()-y0)*scale_y))
        canvas = Image.new('RGBA',(184,184))
        assert position[0]>=0 and position[1]>=0
        assert position[0]+im.width<=184 and position[1]+im.height<=184
        canvas.alpha_composite(im,position)
        frames.append(canvas)
        records.append({'cell':n,'sourceBox':[x0,y0,x1,y1],'bootX':source_boot,'position':list(position)})
    chains = {'interact-west':[idle,*frames[1:5],idle],
              'kneel-west':[idle,*frames[7:11],frames[12]],
              'repair-west':frames[12:18],
              'stand-west':[frames[17],*reversed(frames[7:11]),idle]}
    old = json.loads((ROOT/'major-bill-v3/packs/helmet-256x256-p128-224/manifest.json').read_text())
    result = {k:v for k,v in old.items() if k!='states'}
    result.update(name='Bill independent west whole-figure candidate',status='owner_review_pending',precomposed=True,states=[])
    selected = {s['id']:s for s in old['states']}
    for key,images in chains.items():
        state = copy.deepcopy(selected[key])
        state['frameFiles']=[]
        state['frameDurationsMs']=polish['frameDurationsMs'][key]
        state['provenance']='independent west whole-figure source; fixed head/height calibration and left planted boot; reverse descent for stand'
        for i,im in enumerate(images):
            # Retain west action consumer pivot without changing physical scale.
            padded = Image.new('RGBA',(256,256))
            padded.alpha_composite(im,(36,52))
            dest = HERE/'frames'/key/f'{i:03d}.png'
            dest.parent.mkdir(parents=True,exist_ok=True)
            padded.save(dest)
            state['frameFiles'].append(dest.relative_to(HERE).as_posix())
        result['states'].append(state)
    (HERE/'manifest.json').write_text(json.dumps(result,indent=2)+'\n')
    (HERE/'source-registration.json').write_text(json.dumps({'sourceSha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'scaleX':scale_x,'scaleY':scale_y,'leftBoot':boot,'profilePadding':[36,52],'grade':'west-grade-v1; fixed source material maps, masks reflected only','frames':records},indent=2)+'\n')
    contact = Image.new('RGB',(1104,736),(34,48,56))
    draw = ImageDraw.Draw(contact)
    for r,(key,images) in enumerate(chains.items()):
        for i,im in enumerate(images):
            contact.paste(im,(i*184,r*184),im)
            draw.text((i*184+3,r*184+3),key+' '+str(i),fill='white')
    contact.save(HERE/'contact-sheet.png')
    assert chains['kneel-west'][5].tobytes()==chains['repair-west'][0].tobytes()
    assert chains['repair-west'][5].tobytes()==chains['stand-west'][0].tobytes()
    print('West: 18 independent source poses; 24 frames; retained 256/p128,224 profile; exact joins; no clipping')


if __name__=='__main__':
    main()
