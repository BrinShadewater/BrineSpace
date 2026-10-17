from pathlib import Path
import json
from PIL import Image
P=Path(__file__).resolve().parent;N=P/'review/native'
r=json.loads((N/'report.json').read_text());run=json.loads((N/'run-verification.json').read_text());bare=json.loads((P/'baseline-manifest.json').read_text());helmet=json.loads((P/'blink-manifest.json').read_text())
errors=[];checks=0
def check(ok,label):
    global checks
    checks+=1
    if not ok:errors.append(label)
schedule=[];total=0
for si,state in enumerate(bare['states']):
    state_start=total
    for i,path in enumerate(state['frameFiles']):
        hold=state['frameDurationsMs'][i];schedule.append({'state':state['id'],'index':i,'startMs':total,'endMs':total+hold,'stateStartMs':state_start,'durationMs':hold,'bareSource':path,'helmetSource':helmet['states'][si]['frameFiles'][i]});total+=hold
check(r['schedule']==schedule,'exact package schedule');check(r['cycleDurationMs']==total and r['cycles']==3,'cycle contract');check(len(r['samples'])==len(schedule)*3,'every pose event in both cycles');check(not r['errors'] and run['engineExit']==0,'consumer selection and native success');check(not run['ownerFilesChanged'],'owner files unchanged');check(r['renderer']!='headless','native renderer');check(total*3<=r['observedTotalMs']<total*3+50,'bounded finish overrun')
max_select=0;max_draw=0
for n,sample in enumerate(r['samples']):
    cycle=n//len(schedule);slot=n%len(schedule);entry=schedule[slot];label=f'{cycle}/{entry["state"]}/{entry["index"]}'
    start=cycle*total+entry['startMs'];end=cycle*total+entry['endMs']
    check((sample['cycle'],sample['slot'],sample['state'],sample['index'])==(cycle,slot,entry['state'],entry['index']),'ordered coverage '+label)
    check((sample['scheduledStartMs'],sample['scheduledEndMs'])==(start,end),'absolute boundary '+label)
    check(start<=sample['observedSelectMs']<=sample['observedDrawMs']<end,'pose selected and drawn before deadline '+label)
    max_select=max(max_select,sample['observedSelectMs']-start);max_draw=max(max_draw,sample['observedDrawMs']-start)
    if cycle==0:
        file=N/sample['capture'];check(file.is_file(),'capture '+label)
        if file.exists():check(Image.open(file).size==(1200,720),'viewport '+label)
    else:check(not sample['capture'],'second cycle no capture stalls '+label)
result={'checks':checks,'errors':errors,'statesPerVariant':len(bare['states']),'events':len(r['samples']),'cycleDurationMs':total,'finishOverrunMs':round(r['observedTotalMs']-total*3,3),'maxSelectionLatencyMs':round(max_select,3),'maxDrawLatencyMs':round(max_draw,3),'scope':'moving south blink consumer clocks and complete pose coverage; no temporal artistic acceptance claim'}
(N/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({**result,'errors':errors[:20],'errorCount':len(errors)}));raise SystemExit(bool(errors))
