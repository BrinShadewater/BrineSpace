from pathlib import Path
import json
R=Path(__file__).resolve().parents[2]
p=R/'output/bill-floor-case-flood-route-probe-v1/validation.json'
data=json.loads(p.read_text());data.pop('capturePassed',None);data['mode']='headless-controller-probe';data['nativeScreenshot']=False;p.write_text(json.dumps(data,indent=2)+'\n')
p=R/'tools/run_bill_floor_case_flood_route_probe_v1_validation.py';s=p.read_text().replace("'capturePassed':capture_passed,", "'mode':'headless-controller-probe',").replace("'nativeScreenshot':fresh_photo", "'nativeScreenshot':False");p.write_text(s)
print('Headless probe report now explicitly records no native screenshot.')
