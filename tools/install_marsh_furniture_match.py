"""Install explicit furniture sources with immutable backups and hash records."""
from pathlib import Path
import json,hashlib,shutil
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-furniture-match-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def install(kind=None,backup=False):
    contract=json.loads((BASE/'contract.json').read_text());targets={}
    for k,v in contract.items():
        if kind and k!=kind:continue
        for i in range(v['count']):targets[ROOT/v['runtime']/f'{i:03}.png']=BASE/'frames'/k/f'{i:03}.png'
    if backup:
        baseline=json.loads((ROOT/'character/palette-standard-v1/mapping.json').read_text())['files'];changes=json.loads((ROOT/'character/veld-consistency-v1/mapping.json').read_text())
        for target,source in targets.items():
            rel=target.relative_to(ROOT).as_posix();assert sha(target)==changes.get(rel,{}).get('after',baseline[rel]['sha256']),rel
            assert source.exists() and not (BASE/'installation-backup'/rel).exists(),rel
        for v in contract.values():
            target=ROOT/v['runtime']/'manifest.json';saved=BASE/'installation-backup'/target.relative_to(ROOT);saved.parent.mkdir(parents=True,exist_ok=True);assert not saved.exists();shutil.copy2(target,saved)
    records={}
    for target,source in targets.items():
        rel=target.relative_to(ROOT).as_posix();before=sha(target)
        if backup:
            saved=BASE/'installation-backup'/rel;saved.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(target,saved)
        shutil.copy2(source,target);records[rel]={'before':before,'after':sha(target),'source':source.relative_to(ROOT).as_posix(),'reason':'Marsh fitted identity through existing furniture choreography'}
    if backup:
        (BASE/'colour-lock.json').write_text(json.dumps(records,indent=2)+'\n');(BASE/'installation.json').write_text(json.dumps({'uniqueFrames':13,'newlyAuthoredInteriorPoses':11,'preservedManifest':True,'frames':records},indent=2)+'\n')
    return records
if __name__=='__main__':print('Installed',len(install(backup=True)),'unique furniture frames')
