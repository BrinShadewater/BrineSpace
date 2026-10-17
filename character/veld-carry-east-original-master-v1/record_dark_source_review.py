from pathlib import Path
import hashlib,json,shutil,uuid,time
P=Path(__file__).resolve().parent;R=P.parents[1];D=P/'standing-step-video-v3-dark'
g=json.loads((D/'generation.json').read_text(encoding='utf-8'));assert g['status'].lower()=='success'
r=json.loads((D/'source-registration-v2.json').read_text(encoding='utf-8'));raw=json.loads((D/'full-foreground-diagnostic.json').read_text(encoding='utf-8'))
frozen=json.loads((R/'output/veld-east-native-stride-probe-v1/inputs-before.json').read_text(encoding='utf-8'));changes=[p for p,h in frozen.items() if not (R/p).is_file() or hashlib.sha256((R/p).read_bytes()).hexdigest()!=h];assert not changes
v={'status':'Completed background trial; appearance improves, carrying-walk motion rejected','taskId':g['task_id'],'estimatedUSD':g['estimatedUSD'],'billingVerified':False,'input':json.loads((D/'input-record.json').read_text(encoding='utf-8')),'registration':{k:r[k] for k in ['frameCount','fps','durationMs','checks','failures','ranges','master','alphaControl']},'backgroundMaxDistance':max(x['backgroundMaxDistance'] for x in r['rows']),'backgroundOutsideToleranceFraction':max(x['backgroundBeyondToleranceFraction'] for x in r['rows']),'independentFullForegroundRange':[raw['minimumProjectedNativeFloor'],raw['maximumProjectedNativeFloor']],'extractionCorrection':'Largest-component V0 drops disconnected boot116 and produces misleading floor206/height130. V2 retains ALL dark-key foreground components20rawpixels or larger under same frozen8tolerance/1rawpxerosion. Source RGB/geometry untouched; original complete142 V0 exports and reports retained. Complete raw foreground extent supersedes V0 sole inference.','visualReview':'All6 chronological raw boards/142frames, all6V0 and all6 corrected V2 alpha boards, enlarged original/control/start/mid/end comparison and lowest12 raw boot crops reviewed. Pale white halo greatly reduced visually and head25..26 matches original26 more closely than white-source27. Head axis123..123.5 and top76..77 stable. But clip repeats faster jogging-like phases instead of requested2smallsteps; both boots float above original far220/near223 support projection at multiple phases. This is visible in RAW, not just alpha. No carrying-walk/contact/standing/full material acceptance.','measurementLimits':'Broad upper-body band43..51 includes raised knee at some poses, so maximum cannot establish torso enlargement by itself. Cloth ROI medians63..72/62..69/61..70 are diagnostic only, affected by changing pose. Full foreground extent213.7..225 is not a literal physical sole; lower12 raw crops establish the visible suspended-feet defect independently. One successful changed-background trial cannot establish a universal background effect across generations.','priorNativeInputsUnchanged':len(frozen),'priorNativeInputChanges':changes,'nativeTest':'Not run; raw carrying gait already fails. No helmet packaging, normal selector or gameplay adoption.','bindings':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [D/'source.mp4',D/'master-input.png',D/'prompt.txt',D/'input-record.json',D/'matte.py',D/'source-registration-v2.json',D/'full-foreground-diagnostic.json']}}
(D/'VERDICT.json').write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
ledger=json.loads((P/'EXECUTIONS.json').read_text(encoding='utf-8'));entry={'id':g['task_id'],'provider':'MiniMax direct','folder':D.name,'status':v['status'],'raw':D.name+'/source.mp4','prompt':D.name+'/prompt.txt','estimatedUSD':.28,'billingVerified':False,'verdict':D.name+'/VERDICT.json'};ledger['generations']=[x for x in ledger['generations'] if x['id']!=entry['id']]+[entry];(P/'EXECUTIONS.json').write_text(json.dumps(ledger,indent=2)+'\n',encoding='utf-8')
title='## Veld dark-background native source reviewed — October 3, 2026'
note=title+'''\n\nSingle MiniMax-Hailuo02 task448589965386249 terminalSuccess,6s768P estimateUSD0.28,
billing unverified. standing-step-video-v3-dark retains source/prompt/input/whole
142pose replay/VERDICT. Only backdrop changed white->RGB12,18,24; same actual
native original whole3x nearest,768x960plate,identical endpoints and motion wording.
Exact inverse RGBA still byte-equal to original. Fixed1/3/offset0,-32 retained.
Input alpha control H147/floor222 vs original148/223,head26/torso42 preserved;
IoU.958/RGBintersectionMAE3.32. This extraction loss is separate from source gait.

All6raw/all6initial/all6corrected alpha boards142poses and original/control/whole
endpoint/detail comparison viewed. Source head25..26 vs original26 (white source27),
axis123..123.5/top76..77, pale halo much reduced visually. Background maxRGBdelta4,
none outside frozen tolerance8. Broad upper band43..51 includes raised knee, so its
maximum does NOT by itself prove torso growth. Cloth ROI63..72/62..69/61..70 only
diagnostic. Motion REJECTED: repeated rapid jogging-like phases and visibly both
boots suspended in raw source instead of grounded small carrying steps.

Independent whole foreground exposes V0 extraction loss: largest component drops
disconnected boot116, giving misleading H130/floor206. V2 retains ALL foreground
components20rawpx or larger at same8tolerance/1rawpxerosion; no source RGB/body/pose
repair, V0 preserved. Full raw foreground extent projects213.7..225; lowest12 raw
boot crops viewed independently of alpha, original far220/near223 depth respected.
Corrected all142 H136..149/floor212..224, exact284 replay pixel/duration checks0,
5917ms.308prior native inputs unchanged. No unnecessary native/helmet/normal adoption.

Lessons: dark flat conditioning can reduce pale matte contamination without
guaranteeing walking mechanics. Compare raw boot/contact separately from alpha:
largest-component extraction can silently drop a disconnected boot and exaggerate
clearance. Retain disconnected meaningful foreground parts with a fixed global
rule when backdrop stability supports it; do not fill anatomical holes or repair
geometry. Source head/grade improvement does not make a jogging gait suitable.
Next grounded complete bilateral original-master source and dense standing joins,
physical contact/roll and full ordinary integration; full original action/direction/
furniture/save/Continue acceptance and whole-library polish remain. No live video
or blocker; full goal active/incomplete. Handoff: character/veld-carry-east-original-master-v1/HANDOFF.md.
\n'''
h=P/'HANDOFF.md'
if title not in h.read_text(encoding='utf-8'):
 with h.open('a',encoding='utf-8') as f:f.write('\n'+note)
template=(P/'record_native_milestone.py').read_text(encoding='utf-8');exec(compile(template[template.index('paths=['):],str(Path(__file__)),'exec'))
print(json.dumps({'status':v['status'],'fullSourceFrames':142,'exactReplayChecks':284,'failures':0,'priorNativeInputsUnchanged':len(frozen)}))
