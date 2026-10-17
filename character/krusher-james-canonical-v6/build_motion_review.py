from pathlib import Path
import json,subprocess
P=Path(__file__).resolve().parent;O=P/'review';r=json.load(open(O/'motion/report.json'));run=json.load(open(O/'motion/run-verification.json'));supp=json.load(open(O/'supplement/report.json'));checks=0;seen={(q['cycle'],q['slot']):q for q in r['samples']};missing=[i for i in range(len(r['schedule'])) if (0,i) not in seen];late=[q for q in r['samples'] if q['observedDrawMs']>=q['scheduledEndMs']]
assert len(set(missing))==len(missing);assert all((1,i) in seen for i in range(len(r['schedule'])));assert {q['slot'] for q in supp['samples']}==set(missing);assert not r['errors'] and not supp['errors'] and run['engineExit']==0 and not run['ownerFilesChanged'];checks+=5
for q in r['samples']:
 s=r['schedule'][q['slot']];assert q['state']==s['state'] and q['index']==s['index'];assert q['scheduledStartMs']<=q['observedSelectMs']<q['scheduledEndMs'];assert q['observedDrawMs']>=q['observedSelectMs'];checks+=3
captures=[]
for i,q in enumerate(r['schedule']):
 if (0,i) in seen:path=O/'motion'/seen[(0,i)]['capture']
 else:path=O/'supplement'/next(x for x in supp['samples'] if x['slot']==i)['capture']
 assert path.exists();checks+=1;captures.append((path,q))
with (O/'motion-concat.txt').open('w') as f:
 for path,q in captures:f.write("file '"+path.resolve().as_posix()+"'\noption framerate 1000\nduration "+str(q['durationMs']/1000)+'\n')
 f.write("file '"+path.resolve().as_posix()+"'\noption framerate 1000\n")
with (O/'media.log').open('w') as log:subprocess.run(['ffmpeg','-y','-f','concat','-safe','0','-i',str(O/'motion-concat.txt'),'-t',str(r['cycleDurationMs']/1000),'-vf','fps=60','-c:v','libx264','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(O/'head-fit-motion-preview.mp4')],stdout=log,stderr=log,check=True)
encoded=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(O/'head-fit-motion-preview.mp4')],text=True));assert abs(encoded-r['cycleDurationMs']/1000)<=1/60;checks+=1
validation={'checks':checks,'errors':[],'admissionChecks':r['admissionChecks'],'events':len(r['samples']),'requiredPerCycle':len(r['schedule']),'firstCycleMissing':missing,'secondCycleCoverageComplete':True,'lateDraws':len(late),'maxLateDrawMs':max([q['observedDrawMs']-q['scheduledEndMs'] for q in late],default=0),'supplementChecks':supp['checks'],'scope':'All textures/registration/source clocks admitted; complete second advancing cycle source selections. Actual omissions and late draws recorded above. Controlled midpoint captures fill missing first-cycle images; neither those nor replay certify original wall-clock cadence or station gait distance.'}
(O/'motion/validation.json').write_text(json.dumps(validation,indent=2)+'\n')
(O/'media.json').write_text(json.dumps({'seconds':r['cycleDurationMs']/1000,'encodedSeconds':encoded,'captures':len(captures),'supplementalCaptures':len(missing),'scope':'Native captured poses with original source holds at60fps quantization; actual supplement count recorded. Not an unbroken recording or station lifecycle acceptance.'},indent=2)+'\n');print({k:validation[k] for k in ['checks','events','lateDraws','maxLateDrawMs']});print({'mediaSeconds':encoded,'nativeCaptures':len(captures)})
