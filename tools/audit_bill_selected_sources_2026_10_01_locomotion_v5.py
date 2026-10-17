"""Current Bill loader source inventory; no artwork or reachability acceptance."""
from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parent.parent;O=R/'character/bill-selected-source-audit-2026-10-01-locomotion-v5'
source=(R/'scripts/grid_canvas.gd').read_text(encoding='utf-8');block=source.split('func _load_major_bill_animations() -> void:',1)[1].split('\nfunc ',1)[0]
catalog=json.loads((R/'character/major-bill-v3/catalog.json').read_text());states={'bare':{},'helmet':{}};orders={'bare':[],'helmet':[]};hashes={}
def add(gear,path):
    m=json.loads(path.read_text(encoding='utf-8'));relative=path.relative_to(R).as_posix();orders[gear].append(relative);hashes[relative]=hashlib.sha256(path.read_bytes()).hexdigest()
    for s in m['states']:
        files=['res://'+(path.parent/f).relative_to(R).as_posix() if not f.startswith('res://') else f for f in s['frameFiles']]
        states[gear][s['id']]={'manifest':relative,'sourceFiles':files,'frames':len(files),'standingHeight':m.get('standingHeight'),'pivot':m.get('pivot'),'loop':s.get('loop',True),'manifestStatus':m.get('status'),'fromOriginalCatalog':relative.startswith('character/major-bill-v3/')}
for gear,field in [('bare','body'),('helmet','equipment')]:
    for path in catalog[field]:add(gear,R/'character/major-bill-v3'/path)
for match in re.finditer(r'player\.(load_manifest|load_equipment_manifest)\((?:"diving-helmet",\s*)?"res://([^\"]+)"',block):add('bare' if match[1]=='load_manifest' else 'helmet',R/match[2])
retained={g:[k for k,s in v.items() if s['fromOriginalCatalog']] for g,v in states.items()}
report={'scope':'literal normal Bill loader + original catalog, last manifest wins; not live reachability, art acceptance or full-set completion','loaderBlockSha256':hashlib.sha256(block.encode()).hexdigest(),'manifestSha256':hashes,'loadOrder':orders,'selectedStateSources':states,'retainedOriginalCatalogKeys':retained,'runtimeExceptions':['equipped life_eat/life_drink use inspection, so retained helmet eat/drink rows are not active sealed-mouth meal presentation','specialized accepted east bunk remains a separate original-catalog family','derived renderer/controller behavior must be audited through native execution'],'fullGoalComplete':False}
O.mkdir(exist_ok=True);assert not (O/'source-inventory.json').exists(),'Keep dated evidence; write another revision'
(O/'source-inventory.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
lines=['# Bill current selected sources — October 1, 2026','','Source inventory only. Selection/source age does not establish visual fidelity or runtime reachability.','']
for gear in states:
    lines.extend([f'## {gear}: {len(states[gear])} manifest-selected keys','',f'Retained original catalog keys: {", ".join(retained[gear]) or "none"}.',''])
lines.extend(['## Remaining acceptance','','- Fine identity, materials, anatomy, size/proportions and perspective across all selected clips.','- Motion joins and cadence, including rest lowering/recline and meal wrist/object contact.','- Wider whole-station routes/interruptions and resumed/fresh checkpoint behavior where still unproven.','- Generic rest furniture requires actual compatible station data; current Bill berth uses specialized east bunk.','- Owner visual acceptance remains separate from engine/package checks.'])
(O/'SOURCE_HANDOFF.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps({g:{'selectedKeys':len(states[g]),'originalCatalogKeys':retained[g]} for g in states}))
