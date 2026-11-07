"""Validate source preservation and the complete selected Bill revision."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
from rebuild_bill_art import source_path
ROOT=Path(__file__).resolve().parents[1];ART=ROOT/'character/major-bill-v3'
c=json.loads((ROOT/'tools/bill-art-source-contract.json').read_text());catalog=json.loads((ART/'catalog.json').read_text())
errors=[];counts={};edge=[];baseline={e['id']:e for e in c['states']};selected={}
bunk_durations=[120,240,300,300,300,300,280]
bunk={
    'bunk-enter-east':(list(range(7)),bunk_durations,False),
    'bunk-exit-east':(list(reversed(range(7))),list(reversed(bunk_durations)),False),
    'bunk-sleep-east':([6],[1000],True),
}
def check(ok,why):
    if not ok:errors.append(why)
for path,record in c['sourceFrames'].items():check(hashlib.sha256(source_path(ROOT/path).read_bytes()).hexdigest()==record['sha256'],'Changed original '+path)
for path,digest in c['sourceManifests'].items():check(hashlib.sha256(source_path(ROOT/path).read_bytes()).hexdigest()==digest,'Changed source manifest '+path)
for variant in ['body','equipment']:
    ids=set();count=0
    for rel in catalog[variant]:
        p=ART/rel;m=json.loads(p.read_text());check(m['standingHeight']==148,'Wrong density '+rel)
        for e in m['states']:
            check(e['id'] not in ids,'Duplicate '+e['id']);ids.add(e['id'])
            key=e['id'];old=baseline.get(key)
            if key in bunk:
                order,durations,loop=bunk[key]
                old={'frames':order,'timing':{'durations':durations,'loop':loop}}
                check(m.get('canvas')==[256,272] and m.get('pivot')==[128,224],'Bunk profile '+key)
                check(e['frameFiles']==[f'{i:03}.png' for i in order],'Bunk frame order '+key)
                check(e.get('furnitureFrames')==['bunk' if i>=4 else '' for i in order],'Bunk foreground '+key)
                check(e.get('depthOffsets')==[100 if i>=4 else 96 for i in order],'Bunk depth '+key)
            if old is None:
                errors.append('Unexpected state '+key);continue
            selected[(variant,key)]=(m,e)
            check(len(e['frameFiles'])==len(old['frames']),'Frame count '+variant+'/'+key)
            check(e['frameDurationsMs']==old['timing']['durations'],'Durations '+variant+'/'+key)
            check(e['loop']==old['timing']['loop'],'Loop mode '+variant+'/'+key)
            for field in (['depthOffsets'] if key in bunk else ['facings','waterKinds','waterPoses','depthOffsets']):
                check(len(e.get(field,[]))==len(e['frameFiles']),'Per-frame metadata '+variant+'/'+key+'/'+field)
            for f in e['frameFiles']:
                path=(p.parent/f).resolve();im=Image.open(path).convert('RGBA');a=np.array(im);box=im.getbbox();count+=1
                dimensions=tuple(m['canvas']) if key in bunk else (m['frameWidth'],m['frameHeight'])
                check(im.size==dimensions,'Dimensions '+str(path));check(box is not None,'Empty '+str(path))
                if key in bunk:
                    source=ROOT/'character/bunk-contact-study-2026-09-21'/('bill-entry' if variant=='body' else 'bill-entry-helmet')/f
                    check(im.tobytes()==Image.open(source).convert('RGBA').tobytes(),'Bunk reviewed pixels '+variant+'/'+key+'/'+f)
                check(set(np.unique(a[:,:,3]))<={0,255},'Soft alpha '+str(path))
                if box and (box[0]==0 or box[1]==0 or box[2]==im.width or box[3]==im.height):
                    edge.append(str(path.relative_to(ART)));errors.append('Canvas border touch '+str(path.relative_to(ART)))
    expected={e['id'] for e in c['states']} if variant=='body' else set(c['equipmentStates'])
    expected.update(bunk)
    check(ids==expected,'State coverage '+variant);counts[variant]={'states':len(ids),'frames':count}
for key in list(c['equipmentStates'])+list(bunk):
    if ('body',key) not in selected or ('equipment',key) not in selected:continue
    body,bclip=selected[('body',key)];gear,gclip=selected[('equipment',key)]
    for field in (['pivot','standingHeight','canvas'] if key in bunk else ['pivot','standingHeight','frameWidth','frameHeight']):
        check(body[field]==gear[field],'Equipment profile '+key+'/'+field)
    for field in (['frameDurationsMs','loop','furnitureFrames','depthOffsets'] if key in bunk else ['frameDurationsMs','loop','facings','waterKinds','waterPoses','depthOffsets']):
        check(bclip[field]==gclip[field],'Equipment playback '+key+'/'+field)
result={'errors':errors,'counts':counts,'sourceFramesUnchanged':len(c['sourceFrames']),'sourceManifestsUnchanged':len(c['sourceManifests']),'borderTouches':edge}
out=ROOT/'output/bill-full-replacement-2026-09-12/validation.json';out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({**result,'borderTouches':len(edge)}));raise SystemExit(bool(errors))
