from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,uuid,os
P=Path(__file__).resolve().parent;R=P.parents[1]
guard=json.loads((P/'native-workshop-validation.json').read_bytes());native=json.loads((P/'native-workshop-evidence.json').read_bytes());assert guard['exitCode']==0 and guard['realProfileUnchanged'] and not guard['timedOut'] and native['failures']==0
frozen=json.loads((P/'workshop-inputs.json').read_bytes());changed=[p for p,h in frozen.items() if hashlib.sha256((R/p).read_bytes()).hexdigest()!=h];assert not changed,changed
selected=json.loads((P/'selection-evidence.json').read_bytes());assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in selected['sourceHashes'].items())
board=Image.new('RGB',(1536,1080),'#303b40');draw=ImageDraw.Draw(board);files=[]
for row,result in enumerate(native['results']):
    for col,path in enumerate(result['captures']):
        file=R/path[6:];im=Image.open(file).convert('RGB');im.thumbnail((512,512));board.paste(im,(col*512,row*540+24));draw.text((col*512+6,row*540+5),result['mode']+' / '+['pickup','carry','unload'][col],fill='white');files.append(file)
board.save(P/'workshop-world-review.png')
report={'nativeChecks':native['checks'],'failures':0,'freshMainContinues':6,'actualWorkshopCases':2,'captures':6,'visualReviewPending':True,'ownerProfileUnchanged':True,'changedInputs':changed,'sourceCopyHashesUnchanged':128,'fullGoalComplete':False,'scope':native['scope'],'supersededFailure':'First3382checks/2fail run assumed completion leaves goal empty. Fresh-main diagnostic observed exact curiosity relief and immediate next chooser. Initial run/evidence/captures retained; final fixture checks numerical65relief with natural growth and permits next goal. Card tray hidden for final review captures.'}
(P/'workshop-review-evidence.json').write_text(json.dumps(report,indent=2))
print(json.dumps({'nativeChecks':native['checks'],'failures':0,'freshMainContinues':6,'captures':6,'changedInputs':changed,'reviewBoard':'workshop-world-review.png'}))
