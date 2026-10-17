from pathlib import Path
import json
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parent.parent;N=P/'review/native';PAIR=P.parent/'krusher-moving-equipment-test-v2';report=json.loads((N/'report.json').read_text());run=json.loads((N/'run-verification.json').read_text());bare=json.loads((PAIR/'bare-manifest.json').read_text());helmet=json.loads((PAIR/'helmet-manifest.json').read_text());checks=0;errors=[]
def check(ok,name):
    global checks
    checks+=1
    if not ok:errors.append(name)
schedule=[];time=0
for si,state in enumerate(bare['states']):
    if not state['id'].startswith('walk-'):continue
    for i,path in enumerate(state['frameFiles']):
        duration=state['frameDurationsMs'][i];schedule.append({'state':state['id'],'index':i,'startMs':time,'endMs':time+duration,'durationMs':duration,'bareSource':path,'helmetSource':helmet['states'][si]['frameFiles'][i]});time+=duration
check(schedule==report['schedule'],'exact source schedule');check(report['cycleDurationMs']==time,'source cycle duration');check(report['scheduledTotalMs']==time*2,'two source cycles');check(report['cycles']==2,'two cycles played');check(len(report['samples'])==len(schedule)*2,'no omitted pose event');check(run['engineExit']==0 and not report['errors'],'native engine/capture success');check(not run['ownerFilesChanged'],'owner files unchanged');check(report['renderer']!='headless','native renderer');check(time*2<=report['observedTotalMs']<time*2+50,'global finish within one display interval allowance')
max_selection=0;max_draw=0
for n,sample in enumerate(report['samples']):
    cycle=n//len(schedule);slot=n%len(schedule);entry=schedule[slot];start=cycle*time+entry['startMs'];end=cycle*time+entry['endMs'];select=sample['observedSelectMs'];draw=sample['observedDrawMs']
    check((sample['cycle'],sample['slot'])==(cycle,slot),'ordered complete cycle/pose coverage');check((sample['state'],sample['index'],sample['bareSource'],sample['helmetSource'])==(entry['state'],entry['index'],entry['bareSource'],entry['helmetSource']),'frame/source binding');check(sample['scheduledStartMs']==start and sample['scheduledEndMs']==end,'absolute schedule boundary');check(start<=select<end,'correct pose at observed monotonic selection');check(select<=draw<end,'pose rendered before its source deadline');check(select-start<50,'bounded selection latency with no cumulative reset');max_selection=max(max_selection,select-start);max_draw=max(max_draw,draw-start)
    if cycle==0:
        path=N/sample['capture'];check(path.is_file(),'first cycle capture exists');im=np.array(Image.open(path).convert('RGBA'));check(im.shape==(720,1200,4),'native viewport')
        check(bool(np.any(im[95:463,100:468,:3]!=im[0,0,:3])),'bare sprite rendered')
        check(bool(np.any(im[95:463,580:948,:3]!=im[0,0,:3])),'helmet sprite rendered')
    else:check(sample['capture']=='','later cycles play without capture stalls')
result={'checks':checks,'errors':errors,'cycleDurationMs':time,'cycles':2,'poseEvents':len(report['samples']),'finishOverrunMs':round(report['observedTotalMs']-time*2,3),'maxSelectionLatencyMs':round(max_selection,3),'maxDrawLatencyMs':round(max_draw,3),'scope':'continuous native source clock, declared paired pose bindings and nonempty captures; not station/controller or artistic motion acceptance'};(N/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));raise SystemExit(bool(errors))
