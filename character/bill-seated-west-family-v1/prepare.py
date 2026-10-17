from pathlib import Path
import json
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
E=P.parent/'bill-seated-east-family-v1'
for name in ['build.py','verify.py','build_review.py']:
    (P/name).write_text((E/name).read_text().replace('east','west'))
registry=ROOT/'character/ACTIVE_ASSETS.json';data=json.loads(registry.read_text())
for section,gear in [('actionOverrides','bare'),('equipmentOverrides','helmet')]:
    data[section]['bill-west-sitting-family']=f'character/bill-seated-west-family-v1/{gear}-manifest.json'
registry.write_text(json.dumps(data,indent=2)+'\n')
test=(ROOT/'tests/test_bill_seated_east_selected_renderer.gd').read_text().replace('east','west').replace('EAST','WEST')
(ROOT/'tests/test_bill_seated_west_selected_renderer.gd').write_text(test)
(ROOT/'tests/test_bill_seated_west_selected_renderer.gd.uid').write_text('uid://a7b8w3m6p2r9v\n')
runner=(ROOT/'tools/run_bill_seated_east_selected_renderer_validation.py').read_text().replace('east','west').replace('EAST','WEST')
(ROOT/'tools/run_bill_seated_west_selected_renderer_validation.py').write_text(runner)
print('Prepared west seated family and normal selection fixture')
