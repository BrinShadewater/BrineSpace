from pathlib import Path
import json,shutil,ast
H=Path(__file__).resolve().parent;R=H.parents[1];P=R/'character/krusher-animation-package-v8'
read=lambda p:json.loads(p.read_text())
checks=[]
for name in ['native','repair','bunk','water','west']:
 folder=H/'review'/name;report=read(folder/'report.json');run=read(folder/'run-verification.json')
 assert not report.get('errors') and not report.get('failures') and run['engineExit']==0 and not run['ownerFilesChanged']
 log=(folder/'engine.log').read_text(errors='replace')
 assert not any(word in log for word in ['ERROR:','SCRIPT ERROR','WARNING:','leaked at exit','Orphan StringName'])
 checks.append({'fixture':name,'checks':report['checks'],'failures':0,'engineExit':0,'ownerFilesFingerprinted':run['ownerFilesFingerprinted'],'ownerFilesChanged':[]})
 target=P/'verification'/name;target.mkdir(parents=True,exist_ok=True)
 for file in ['report.json','run-verification.json','engine.log']:shutil.copyfile(folder/file,target/file)
audit=read(H/'alias-final-audit.json');assert audit['inconsistentGroups']==0
summary={'package':'krusher-animation-package-v8','states':{'bare':338,'helmet':248},'frameHolds':8058,'uniquePNG':3486,'packageChecks':read(P/'source-validation.json')['checks'],'nativeChecks':sum(q['checks'] for q in checks),'nativeFailures':0,'captures':352,'registeredAliasConflicts':0,'fixtures':checks,'scope':'Complete asset coverage and final sampled/native fixtures; owner visual acceptance and normal roster integration are separate.'}
(P/'verification/summary.json').write_text(json.dumps(summary,indent=2)+'\n')
for file in ['alias-final-audit.json','floor-cue-proof.json','remote-preview.json','prompts.json']:shutil.copyfile(H/file,P/'verification'/file)
index=read(P/'package.json');index['status']='Complete revised animation asset candidate; final native and sampled station checks passed; owner review pending';index['verification']='verification/summary.json';(P/'package.json').write_text(json.dumps(index,indent=2)+'\n')
readme='''# Krusher Dom animation asset set

System Administrator / AI & Robotics / James utility suit / matte muted cyan #527C80.

338 bare + 248 helmet states, 8,058 frame holds, 3,486 unique RGBA PNGs. Includes locomotion, tablet/inspection, repairs/welding, cargo/turns, seated activities, meals, helmet fitting, rest/bunk, recovery/salvage, collapse and swimming/cargo/distress/interruption states. Counts include recorded aliases and derived returns; they are not unique generated drawings. Sealed-helmet meal keys retain the original tablet aliases.

Open `index.html` for local playback. The full private browser with search, gear switching, pause, scrubbing and speed controls is [online](https://krusher-dom-preview.brinshadewater.chatgpt.site/animations/). `references/character-sheet.png` shows the current native turnaround.

Load the ordered whole manifest paths in `package.json`; helmet packs use `diving-helmet`. Every PNG is inside this folder. Preserve each pack's canvas, pivot, standing ruler, sampling and state clocks. Station locomotion is distance-driven; the browser replays clocks. Source provenance is retained in the index.

Validation: 16,790 package checks and 72,998 final native checks, zero failures/errors/warnings/leaks. All 8,058 slots and clock boundaries checked. Four final station fixtures add 352 captures across repair, bunk, furnished water routes and West case release/interruptions. All 2,947 fingerprinted owner non-log files unchanged per native run. See `verification/summary.json` and the actor handoff.

Agent visual review covers all families in representative poses and selected motion/station contexts. This is a complete asset candidate ready for owner review; ordinary roster integration and every-clip/layout continuous-motion acceptance remain separate.

Rebuild without generation: `python character/krusher-head-fit-v7/rebuild_all.py` from the project root. Full source/provenance and handoff: `character/krusher-head-fit-v7/`. No game export or game-repository commit was performed.
'''
(P/'README.md').write_text(readme)
html=P/'index.html';text=html.read_text();text=text.replace('Complete corrected head-fit candidate library; fresh station review remains.','Complete revised asset candidate; final native and sampled station checks passed. Owner review remains.');html.write_text(text)
# Keep the package builder's presentation current for later deterministic rebuilds.
builder=H/'build_package.py';text=builder.read_text();text=text.replace('corrected head-fit candidate; fresh station review pending','complete revised animation asset candidate; owner review pending').replace('Complete corrected head-fit candidate library; fresh station review remains.','Complete revised asset candidate; owner review remains.').replace('Repaired head source coverage is complete. Fresh world-context checks remain; this package does not install a normal playable crew member.','Revised source coverage is complete. Normal roster integration and owner visual acceptance remain separate.');builder.write_text(text)
for script in H.glob('*.py'):ast.parse(script.read_text(encoding='utf-8-sig'),filename=str(script))
print(json.dumps({'packageChecks':summary['packageChecks'],'nativeChecks':summary['nativeChecks'],'nativeFailures':0,'captures':352,'aliasConflicts':0,'scriptSyntaxChecked':len(list(H.glob('*.py')))}))
