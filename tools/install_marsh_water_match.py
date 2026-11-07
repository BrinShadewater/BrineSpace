"""Install matched swim/start/stop clips plus exact shared turn endpoints."""
from pathlib import Path
import json,hashlib,shutil
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-water-match-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def install(backup=False):
    contract=json.loads((BASE/'contract.json').read_text());targets={};manifests=set()
    for state,info in contract['states'].items():
        indices=(0,len(info['files'])-1) if state.startswith('swim-turn-') else range(len(info['files']))
        for i in indices:
            target=(ROOT/info['files'][i]).resolve();source=BASE/'frames'/state/f'{i:03}.png';targets[target]=source
        manifests.add(info['manifest'])
    if backup:
        baseline=json.loads((ROOT/'character/palette-standard-v1/mapping.json').read_text())['files'];changes=json.loads((ROOT/'character/veld-consistency-v1/mapping.json').read_text())
        for target,source in targets.items():
            rel=target.relative_to(ROOT).as_posix();assert sha(target)==changes.get(rel,{}).get('after',baseline[rel]['sha256']),rel
            assert source.exists() and not (BASE/'installation-backup'/rel).exists(),rel
        for rel in manifests:
            saved=BASE/'installation-backup'/rel;saved.parent.mkdir(parents=True,exist_ok=True);assert not saved.exists();shutil.copy2(ROOT/rel,saved)
    records={}
    for target,source in targets.items():
        rel=target.relative_to(ROOT).as_posix();before=sha(target)
        if backup:
            saved=BASE/'installation-backup'/rel;saved.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(target,saved)
        shutil.copy2(source,target);records[rel]={'before':before,'after':sha(target),'source':source.relative_to(ROOT).as_posix(),'reason':'Marsh fitted water-motion identity with shared endpoints'}
    if backup:
        (BASE/'colour-lock.json').write_text(json.dumps(records,indent=2)+'\n');(BASE/'installation.json').write_text(json.dumps({'frameCount':len(records),'newSourcePoses':44,'preservedManifest':True,'historicalTurnInteriorsRemain':True,'frames':records},indent=2)+'\n')
    return records
if __name__=='__main__':print('Installed',len(install(backup=True)),'water-motion frames/endpoints')
