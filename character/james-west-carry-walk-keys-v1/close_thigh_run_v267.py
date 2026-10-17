from pathlib import Path
import json,hashlib,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'thigh-window-v267';study=p/'thigh-run-v266';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();n=json.loads((out/'native-evidence.json').read_bytes());v=json.loads((out/'native_probe-validation.json').read_bytes());frozen=json.loads((out/'inputs.json').read_bytes());d=json.loads((study/'inputs.json').read_bytes());report=json.loads((study/'package-review.json').read_bytes())
assert (n['checks'],n['failures'],n['captures'])==(112,0,8)
assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'] and not v['profileDelta']
assert all(sha(r/f)==h for f,h in frozen['preLaunchSha256'].items())
assert all(sha(r/f)==h for f,h in d['referenceSha256'].items()) and sha(study/'prompt.txt')==d['promptSha256']
for row in d['sources']:assert all(sha(r/item['file'])==item['sha256'] for item in row['files'].values())
report.update(disposition='unselected_construction_run_original_brightness_not_met',rawVisuallyReviewed=True,sourceBoardsReviewed=['thigh-detail-review.png','paired-source-review.png'],nativeIncluded=True,findings=['Five target poses now have quilt/yellow thigh construction; original knee/alpha/silhouette and all outside component exact. Pose10 reference stays entirely unchanged despite raw generator adding a panel there.', 'Raw backdrop excluded by original component/alpha admission; no raw transparency claim. Original charcoal brightness not met: medians rise roughly7..16 levels across all five. Retained construction studies only, not final material acceptance.', 'All eight paired native captures4..11 at four display sizes and source board reviewed. Narrow source/time checks do not establish full49 material motion, anatomy/perspective/contact or normal lifecycle.'])
(study/'package-review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
(study/'generation.json').write_text(json.dumps(dict(state='terminal_copied',execution='f913babb-ead1-4e73-b2ca-84ec546b9cbd',method='builtin_imagegen_five_targets_one_reference',rawSha256=sha(study/'raw.png'),prompt='prompt.txt',rawBackdropExcluded=True),indent=2)+'\n',encoding='utf-8')
ledger=p/'material-repair-progress.json';old=ledger.read_bytes();progress=json.loads(old);new=[]
for phase in range(5,10):new.append(dict(phase=phase,version=266,sources={gear:dict(file=(study/f'phase{phase}/{gear}-head-protected.png').relative_to(r).as_posix(),sha256=sha(study/f'phase{phase}/{gear}-head-protected.png')) for gear in ['bare','helmet']},selected=False))
progress['thighConstructionStudies']=[s for s in progress.get('thighConstructionStudies',[]) if s['phase'] not in range(5,10)]+new
progress['nextVisualRepair']='Extend original-master garment construction through16..29 and later panel poses; original charcoal grade of all construction studies still unresolved. Preserve correct existing fabric, pose/knees and source alpha. Full49 temporal/master anatomy/perspective/contact, normal cargo lifecycle and all-family consistency remain.'
assert ledger.read_bytes()==old;ledger.write_text(json.dumps(progress,indent=2)+'\n',encoding='utf-8')
(out/'review.json').write_text(json.dumps(dict(nativeChecks=112,nativeFailures=0,pairedSources=16,reviewedNativeCaptures=8,reviewedNativeBoards=['native-review-0.png','native-review-1.png','native-review-2.png'],sourceIndices=list(range(4,12)),durationsMs=[40,40,40,40,30,20,20,20],reviewedSourceBoard='local-source-review.png',constructionStudy=266,selected=False,sourceAcceptance=False,continuousVisualMotionAcceptance=False,normalChanged=False,fullGoalComplete=False),indent=2)+'\n',encoding='utf-8')
section='''### James five-pose thigh construction run - October3,2026

V2663x2 sheet edits5..9 with10 unchanged reference; raw1536x1024 and source
admission/detail/paired boards reviewed. Fine quilt/yellow garment construction
now spans these five target poses; original knee/alpha/silhouette and outside
component exact, shared body paired. Reference10 entirely preserved even though
raw generation reintroduced a panel there. Generated backdrop excluded; original
alpha used. Median49.50to64.71/50.93to64.82/58.53to65.64/49.50to65.71/
48.50to64.50: original matte brightness NOT achieved. UNSELECTED construction
studies only; no main selected sources or normal runtime replacement.
V267eight consecutive4..11 poses, original250ms clock,16paired sources:
112native checks0/8captures; source and all three native boards reviewed at
four display sizes/both gears. Scratch profile unchanged and frozen hashes stable.

Lesson: multi-cell edits may rewrite an explicitly protected reference and add a
backdrop. Preserve reference bytes and source alpha through exact component-only
packaging; never claim transparent raw from the requested option alone. Coherent
fabric construction still needs independent matte brightness and temporal review.
Next16..29 and later panel runs, preserve correct existing cloth; construction
study grade remains unresolved. Full49 motion/master anatomy/perspective/contact,
normal cargo lifecycle and all-family consistency/polish remain open.
Goal active/incomplete. Handoff:
character/james-west-carry-walk-keys-v1/thigh-window-v267/HANDOFF.md.
'''
guides=record_guides(r,section,'### James thigh boundaries and full49 construction review')
for folder in [study,out]:(folder/'HANDOFF.md').write_text('# Project handoff\n\n'+section+'\nChanged: five target raw/source candidates and frozen prompt/reference, V267 source/native evidence, study ledger, five guides. Checks112/0/8 with original profile/hashes preserved.\n',encoding='utf-8')
with (p/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n'+section)
rasters=[f.relative_to(r).as_posix() for folder in [study,out] for f in folder.rglob('*') if f.suffix.lower() in ['.png','.apng']];attrs=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(rasters)+'\0').encode(),cwd=r,capture_output=True,check=True).stdout.split(b'\0');assert all(attrs[i+2]==b'lfs' for i in range(0,len(attrs)-1,3))
print(json.dumps(dict(unselectedStudy=266,newConstructionPoses=5,checks=112,failures=0,reviewedCaptures=8,guides=guides,lfsRasters=len(rasters),goalComplete=False)))
