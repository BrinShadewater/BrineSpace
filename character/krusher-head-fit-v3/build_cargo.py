from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import binary_dilation,distance_transform_edt,label
R=Path(__file__).resolve().parents[2];H=Path(__file__).resolve().parent;OLD=R/'character/krusher-cargo-family-v1';PREV=R/'character/krusher-cargo-family-v2';P=R/'character/krusher-cargo-family-v3';P.mkdir(exist_ok=True)
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def arr(p):return np.array(Image.open(p).convert('RGBA'))
previous={q['output']:q for q in read(PREV/'revision.json')['records']};records=[];yy,xx=np.indices((256,256))
for q in read(OLD/'provenance.json')['records']:
    g,v=q['gear'],q['view'];a=arr(OLD/q['output']);out=a.copy();mask=np.zeros((256,256),bool);details={};protected=q['headBox'][3]+14
    if v!='north':
        bowed='repair-side-heads' in q['headSource'];kind='bare' if g=='bare' else 'visor';sourceview=v if g=='bare' or v not in ['ne','nw'] else ('east' if v=='ne' else 'west')
        hp=H/'sources'/f'{kind}-{sourceview}{"-bowed" if bowed else ""}-native.png';head=Image.open(hp).convert('RGBA');details={'headSource':'res://'+hp.relative_to(R).as_posix(),'headHash':sha(hp),'bowed':bowed}
        if g=='bare':
            oldhead=Image.open(R/q['headSource']).convert('RGBA');ax,ay=q['headPaste'];oldlayer=Image.new('RGBA',(256,256));oldlayer.paste(oldhead,(ax,ay));remove=(np.array(oldlayer)[:,:,3]>0)&(np.array(Image.open(OLD/q['allowedMask']))>0);out[remove]=0
            if len(v)==2 or bowed:paste=[ax-(head.width-oldhead.width)//2,ay+oldhead.height-head.height+(2 if len(v)==2 else 0)]
            else:paste=[ax-4 if v=='east' else ax+2 if v=='west' else ax-(head.width-oldhead.width)//2,ay]
            # These original turning bodies raise the collar relative to the
            # old face-only anchor. Register the whole authored head, retaining
            # its neck and pixels, rather than drawing a connecting bridge.
            if q['state']=='carry-turn-east-north' and q['frame'] in [0,2]:
                dy=4 if q['frame']==0 else 2
                paste[1]+=dy;details['collarRegistrationOffset']=[0,dy]
            layer=Image.new('RGBA',(256,256));layer.paste(head,tuple(paste));ha=np.array(layer);opaque=ha[:,:,3]>0;out[opaque]=ha[opaque];mask=remove|opaque;details.update(paste=paste,oldPaste=[ax,ay],oldHeadSource='res://'+q['headSource'])
            # Retired inserted heads left small disconnected face fragments.
            # Remove only inherited components in the original head envelope;
            # no current authored head pixel or connected body is touched.
            labs,n=label(out[:,:,3]>0);clean=np.zeros_like(mask);x0,y0,x1,y1=q['headBox']
            for component,size in enumerate(np.bincount(labs.ravel())):
                if component==0 or size>12:continue
                region=labs==component;sy,sx=np.where(region)
                if not np.any(region&opaque) and sx.min()>=x0-14 and sx.max()<x1+14 and sy.min()>=min(ay,paste[1])-5 and sy.max()<y1+3:clean|=region
            out[clean]=0;mask|=clean;details['removedInheritedHeadFragments']=int(clean.sum())
            if q['state']=='carry-turn-north-west' and q['frame']==4:
                # Original profile nose fragments sit outside the old insertion
                # window, connected only by faint alpha. This observed local
                # envelope is wholly above the connected shoulder/collar.
                ghost=(xx>=110)&(xx<114)&(yy>=78)&(yy<97)&(a[:,:,3]>0)&~opaque
                out[ghost]=0;mask|=ghost;details['oldProfileFragmentBox']=[110,78,114,97];details['oldProfileFragmentPixels']=int(ghost.sum())
        else:
            prev=previous[q['output']];base=np.array(Image.open(PREV/prev['mask']))>0;original=arr(R/q['source']);rgb=original[:,:,:3].astype(float)
            shell_restore=None
            if q['state']=='carry-turn-north-west' and q['frame']==4:
                # Warm bronze shell pixels were incorrectly included in the
                # old portrait hull. Restore original hardware, then fit only
                # the actual narrow visor aperture observed in the source.
                shell_restore=(np.array(Image.open(OLD/q['allowedMask']))>0)&(yy<96)
                out[shell_restore,:3]=original[shell_restore,:3]
                polygon=[[116,79],[120,80],[122,85],[122,89],[119,94],[114,92],[114,85],[115,81]]
                region=Image.new('L',(256,256));ImageDraw.Draw(region).polygon([tuple(p) for p in polygon],fill=255);mask=(np.array(region)>0)&(a[:,:,3]>180)
                details.update(restoredOriginalShell='res://'+q['source'],visorPolygon=polygon)
            elif v in ['ne','nw']:
                aperture=prev['details']['protectedVisorAperture'];x0,y0,x1,y1=aperture;mask=base.copy();details['protectedVisorAperture']=aperture
            else:
                x0,y0,x1,y1=prev['details']['newFaceBox'];mask=binary_dilation(base,iterations=1)
                for dy in range(1,4):mask[:-dy]|=base[dy:]
                glass=(rgb[:,:,2]>rgb[:,:,0]*1.2)&(rgb[:,:,1]>rgb[:,:,0]*1.2);metal=(rgb.max(2)-rgb.min(2)<12)&(rgb.mean(2)>75)&(yy<y0)
                mask&=(xx>=x0)&(xx<x1)&(yy>=y0-3)&(yy<y1)&~glass&~metal&(a[:,:,3]>180)
            sy,sx=np.where(mask);box=[int(sx.min()),int(sy.min()),int(sx.max()+1),int(sy.max()+1)];part=np.array(head);nearest=distance_transform_edt(part[:,:,3]==0,return_distances=False,return_indices=True);part[:,:,:3]=part[nearest[0],nearest[1],:3];part[:,:,3]=255;fit=Image.fromarray(part).resize((box[2]-box[0],box[3]-box[1]),Image.Resampling.NEAREST);layer=Image.new('RGBA',(256,256));layer.paste(fit,(box[0],box[1]));out[mask,:3]=np.array(layer)[mask,:3];details['visorBox']=box
            if shell_restore is not None:
                restore_only=shell_restore&~mask;details['restoredShellPixels']=int(restore_only.sum());rel='restored-shell-mask/'+Path(q['output']).name;(P/rel).parent.mkdir(parents=True,exist_ok=True);Image.fromarray(restore_only.astype('uint8')*255).save(P/rel);details['restoredShellMask']=rel;mask|=shell_restore
    assert np.array_equal(a[~mask],out[~mask]);assert np.array_equal(a[protected:],out[protected:])
    if g=='helmet':assert np.array_equal(a[:,:,3],out[:,:,3])
    target=P/q['output'];target.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(out).save(target);mr='head-masks/'+g+'/'+target.name;(P/mr).parent.mkdir(parents=True,exist_ok=True);Image.fromarray(mask.astype('uint8')*255).save(P/mr)
    records.append({'gear':g,'state':q['state'],'frame':q['frame'],'view':v,'source':'res://'+(OLD/q['output']).relative_to(R).as_posix(),'sourceHash':sha(OLD/q['output']),'output':q['output'],'outputHash':sha(target),'mask':mr,'protectedFromRow':protected,'changedPixels':int(np.any(a!=out,2).sum()),'details':details})
for g in ['bare','helmet']:(P/(g+'-manifest.json')).write_bytes((OLD/(g+'-manifest.json')).read_bytes())
(P/'revision.json').write_text(json.dumps({'records':records,'scope':'Complete H3 cardinal/quarter head-neck and visor identity on original cargo body/case. Whole original manifest bytes exact. Rear retained; staged partial full-library revision.'},indent=2)+'\n')
profile=R/'character/krusher-cargo-settle-profile-v3';profile.mkdir(exist_ok=True)
for g in ['bare','helmet']:
    original=R/'character/krusher-cargo-settle-profile-v1'/(g+'-manifest.json');m=read(original)
    for s in m['states']:s['frameFiles']=[f.replace(OLD.name,P.name) for f in s['frameFiles']]
    (profile/(g+'-manifest.json')).write_text(json.dumps(m,indent=2)+'\n')
(P/'pack-index.json').write_text(json.dumps({'candidatePacks':{g:['res://'+(P/(g+'-manifest.json')).relative_to(R).as_posix(),'res://'+(profile/(g+'-manifest.json')).relative_to(R).as_posix()] for g in ['bare','helmet']}},indent=2)+'\n')
(P/'native').mkdir(exist_ok=True)
for name in ['review.gd']:
    native=(PREV/'native'/name).read_text().replace(PREV.name,P.name).replace('krusher-cargo-settle-profile-v2','krusher-cargo-settle-profile-v3')
    native=native.replace('if i in [0,s.frameFiles.size()/2,s.frameFiles.size()-1]:','if i in [0,s.frameFiles.size()/2,s.frameFiles.size()-1] or (s.id=="carry-turn-east-north" and i==2) or (s.id=="carry-turn-north-west" and i==4):')
    (P/'native'/name).write_text(native)
(P/'run_native.py').write_text((PREV/'run_native.py').read_text().replace(PREV.name,P.name))
media=(PREV/'build_review.py').read_text().replace("\\nduration {hold/1000:.9f}","\\noption framerate 1000\\nduration {hold/1000:.9f}").replace("file 'video-frames/{name}'\\n\")","file 'video-frames/{name}'\\noption framerate 1000\\n\")").replace("'-vf','fps=60'","'-t',str(t),'-vf','fps=60'")
(P/'build_review.py').write_text(media)
print(json.dumps({'unique':len(records),'changed':sum(q['changedPixels']>0 for q in records)}))
