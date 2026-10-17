from pathlib import Path
import json,copy,hashlib
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];bindings={};checks=[]
for gear in ['bare','helmet']:
    root=None;states=[]
    for direction in ['east','south','west','north']:
        folder=P.parent/f'bill-rest-{"helmet-" if gear=="helmet" else ""}{direction}-coherent-v1'
        m=json.loads((folder/'manifest.json').read_text());root=root or copy.deepcopy(m)
        assert [m[k] for k in ['frameWidth','frameHeight','pivot','standingHeight','precomposed','textureFilter']]==[256,256,[128,224],148,True,'linear']
        assert len(m['states'])==3
        for state in m['states']:
            s=copy.deepcopy(state)
            if direction=='east' and 'restHeadOffset' in s:
                s['restHeadOffset'][1]=round(s['restHeadOffset'][1]+384*.038,4)
                s['headAnchorCorrection']='includes the normal Bill room draw lift14.592'
            states.append(s)
            for file in s['frameFiles']:
                assert file.startswith('res://') and (R/file[6:]).is_file()
                bindings[file]=hashlib.sha256((R/file[6:]).read_bytes()).hexdigest()
        entry,wake,sleep=states[-3:]
        assert entry['frameFiles'][::-1]==wake['frameFiles'] and entry['frameDurationsMs'][::-1]==wake['frameDurationsMs']
        assert sum(entry['frameDurationsMs'])==sum(wake['frameDurationsMs'])==800 and sum(sleep['frameDurationsMs'])==1200
        assert entry['frameFiles'][-1]==sleep['frameFiles'][0]==wake['frameFiles'][0]
        checks.append(gear+' '+direction+' endpoints/timing/density/literal paths')
    root.update(name='Bill cardinal generic rest '+gear+' family',states=states,status='selected_runtime',scope='generic rest; specialised east bunk remains separate; physical generic bed contexts pending')
    (P/('manifest.json' if gear=='bare' else 'helmet-manifest.json')).write_text(json.dumps(root,indent=2)+'\n',encoding='utf-8')
bare=json.loads((P/'manifest.json').read_text());gear=json.loads((P/'helmet-manifest.json').read_text())
assert [s.get('restHeadOffset') for s in bare['states']]==[s.get('restHeadOffset') for s in gear['states']]
(P/'verification.json').write_text(json.dumps({'passed':True,'checks':checks,'states':24,'uniquePNG':len(bindings),'frameReferences':sum(len(s['frameFiles']) for m in [bare,gear] for s in m['states']),'sha256':bindings,'scope':'unchanged authored PNGs; paired clocks/density and corrected east head-anchor metadata; visual/physical proof separate'},indent=2)+'\n',encoding='utf-8')
board=Image.new('RGB',(2048,2048),(34,52,62))
for d in range(4):
    for g,m in enumerate([bare,gear]):
        for i,f in enumerate(m['states'][d*3]['frameFiles']):
            im=Image.open(R/f[6:]);board.paste(im,(i*256,(d*2+g)*256),im)
board.save(P/'cardinal-review.png')
html=(P.parent/'bill-rest-west-coherent-v1/index.html').read_text(encoding='utf-8')
html=html.replace('Bill west rest candidate','Bill cardinal rest family').replace('Bill · West rest','Bill · Cardinal rest family').replace('Bare candidate. Exact selected idle, eight authored lowering poses, reversed rise, relaxed sleep. Compare with the idle beneath each action. Equipment, compatible furniture and normal runtime selection remain pending. Current habitation uses the selected east bunk.','Paired normal-loader family. Compare each action with its selected idle. Specialised east bunk remains separate; live motion polish and generic furniture contacts remain pending.')
html=html.replace("const m=await (await fetch('manifest.json')).json();","const equipment=new URLSearchParams(location.search).get('gear')==='helmet'; const m=await (await fetch(equipment?'helmet-manifest.json':'manifest.json')).json();")
html=html.replace("const master=new Image();master.src='../bill-seated-west-coherent-v1/frames/sit-down-west/000.png';await master.decode();",'')
html=html.replace('for(const s of m.states){const el=',"for(const s of m.states){const direction=s.id.split('-').at(-1);const master=new Image();master.src=`../bill-seated-${equipment?'helmet-':''}${direction}-coherent-v1/frames/sit-down-${direction}/000.png`;await master.decode();const el=")
(P/'index.html').write_text(html,encoding='utf-8')
print('Built24 paired rest states/144 references/64 unchanged PNGs; corrected east anchor')
