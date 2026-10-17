from pathlib import Path
import copy,json,hashlib,shutil
P=Path(__file__).resolve().parent;R=P.parent.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
records=[];manifests=[]
actions = {'bare': ['krusher-tablet-east-v1','krusher-tablet-south-v1','krusher-tablet-west-v1','krusher-tablet-north-v2'], 'helmet': ['krusher-tablet-east-helmet-v1','krusher-tablet-south-helmet-v1','krusher-tablet-west-helmet-v1','krusher-tablet-north-helmet-v1']}
for gear in ['bare','helmet']:
    base=R/'character/krusher-james-canonical-v1'/f'{gear}-manifest.json'
    sources=[base]+[R/'character'/action/f'{gear}-manifest.json' for action in actions[gear]]
    m=json.loads(base.read_text())
    for source in sources[1:]:m['states']+=json.loads(source.read_text())['states']
    m['name']='Krusher Dom / selected James utility suit'
    m['status']='Selected base with four-direction tablet candidates; no normal selection'
    for source in sources:
        manifests.append({'source':source.relative_to(R).as_posix(),'sha256':sha(source)})
        source_m=json.loads(source.read_text())
        for original in source_m['states']:
            state=next(s for s in m['states'] if s['id']==original['id'])
            files=[]
            for i,relative in enumerate(original['frameFiles']):
                src=(source.parent/relative).resolve();target=f'frames/{gear}/{state["id"]}/{i:03}.png'
                dst=P/target;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst);files.append(target)
                records.append({'file':target,'source':src.relative_to(R).as_posix(),'sha256':sha(src)})
            state['frameFiles']=files
    (P/f'{gear}-manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
(P/'provenance.json').write_text(json.dumps({'identity':m['identity'],'sources':manifests,'frames':records,'scope':'Selected James locomotion plus paired East/South/West/North tablet candidates; source bytes, clocks and registration retained; game selectors unchanged'},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'frames':len(records),'statesPerGear':len(m['states'])}))
