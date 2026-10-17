"""Register selected Veld basic water packs and conservatively expand their envelopes."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
H=Path(__file__).resolve().parent;R=H.parents[1];revision=H/'revisions/installed-basic-water-v1';revision.mkdir(parents=True,exist_ok=True)
registry=R/'character/ACTIVE_ASSETS.json';clearance=R/'character/dr-veld-v2/clearance.json'
for path in [registry,clearance]:
    saved=revision/path.name
    if not saved.exists():saved.write_bytes(path.read_bytes())
selection=json.loads((H/'candidate-selection.json').read_text());assets=json.loads(registry.read_text());bounds=json.loads(clearance.read_text());old=json.loads(json.dumps(bounds));measurements=[]
for entry in selection['manifests']:
    path=R/entry['path'];manifest=json.loads(path.read_text());variant=entry['variant'];direction=manifest['states'][0]['id'].split('-')[-1]
    key='veld-water-'+direction;assets['actionOverrides' if variant=='bare' else 'equipmentActionOverrides'][key]=entry['path']
    binding={'script':'scripts/grid_canvas.gd','contains':'res://'+entry['path']}
    if binding not in assets['bindings']:assets['bindings'].append(binding)
    scale=384*.17/manifest['standingHeight'];pivot=np.array(manifest['pivot'])
    for state in manifest['states']:
        boxes=[]
        for file in state['frameFiles']:
            image=Image.open(path.parent/file).convert('RGBA');a=np.array(image);y,x=np.where(a[:,:,3]>20);box=np.array([x.min(),y.min(),x.max()+1,y.max()+1],float)
            boxes.append((box-np.tile(pivot,2))*scale)
        boxes=np.array(boxes);extent=[float(boxes[:,0].min()),float(boxes[:,1].min()),float(boxes[:,2].max()),float(boxes[:,3].max())]
        key=state['id'];kind='tread' if key.startswith('tread-') else 'swim' if key.startswith('swim-') and not key.startswith(('swim-start-','swim-stop-')) else 'actions';slot='transition-'+direction if kind=='actions' else direction
        current=bounds[kind][variant][slot];bounds[kind][variant][slot]=[min(current[i],extent[i]) if i<2 else max(current[i],extent[i]) for i in range(4)]
        measurements.append({'variant':variant,'state':key,'nativeUnion':extent,'scale':scale,'clearanceSlot':kind+'/'+variant+'/'+slot})
for kind in old:
    for variant,states in old[kind].items():
        for key,extent in states.items():
            affected=kind in ['swim','tread'] or (kind=='actions' and key.startswith('transition-'))
            if not affected:assert bounds[kind][variant][key]==extent
            else:assert all(bounds[kind][variant][key][i]<=extent[i] if i<2 else bounds[kind][variant][key][i]>=extent[i] for i in range(4))
registry.write_text(json.dumps(assets,indent=2)+'\n');clearance.write_text(json.dumps(bounds,indent=2)+'\n')
selection['status']='installed_basic_water_pending_full_motion_world_and_owner_acceptance';selection['installedGate']='character/veld-water-material-v2/native-installed-basic-v1-checks.json'
(H/'candidate-selection.json').write_text(json.dumps(selection,indent=2)+'\n')
(H/'installed-clearance-v1.json').write_text(json.dumps({'scope':'32 selected basic states, alpha>20 unions in NPC384-cell world units; old safe bounds and retained other actions/life preserved','measurements':measurements,'clearanceSha256':hashlib.sha256(clearance.read_bytes()).hexdigest()},indent=2)+'\n')
print('8 literal registry bindings installed;32 measured state envelopes; retained other clearance entries unchanged.')
