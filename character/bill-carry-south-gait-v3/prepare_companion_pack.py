"""Derive deterministic paired entry/export guards from the established North pack."""
from pathlib import Path
import shutil,json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];E=R/'character/bill-carry-start-south-v2'
(E/'sources').mkdir(parents=True,exist_ok=True)
for name in ['first-step-v1.png','prompt-first-step-v1.txt']:
 shutil.copy2(R/'character/bill-carry-start-south-v1/sources'/name,E/'sources'/name)
s=(R/'character/bill-carry-start-north-v2/build.py').read_text(encoding='utf-8')
s=s.replace('bill-carry-north-gait-v2','bill-carry-south-gait-v3').replace('north','south').replace('North','South').replace('164','168').replace('149/height','144/height')
s=s.replace("[('early-start-v2.png',[0,1]),('low-step-v4.png',[2])]","[('first-step-v1.png',[0,1,2])]").replace('count=4','count=5')
s=s.replace("reg={'calibration':cal", "reg={'actualMasterRuler':144,'reusedAuthoringSource':'character/bill-carry-start-south-v1/sources/first-step-v1.png','calibration':cal")
(E/'build.py').write_text(s,encoding='utf-8')
for source,target in [('bill-carry-north-gait-v2',P),('bill-carry-start-north-v2',E)]:
 s=(R/'character'/source/'verify.py').read_text(encoding='utf-8')
 s=s.replace('bill-carry-start-north-v2','bill-carry-start-south-v2').replace('bill-carry-north-gait-v2','bill-carry-south-gait-v3').replace('north','south').replace('NORTH','SOUTH').replace('164','168')
 if source=='bill-carry-north-gait-v2':
  s=s.replace('protected=Y<168;rows={}',"protected=Y<168;rows={}\ncheck(reg['actualMasterRuler']==144,'Actual South opaque ruler, distinct from nominal148')")
 else:
  s=s.replace("'No cropping/height drift above upper')","'No cropping/height drift above upper')\n  check(y.max()==222,'Master floor register, including bridge interiors')")
 (target/'verify.py').write_text(s,encoding='utf-8')
provenance=[]
for name,prompt,outcome in [('first-half-v1.png','prompt-first-v1.txt','Use0,1,2; compact first half'),('opposite-rejected-v1.png','prompt-opposite-v1.txt','Rejected wrong leading leg; no extracted poses'),('opposite-rejected-v2.png','prompt-opposite-corrected-v2.txt','Rejected wrong first two legs; no extracted poses'),('opposite-partial-v3.png','prompt-opposite-edit-v3.txt','Use0and2 only; sample1 wrong support'),('opposite-low-pass-v4.png','prompt-passing-only-v4.txt','Use1 only; corrected low passing foot')]:
 provenance.append({'source':name,'sha256':hashlib.sha256((P/'sources'/name).read_bytes()).hexdigest(),'prompt':prompt,'outcome':outcome,'method':'Built-in transparent image generation/edit; no mirror'})
(P/'sources/provenance.json').write_text(json.dumps(provenance,indent=2)+'\n',encoding='utf-8')
(E/'sources/provenance.json').write_text(json.dumps({'source':'first-step-v1.png','sha256':hashlib.sha256((E/'sources/first-step-v1.png').read_bytes()).hexdigest(),'original':'character/bill-carry-start-south-v1/sources/first-step-v1.png','method':'Retained original built-in authored first-step source, re-packaged with actual144master ruler; original source bytes unchanged','prompt':'prompt-first-step-v1.txt'},indent=2)+'\n',encoding='utf-8')
print('Paired South entry builder, guards and authoring provenance saved')
