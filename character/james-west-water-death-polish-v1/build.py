from pathlib import Path
import json,copy,sys,hashlib,importlib.util
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];rawroot=P.parent/'james-death-west-v1';source=rawroot/'source-water-v4.png'
sys.path.insert(0,str(P.parent/'james-water-family-v1'))
from extract_sources import extract
spec=importlib.util.spec_from_file_location('death_material_helpers',P.parent/'james-death-family-v1/build.py');helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
cells=extract(source,6,6);heads=[[93.67787839586029,41.8745148771022],[81.19898605830164,43.9340937896071],[73.52329749103943,47.80167264038232],[38.5717674970344,48.69513641755635],[40.78321678321678,50.504662004662],[41.882290562036054,52.01484623541888]]
scale=25/60;points=[];registered=[];tracking=[]
for i,(cell,box) in enumerate(cells):
    point=np.array(heads[i]);pos=np.rint(np.array([114,214])-point*scale).astype(int);small=cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.LANCZOS);out=Image.new('RGBA',(256,360));out.alpha_composite(small,tuple(pos));actual=point*scale+pos
    points.append(actual);registered.append(out);tracking.append(dict(sourceBox=box,sourceHead=heads[i],worldHead=actual.tolist(),translation=pos.tolist(),fixedScale=scale))
target=helper.endpoint('bare','swim','west');gold,neutral=helper.color_gain(registered[0],target,points[0]);bare=[helper.grade(im,point,gold,neutral) for im,point in zip(registered,points)]
w=P.parent/'james-water-west-v1';hr=json.loads((w/'helmet-registration.json').read_text());hs=Image.open(w/'source-helmet.png').convert('RGBA');donor=hr['tracking']['6'];patch=hs.crop(donor['sourceHeadBox']);patch=patch.resize((round(patch.width*hr['fixedHeadScale']),round(patch.height*hr['fixedHeadScale'])),Image.Resampling.LANCZOS)
a=np.array(patch);r,g,b=a[:,:,:3].astype(float).transpose(2,0,1);mask=(a[:,:,3]>0)&(abs(r-g)<13)&(abs(g-b)<17);rgb=a[:,:,:3].astype(float);rgb[mask]*=.9;a[:,:,:3]=np.rint(rgb).clip(0,255).astype('uint8');patch=Image.fromarray(a)
helmet=[]
for i,im in enumerate(bare):
    head=patch.rotate([0,0,0,8,15,20][i],resample=Image.Resampling.BICUBIC,expand=True);pos=np.rint(points[i]+np.array(hr['centerOffset'])-[head.width/2,head.height/2]).astype(int)
    a=np.array(im);yy,xx=np.indices(a.shape[:2]);erase=((xx-points[i][0])/14)**2+((yy-(points[i][1]-1))/14)**2<=1;a[erase]=0;out=Image.fromarray(a);out.alpha_composite(head,tuple(pos));helmet.append(out)
    tracking[i].update(helmetDonor=donor['sourceHead'],helmetBox=donor['sourceHeadBox'],helmetScale=hr['fixedHeadScale'],helmetAngle=[0,0,0,8,15,20][i],helmetPosition=pos.tolist(),editRegion=[min(int(points[i][0]-14),int(pos[0])),min(int(points[i][1]-15),int(pos[1])),max(int(points[i][0]+15),int(pos[0])+head.width),max(int(points[i][1]+14),int(pos[1])+head.height)])
bare[0]=helper.endpoint('bare','swim','west');helmet[0]=helper.endpoint('helmet','swim','west')
installed=(P/'selection.json').exists() and json.loads((P/'selection.json').read_text()).get('runtimeInstalled',False);hashes={}
for mode,rows in [('bare',bare),('helmet',helmet)]:
    old=json.loads((P.parent/'james-death-family-v1'/(mode+'-manifest.json')).read_text());pack={k:copy.deepcopy(v) for k,v in old.items() if k!='states'};state=copy.deepcopy(next(s for s in old['states'] if s['id']=='death-water-west'));files=[]
    for i,im in enumerate(rows):
        file=P/'frames'/mode/f'{i:03d}.png';file.parent.mkdir(parents=True,exist_ok=True);im.save(file);rel=file.relative_to(P).as_posix();files.append(rel);hashes[rel]=hashlib.sha256(file.read_bytes()).hexdigest()
    state.update(frameFiles=files,provenance=dict(source='../james-death-west-v1/source-water-v4.png',sourcePoses=list(range(6)),exactSelectedEntry=True,fixedScale=scale));pack.update(name='James West water death proportions '+mode,status='installed_owner_review_pending' if installed else 'staged_owner_review_pending',states=[state]);(P/(mode+'-manifest.json')).write_text(json.dumps(pack,indent=2)+'\n')
record=dict(source=str(source.relative_to(R)),sourceSha256=hashlib.sha256(source.read_bytes()).hexdigest(),fixedScale=scale,ruler='Reviewed60px full cranial span against25px selected West skull; one fixed atlas density, no body silhouette fitting',goldGain=gold.tolist(),neutralGain=neutral,tracking=tracking,helmetSource=str((w/'source-helmet.png').relative_to(R)),helmetSourceSha256=hashlib.sha256((w/'source-helmet.png').read_bytes()).hexdigest(),runtimeInstalled=installed)
(P/'registration.json').write_text(json.dumps(record,indent=2)+'\n');(P/'frame-hashes.json').write_text(json.dumps(hashes,indent=2)+'\n')
board=Image.new('RGB',(1536,760),'#303b40');draw=ImageDraw.Draw(board)
for row,(mode,rows) in enumerate([('bare',bare),('helmet',helmet)]):
    for i,im in enumerate(rows):board.paste(im,(i*256,row*380+20),im);draw.text((i*256+8,row*380+6),mode+' '+str(i),fill='white')
board.save(P/'paired-contact.png');print('Built paired West water death6poses; fixed25/60 density; compact projected limbs; exact selected swim entry')
