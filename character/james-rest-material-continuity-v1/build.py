"""One facing-level material correction over complete ordinary rest sources."""
from pathlib import Path
import json,copy,runpy,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];A=R/'character/james-rest-motion-audit-2026-10-01'
helpers=runpy.run_path(str(A/'material_helpers.py'));region=helpers['region'];masks=helpers['masks']
calibration=P/'calibration.json'
if not calibration.exists():calibration.write_text((A/'material-diagnostics.json').read_text(),encoding='utf-8')
stats=json.loads(calibration.read_text())['directions'];binding=P/'source-bindings.json'
if not binding.exists():
    cov=json.loads((R/'character/james-animation-coverage-2026-09-30/runtime-coverage.json').read_text());frozen={g:{k:v for k,v in cov[g].items() if k.startswith(('lie-down-','sleep-','get-up-'))} for g in ['body','equipment']}
    assert all('james-rest-material-continuity-v1' not in v['path'] for rows in frozen.values() for v in rows.values());binding.write_text(json.dumps(frozen,indent=2)+'\n',encoding='utf-8')
bindings=json.loads(binding.read_text());records=[];cache={};boards={};selection=json.loads((P/'selection.json').read_text()) if (P/'selection.json').exists() else {}
for mode,group in [('bare','body'),('helmet','equipment')]:
    pack=None
    for direction in ['north','south','east','west']:
        for action in ['lie-down','sleep','get-up']:
            key=action+'-'+direction;file=R/bindings[group][key]['path'];original=json.loads(file.read_text());state=next(s for s in original['states'] if s['id']==key)
            if pack is None:pack={k:copy.deepcopy(v) for k,v in original.items() if k!='states'};pack.update(name='James ordinary rest master materials '+mode,status=selection.get('status','candidate_material_review_pending'),states=[])
            new=copy.deepcopy(state);new['frameFiles']=[];rows=[]
            for i,f in enumerate(state['frameFiles']):
                src=R/f.removeprefix('res://') if f.startswith('res://') else (file.parent/f).resolve();im=Image.open(src).convert('RGBA');a=np.array(im);out=a.copy();pose=state['provenance']['sourcePoses'][i];box=region(direction,pose);neutral,gold,protect=masks(a,box)
                if pose==0:neutral[:]=False;gold[:]=False
                for material,mask in [('neutral',neutral),('gold',gold)]:out[:,:,:3][mask]=np.rint(a[:,:,:3][mask].astype(float)*np.array(stats[direction]['stats'][material]['fixedGain'])).clip(0,255).astype(np.uint8)
                assert np.array_equal(a[:,:,3],out[:,:,3]) and np.array_equal(a[protect],out[protect]);assert np.array_equal(a[~(neutral|gold)],out[~(neutral|gold)])
                dest=P/'frames'/mode/key/f'{i:03}.png';dest.parent.mkdir(parents=True,exist_ok=True);revised=Image.fromarray(out);revised.save(dest);new['frameFiles'].append(dest.relative_to(P).as_posix());rows.append((im,revised))
                records.append({'mode':mode,'key':key,'index':i,'source':src.relative_to(R).as_posix(),'sourceSha256':hashlib.sha256(src.read_bytes()).hexdigest(),'output':new['frameFiles'][-1],'sourcePose':pose,'protectedHead':box,'alphaExact':True,'headExact':True,'changedPixels':int(np.any(a!=out,2).sum())})
            new['provenance']['restMaterialContinuity']={'sourceManifest':file.relative_to(R).as_posix(),'method':'One pooled unique-interior source neutral/gold gain per direction shared bare/helmet; original protected head plus common-shell edit union excluded. All geometry/alpha/clocks/rest anchors preserved; exact standing source0. No additional tone-curve pass or pose-specific normalization.','gains':stats[direction]['stats']};pack['states'].append(new);boards[(mode,key)]=rows
    (P/(mode+'-manifest.json')).write_text(json.dumps(pack,indent=2)+'\n',encoding='utf-8')
for direction in ['north','south','east','west']:
    board=Image.new('RGB',(6*256,4*280),'#303b40');d=ImageDraw.Draw(board)
    for mode_i,mode in enumerate(['bare','helmet']):
        rows=boards[(mode,'lie-down-'+direction)]
        for i,(original,revised) in enumerate(rows):
            for treatment,img in enumerate([original,revised]):
                row=mode_i*2+treatment;board.paste(img,(i*256,row*280+24),img);d.text((i*256+5,row*280+5),mode+' '+('original' if treatment==0 else 'fixed material')+' '+str(i),fill='white')
    board.save(P/(direction+'-comparison.png'))
(P/'material-evidence.json').write_text(json.dumps({'sourceReferences':len(records),'alphaAllExact':True,'protectedHeadAllExact':True,'clockGeometryChanges':False,'gains':{d:s['stats'] for d,s in stats.items()},'records':records,'productionInstalled':False,'scope':'Broad neutral/ochre material masks outside existing head/shell ownership regions; can include neutral gloves/metal/tools and ochre boots/belt pieces. Mask is not semantic shoulder-only. No per-frame correction or skin/head changes.'},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'frames':len(records),'changedFrames':sum(r['changedPixels']>0 for r in records),'headAlphaExact':True,'clockGeometryChanges':False,'productionInstalled':False}))
