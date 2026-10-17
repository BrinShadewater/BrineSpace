from pathlib import Path
import json,hashlib,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'thigh-window-v271';study=p/'thigh-run-v270';original=p/'thigh-run-v268';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();n=json.loads((out/'native-evidence.json').read_bytes());v=json.loads((out/'native_probe-validation.json').read_bytes());frozen=json.loads((out/'inputs.json').read_bytes());d=json.loads((study/'inputs.json').read_bytes());report=json.loads((study/'package-review.json').read_bytes())
assert (n['checks'],n['failures'],n['captures'])==(112,0,8)
assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'] and not v['profileDelta']
assert all(sha(r/f)==h for f,h in frozen['preLaunchSha256'].items())
assert all(sha(r/f)==h for f,h in d['referenceSha256'].items()) and sha(study/'prompt.txt')==d['promptSha256']
assert sha(study/'raw.png')==sha(original/'raw.png')==d['rawSha256']
for row in d['sources']:assert all(sha(r/item['file'])==item['sha256'] for item in row['files'].values())
report.update(disposition='unselected_construction_original_brightness_not_met',rawVisuallyReviewed=True,sourceBoardsReviewed=['thigh-detail-review.png','paired-source-review.png'],nativeIncluded=True,findings=['Five16..20 target poses now carry quilt/yellow construction, with wider pose-specific19/20 admission removing more of the original panel edge. Original knee ROI, alpha/silhouette and outside component exact; shared body paired.', 'Faint flat-stitch wording still yields padded lighter cloth. Same-mask medians roughly50..53to62..66; original charcoal brightness not met. Source-stage garment anatomy/seam topology remains provisional.', 'Raw generation changed reference15 and added backdrop/lower-leg stitches: all excluded through original reference bytes and restricted admission. Existing raw reused for V270; no second generation.', 'All eight14..21 native captures and three paired four-size boards visually reviewed. Panel construction at untouched21 persists. No complete temporal/master proportion/perspective/contact or normal lifecycle acceptance.'])
(study/'package-review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
(original/'generation.json').write_text(json.dumps(dict(state='terminal_copied',execution='c7b1197e-c067-446f-8b99-5c11886de9c3',method='builtin_imagegen_five_targets_one_reference',rawSha256=sha(original/'raw.png'),prompt='prompt.txt'),indent=2)+'\n',encoding='utf-8')
(study/'generation.json').write_text(json.dumps(dict(state='reused_raw_packaging_only',newGeneration=False,execution='c7b1197e-c067-446f-8b99-5c11886de9c3',rawSource=d['rawSource'],rawSha256=sha(study/'raw.png')),indent=2)+'\n',encoding='utf-8')
ledger=p/'material-repair-progress.json';old=ledger.read_bytes();progress=json.loads(old);new=[]
for phase in range(16,21):new.append(dict(phase=phase,version=270,sources={gear:dict(file=(study/f'phase{phase}/{gear}-head-protected.png').relative_to(r).as_posix(),sha256=sha(study/f'phase{phase}/{gear}-head-protected.png')) for gear in ['bare','helmet']},selected=False))
progress['thighConstructionStudies']=[s for s in progress.get('thighConstructionStudies',[]) if s['phase'] not in range(16,21)]+new
progress['nextVisualRepair']='Remaining21..29 and later panel poses need pose-specific garment construction; 21unselected construction studies include0/1/2/5..20/47/48, with grade still unresolved. Preserve correct existing cloth, anatomy/knees and alpha. Full49 temporal/master proportion/perspective/contact, normal cargo lifecycle and all-family consistency remain.'
assert ledger.read_bytes()==old;ledger.write_text(json.dumps(progress,indent=2)+'\n',encoding='utf-8')
(out/'review.json').write_text(json.dumps(dict(nativeChecks=112,nativeFailures=0,pairedSources=16,reviewedNativeCaptures=8,reviewedNativeBoards=['native-review-0.png','native-review-1.png','native-review-2.png'],sourceIndices=list(range(14,22)),durationsMs=[20]*8,reviewedSourceBoard='local-source-review.png',constructionStudy=270,reusedRaw=268,selected=False,sourceAcceptance=False,continuousVisualMotionAcceptance=False,normalChanged=False,fullGoalComplete=False),indent=2)+'\n',encoding='utf-8')
section='''### James later diagonal thigh run and edge admission - October3,2026

V268 five16..20 targets plus unchanged15 reference generated as3x2sheet.
Raw1536x1024 and first protected sources reviewed; initial19/20 admission left
panel-edge strips. V270 reuses exact same raw, widens19/20 component admission
leftward while preserving original knee ROI; no new generation. Final admission,
details/paired sources reviewed before native launch. Five poses retain exact
knees, alpha/silhouette, outside component and shared body. Reference15 wholly
unchanged locally despite generator adding a panel; backdrop/calf stitches excluded.
Flat faint-stitch wording still yields brighter padded fabric: medians50..53to62..66.
Construction studies UNSELECTED; original matte brightness not achieved.
V271 consecutive14..21, original160ms,16paired sources:112native checks0/
8captures, source and all three native boards reviewed at four sizes/both gears.
Scratch profile unchanged and frozen hashes stable. Original panel persists at21.
No main selected source or normal runtime changes. V269 prepared script never run.

Lesson: cloth boundary shifts per pose, even within one diagonal stride run;
inspect full old panel extent and knee independently, then reuse valid raw when
only packaging under-covers it. Stronger flat-quilt wording does not bound fabric
brightness. Preserve raw reference/background changes outside exact edit scope.
Next21..29 and later panel poses, preserve correct existing construction; whole
study grade remains unresolved. Full49 temporal/master proportions/perspective/
contact, normal cargo lifecycle and all-family consistency/polish remain open.
Goal active/incomplete. Handoff:
character/james-west-carry-walk-keys-v1/thigh-window-v271/HANDOFF.md.
'''
guides=record_guides(r,section,'### James five-pose thigh construction run')
for folder in [original,study,out]:(folder/'HANDOFF.md').write_text('# Project handoff\n\n'+section+'\nChanged: five generated target candidates, reuse/wider19/20 admission, frozen input/prompt provenance, V271 source/native evidence, unselected study ledger and five guides. Checks112/0/8; owner profile and frozen inputs preserved.\n',encoding='utf-8')
with (p/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n'+section)
rasters=[f.relative_to(r).as_posix() for folder in [original,study,out] for f in folder.rglob('*') if f.suffix.lower() in ['.png','.apng']];attrs=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(rasters)+'\0').encode(),cwd=r,capture_output=True,check=True).stdout.split(b'\0');assert all(attrs[i+2]==b'lfs' for i in range(0,len(attrs)-1,3))
print(json.dumps(dict(unselectedStudy=270,reusedRaw=268,newConstructionPoses=5,totalConstructionStudies=len(progress['thighConstructionStudies']),checks=112,failures=0,reviewedCaptures=8,guides=guides,lfsRasters=len(rasters),goalComplete=False)))
