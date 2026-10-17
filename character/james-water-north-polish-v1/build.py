from pathlib import Path
import json,copy,sys,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];old=P.parent/'james-water-north-v1'
installed=(P/'selection.json').exists() and json.loads((P/'selection.json').read_text()).get('runtimeInstalled',False)
sys.path.insert(0,str(P.parent/'james-water-family-v1'))
from extract_sources import extract
from build import grade,protection,gold

source=old/'source-polish-v6.png';cells=extract(source,10,5)
heads=[(170,50),(474,50),(770,50),(1070,50),(1367,50),(170,553),(474,600),(797,633),(1110,672),(1400,714)]
scale=148/478 # One neutral upright body-density ruler; never normalize individual poses.
lead_source=old/'source-lead-in-v7.png'
cells[6]=extract(lead_source,1,1)[0]
heads[6]=(486,355)
scales=[scale]*10
scales[6]=(66*scale)/188 # Independent single-pose source density from the same cranial ruler.
reg=[];rows=[]
for i,(cell,box) in enumerate(cells):
    sc=scales[i]
    local=np.array(heads[i])-np.array(box[:2]);target=np.array([128,110])
    at=np.rint(target-local*sc).astype(int)
    small=cell.resize((round(cell.width*sc),round(cell.height*sc)),Image.Resampling.LANCZOS)
    im=Image.new('RGBA',(256,276));im.alpha_composite(small,tuple(at))
    actual=local*sc+at;rows.append(im)
    reg.append(dict(source=('source-lead-in-v7.png' if i==6 else source.name),sourceBox=box,sourceHeadAnchor=list(heads[i]),headAnchor=actual.tolist(),translation=at.tolist(),fixedScale=sc))
mroot=R/'character/crew-runtime-matte-v1/branforth';mp=json.loads((mroot/'manifest.json').read_text());ms=next(s for s in mp['states'] if s['id']=='idle-north')
master=Image.open(mroot/ms['frameFiles'][0]).convert('RGBA');ma=np.array(master)
mastermask=protection(master.size,[92,37],'north')
gain=np.median(ma[:,:,:3][gold(ma,mastermask)],axis=0)/np.median(np.array(rows[0])[:,:,:3][gold(np.array(rows[0]),protection(rows[0].size,reg[0]['headAnchor'],'north'))],axis=0)
rows=[grade(im,protection(im.size,reg[i]['headAnchor'],'north'),gain) for i,im in enumerate(rows)]
donors=extract(old/'source-helmet.png',6,6);hr=json.loads((old/'helmet-registration.json').read_text());patches=[]
for cell,box in donors:
    a=np.array(cell);rgb=a[:,:,:3].astype(float);r,g,b=rgb.transpose(2,0,1);mask=(a[:,:,3]>0)&(abs(r-g)<13)&(abs(g-b)<17);rgb[mask]*=.9;a[:,:,:3]=np.rint(rgb).clip(0,255).astype('uint8')
    patch=Image.fromarray(a).resize((round(cell.width*hr['fixedHeadScale']),round(cell.height*hr['fixedHeadScale'])),Image.Resampling.LANCZOS);patches.append(patch)
helmet=[];hreg=[]
for i,body in enumerate(rows):
    di=0 if i<6 else [1,1,4,4][i-6];patch=patches[di];point=np.array(reg[i]['headAnchor']);target=point+np.array(hr['centerOffset']);pos=np.rint(target-[patch.width/2,patch.height/2]).astype(int)
    a=np.array(body);yy,xx=np.indices(a.shape[:2]);erase=((xx-point[0])/14)**2+((yy-(point[1]-1))/14)**2<=1;a[erase]=0;out=Image.fromarray(a);out.alpha_composite(patch,tuple(pos))
    foreground=(yy<point[1]-12)&(np.array(body)[:,:,3]>0) if i>=6 else np.zeros(a.shape[:2],bool)
    aa=np.array(out);aa[foreground]=np.array(body)[foreground];helmet.append(Image.fromarray(aa))
    hreg.append(dict(sourceHead=di,position=pos.tolist(),sourceBox=donors[di][1],fixedHeadScale=hr['fixedHeadScale'],editRegion=[min(int(point[0]-14),int(pos[0])),min(int(point[1]-15),int(pos[1])),max(int(point[0]+15),int(pos[0])+patch.width),max(int(point[1]+14),int(pos[1])+patch.height)]))
