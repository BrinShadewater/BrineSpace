"""Reuse exact held-source evidence only; do not equate it with motion acceptance."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'character/marsh-current-family-audit-2026-10-03-post-cargo'
OLD=ROOT/'character/marsh-full-family-audit-2026-10-03'
read=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
current=read(OUT/'inventory.json');old=read(OLD/'inventory.json')
candidates={}
for p in OLD.glob('*review*.json'):
    for b in read(p).get('boards',[]):
        path=ROOT/b['board'];assert sha(path)==b['boardSha256']
        candidates.setdefault(b['family'],[]).append({'receipt':p.relative_to(ROOT).as_posix(),'board':b['board'],'sha256':b['boardSha256'],'states':b['sourceStates']})
for b in read(OLD/'scope-evidence.json')['visuallyReviewedBoardsThisTurn']:
    path=ROOT/b['path'];assert sha(path)==b['sha256']
    if path.name.endswith('-contact.png'):
        family=path.name.removesuffix('-contact.png')
        keys=next(x['keys'] for x in old['boards'] if x['family']==family)
        candidates.setdefault(family,[]).append({'receipt':(OLD/'scope-evidence.json').relative_to(ROOT).as_posix(),'board':b['path'],'sha256':b['sha256'],'states':{k:old['states'][k] for k in keys}})
early=ROOT/'character/marsh-selected-family-audit-2026-10-02/inventory.json'
for b in read(early)['boards']:
    if not b.get('visualReviewed'):continue
    e=read(early);path=early.parent/b['file'];assert sha(path)==b['sha256']
    candidates.setdefault(b['family'],[]).append({'receipt':early.relative_to(ROOT).as_posix(),'board':path.relative_to(ROOT).as_posix(),'sha256':b['sha256'],'states':{k:e['states'][k] for k in b['keys']}})
def signature(s):
    return ([f['sha256'] for f in s['frames']],s['durationsMs'],s['loop'],s['pivot'],s['standingHeight'])
reused=[];pending=[]
for board in current['boards']:
    family=board['family'];matches=[]
    for c in candidates.get(family,[]):
        if set(c['states'])!=set(board['keys']):continue
        if all(signature(c['states'][k])==signature(current['states'][k]) for k in board['keys']) and c['sha256']==board['sha256']:
            matches.append({k:v for k,v in c.items() if k!='states'})
    if matches:
        reused.append({'family':family,'board':board['file'],'sha256':board['sha256'],'evidence':matches,'scope':'Exact unchanged complete held-source board. No new continuous/native/contact acceptance.'})
    else:pending.append(family)
current['heldReviewReconciliation']={'reused':reused,'pendingFamilies':pending,'pendingCount':len(pending),'fullGoalComplete':False}
current['normalAdmission']=True
current['normalAdmissionScope']='Snapshot resolves only actual normal catalogue; inventory does not grant visual acceptance.'
(OUT/'inventory.json').write_text(json.dumps(current,indent=2)+'\n')
print(f'{len(reused)}complete held-family boards reuse exact evidence;{len(pending)}need current complete review')
print(', '.join(pending))
