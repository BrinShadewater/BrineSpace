"""Staged native master identity repair over unchanged accepted cargo sources."""
from pathlib import Path
import json, copy, hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import binary_dilation,binary_fill_holes,label
P=Path(__file__).resolve().parent;R=P.parents[1]
audit=json.loads((R/'character/bill-selected-source-audit-2026-10-01-locomotion-v10/source-inventory.json').read_text())
reg=json.loads((P.parent/'bill-run-head-locked-v1/head-registration.json').read_text())
headref=next(d for d in reg['directions'] if d['direction']=='north')
barehead=Image.open(P.parent/'bill-run-head-locked-v1'/headref['componentFile']).convert('RGBA')
gearhead=Image.open(P.parent/'bill-seated-helmet-north-coherent-v1/sources/canonical-head.png').convert('RGBA')
oldreg=json.loads((P.parent/'bill-cargo-helmet-north-v1/helmet-registration.json').read_text())['frames']
angles={'pickup-north':[0]*12,'carry-north':[0]*6,'unload-north':[0]*12}
yy,xx=np.indices((256,256));records=[];masters={};manifests={}
(P/'sources').mkdir(parents=True,exist_ok=True)
for gear,head,box in [('bare',barehead,headref['sourceBox']),('helmet',gearhead,[111,70,146,106])]:
    plane=Image.new('RGBA',(256,256));plane.alpha_composite(head,tuple(box[:2]));masters[gear]=plane;head.save(P/f'sources/{gear}-master-head.png')
    original=json.loads((R/audit['selectedStateSources'][gear]['carry-north']['manifest']).read_text())
    m=copy.deepcopy(original);m.update(name='Bill north cargo native master identity candidate',status='selected_runtime',frameWidth=256,frameHeight=256,pivot=[128,224],standingHeight=148,textureFilter='linear');m['states']=[];manifests[gear]=m
for key in angles:
    ref=audit['selectedStateSources']['bare'][key];baremanifest=json.loads((R/ref['manifest']).read_text());state=next(s for s in baremanifest['states'] if s['id']==key)
    gearref=audit['selectedStateSources']['helmet'][key];oldstates={g:next(s for s in json.loads((R/audit['selectedStateSources'][g][key]['manifest']).read_text())['states'] if s['id']==key) for g in masters}
    outfiles={g:[] for g in masters}
    for i,file in enumerate(ref['sourceFiles']):
        im=Image.open(R/file[6:]).convert('RGBA');a=np.array(im);rgb=a[:,:,:3].astype(float)
        top=int(np.where(a[:,:,3]>180)[0].min());old=next(r for r in oldreg if r['file'].endswith(f'{key}/{i:03}.png'))
        center=old['bareHeadCenter'];angle=angles[key][i]
        endpoint=(key=='pickup-north' and i==0) or (key=='unload-north' and i==11)
        left=int(center-16);right=int(center+16)
        warm=(a[:,:,3]>0)&(rgb[:,:,0]>rgb[:,:,1]*1.03)&(rgb[:,:,0]>rgb[:,:,2]*1.02)&(xx>=left)&(xx<right)&(yy>=top)&(yy<top+31)
        labels,n=label(warm);parts=[]
        for ident in range(1,n+1):
            ys,xs=np.where(labels==ident)
            if len(xs)>20 and ys.min()<top+14:parts.append((float(xs.mean()),ident))
        assert parts,(key,i)
        ident=min(parts)[1];erase=labels==ident
        erase=binary_dilation(binary_fill_holes(erase),iterations=1)&(a[:,:,3]>0)&(xx>=left)&(xx<right)&(yy>=top-2)&(yy<top+31)
        # Preserve neutral collar/backpack pixels surrounding the warm original head.
        erase&=~((rgb.max(2)-rgb.min(2)<12)&(yy>=top+12))
        hair=(a[:,:,3]>180)&(xx>=center-16)&(xx<center+16)&(yy>=top)&(yy<top+27)&(rgb[:,:,0]>rgb[:,:,2]*1.08)&(rgb[:,:,1]>rgb[:,:,2]*1.04)&(rgb.max(2)-rgb.min(2)>5)
        assert hair.any(),(key,i)
        necky=int(np.where(hair)[0].max())
        dx=round(center-128);dy=necky-100
        base=a.copy();base[erase]=0
        for gear in masters:
            originalfile=audit['selectedStateSources'][gear][key]['sourceFiles'][i]
            if endpoint:out=Image.open(R/originalfile[6:]).convert('RGBA')
            else:
                component=masters[gear].rotate(angle,resample=Image.Resampling.BICUBIC,center=(128,100)) if angle else masters[gear]
                out=Image.fromarray(base);out.alpha_composite(component,(dx,dy))
            dest=P/f'frames/{gear}/{key}/{i:03}.png';dest.parent.mkdir(parents=True,exist_ok=True);out.save(dest);outfiles[gear].append('res://'+dest.relative_to(R).as_posix())
            mask=P/f'sources/erase-{key}-{i:03}.png';Image.fromarray(erase.astype('uint8')*255).save(mask)
            records.append({'gear':gear,'state':key,'frame':i,'bareFile':file,'bareSha256':hashlib.sha256((R/file[6:]).read_bytes()).hexdigest(),'originalFile':originalfile,'originalSha256':hashlib.sha256((R/originalfile[6:]).read_bytes()).hexdigest(),'endpointExact':endpoint,'headAxis':center,'sourceTop':top,'neckY':necky,'angle':angle,'translation':[dx,dy],'eraseMask':mask.relative_to(P).as_posix(),'output':outfiles[gear][-1]})
    for gear in masters:
        st=copy.deepcopy(oldstates[gear]);st['frameFiles']=outfiles[gear];st['provenance']='Original cargo anatomy/case/clock; native accepted identity at scale1, rear hair/collar translation; review candidate'
        manifests[gear]['states'].append(st)
for gear,m in manifests.items():
    (P/('manifest.json' if gear=='bare' else 'helmet-manifest.json')).write_text(json.dumps(m,indent=2)+'\n')
(P/'head-registration.json').write_text(json.dumps({'nativeScale':1,'neckAnchor':[128,100],'bareSourceBox':headref['sourceBox'],'gearSourceBox':[111,70,146,106],'sourceInventory':'character/bill-selected-source-audit-2026-10-01-locomotion-v10/source-inventory.json','frames':records},indent=2)+'\n')
board=Image.new('RGB',(3072,1536),(34,52,62));draw=ImageDraw.Draw(board)
for row,(gear,key) in enumerate((g,k) for g in masters for k in angles):
    for col,file in enumerate(next(s for s in manifests[gear]['states'] if s['id']==key)['frameFiles']):
        im=Image.open(R/file[6:]);board.paste(im,(col*256,row*256),im);draw.text((col*256+4,row*256+4),gear+' '+key+' '+str(col),fill='white')
board.save(P/'contact-sheet.png');print('Built60 paired cargo references; staged native head/helmet repair')