maps={'tread':[0,1,2,3,4,0],'swim-start':[0,6,7,8,9,-1],'swim-stop':[-1,9,8,7,6,0]};hashes={}
for mode,generated in [('bare',rows),('helmet',helmet)]:
    pack=json.loads((old/(mode+'-manifest.json')).read_text());pack['states']=[s for s in pack['states'] if s['id']!='swim-north'];pack.update(name='James North water proportions polish '+mode,status='installed_owner_review_pending' if installed else 'staged_owner_review_pending')
    endpoint=Image.open(old/('frames/swim/000.png' if mode=='bare' else 'frames/helmet/swim/000.png')).convert('RGBA')
    for state in pack['states']:
        action=state['id'].removesuffix('-north');files=[]
        for j,i in enumerate(maps[action]):
            im=endpoint if i==-1 else generated[i];file=P/'frames'/mode/action/(f'{j:03d}.png');file.parent.mkdir(parents=True,exist_ok=True);im.save(file);rel=file.relative_to(P).as_posix();files.append(rel);hashes[rel]=hashlib.sha256(file.read_bytes()).hexdigest()
        state.update(frameFiles=files,provenance=dict(source='../james-water-north-v1/source-polish-v6.png',leadInSource='../james-water-north-v1/source-lead-in-v7.png',sourcePoses=maps[action],exactSelectedSwimEndpoint=True,fixedAtlasScale=scale,leadInSourceScale=scales[6]))
    (P/(mode+'-manifest.json')).write_text(json.dumps(pack,indent=2)+'\n')
registration=dict(sourceSha256=hashlib.sha256(source.read_bytes()).hexdigest(),source=str(source.relative_to(R)),fixedScale=scale,scaleRuler='Neutral upright478px source to148px master; all10 poses one fixed density',goldGain=gain.tolist(),tracking=reg,helmetTracking=hreg,helmetSourceSha256=hashlib.sha256((old/'source-helmet.png').read_bytes()).hexdigest(),ownerReviewPending=True,runtimeInstalled=False)
registration.update(leadInSource=str(lead_source.relative_to(R)),leadInSourceSha256=hashlib.sha256(lead_source.read_bytes()).hexdigest(),leadInRuler='v6 cranial66px at148/478 source scale matches v7 cranial188px; independent source density, no silhouette fitting')
registration.update(runtimeInstalled=installed,scaleRuler='Neutral upright478px atlas to148px master; fixed atlas density plus independently cranial-calibrated lead-in source')
(P/'registration.json').write_text(json.dumps(registration,indent=2)+'\n');(P/'frame-hashes.json').write_text(json.dumps(hashes,indent=2)+'\n')
board=Image.new('RGB',(1536,1050),'#303b40');draw=ImageDraw.Draw(board)
for row,mode in enumerate(['bare','helmet']):
    pack=json.loads((P/(mode+'-manifest.json')).read_text())
    for ar,state in enumerate(pack['states']):
        for j,f in enumerate(state['frameFiles']):
            im=Image.open(P/f);small=im.resize((142,153),Image.Resampling.LANCZOS);at=(j*256+30,(row*3+ar)*175+20);board.paste(small,at,small);draw.text((at[0],at[1]-15),mode+' '+state['id']+' '+str(j),fill='white')
board.save(P/'paired-contact.png')
print('Built3 North water states per mode;36 refs; fixed source rulers; selected swim endpoints retained; selection status preserved')
