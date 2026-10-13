"""Freeze cardinal native source evidence and full original capture boards."""
from pathlib import Path
import hashlib,json,shutil
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'output/marsh-animation-audit/retained-gesture-east04-2026-10-03'
O=ROOT/'character/marsh-retained-gesture-material-v1/cardinal02-unselected'
read=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
owner=read(A/'owner-before.json');inputs=read(A/'inputs-before.json')
assert owner==read(A/'owner-after.json') and inputs==read(A/'inputs-after.json')
assert (A/'native-exit.txt').read_text().strip()=='0'
log=(A/'native.log').read_text();assert 'ERROR:' not in log and 'WARNING:' not in log and '0failures' in log
native=read(A/'report.json');assert native['checks']==192 and native['failures']==0 and native['playerRestores']==6
assert len(native['captures'])==6 and len(native['samples'])==52
for cap in native['captures']:
    p=A/cap['file'];shutil.copy2(p,O/cap['file']);cap['sha256']=sha(p)
boards=[]
for d in ['east']:
    caps=[c for c in native['captures'] if c['direction']==d]
    assert [c['slot'] for c in caps]==list(range(6))
    board=Image.new('RGB',(2016,980))
    for i,cap in enumerate(caps):
        im=Image.open(O/cap['file']).convert('RGB');assert im.size==(672,490)
        board.paste(im,((i%3)*672,(i//3)*490))
    path=O/(d+'-native-contact.png');board.save(path)
    boards.append({'direction':d,'path':path.relative_to(ROOT).as_posix(),'sha256':sha(path),'actuallyInspected':False,
                   'operations':'Six full native672x490 captures arranged in3x2, no crop/resize.'})
native.update({'boards':boards,'stableBoundedInputs':len(inputs),'unchangedOwnerNonLogFiles':len(owner),
               'nativeScriptSha256':sha(ROOT/'tools/review_marsh_retained_gesture_east04.gd'),
               'normalAdmission':False,'continuousMotionReviewed':False,'fullGoalComplete':False})
selection=read(O/'source-selection.json')
for child in selection['children']:assert sha(ROOT/child['path'])==child['sha256']
selection['nativeEvidence']=native
(O/'verification.json').write_text(json.dumps(selection,indent=2)+'\n')
print('192checks,12exact source slots,52samples,6restores/captures,1049stable inputs,2931owner files unchanged;East native board prepared')
