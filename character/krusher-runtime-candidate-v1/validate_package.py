from pathlib import Path
import hashlib,json
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parent.parent;m=json.loads((P/'provenance.json').read_text());errors=[];checks=0
def check(ok,label):
    global checks
    checks+=1
    if not ok:errors.append(label)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for path,digest in m['sourceHashes'].items():check(sha(R/path)==digest,'input changed: '+path)
for record in m['records']:check(sha(P/record['output'])==record['sha256'],'package bytes: '+record['output'])
for path in set(r['output'] for r in m['records']):
    im=Image.open(P/path);check(im.size==(184,184) and im.mode=='RGBA','canvas/alpha: '+path)
manifests=[json.loads((P/f'{g}-manifest.json').read_text()) for g in ['bare','helmet']]
for manifest in manifests:
    check(manifest['pivot']==[92,172] and manifest['standingHeight']==148,'registration')
    for state in manifest['states']:
        check(state['frameCount']==len(state['frameFiles'])==len(state['frameDurationsMs']),'count/timing: '+state['id'])
        check(all(x>0 for x in state['frameDurationsMs']),'positive holds')
        root=P.parent/('krusher-terminal-gear-pair-v1' if state['id'].startswith('terminal-') else 'krusher-moving-equipment-test-v2')
        original=next(s for s in json.loads((root/f"{manifest['equipmentVariant']}-manifest.json").read_text())['states'] if s['id']==state['id'])
        check(state['frameDurationsMs']==original['frameDurationsMs'] and state['loop']==original['loop'],'source clock exact')
    states={s['id']:s for s in manifest['states']};idle=states['idle-west']['frameFiles'][0]
    check(states['terminal-raise-west']['frameFiles'][0]==idle and states['terminal-lower-west']['frameFiles'][-1]==idle,'exact canonical idle alias')
    check(states['terminal-raise-west']['frameFiles'][-1]==states['terminal-type-west']['frameFiles'][0]==states['terminal-lower-west']['frameFiles'][0],'held joins alias')
for b,h in zip(manifests[0]['states'],manifests[1]['states']):check((b['id'],b['frameDurationsMs'],b['loop'])==(h['id'],h['frameDurationsMs'],h['loop']),'gear compatible clock')
result={'checks':checks,'errors':errors,'uniqueFrames':m['uniqueOutputs'],'frameReferences':m['frameReferences'],'statesPerGear':len(manifests[0]['states']),'scope':'Package source bytes, metadata, timing, registration and joins; not artistic acceptance.'};(P/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));raise SystemExit(bool(errors))
