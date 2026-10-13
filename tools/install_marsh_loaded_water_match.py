"""Install the matching loaded frames, preserving every runtime manifest byte."""
from pathlib import Path
import json,hashlib,shutil
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-loaded-water-match-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def install(backup=False):
    contract=json.loads((BASE/'contract.json').read_text());records={};targets={};manifests=set()
    for state,info in contract['states'].items():
        manifests.add(info['manifest'])
        indices=[5] if state.startswith('swim-pickup-') else [0] if state.startswith('cargo-drain-') else range(len(info['files']))
        for i in indices:targets[(ROOT/info['files'][i]).resolve()]=BASE/f'frames/{state}/{i:03}.png'
    if backup:
        baseline=json.loads((ROOT/'character/palette-standard-v1/mapping.json').read_text())['files'];changes=json.loads((ROOT/'character/veld-consistency-v1/mapping.json').read_text());
        for pack in ('marsh-carry-chain-v1','marsh-cargo-drain-match-v1','marsh-swim-pickup-match-v1','marsh-salvage-match-v1'):
            lock=ROOT/'character'/pack/'colour-lock.json'
            if lock.exists():changes.update(json.loads(lock.read_text()))
        for target,source in targets.items():
            rel=target.relative_to(ROOT).as_posix();assert sha(target)==changes.get(rel,{}).get('after',baseline[rel]['sha256']),rel;assert source.exists() and not (BASE/'installation-backup'/rel).exists(),rel
        for rel in manifests:
            saved=BASE/'installation-backup'/rel;saved.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/rel,saved)
    for target,source in targets.items():
        rel=target.relative_to(ROOT).as_posix();before=sha(target)
        if backup:
            saved=BASE/'installation-backup'/rel;saved.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(target,saved)
        shutil.copy2(source,target);records[rel]={'before':before,'after':sha(target),'source':source.relative_to(ROOT).as_posix(),'reason':'Matched fitted swimming turn identity and exact loop joins'}
    if backup:
        (BASE/'colour-lock.json').write_text(json.dumps(records,indent=2)+'\n');(BASE/'installation.json').write_text(json.dumps({'frameCount':len(records),'newSourcePoses':28,'frames':records},indent=2)+'\n')
    return records
if __name__=='__main__':print('Installed',len(install(backup=True)),'loaded loop/turn/boundary frames')
