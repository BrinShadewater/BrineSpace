from pathlib import Path
import copy,hashlib,json,shutil
P=Path(__file__).resolve().parent;R=P.parent.parent
MOVE=P.parent/'krusher-moving-equipment-test-v2';ACTION=P.parent/'krusher-terminal-gear-pair-v1'
P.mkdir(exist_ok=True);records=[];input_hashes={};sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for gear in ['bare','helmet']:
    mp=MOVE/f'{gear}-manifest.json';ap=ACTION/f'{gear}-manifest.json'
    for path in [mp,ap]:input_hashes[path.relative_to(R).as_posix()]=sha(path)
    m=json.loads(mp.read_text());a=json.loads(ap.read_text());out=copy.deepcopy(m)
    out.update({'name':'Krusher Dom','characterId':'krusher-dom','title':'System Administrator','department':'AI & Robotics','accentTarget':'#527C80','version':'runtime-candidate-v1','status':'unselected candidate; technical source and native timing evidence retained; artistic motion review pending','baseFamily':'Bill','equipmentVariant':gear})
    out['states']=[]
    for root,manifest in [(MOVE,m),(ACTION,a)]:
        for state in manifest['states']:
            copied=copy.deepcopy(state);paths=[]
            for path in state['frameFiles']:
                source=root/path;dest_path=path
                if root==ACTION:
                    dest_path=f'frames/{gear}/terminal/{Path(path).name}'
                    if Path(path).name=='idle.png':
                        dest_path=f'frames/{gear}/idle-west/000.png'
                        assert source.read_bytes()==(MOVE/dest_path).read_bytes(),'idle alias differs'
                dest=P/dest_path;dest.parent.mkdir(parents=True,exist_ok=True)
                digest=sha(source);input_hashes[source.relative_to(R).as_posix()]=digest
                if dest.exists() and sha(dest)!=digest:raise RuntimeError('Conflicting package path: '+dest_path)
                if not dest.exists():shutil.copyfile(source,dest)
                paths.append(dest_path);records.append({'gear':gear,'state':state['id'],'source':source.relative_to(R).as_posix(),'output':dest_path,'sha256':digest})
            copied['frameFiles']=paths;out['states'].append(copied)
    out['actionMeaning']=a['actionMeaning'];out['transitions']=a['transitions'];out['limitations']=['Terminal action is west-only','No authored expressions or turning inbetweens','No normal game selection or station/controller integration','Other crew base families require independent compatibility review']
    (P/f'{gear}-manifest.json').write_text(json.dumps(out,indent=2)+'\n')
report={'method':'Byte-preserving consolidation of existing candidate packages; terminal idle aliases the locomotion master. No generation, scaling or recolouring.','sourceHashes':input_hashes,'records':records,'uniqueOutputs':len(set(r['output'] for r in records)),'frameReferences':len(records)}
(P/'provenance.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['uniqueOutputs','frameReferences']}))
