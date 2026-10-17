from pathlib import Path
import json,shutil
H=Path(__file__).resolve().parent;P=H.parent/'krusher-animation-package-v10';read=lambda p:json.loads(p.read_text());summary=read(H/'visual-review.json');fixtures=[]
for name in ['native','water','repair','bunk','west']:
 folder=H/'review'/name;report=read(folder/'report.json');run=read(folder/'run-verification.json');log=(folder/'engine.log').read_text(errors='replace');assert run['engineExit']==0 and not run['ownerFilesChanged'] and not report.get('errors') and not report.get('failures');assert not any(w in log for w in ['ERROR:','SCRIPT ERROR','WARNING:','leaked at exit','Orphan StringName']);target=P/'verification'/name;target.mkdir(parents=True,exist_ok=True)
 for f in ['report.json','run-verification.json','engine.log']:shutil.copyfile(folder/f,target/f)
 fixtures.append({'fixture':name,'checks':report['checks'],'captures':len(report.get('records',[])),'ownerFilesFingerprinted':run['ownerFilesFingerprinted'],'ownerFilesChanged':[]})
summary['fixtures']=fixtures;summary['nativeChecks']=sum(q['checks'] for q in fixtures);summary['nativeFailures']=0;summary['packageChecks']=read(P/'source-validation.json')['checks'];summary['registeredPoseGroups']=read(H/'registered-alias-audit.json')['registeredPoseGroups'];assert not read(H/'registered-alias-audit.json')['conflicts'];(P/'verification/summary.json').write_text(json.dumps(summary,indent=2)+'\n')
for f in ['bank-validation.json','registered-alias-audit.json','visual-review.json','preview-export.json']:shutil.copyfile(H/f,P/'verification'/f)
shutil.copyfile(H/'style-neck-comparison.png',P/'references/continuity-comparison.png');idx=read(P/'package.json');idx['verification']='verification/summary.json';idx['status']='Full continuity repair candidate; native checks passed; owner visual acceptance pending';(P/'package.json').write_text(json.dumps(idx,indent=2)+'\n')
removed=0
for f in (P/'frames').glob('*.png'):
 if 'frames/'+f.name not in idx['files']:f.unlink();removed+=1
print(json.dumps({'nativeChecks':summary['nativeChecks'],'failures':0,'unreferencedBuildFramesRemoved':removed,'fixtures':fixtures}))
