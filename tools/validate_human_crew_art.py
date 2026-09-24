"""Validate complete human crew candidates against their frozen native contracts."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
import argparse
from rebuild_bill_art import source_path
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('actor',choices=['veld','branforth','marsh'])
args=parser.parse_args()
ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'character'/({'veld':'dr-veld-v2','branforth':'chief-engineer-branforth-v2','marsh':'marsh-v2'}[args.actor])
c=json.loads((ROOT/'tools/crew-art-source-contracts'/(args.actor+'.json')).read_text());catalog=json.loads((ART/'catalog.json').read_text())
c['equipmentStates']=[] if args.actor=='marsh' else [e['id'] for e in c['equipment']]
errors=[];counts={};edge=[];baseline={e['id']:e for e in c['states']};selected={}
supplement_path=ROOT/'tools/crew-art-source-contracts'/(args.actor+'-supplemental.json')
supplements=json.loads(supplement_path.read_text()) if supplement_path.exists() else {}
bunk_durations=[120,240,300,300,300,300,280]
bunk={'bunk-enter-east':(list(range(7)),bunk_durations,False),
      'bunk-exit-east':(list(reversed(range(7))),list(reversed(bunk_durations)),False),
      'bunk-sleep-east':([6],[1000],True)}
berth_durations=[120,300,300,300,300,280]
berth=({'berth-lie-east':(list(range(6)),berth_durations,False),
        'berth-rise-east':(list(reversed(range(6))),list(reversed(berth_durations)),False),
        'berth-sleep-east':([5],[1000],True)} if args.actor=='marsh' else {})
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
            extra=supplements.get(key) if variant=='body' else None
            if key in berth:
                order,durations,loop=berth[key]
                old={'frames':order,'timing':{'durations':durations,'loop':loop}}
                check(rel=='supplemental/berth-east/manifest.json','Berth manifest '+key)
                check(m.get('pivot')==[92,172] and [m.get('frameWidth'),m.get('frameHeight')]==[184,184],'Berth profile '+key)
                check(e['frameFiles']==[f'{i:03}.png' for i in order],'Berth order '+key)
                check(e.get('depthOffsets')==[32 if i==0 else 64 if i==1 else 96 for i in order],'Berth depth '+key)
            if key in bunk:
                order,durations,loop=bunk[key]
                old={'frames':order,'timing':{'durations':durations,'loop':loop}}
                check(m.get('canvas')==([256,272] if args.actor=='marsh' else [256,256]) and m.get('pivot')==[128,224],'Bunk profile '+key)
                check(e['frameFiles']==[f'{i:03}.png' for i in order],'Bunk frame order '+key)
                check(e.get('furnitureFrames')==['bunk' if i>=4 else '' for i in order],'Bunk foreground '+key)
                check(e.get('depthOffsets')==[100 if i>=4 else 96 for i in order],'Bunk depth '+key)
            if extra:
                old={'frames':extra['sha256'],'timing':{'durations':extra['durations'],'loop':extra['loop']}}
                check(rel==extra['manifest'],'Supplement manifest '+key)
                check(m['pivot']==extra['pivot'] and [m['frameWidth'],m['frameHeight']]==extra['canvas'],'Supplement registration '+key)
            if old is None:
                errors.append('Unexpected state '+key);continue
            selected[(variant,key)]=(m,e)
            check(len(e['frameFiles'])==len(old['frames']),'Frame count '+variant+'/'+key)
            expected_durations=[130,170,150,200,150,100] if args.actor=='branforth' and key=='walk-west' else old['timing']['durations']
            check(e['frameDurationsMs']==expected_durations,'Durations '+variant+'/'+key)
            check(e['loop']==old['timing']['loop'],'Loop mode '+variant+'/'+key)
            for field in (['depthOffsets'] if key in bunk or key in berth else ['facings','waterKinds','waterPoses','depthOffsets']):
                check(len(e.get(field,[]))==len(e['frameFiles']),'Per-frame metadata '+variant+'/'+key+'/'+field)
            for index,f in enumerate(e['frameFiles']):
                path=(p.parent/f).resolve();im=Image.open(path).convert('RGBA');a=np.array(im);box=im.getbbox();count+=1
                if extra:check(index<len(extra['sha256']) and hashlib.sha256(path.read_bytes()).hexdigest()==extra['sha256'][index],'Supplement pixels '+key+'/'+str(index))
                dimensions=tuple(m['canvas']) if key in bunk else (m['frameWidth'],m['frameHeight'])
                check(im.size==dimensions,'Dimensions '+str(path));check(box is not None,'Empty '+str(path))
                if key in bunk:
                    source=ROOT/'character/bunk-contact-study-2026-09-21'/(args.actor+'-entry'+('' if variant=='body' else '-helmet'))/f
                    check(im.tobytes()==Image.open(source).convert('RGBA').tobytes(),'Bunk reviewed pixels '+variant+'/'+key+'/'+f)
                check(set(np.unique(a[:,:,3]))<={0,255},'Soft alpha '+str(path))
                if box and (box[0]==0 or box[1]==0 or box[2]==im.width or box[3]==im.height):
                    edge.append(str(path.relative_to(ART)));errors.append('Canvas border touch '+str(path.relative_to(ART)))
    expected={e['id'] for e in c['states']} if variant=='body' else set(c['equipmentStates'])
    if variant=='body':expected.update(supplements)
    if variant=='body':expected.update(berth)
    if variant=='body' or args.actor!='marsh':expected.update(bunk)
    check(ids==expected,'State coverage '+variant);counts[variant]={'states':len(ids),'frames':count}
for key in c['equipmentStates']+(list(bunk) if args.actor!='marsh' else []):
    if ('body',key) not in selected or ('equipment',key) not in selected:continue
    body,bclip=selected[('body',key)];gear,gclip=selected[('equipment',key)]
    for field in (['pivot','standingHeight','canvas'] if key in bunk else ['pivot','standingHeight','frameWidth','frameHeight']):
        check(body[field]==gear[field],'Equipment profile '+key+'/'+field)
    for field in (['frameDurationsMs','loop','furnitureFrames','depthOffsets'] if key in bunk else ['frameDurationsMs','loop','facings','waterKinds','waterPoses','depthOffsets']):
        check(bclip[field]==gclip[field],'Equipment playback '+key+'/'+field)
result={'errors':errors,'counts':counts,'sourceFramesUnchanged':len(c['sourceFrames']),'sourceManifestsUnchanged':len(c['sourceManifests']),'borderTouches':edge}
out=ROOT/'output/crew-replacement-2026-09-12'/args.actor/'validation.json';out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({**result,'borderTouches':len(edge)}));raise SystemExit(bool(errors))
