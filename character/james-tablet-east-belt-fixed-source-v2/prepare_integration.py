from pathlib import Path
import json,os
P=Path(__file__).resolve().parent;R=P.parents[1]
grid=R/'scripts/grid_canvas.gd';data=grid.read_bytes()
needle=b'\t\t\tplayer.load_manifest("res://character/james-meal-service-south-open-v1/handoffs-manifest.json", true)'
addition=b'\t\t\tplayer.load_manifest("res://character/james-tablet-east-belt-fixed-source-v2/bare-manifest.json", true)\r\n\t\t\tif not player.load_equipment_manifest("diving-helmet", "res://character/james-tablet-east-belt-fixed-source-v2/helmet-manifest.json"):\r\n\t\t\t\tpush_error("James East separate-tablet helmet mismatch")\r\n'
if b'res://character/james-tablet-east-belt-fixed-source-v2/bare-manifest.json' not in data:
    assert data.count(needle)==1;grid.write_bytes(data.replace(needle,addition+needle))
registry=R/'character/ACTIVE_ASSETS.json';a=json.loads(registry.read_text(encoding='utf-8'));a['actionOverrides']['branforth-east-separate-tablet']='character/james-tablet-east-belt-fixed-source-v2/bare-manifest.json';a['actionOverrides']['branforth-east-separate-tablet-helmet']='character/james-tablet-east-belt-fixed-source-v2/helmet-manifest.json';registry.write_text(json.dumps(a,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
old=R/'character/james-inspect-material-continuity-v1'
s=(old/'validate.gd').read_text(encoding='utf-8').replace('james-inspect-material-continuity-v1','james-tablet-east-belt-fixed-source-v2')
s=s.replace('JAMES MATERIAL BOOT','JAMES EAST SEPARATE TABLET BOOT').replace('JAMES TABLET MATERIAL CONTINUITY:','JAMES EAST SEPARATE TABLET:')
s=s.replace('All selected inspection, diagnostic and sealed meal substitute source references through normal loader; clocks/pivots/density and inspection loop/life policy. Native route/gear journeys not exercised.','All new East inspection/interaction source references and sealed-meal compatibility substitutes through normal loader. All-direction inspection seams/clocks retained. Native route/gear journeys not exercised.')
(P/'validate.gd').write_text(s,encoding='utf-8')
s=(old/'native-arrival-continue.gd').read_text(encoding='utf-8').replace('james-inspect-material-continuity-v1','james-tablet-east-belt-fixed-source-v2').replace('All1130 dry tablet slots','All1146 selected dry tablet slots (new141 East source poses per mode)')
(P/'native-arrival-continue.gd').write_text(s,encoding='utf-8')
(P/'run_arrival_validation.py').write_text((old/'run_arrival_validation.py').read_text(encoding='utf-8'),encoding='utf-8')
sel=json.loads((P/'source-selection.json').read_text());sel.update(status='selected_native_validation_pending',productionInstalled=True,remaining=['Normal native source/clock/gear seam checks','Actual eight-direction/mode approaches and fresh-scene Continue','Native anatomical/occlusion review','Full James family consistency goal']);(P/'source-selection.json').write_text(json.dumps(sel,indent=2)+'\n',encoding='utf-8')
print('New East bare/helmet and six-slot sealed-meal source bindings installed before South pivot overrides; native fixtures prepared.')
