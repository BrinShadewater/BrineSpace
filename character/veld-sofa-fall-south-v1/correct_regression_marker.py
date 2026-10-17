"""Correct report parsing using the unchanged terminal native evidence."""
from pathlib import Path
import json,hashlib,shutil
R=Path(__file__).resolve().parents[2];O=R/'output/veld-sofa-fall-south-regressions-v1';p=O/'validation.json'
old=json.loads(p.read_text());backup=O/'validation-before-marker-correction.json'
if not backup.exists():shutil.copy2(p,backup)
name='test_veld_lounge_partial_fall_north_native.gd';log=O/(name+'.log');text=log.read_text(encoding='utf-8')
record=next(v for v in old['results'] if v['test']==name)
assert record['returnCode']==0 and record['logSha256']==hashlib.sha256(log.read_bytes()).hexdigest()
assert 'VELD PARTIAL LOUNGE NORTH FALL: 23589 checks,0 failures;8 fresh disk restores' in text and not any(v in text for v in ['ERROR:','SCRIPT ERROR','Artwork unavailable:'])
record['passed']=True
old['passed']=all(v['passed'] for v in old['results']) and not old['realProfileChanges'] and not old['frozenInputChanges']
old['markerCorrection']={'test':name,'previous':'VELD PARTIAL LOUNGE FALL NATIVE','corrected':'VELD PARTIAL LOUNGE NORTH FALL','nativeRerun':False,'evidence':'original engine0 clean native log/hash and actual test success line'}
p.write_text(json.dumps(old,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'northNativePassed':record['passed'],'aggregatePassed':old['passed'],'nativeRerun':False,'oldBunkFailureRetained':True}))
