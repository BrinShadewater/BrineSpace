from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;A=P.parent;R=A.parents[1]
generation=json.loads((P/'generation.json').read_bytes());assert generation['status']=='Success'
source=json.loads((P/'source-registration-v2.json').read_bytes());grade=json.loads((P/'stationary-grade-audit.json').read_bytes())
assert len(grade['rows'])==source['frameCount']==142
for name,expected in grade['bindings'].items():assert hashlib.sha256((P/name).read_bytes()).hexdigest()==expected,name
assert hashlib.sha256((P/'master-input.png').read_bytes()).hexdigest()==generation['imageSha256']==generation['lastImageSha256']
assert hashlib.sha256((P/'source.mp4').read_bytes()).hexdigest()==source['sourceSHA256']
source['visualReview']='All six complete raw and six registered alpha chronology boards, master/control/source board and stationary trouser detail board inspected October3,2026. No complete continuous/native/controller acceptance.'
(P/'source-registration-v2.json').write_text(json.dumps(source,indent=2)+'\n')
grade['visualReview']='Fixed region detail board inspected; brighter interior cloth confirmed, not accepted as master-matched grade.'
(P/'stationary-grade-audit.json').write_text(json.dumps(grade,indent=2)+'\n')
v3=json.loads((A/'AUDIT-v3.json').read_bytes());v3['visualReview']='Raw, original/old-action/new-key comparison and high-source control comparison viewed October3,2026; head matches, floor/cloth mismatch retained.'
(A/'AUDIT-v3.json').write_text(json.dumps(v3,indent=2)+'\n')
ledger=json.loads((A/'EXECUTIONS.json').read_bytes());ledger['v3']=dict(builtinExecution='exec-73bafe46-04cb-4573-bcbf-c068633b6eb4',status='terminal generated and reviewed; high-source head/detail improved, floor/cloth mismatch; not adopted',rawSHA256=hashlib.sha256((A/'raw-key-v3.png').read_bytes()).hexdigest(),inputRecord='HIGH_SOURCE_INPUT.json',prompt='high-source-prompt.txt')
ledger['originalActionVideo']=dict(taskId=generation['task_id'],status='terminal Success, downloaded and full-source reviewed; motion retained, interior cloth grade drift unresolved',estimatedUSD=generation['estimatedUSD'],billingVerified=False,sourceSHA256=source['sourceSHA256'],frames=142,durationMs=5917)
(A/'EXECUTIONS.json').write_text(json.dumps(ledger,indent=2)+'\n')
verdict=dict(status='Full stationary action source retained; original-master grade fails in interior; no normal adoption',all142SourcesKept=True,sourceAppearance='Head/height/floor stable; matte warm face and original equipment are much closer than selected soft action family. Arm draw/operate/stow visible in one action cycle. Pose boards do not certify continuous smoothness.',grade='Fixed original cloth mask below arm action: original62/61/60, video first63/62/62, middle71/71/70, last62/62/60. Coverage differs, but direct detail view corroborates interior brightening. Cannot accept merely because endpoints match.',registration='OutputH146/top77/floor222 equals unchanged input alpha control; originalH148/top76/floor223. Extraction erosion explains this difference, not demonstrated temporal scale drift. No per-frame refloor/rescale.',next='Resolve whole-source stationary material/detail preservation, then paired original helmet and native all-source/action-idle joins. Full Veld matrix/integration/polish remains.')
(P/'VERDICT.json').write_text(json.dumps(verdict,indent=2)+'\n')
page='<!doctype html><meta charset="utf-8"><title>Veld West scanner action</title><style>body{background:#202a30;color:white;font:16px system-ui;margin:24px}.row{display:flex;gap:36px;align-items:end}figure{margin:12px}img{image-rendering:pixelated}video{max-width:620px}button{padding:10px;font:inherit}a{color:#b7daee}</style><h1>Veld West scanner action</h1><p>Complete new action beside the original master. Her proportions stay steady; suit brightness during the action still needs correction.</p><button onclick="document.querySelectorAll(\'.replay\').forEach(i=>i.src=\'full-source-review-v2.png?v=\'+Date.now())">Replay action</button>'
for s in [47,93,148]:
 page+=f'<h2>Standing height {s}</h2><div class="row"><figure><img src="registered-reference.png" width="{256*s/148}"><figcaption>Original master</figcaption></figure><figure><img class="replay" src="full-source-review-v2.png" width="{256*s/148}"><figcaption>New complete action</figcaption></figure></div>'
