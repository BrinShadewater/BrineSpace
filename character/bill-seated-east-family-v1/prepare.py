from pathlib import Path
import json
P=Path(__file__).resolve().parent
ROOT=P.parent.parent
source=P.parent/'bill-seated-north-family-v1'
for name in ['build.py','verify.py']:
    text=(source/name).read_text().replace('north','east').replace('bill-seated-idle-east-v1','bill-seated-loops-east-v1')
    if name=='build.py':
        text=text.replace(", (P.parent/'bill-reading-east-v1',gear+'-manifest.json')",'')
        text=text.replace(",(P.parent/'bill-reading-east-v1',gear+'-manifest.json')",'')
    (P/name).write_text(text)
registry=ROOT/'character/ACTIVE_ASSETS.json'
data=json.loads(registry.read_text())
for section,gear in [('actionOverrides','bare'),('equipmentOverrides','helmet')]:
    data[section]['bill-east-sitting-family']=f'character/bill-seated-east-family-v1/{gear}-manifest.json'
registry.write_text(json.dumps(data,indent=2)+'\n')
runner=(ROOT/'tools/run_bill_reading_entry_east_candidate_validation.py').read_text()
runner=runner.replace('bill-reading-entry-east-candidate-native-v1','bill-seated-east-selected-renderer-v1').replace('test_bill_reading_entry_east_candidates','test_bill_seated_east_selected_renderer').replace('BILL READING ENTRY','BILL EAST SELECTED')
(ROOT/'tools/run_bill_seated_east_selected_renderer_validation.py').write_text(runner)
print('Prepared east selected family tools and registry')
