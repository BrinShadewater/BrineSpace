from pathlib import Path
import json,shutil
P=Path(__file__).resolve().parent;R=P.parents[1];file=R/'scripts/grid_canvas.gd';data=file.read_bytes()
needle=b'\t\t\tplayer.load_manifest("res://character/james-water-north-polish-v1/bare-manifest.json", true)'
extra=b'\t\t\tplayer.load_manifest("res://character/james-sleep-cadence-v1/bare-manifest.json", true)\r\n\t\t\tif not player.load_equipment_manifest("diving-helmet", "res://character/james-sleep-cadence-v1/helmet-manifest.json"):\r\n\t\t\t\tpush_error("James sleep cadence shared helmet mismatch")\r\n'
if b'res://character/james-sleep-cadence-v1/bare-manifest.json' not in data:
    assert data.count(needle)==1;file.write_bytes(data.replace(needle,extra+needle))
file=R/'character/ACTIVE_ASSETS.json';m=json.loads(file.read_text());m['actionOverrides']['branforth-sleep-cadence']='character/james-sleep-cadence-v1/bare-manifest.json';m['actionOverrides']['branforth-sleep-cadence-helmet']='character/james-sleep-cadence-v1/helmet-manifest.json';file.write_text(json.dumps(m,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
shutil.copy2(R/'character/james-north-rest-polish-v1/no-layout-overrides.json',P/'no-layout-overrides.json')
(P/'selection.json').write_text(json.dumps({'status':'installed_native_review_pending','runtimeInstalled':True,'fullSetComplete':False,'change':'Visual sleep cycle only960ms to3600ms, all eight selected states; no art/simulation changes.'},indent=2)+'\n',encoding='utf-8')
print('Shared sleep visual clock installed after selected North rest; native validation pending.')
