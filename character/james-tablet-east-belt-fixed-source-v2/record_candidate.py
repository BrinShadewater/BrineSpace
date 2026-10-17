from pathlib import Path
import json,os
P=Path(__file__).resolve().parent;R=P.parents[1]
g=json.loads((P/'generation.json').read_text());v=json.loads((P/'candidate-validation.json').read_text());assert g['status']=='Success' and not v['failures']
selection={'status':'full_motion_bare_helmet_candidate_native_pending','productionInstalled':False,'taskId':g['task_id'],'sourceSha256':json.loads((P/'checks.json').read_text())['sourceSha256'],'fullSourceFrames':141,'visualReview':'All141 raw body/head/bounded hand-tablet-belt poses and all141 candidate helmet head poses reviewed. Separate broad tablet draw/read/stow, wrench remains belt-attached; no repeat of v1 obvious yellow/green flash. Common East shell fit inspected.','masterRuler':'Same alpha>192 master/source crown25/sole171/H147. Fixed scale.25 retained, no additional resizing or per-pose translation. Earlier2px shortage estimate compared incompatible opacity evidence.','material':'One pooled neutral correction48,39,50 to48,43,47. Head/skin/gold protected by original fixed mask; pale tablet rear remains secondary concern.','checks':v,'remaining':['Complete paired motion playback/native anatomy and occlusion review','Normal loader selection order: paired base/equipment before larger South overrides','Replace sealed-meal East diagnostic source substitutes consistently','Normal full source action clock and actual approaches/fresh disk Continue','Full James cross-family material/proportions/perspective and other pending native contexts'],'billing':'Two source attempts estimated US$0.38 total; verified billing unavailable. v1 rejected with raw temporal-color evidence.'}
(P/'source-selection.json').write_text(json.dumps(selection,indent=2)+'\n',encoding='utf-8')
with (P/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('''

## Completed source and paired candidate milestone
Task447781086630402 terminal Success; no live generation. Raw source hash
bfb703cb939287b783e933dc2cfc6e341e5589f158144016ea5a32572751125d.
141frames/24fps, inverse ruler.25/-4,-4, zero extraction crop loss. All raw
body/head/tool poses reviewed; no repeat of obvious v1 flash; wrench belt-attached.
Fixed neutral suit gain[1,1.1025641026,.94], protects y<60 head, warm skin/gold;
can include neutral tablet casing/gloves/tools. Pale tablet rear still a concern.
Same opacity threshold confirms master/source both147px(crown25/sole171): no
resizing. Previous2px shorter estimate was not a same-threshold comparison.
Full paired141poses each; exact idle endpoints; interact5500ms,inspect6000ms;
source-authored stow, no reversed lift. Common accepted shell fit follows face,
angle0; all141 helmet head poses reviewed.1149packagechecks/0failures. Bare crown
25..26, helmet16..18, soles171; max adjacent crown step1. Encoded GIF6000ms.
Nothing installed; no native test run for this candidate. Old East wrench defect
still selected. Next: complete paired playback review, add consistent sealed-meal
East source substitutes, normal loader ordering, native all-source playback and
actual approaches/fresh Continue using scratch/fingerprint guard. Full goal active.
''')
note='''

## James East constant-light paired candidate — October 1, 2026

Task447781086630402 terminal Success, no generation live. v2 raw full141 source
body/head/tool poses reviewed: separate tablet and belt wrench maintained, no
repeat of obvious v1 yellow/green flash. One pooled neutral gain[1,1.1025641026,.94]
toward exact master, with head/skin/gold protection. Tablet rear remains pale.
Same alpha>192 comparison confirms master/source both147px,crown25,sole171;
retain fixed.25 inverse ruler, no resize/part edits/per-frame translation. Earlier
two-pixel shortage estimate was not a same-threshold comparison.

Staged full141 bare+141 common-shell poses, exact master idle endpoints, full
authored stow instead of reverse lift, interact5500ms/inspect6000ms. All141 helmet
heads reviewed; adjacent crown steps<=1px, soles171.1149packagechecks/0failures;
encoded paired-candidate.gif6000ms. Numeric checks do not certify tool identity,
motion quality or native behavior. No new selection/native run: old East wrench
defect remains installed. Next paired playback/native anatomy/occlusion, consistent
sealed-meal substitutes, normal loader order and actual approaches/fresh Continue.
Full James animation/master consistency and cross-family polish goal active.
'''
for path in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    data=path.read_bytes()
    if b'## James East constant-light paired candidate' in data:continue
    enc=note.encode('utf-8');new=enc.lstrip(b'\n')+b'\n'+data if path.name=='CURRENT_STATUS.md' else data+enc
    tmp=path.with_name(path.name+'.james-paired-candidate.tmp');tmp.write_bytes(new);os.replace(tmp,path)
(P/'index.html').write_text('<!doctype html><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{background:#303b40;color:white;font:18px system-ui;max-width:1288px;margin:auto}img,video{max-width:100%}</style><h1>James East separate-tablet candidate</h1><p>Full source motion, fixed neutral material correction and selected common helmet. Exact idle endpoints. Staged; native selection/playback and Continue checks pending.</p><img src="paired-candidate.gif"><img src="master-material-comparison.png"><video src="source.mp4" controls loop></video>',encoding='utf-8')
print('Source/candidate evidence and five guides updated;1149 checks pass; no runtime selection.')
