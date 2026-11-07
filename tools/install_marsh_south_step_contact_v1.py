"""Preserve the revised whole figure; restore supporting sole by whole translation."""
from pathlib import Path
import copy,json,hashlib
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];CAT=ROOT/'character/marsh-v2/catalog.json'
SOURCE=ROOT/'character/marsh-south-step-detail-v1';BASE=ROOT/'character/marsh-v2/supplemental/south-step-contact-v1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
failed=ROOT/'output/marsh-animation-audit/south-step-normal-world-v1-2026-10-03'
r=json.loads((failed/'report.json').read_text());assert r['checks']==874 and r['failures']==24 and len(r['captures'])==44
assert json.loads((failed/'inputs-before.json').read_text())==json.loads((failed/'inputs-after.json').read_text())
assert json.loads((failed/'owner-before.json').read_text())==json.loads((failed/'owner-after.json').read_text())
before_bytes=CAT.read_bytes();catalog=json.loads(before_bytes);before=copy.deepcopy(catalog);selected=None
for rel in catalog['body']:
    mp=(CAT.parent/rel).resolve();m=json.loads(mp.read_text())
    for s in m['states']:
        if s['id']=='walk-step-south':selected=(mp,m,s)
assert selected and not BASE.exists()
mp,m,state=selected;old=copy.deepcopy(state);new=copy.deepcopy(state)
source=ROOT/state['frameFiles'][3].removeprefix('res://')
im=Image.open(source).convert('RGBA');assert im.size==(184,184)
a=np.asarray(im);assert (a[-1,:,3]==0).all(),'Whole translation cannot clip visible pixels'
translated=Image.new('RGBA',im.size);translated.paste(im,(0,1));b=np.asarray(translated)
assert np.array_equal(b[1:],a[:-1]) and int((a[:,:,3]>0).sum())==int((b[:,:,3]>0).sum())
staged=SOURCE/'candidate-02-registered-frame.png';assert not staged.exists();translated.save(staged)
BASE.mkdir();(BASE/'catalog-before.json').write_bytes(before_bytes)
dest=BASE/'phase-003.png';dest.write_bytes(staged.read_bytes())
new['frameFiles'][3]='res://'+dest.relative_to(ROOT).as_posix()
manifest={k:v for k,v in m.items() if k!='states'};manifest['states']=[new]
manifest.update(normalAdmission=True,fullGoalComplete=False,revision='South step detail02 whole-frame Y+1 registration; supporting sole restored with exact pixels, no resampling or anatomy change.')
out=BASE/'manifest.json';out.write_text(json.dumps(manifest,indent=2)+'\n')
catalog['body'].append(out.relative_to(CAT.parent).as_posix());CAT.write_text(json.dumps(catalog,indent=2)+'\n')
receipt={'catalogBefore':before,'catalogBeforeSha256':hashlib.sha256(before_bytes).hexdigest(),'catalogAfterSha256':sha(CAT),'oldState':old,'newState':new,'revisedSlot':3,'source':source.relative_to(ROOT).as_posix(),'sourceSha256':sha(source),'translatedFrame':staged.relative_to(ROOT).as_posix(),'translatedFrameSha256':sha(staged),'wholeTranslation':[0,1],'operation':'Every visible pixel translated together; equal RGBA rows and visible count, no clipping/resampling/painting/splice/scale/pivot metadata change.','discoveredFailure':'24strict supporting-depth assertions in real normal actor/main/grid across four route lengths; phase3 right sole1sourcepixel high.','normalAdmission':True,'fullGoalComplete':False}
(BASE/'admission.json').write_text(json.dumps(receipt,indent=2)+'\n')
oldpose=Image.open(ROOT/'character/marsh-south-step-v1/candidate-05/003.png').convert('RGBA')
board=Image.new('RGB',(3*184,214),'#293b40');draw=ImageDraw.Draw(board)
for i,(name,t) in enumerate([('original pose',oldpose),('detail02 before',im),('whole Y+1',translated)]):
    board.paste(t,(i*184,25),t);draw.text((i*184+3,5),name,fill='white')
board.resize((1104,428),Image.Resampling.NEAREST).save(SOURCE/'contact-registration-2x.png')
print('Whole pose shiftedY+1;all visible RGBA pixels preserved;1slot/1state revised,6drawings/227other states retained')
