from pathlib import Path
import json,shutil,ast
H=Path(__file__).resolve().parent;R=H.parents[1];P=R/'character/krusher-animation-package-v9';OLD=R/'character/krusher-animation-package-v8';read=lambda p:json.loads(p.read_text());checks=[];captures=0
for name in ['native','repair','bunk','water','west']:
 folder=H/'review'/name;report=read(folder/'report.json');run=read(folder/'run-verification.json');assert not report.get('errors') and not report.get('failures') and run['engineExit']==0 and not run['ownerFilesChanged'];log=(folder/'engine.log').read_text(errors='replace');assert not any(w in log for w in ['ERROR:','SCRIPT ERROR','WARNING:','leaked at exit','Orphan StringName']);captures+=len(report.get('records',[]));checks.append({'fixture':name,'checks':report['checks'],'failures':0,'engineExit':0,'ownerFilesFingerprinted':run['ownerFilesFingerprinted'],'ownerFilesChanged':[]});target=P/'verification'/name;target.mkdir(parents=True,exist_ok=True)
 for file in ['report.json','run-verification.json','engine.log']:shutil.copyfile(folder/file,target/file)
new=read(P/'package.json');old=read(OLD/'package.json');groups={};cache={}
def files(root,index,key):
 mp=root/index['states'][key]['manifest'];m=cache.setdefault(str(mp),read(mp));return next(s for s in m['states'] if s['id']==key.split(':',1)[1])['frameFiles']
for key in old['states']:
 for a,b in zip(files(OLD,old,key),files(P,new,key)):groups.setdefault(a,set()).add(b)
assert all(len(v)==1 for v in groups.values());alias={'sourceDrawings':len(groups),'conflictingReplacements':0,'scope':'Every occurrence of each V8 source drawing maps to one identical V9 drawing across all 8058 holds.'};(H/'alias-final-audit.json').write_text(json.dumps(alias,indent=2)+'\n')
summary={'package':'krusher-animation-package-v9','states':{'bare':338,'helmet':248},'frameHolds':8058,'uniquePNG':len(new['files']),'changedDrawings':read(H/'bank-validation.json')['changedDrawings'],'bankChecks':read(H/'bank-validation.json')['checks'],'packageChecks':read(P/'source-validation.json')['checks'],'nativeChecks':sum(q['checks'] for q in checks),'nativeFailures':0,'captures':captures,'registeredAliasConflicts':0,'fixtures':checks,'scope':'Revised matte head style and anatomical collar candidate. Complete source coverage, protected-pixel checks and native fixtures pass. Owner visual acceptance remains pending.'};(P/'verification/summary.json').write_text(json.dumps(summary,indent=2)+'\n')
for file in ['alias-final-audit.json','floor-cue-proof.json','bank-validation.json','remote-preview.json','action-prompts.json','standing-style-prompt.txt']:shutil.copyfile(H/file,P/'verification'/file)
new['status']='Revised matte style and anatomical neck candidate; native checks passed; owner visual review pending';new['verification']='verification/summary.json';(P/'package.json').write_text(json.dumps(new,indent=2)+'\n');shutil.copyfile(H/'style-neck-comparison.png',P/'references/style-neck-comparison.png')
(P/'README.md').write_text("""# Krusher Dom animation set — style and neck revision

338 bare + 248 helmet states; 8,058 frame holds; 3,486 unique PNGs. The V8 head treatment was rejected by the owner for differing style/pixel density and disconnected necks. V9 uses newly authored matte heads, preserved antialiased edges and short necks fitted behind the original collar. Prone south necks are hidden behind the jaw. Original body skin is restored only at the anatomical contact, excluding gold suit pixels.

Load the ordered whole manifest paths in package.json. Preserve every pack's canvas, pivot, 148-pixel standing ruler and source clocks. Helmet packs use diving-helmet. All frames are portable inside this folder. Counts include aliases and derived returns. Sealed-helmet meals retain the source tablet aliases.

[Private animation comparison](https://krusher-dom-preview.brinshadewater.chatgpt.site/animations/) includes Previous/Revised selection for all states. Open index.html for local current-set playback. references/style-neck-comparison.png shows six matched examples.

Verification: 17,424 source protection checks, 16,790 package checks, 72,998 native checks; zero failures/errors/warnings/leaks. Every repeated source drawing maps consistently. Four station fixtures produced 352 captures. All 2,947 owner non-log files were unchanged per isolated run. Body pixels outside declared head/neck masks and every helmet alpha pixel are exact. See verification/summary.json.

Visual review covers 256 representative family/gear/facing poses, enlarged collar details, selected browser playback and sampled station captures. Owner visual acceptance and exhaustive continuous motion review remain separate. No normal roster integration, game export or game-repository commit was performed.

Sources and rebuild scripts: character/krusher-style-neck-v1/ and character/krusher-style-neck-bank-v1/. Run validate_final.py for the deterministic package build and isolated native fixtures. Generated source sheets and exact prompts are retained.
""",encoding='utf8')
for p in H.glob('*.py'):ast.parse(p.read_text(encoding='utf-8-sig'),filename=str(p))
print(json.dumps(summary))
