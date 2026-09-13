"""Derive runtime clearance and locker events from complete rebuilt crew catalogs."""
from pathlib import Path
import argparse,copy,json
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
REVISIONS={'veld':'dr-veld-v2','branforth':'chief-engineer-branforth-v2','marsh':'marsh-v2'}
def read(path):return json.loads(path.read_text())
def union(a,b):return [min(a[i],b[i]) if i<2 else max(a[i],b[i]) for i in range(4)]
def finalize(actor):
    root=ROOT/'character'/REVISIONS[actor];catalog=read(root/'catalog.json'); extents={'bare':{},'helmet':{}}
    for variant,group in [('bare','body'),('helmet','equipment')]:
        for rel in catalog[group]:
            path=root/rel;pack=read(path);pivot=pack['pivot'];factor=65.28/pack['standingHeight']
            for state in pack['states']:
                boxes=[]
                for file in state['frameFiles']:
                    with Image.open(path.parent/file) as image: boxes.append(image.getbbox())
                bounds=[min(b[0] for b in boxes),min(b[1] for b in boxes),max(b[2] for b in boxes),max(b[3] for b in boxes)]
                extents[variant][state['id']]=[(v-pivot[i%2])*factor for i,v in enumerate(bounds)]
                if actor!='marsh' and variant=='bare' and state['id'] in ['equip-helmet-east','remove-helmet-east']:
                    original=read(ROOT/'character/crew-underwater-v1/locker'/(actor+'-'+state['id'])/'manifest.json')['states'][0]
                    entry=copy.deepcopy(state);entry['events']=original.get('events',[])
                    folder=root/'locker'/state['id'];folder.mkdir(parents=True,exist_ok=True)
                    (folder/'manifest.json').write_text(json.dumps({**pack,'states':[entry]},indent=2)+'\n')
    if actor=='marsh':
        result=read(ROOT/'character/animation-expansion-v5/marsh/clearance.json')
        for mode,by_direction in result.items():
            for direction,old in by_direction.items():
                for key,bounds in extents['bare'].items():
                    if key.endswith('-'+direction): old=union(old,bounds)
                by_direction[direction]=old
    else:
        result={}
        for kind,source in [('actions','crew-actions-v1'),('life','crew-life-v1')]:
            result[kind]=read(ROOT/'character'/source/'clearance.json')[actor]
            for variant,states in result[kind].items():
                for key,old in states.items():
                    facing=key.split('-')[-1]
                    candidates=[key] if key in extents[variant] else [k for k in extents[variant] if (k.startswith(('swim-start-','swim-stop-','swim-turn-')) if key.startswith('transition-') else 'carry-turn-' in k) and facing in k.split('-')]
                    if not candidates: raise ValueError('Missing clearance family: '+key)
                    for candidate in candidates: old=union(old,extents[variant][candidate])
                    states[key]=old
        water=read(ROOT/'character/crew-underwater-v1/swim-clearance.json')
        for kind,source in [('swim','actors'),('tread','treading')]:
            result[kind]=water[source][actor]
            for variant,states in result[kind].items():
                for direction,old in states.items():states[direction]=union(old,extents[variant][kind+'-'+direction])
    (root/'clearance.json').write_text(json.dumps(result,indent=2)+'\n')
    return {'actor':actor,'bodyStates':len(extents['bare']),'equipmentStates':len(extents['helmet'])}
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('actor',choices=REVISIONS);args=parser.parse_args()
    print(json.dumps(finalize(args.actor)))