page+='<h2>Original motion source</h2><video controls src="source.mp4"></video><p><a href="master-source-comparison-v2.png">Master comparison</a> · <a href="stationary-trouser-grade-review.png">Cloth comparison</a> · <a href="VERDICT.json">Findings</a></p>'
(P/'index.html').write_text(page,encoding='utf-8')
entry='''

## High-detail master and complete stationary action — October 3, 2026

prepare_high_source.py reconstructs original West native master byte-exact before
using unchanged high-source crop RGB on a1576square appearance guide. Both original
and high-source-control have top76/floor223. Builtin exec-73bafe46-04cb-4573-bcbf-c068633b6eb4
returns V3H150/top77/floor226/head27/axis133, clothpatch66/64/64. Original head
width/axis and detail improved, floor/cloth mismatches remain; no corrective scaling.
Raw/comparison/control boards viewed. Previous V1/V2 sources preserved.

original-action-video-v1: MiniMax448608910385602 terminalSuccess,6s768Psquare24fps,
142source frames/5917ms; estimatedUSD.28,billingunverified. Unchanged originalnative
standing3x on RGB12,18,24 is BOTH first/last image, no generated key supplied.
Frozen1/3offset0, darktolerance8/allforegroundcomponents>=20raw/onepixel erosion;
whole opaque RGB unchanged. All142retained;284APNG exactpixel/duration checks0.
Six raw and six registered chronologies plus master/control and cloth detail viewed.
SourceH146/head26..27/top77/floor222 is temporally stable; inputextractioncontrol
alsoH146/top77/floor222 vsoriginal148/76/223. No temporal shrink claim from erosion.

Full scanner draw/operate/stow retained as useful motion. Grade remains FAILED:
fixed original cloth-only mask below arms: master62/61/60;source0 63/62/62,
source71 71/71/70,source141 62/62/60. Different coverage does not itself prove colour
change, but direct detail confirms brighter interior trousers. Head/floor stability
and endpoint match do not accept entire sequence. No helmet/native/controller/normal
adoption. Next whole-source material preservation then paired original helmet,
all-source native action/idle joins, other directions/actions and full integration.
'''
with (A/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write(entry)
title='## Veld original West complete scanner action source review — October 3, 2026'
note=title+'\n\n'+entry.split('## High-detail master and complete stationary action — October 3, 2026\n\n')[1]+'\nLesson: high-density original source and native appearance input are distinct\ncontrolled trials. Rebuild the original export to prove extraction provenance.\nA stationary finite action can preserve head/boot registration while interior\ncloth brightens. Inspect below-arm fixed original material regions and direct\ndetails, not only overall pose medians or matching endpoints. Record extraction\ncontrol separately so deterministic erosion is not mislabeled model shrink.\nWhole-source generation still governs visual repair; no local palette/anatomy rescue.\nFull Veld objective active/incomplete; no live job. Evidence/HANDOFF:\ncharacter/veld-interact-west-original-master-v1.\n\n'
code=(R/'character/veld-carry-east-original-master-v1/record_native_milestone.py').read_text(encoding='utf-8')
exec('from pathlib import Path\nimport shutil,uuid,time\n'+code[code.index('paths=['):],dict(P=P,R=R,title=title,note=note))
print('142 complete source frames bound; 284 replay checks0; 12 chronology boards reviewed; grade unresolved')
