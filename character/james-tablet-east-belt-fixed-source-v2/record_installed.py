from pathlib import Path
import json,os
P=Path(__file__).resolve().parent;R=P.parents[1]
native=json.loads((P/'validate-evidence.json').read_text());routes=json.loads((P/'native-arrival-continue-evidence.json').read_text());wrappers=[json.loads((P/name).read_text()) for name in ['validate-validation.json','native-arrival-continue-validation.json']]
assert native['failures']==0 and routes['failures']==0 and routes['mismatches']==0 and len(routes['results'])==8
assert all(w['exitCode']==0 and not w['timedOut'] for w in wrappers)
status='installed_native_verified_owner_review_pending'
selection=json.loads((P/'source-selection.json').read_text());selection.update(status=status,productionInstalled=True,nativeLoader=native,actualApproachesContinue=routes,profileGuards=[{'realProfileUnchanged':w['realProfileUnchanged'],'profileDelta':w['profileDelta']} for w in wrappers],remaining=['Owner full-motion review and pale tablet rear material judgment','Workstation-specific rotations, actual gear/locker transitions, exterior and furniture contexts','Full James animation/master consistency and cross-family polish; North sleep breathing next'])
(P/'source-selection.json').write_text(json.dumps(selection,indent=2)+'\n',encoding='utf-8')
(P/'selection.json').write_text(json.dumps({'status':status,'runtimeInstalled':True,'fullSetComplete':False,'sourceSelection':'source-selection.json','rawSourceFrames':141,'pairedFrames':282,'nativeLoaderChecks':native['checks'],'routeContinueChecks':routes['checks'],'failureCount':0},indent=2)+'\n',encoding='utf-8')
for mode in ['bare','helmet']:
    file=P/(mode+'-manifest.json');m=json.loads(file.read_text());m['status']=status;file.write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
evidence=P/'paired-candidate-evidence.json';e=json.loads(evidence.read_text());e['productionInstalled']=True;e['limits']=['Selected through normal loader, all East references verified; eight dry generic approaches and fresh midpoint Continues pass.','Compatibility sealed meals now use new East source indices0,32,60,86,123,140; actual closed-helmet life stages play full inspect-east.','Numeric evidence is scoped; owner/full-set/native furniture and gear/locker/exterior acceptance remain separate.'];evidence.write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
(P/'HANDOFF.md').write_text('''# Project handoff

Updated:2026-10-01 · Project:Brine Space · Task:James East separate-tablet replacement

## Objective and acceptance
Full James animations/master/style/perspective/size/proportion/grade consistency,
then cross-family polish. Goal active. This East replacement installed, native
verified; owner review and full-set/native-context acceptance remain incomplete.

## Accepted decisions and constraints
Wrench remains belt-attached; separate tablet faces James. Exact East master,
fixed.25 inverse ruler/-4,-4, no extra resize/part edits/per-frame translation.
All141 authored source poses and actual stow retained, exact master idle endpoints.
One pooled neutral gain[1,1.1025641026,.94]; skin/gold/head protected. Common shell
tracks face, rotation0. v1 rejected raw yellow/green temporal flash; no pose deletion.

## Current state
New bare/helmet manifests override East interact/inspect; sealed compatibility
eat/drink six slots updated to source0,32,60,86,123,140 with original clocks.
scripts/grid_canvas.gd loads pair after material family and before larger South
overrides; character/ACTIVE_ASSETS.json records paths. Original sources preserved.
Raw v2 bfb703cb939287b783e933dc2cfc6e341e5589f158144016ea5a32572751125d.
Installed141poses per mode; interact5500ms,inspect6000ms with terminal500ms hold.
Same alpha>192 master/source H147,crown25,sole171. Earlier2px estimate was not
same-threshold evidence. Bare crown25..26,helmet16..18,sole171,adjacent crown<=1.

## Verification
1183packagechecks/0failures including sealed substitutions;2356normal native
loader checks/0failures/4captures.4798actual route checks/0failures/0mismatches,
8collision-checked generic dry48unit approaches,four facings/bare+helmet;
all1146selected directional diagnostic slots through NPC.update,8fresh-scene
midpoint disk Continues exact actor/playback/clock/pause/pixels,normal6s completion
and need relief.24native scene captures reviewed with fixed center details;
all actors visible, East tablet/read/stow body and belt wrench visible. These are
three captures per route, not continuous native video or all context acceptance.
Engines0/no timeout/scratch APPDATA. Both strict guards false,last_session.json
only; cause unproven. No profile rollback. Native .gd/.uid pairs retained.

## Next action
North sleep: new all-six-pose clock review records current960ms loop, source
poses6,7,8,9,10,6,exact first/last. Review breathing cadence/motion before changing
it; no rest art/timing changes yet. Preserve exact lying/get-up handoffs and test
normal bunk/native Continue after a real revision. Broader full-frame master and
furniture/rotations/gear-locker/exterior/travel/context polish remains. Pale East
tablet rear is still a material concern. No generation or native process live.
''',encoding='utf-8')
note='''

## James East separate-tablet native replacement — October 1, 2026

New v2 selected through normal grid loader after material pair/before South
pivot overrides; ACTIVE_ASSETS records bare/helmet. Full141poses each, exact idle
endpoints; interact5500ms/inspect6000ms. Sealed compatibility eat/drink six-source
bindings now0,32,60,86,123,140; actual closed-helmet life selects full inspection.
1183package/2356native loader checks pass.4798route checks pass:8actual generic
dry collision-checked approaches,four facings/bare+helmet,all1146 diagnostic
source slots in NPC.update,8fresh-scene midpoint disk Continues exact actor/clock/
playback/pause/pixels,normal6s completion/need relief.24scene views reviewed;
East wrench belt-attached and tablet visible through read/stow. Captures are
three per route, not all-frame native video or furniture/locker/exterior proof.
Engines0,no timeout,scratch. Both strict guards false,last_session.json only,
cause unproven; no rollback. New candidate/fixture .gd/.uid pairs kept.

Current inventory329bare/4232references,239helmet/3716references,zero retained;
coverage only, not full-set visual acceptance. Four representative diagnostic/
meal family boards refreshed; East grade/height matches scoped master checks.
Pale tablet rear remains concern. Next North sleep breathing: all6current poses
review board/source clocks saved in james-north-rest-polish-v1; current960ms loop,
source6,7,8,9,10,6,exact seam. No rest timing/art changes yet. Full James goal active.
'''
for path in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    data=path.read_bytes()
    if b'## James East separate-tablet native replacement' in data:continue
    enc=note.encode('utf-8');updated=enc.lstrip(b'\n')+b'\n'+data if path.name=='CURRENT_STATUS.md' else data+enc;tmp=path.with_name(path.name+'.james-east-native.tmp');tmp.write_bytes(updated);os.replace(tmp,path)
(P/'index.html').write_text('<!doctype html><style>body{background:#303b40;color:white;font:18px system-ui;max-width:1288px;margin:auto}img{max-width:100%}</style><h1>James East separate tablet</h1><p>Installed bare/shared helmet full motion. 2356 normal-loader and 4798 actual approach/Continue checks pass. Owner review and full-set polish pending.</p><img src="paired-candidate.gif"><img src="native-arrival-continue-review.png"><img src="master-material-comparison.png">',encoding='utf-8')
print('Installed East native milestone recorded; goal remains full-scope active; no live jobs.')
