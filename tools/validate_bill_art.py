"""Validate source preservation and the complete selected Bill revision."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];ART=ROOT/'character/major-bill-v3'
c=json.loads((ROOT/'tools/bill-art-source-contract.json').read_text());catalog=json.loads((ART/'catalog.json').read_text())
errors=[];counts={};edge=[];baseline={e['id']:e for e in c['states']};selected={}
def check(ok,why):
    if not ok:errors.append(why)
for path,record in c['sourceFrames'].items():check(hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==record['sha256'],'Changed original '+path)
for path,digest in c['sourceManifests'].items():check(hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,'Changed source manifest '+path)
for variant in ['body','equipment']:
    ids=set();count=0
    for rel in catalog[variant]:
        p=ART/rel;m=json.loads(p.read_text());check(m['standingHeight']==148,'Wrong density '+rel)
        for e in m['states']:
            check(e['id'] not in ids,'Duplicate '+e['id']);ids.add(e['id'])
            key=e['id'];old=baseline.get(key)
            if old is None:
                errors.append('Unexpected state '+key);continue
            selected[(variant,key)]=(m,e)
            check(len(e['frameFiles'])==len(old['frames']),'Frame count '+variant+'/'+key)
            check(e['frameDurationsMs']==old['timing']['durations'],'Durations '+variant+'/'+key)
            check(e['loop']==old['timing']['loop'],'Loop mode '+variant+'/'+key)
            for field in ['facings','waterKinds','waterPoses','depthOffsets']:
                check(len(e.get(field,[]))==len(e['frameFiles']),'Per-frame metadata '+variant+'/'+key+'/'+field)
            for f in e['frameFiles']:
                path=(p.parent/f).resolve();im=Image.open(path).convert('RGBA');a=np.array(im);box=im.getbbox();count+=1
                check(im.size==(m['frameWidth'],m['frameHeight']),'Dimensions '+str(path));check(box is not None,'Empty '+str(path))
                check(set(np.unique(a[:,:,3]))<={0,255},'Soft alpha '+str(path))
                if box and (box[0]==0 or box[1]==0 or box[2]==im.width or box[3]==im.height):
                    edge.append(str(path.relative_to(ART)));errors.append('Canvas border touch '+str(path.relative_to(ART)))
    expected={e['id'] for e in c['states']} if variant=='body' else set(c['equipmentStates'])
    check(ids==expected,'State coverage '+variant);counts[variant]={'states':len(ids),'frames':count}
for key in c['equipmentStates']:
    if ('body',key) not in selected or ('equipment',key) not in selected:continue
    body,bclip=selected[('body',key)];gear,gclip=selected[('equipment',key)]
    for field in ['pivot','standingHeight','frameWidth','frameHeight']:
        check(body[field]==gear[field],'Equipment profile '+key+'/'+field)
    for field in ['frameDurationsMs','loop','facings','waterKinds','waterPoses','depthOffsets']:
        check(bclip[field]==gclip[field],'Equipment playback '+key+'/'+field)
result={'errors':errors,'counts':counts,'sourceFramesUnchanged':len(c['sourceFrames']),'sourceManifestsUnchanged':len(c['sourceManifests']),'borderTouches':edge}
out=ROOT/'output/bill-full-replacement-2026-09-12/validation.json';out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({**result,'borderTouches':len(edge)}));raise SystemExit(bool(errors))
