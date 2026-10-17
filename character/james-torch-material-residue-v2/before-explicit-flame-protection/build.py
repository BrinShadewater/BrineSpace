"""Deterministic correction of residue missed by the existing cold-material mask."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,copy
P=Path(__file__).resolve().parent;R=P.parents[1];OLD=R/'character/james-standing-torch-consistency-v2'
review=json.loads((OLD/'review-evidence.json').read_text());bindings=P/'source-bindings.json'
if not bindings.exists():
    current=json.loads((R/'character/james-animation-coverage-2026-09-30/runtime-coverage.json').read_text())
    coverage={mode:{key:row for key,row in current[mode].items() if key.startswith(('idle-','torch-draw-','weld-','torch-stow-'))} for mode in ['body','equipment']}
    bindings.write_text(json.dumps({'coverage':coverage,'sourceRecords':review['records']},indent=2)+'\n')
frozen=json.loads(bindings.read_text());coverage=frozen['coverage']
for source in frozen['sourceRecords']:
    assert hashlib.sha256((R/source['path']).read_bytes()).hexdigest()==source['sha256'],'Frozen source changed: '+source['path']
L=np.array([.2126,.7152,.0722]);cache={};records=[];manifests={};configs={}
def load(path):
    if path not in cache:cache[path]=json.loads(path.read_text())
    return cache[path]
def frame(file,manifest):return R/file.removeprefix('res://') if file.startswith('res://') else manifest.parent/file
def mask(a):
    rgb=a[:,:,:3].astype(float);r,g,b=rgb.transpose(2,0,1);y=np.indices(a.shape[:2])[0]
    excess=g-(r+b)/2;spread=np.ptp(rgb,axis=2)
    yellow=(r>b+12)&(g>b+8)&(r>=g-2)
    # Only modest neutral-material spill below the collar; rigid head/shell,
    # intentional saturated engineering yellow and blue/cyan flame stay exact.
    weight=np.clip((excess-4)/6,0,1)*np.clip((35-spread)/10,0,1)
    weight*=((y>=60)&(a[:,:,3]>0)&(~yellow)&(rgb.mean(2)>12)&(rgb.mean(2)<170))
    return weight,excess
for mode in ['bare','helmet']:
    states=[]
    for direction in ['east','north','south','west']:
        configs[direction]={'greenExcessThreshold':4,'greenExcessFullWeight':10,'chromaFadeStart':25,'chromaFadeEnd':35,'headProtectedAboveY':60,'lumaWeights':L.tolist(),'targetGreenExcess':0,'method':'Fixed equal-luminance green-residue suppression; original red-minus-blue relationship retained. Same transform/mask in both gears, no per-frame adaptive exposure.'}
        master_path=R/coverage['body' if mode=='bare' else 'equipment']['idle-'+direction]['path'];master_m=load(master_path);master_s=next(s for s in master_m['states'] if s['id']=='idle-'+direction)
        master=np.array(Image.open(frame(master_s['frameFiles'][0],master_path)).convert('RGBA'))
        for key in ['torch-draw-'+direction,'weld-'+direction,'torch-stow-'+direction]:
            manifest_path=R/coverage['body' if mode=='bare' else 'equipment'][key]['path'];m=load(manifest_path);s=copy.deepcopy(next(s for s in m['states'] if s['id']==key));files=[]
            for index,f in enumerate(s['frameFiles']):
                src=frame(f,manifest_path);a=np.array(Image.open(src).convert('RGBA'));weight,excess=mask(a)
                exact_neutral=np.array_equal(a,master)
                if exact_neutral:weight[:]=0
                rgb=a[:,:,:3].astype(float);delta=-excess*weight
                correction=np.stack((-.7152*delta,.2848*delta,-.7152*delta),axis=2)
                b=a.copy();b[:,:,:3]=np.clip(np.rint(rgb+correction),0,255).astype('uint8')
                assert np.array_equal(a[:,:,3],b[:,:,3]) and np.array_equal(a[weight==0],b[weight==0])
                assert np.array_equal(a[:60],b[:60])
                rel=f'frames/{mode}/{key}/{index:03d}.png';dest=P/rel;dest.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(b).save(dest);files.append('res://'+dest.relative_to(R).as_posix())
                changed=np.any(a!=b,axis=2);lumadiff=np.abs((b[:,:,:3].astype(float)-rgb)@L)
                records.append({'mode':mode,'key':key,'index':index,'source':src.relative_to(R).as_posix(),'sourceSha256':hashlib.sha256(src.read_bytes()).hexdigest(),'destination':dest.relative_to(R).as_posix(),'changedPixels':int(changed.sum()),'alphaExact':True,'headExact':True,'outsideMaskExact':True,'neutralExact':exact_neutral,'maxLumaRoundingDifference':float(lumadiff.max())})
            s['frameFiles']=files;s.setdefault('provenance',{})['materialResidueCorrection']=configs[direction];states.append(s)
    head={k:copy.deepcopy(v) for k,v in m.items() if k!='states'};head['name']='James torch bounded neutral-material residue '+mode;head['status']='staged_material_candidate_native_pending';head['states']=states;manifests[mode]=head
    (P/f'{mode}-manifest.json').write_text(json.dumps(head,indent=2)+'\n')
(P/'material-config.json').write_text(json.dumps(configs,indent=2)+'\n')
(P/'build-evidence.json').write_text(json.dumps({'sourceReferences':len(records),'changedReferences':sum(r['changedPixels']>0 for r in records),'changedPixels':sum(r['changedPixels'] for r in records),'records':records,'scope':'Code-native correction of existing grade mask omission; no authored geometry/frame/timing change, candidate unselected. Exact neutral/alpha/head/outside-mask and equal-luminance RGB correction.'},indent=2))
# Representative flagged source slots and all exact idle joins, full source review follows.
board=Image.new('RGB',(4*552,4*220),'#303b40');draw=ImageDraw.Draw(board)
for row,direction in enumerate(['east','north','south','west']):
    for gear,mode in enumerate(['bare','helmet']):
        for i,index in enumerate([1,7]):
            record=next(r for r in records if r['mode']==mode and r['key']=='torch-draw-'+direction and r['index']==index)
            x=(gear*2+i)*552;y=row*220
            for j,path in enumerate([record['source'],record['destination']]):
                im=Image.open(R/path).convert('RGBA');board.paste(im,(x+j*184,y+24),im)
            draw.text((x+3,y+3),direction+' '+mode+' draw'+str(index)+' before / candidate',fill='white')
board.save(P/'material-comparison.png')
print(json.dumps({'references':len(records),'changedReferences':sum(r['changedPixels']>0 for r in records),'changedPixels':sum(r['changedPixels'] for r in records),'candidateSelected':False}))
