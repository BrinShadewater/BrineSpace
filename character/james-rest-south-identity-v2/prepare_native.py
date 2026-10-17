from pathlib import Path
import json,uuid,os
P=Path(__file__).resolve().parent;R=P.parents[1]
v=json.loads((P/'packaging-validation.json').read_text());assert not v['failures']
grid=R/'scripts/grid_canvas.gd';data=grid.read_bytes()
needle=b'\t\t\tplayer.load_manifest("res://character/james-water-north-polish-v1/bare-manifest.json", true)'
addition=b'\t\t\tplayer.load_manifest("res://character/james-rest-south-identity-v2/bare-manifest.json", true)\r\n\t\t\tif not player.load_equipment_manifest("diving-helmet", "res://character/james-rest-south-identity-v2/helmet-manifest.json"):\r\n\t\t\t\tpush_error("James South rest identity helmet mismatch")\r\n'
if b'res://character/james-rest-south-identity-v2/bare-manifest.json' not in data:
    assert data.count(needle)==1
    temp=grid.with_name(grid.name+'.'+uuid.uuid4().hex+'.tmp');temp.write_bytes(data.replace(needle,addition+needle));os.replace(temp,grid)
file=R/'character/ACTIVE_ASSETS.json';m=json.loads(file.read_text());m['actionOverrides']['branforth-south-rest-identity']='character/james-rest-south-identity-v2/bare-manifest.json';m['actionOverrides']['branforth-south-rest-identity-helmet']='character/james-rest-south-identity-v2/helmet-manifest.json';file.write_text(json.dumps(m,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
(P/'selection.json').write_text(json.dumps({'status':'installed_native_validation_pending','runtimeInstalled':True,'sourceVersion':'source-v2.png plus template-v8 chest interiors','sourceReferences':36,'fullSetComplete':False,'rejected':'candidate-v2-review.json','packageChecks':v['checks'],'nativeScope':'Normal loader and every source pose via prescribed South life stages in NPC renderer. Ordinary retained berths select North; specialized East bunk is separate. No actual South ordinary berth route claim.'},indent=2)+'\n')
print('South paired override installed after ordinary rest material; other facings retained.')
