"""Resolve the current normal Veld manifest order; inventory is not visual acceptance."""
from pathlib import Path
import json,re,hashlib
R=Path(__file__).resolve().parents[3];P=Path(__file__).resolve().parent
grid=(R/'scripts/grid_canvas.gd').read_text(encoding='utf-8')
block=grid.split('if actor == "veld":',1)[1].split('elif actor == "branforth":',1)[0]
catalog_path=R/'character/dr-veld-v2/catalog.json'
catalog=json.loads(catalog_path.read_text(encoding='utf-8'))
bare=['character/dr-veld-v2/'+s for s in catalog['body']]
helmet=['character/dr-veld-v2/'+s for s in catalog['equipment']]
bare+=re.findall(r'player\.load_manifest\("res://([^"\n]+)"',block)
helmet+=re.findall(r'player\.load_equipment_manifest\("diving-helmet", "res://([^"\n]+)"',block)
bindings={};resolved={};missing=[];source_bindings={}
for gear,paths in [('bare',bare),('helmet',helmet)]:
    states={}
    for relative in paths:
        path=R/relative;raw=path.read_bytes();bindings[relative]=hashlib.sha256(raw).hexdigest()
        data=json.loads(raw)
        for state in data['states']:
            sources=[]
            for source in state['frameFiles']:
                target=R/source[6:] if source.startswith('res://') else path.parent/source
                target=target.resolve()
                if not target.is_file():missing.append(str(target))
                else:
                    key=target.relative_to(R).as_posix()
                    if key not in source_bindings:source_bindings[key]=hashlib.sha256(target.read_bytes()).hexdigest()
                sources.append(target.relative_to(R).as_posix())
            states[state['id']]={'manifest':relative,'slots':len(sources),'frameFiles':sources,'standingHeight':data.get('standingHeight',74),'pivot':data.get('pivot',[46,86]),'frameSize':data.get('frameSize'),'frameDurationsMs':state.get('frameDurationsMs'),'fps':state.get('fps',data.get('fps')),'loop':state.get('loop'),'profileScope':'source declared, not measured rendered height'}
    resolved[gear]=states
inventory={'scope':'Static current normal loader/catalog resolution, final override per state; no runtime dispatch/visual/master/save acceptance inferred','loader':{'bare':bare,'helmet':helmet},'bindings':bindings,'sourceBindings':source_bindings,'resolved':resolved,'missingSources':missing,'counts':{g:len(v) for g,v in resolved.items()},'unpairedIds':{g:sorted(set(resolved[g])-set(resolved['helmet' if g=='bare' else 'bare'])) for g in resolved}}
(P/'selected-library.json').write_text(json.dumps(inventory,indent=2)+'\n',encoding='utf-8')
rows=['# Veld selected library coverage snapshot','', 'October 3, 2026. Resolved from the actual loader and original catalog, including later overrides. This is an inventory, not an acceptance report.','', '| State | Bare source | Helmet source |','|---|---|---|']
for state in sorted(set(resolved['bare'])|set(resolved['helmet'])):
    cells=[]
    for gear in ['bare','helmet']:
        item=resolved[gear].get(state)
        cells.append((item['manifest']+' ('+str(item['slots'])+' slots)') if item else 'No selected state')
    rows.append('| '+state+' | '+' | '.join(cells)+' |')
rows+=['','Full original-master action/direction coverage, continuous contact/joins, ordinary integration and final cross-library polish remain open. This current inventory is not full visual acceptance.','']
(P/'SELECTED_COVERAGE.md').write_text('\n'.join(rows)+'\n',encoding='utf-8')
furniture={g:{s:v['manifest'] for s,v in states.items() if s.startswith(('sit-','read-seated-'))} for g,states in resolved.items()}
(P/'furniture-summary.json').write_text(json.dumps(furniture,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'selectedStates':inventory['counts'],'manifestCount':len(bindings),'uniqueSources':len(source_bindings),'missingSources':len(missing),'unpairedIds':inventory['unpairedIds'],'furnitureStates':{g:len(v) for g,v in furniture.items()}}))
