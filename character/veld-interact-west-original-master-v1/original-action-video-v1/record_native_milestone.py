from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;A=P.parent;R=P.parents[2];N=R/'output/veld-west-interact-source-v1'
validation=json.loads((N/'validation.json').read_bytes());assert validation['passed']
inputs=json.loads((N/'inputs-after.json').read_bytes());assert all(hashlib.sha256((R/name).read_bytes()).hexdigest()==sha for name,sha in inputs.items())
audit=json.loads((P/'uneroded-source-audit.json').read_bytes());audit['visualReview']='All six uneroded source chronology boards, master/old/new-control comparison and paired fitting board viewed October3,2026. No visible isolated halo in inspected boards; full finish acceptance remains open.'
(P/'uneroded-source-review.json').write_text(json.dumps(audit,indent=2)+'\n')
native=json.loads((P/'native-review.json').read_bytes());native['visualReview']='All six native142-pose gear chronology boards inspected and both complete source035 native presentations at47/93/148 beside original master and actual selected idle viewed. Static source-clock evidence; no continuous scene/controller acceptance.'
(P/'native-visual-review.json').write_text(json.dumps(native,indent=2)+'\n')
verdict=dict(status='Complete paired142-source West scanner action staged and native appearance reviewed; full material/idle joins/runtime acceptance open',registration='Uniform omission of one raw pixel erosion restores originalH148/top76/floor223 in control and all142source poses; headband28/axis132.5 constant vsoriginal27/133. No RGB, source motion, per-pose scale/registration changes.',gradeCorrection='Prior differing-coverage median exaggerates a pure grade comparison. Identical141pixels in ALL eroded frames/control: original68/68/67,first66/66/65,middle70/69/69,last65/65/63. Uneroded222commonpixels: original65/64/63,first64/63/62,middle68/67/67,last62/61.5/60. Residual brightness and changed folds/panel appearance remain; fixed spatial pixels are not guaranteed anatomical correspondence.',equipment='Unchanged original West mixed-v5 whole33x39 shell005 at constant116,65; clear117,76,150,103; all source bodies outside fitting exact. No per-frame helmet fitting or recolouring.',native=dict(checks=577,failures=0,presentations=284,seconds=validation['seconds'],inputsUnchanged=445,ownerProfileFilesUnchanged=validation['realProfileFileCount'],replayChecks=568),next='Resolve stationary fabric/detail preservation and review full continuous action/idle handoffs before normal adoption; other cardinal action/cargo/furniture/water/death/integration/polish remain.')
(P/'NATIVE_SOURCE_VERDICT.json').write_text(json.dumps(verdict,indent=2)+'\n')
page='<!doctype html><meta charset="utf-8"><title>Veld West scanner comparison</title><style>body{background:#202a30;color:#eee;font:16px system-ui;margin:24px}.row{display:flex;gap:32px;align-items:end}figure{margin:12px}img{image-rendering:pixelated}button{padding:10px 16px;font:inherit;margin-right:8px}a{color:#b7daee}</style><h1>Veld West scanner comparison</h1><p>Complete scanner action beside the original master and current idle. Height and helmet placement are stable. Suit finish and the handoff to idle remain under review.</p><button onclick="setGear(\'bare\')">Standard</button><button onclick="setGear(\'helmet\')">Helmet</button><button onclick="setGear(gear)">Replay</button>'
for s in [47,93,148]:
 page+=f'<h2>Standing height {s}</h2><div class="row">'
 for role,label in [('action','New scanner action'),('master','Original master'),('idle','Current idle')]:page+=f'<figure><img class="{role}" width="{256*s/148}"><figcaption>{label}</figcaption></figure>'
 page+='</div>'
page+='<p><a href="bare-native-full-source.png">Standard game-size comparison</a> · <a href="helmet-native-full-source.png">Helmet game-size comparison</a> · <a href="uneroded-master-control-comparison.png">Detail comparison</a></p><script>let gear="bare";function setGear(g){gear=g;document.querySelectorAll(".action").forEach(i=>i.src=g+"-full-source-review-uneroded.png?v="+Date.now());document.querySelectorAll(".master").forEach(i=>i.src=g+"-original-reference.png");document.querySelectorAll(".idle").forEach(i=>i.src=g+"-selected-idle.png")}setGear(gear)</script>'
(P/'native-comparison.html').write_text(page,encoding='utf-8')
entry='''

## Complete paired West source native/control correction — October 3, 2026

Common-pixel diagnostic qualifies earlier large cloth-median claim: differing
opaque coverage exaggerated pure grade comparison. Fixed141pixels common to all
eroded frames/control:original68/68/67,first66/66/65,middle70/69/69,last65/65/63.
Uniform alpha-only removal of one-raw-pixel erosion restores originalH148/top76/
floor223 in control and ALL142source poses; constant headband28/axis132.5 vsoriginal
27/133. Uneroded222commonpixels:original65/64/63,first64/63/62,middle68/67/67,
last62/61.5/60. Residual finish/folds/panels differ; spatialpixels are not guaranteed
anatomical correspondence. Retain prior eroded evidence, no retrospective rewrite.

New full142 paired source package/finite manifests/994buildchecks0. Whole original
West mixed-v5shell00533x39 atconstant116,65; clear117,76,150,103; body outsidefitting
exact, no per-frame helmfit. Both142source replays, original references and actual
selectedidle comparison exports. All six alpha/noerosion source boards/control/
paired fitting board viewed. tests/test_veld_west_interact_source_v1.gd+.uid,
tools/run_veld_west_interact_source_v1.py:577nativechecks0/284presentations10.35s,
engine0/no errors/445inputs and2931ownerfilesunchanged in scratchAPPDATA.
568nativeAPNGpixel/durationchecks0; six complete gear chronology boards and both
whole native035 at47/93/148 inspected. New source is materially closer than old
cool oversized selectedinteriors, but full material/continuous motion/idle joins/
normal controller/save integration acceptance remains open. No normal selector
change or new paid generation. Source record/445native bindings now frozen.

Lesson: test exact unchanged input through alpha extraction before interpreting
output bounds. Uniform erosion can consume original head/sole details; where the
background permits, retain meaningful component edges and compare at one ruler.
Use identical common-opaque reference pixels to distinguish grade changes from
sample coverage; still inspect geometry/texture directly. Do not claim a shape
or material fix from a narrower statistical mask. Next source finish/idle joins,
other directions/full source matrix/integration/cross-library polish. Goal active.
'''
with (A/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write(entry)
title='## Veld paired West scanner native source and alpha-control correction — October 3, 2026'
note=title+'\n\n'+entry.split('## Complete paired West source native/control correction — October 3, 2026\n\n')[1]+'\nHandoff:character/veld-interact-west-original-master-v1/HANDOFF.md.\n\n'
code=(R/'character/veld-carry-east-original-master-v1/record_native_milestone.py').read_text(encoding='utf-8')
exec('from pathlib import Path\nimport shutil,uuid,time\n'+code[code.index('paths=['):],dict(P=P,R=R,title=title,note=note))
print('Native milestone recorded;445bound inputs still stable; grade/normal acceptance open')
