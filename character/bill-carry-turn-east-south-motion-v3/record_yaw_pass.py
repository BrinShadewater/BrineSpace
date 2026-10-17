from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1]
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
e=json.loads((P/'generation-evidence.json').read_text())
e['outputs']['bare-v8']='exec-75261a86-0eb0-492f-b197-50a0f53cb1bf'
for bucket,filename in [('prompts','sources/prompt-bare-v8.txt'),('rawSources','sources/bare-v8.png')]:e[bucket]['bare-v8']={'file':filename,'sha256':digest(P/filename)}
e['candidates']['bare-v8']='Only third source cell adopted over v7: clearer coordinated head/collar/chest/shoulder/case/stance yaw toward front. Other cells excluded. Original v7 first-figure148/682 ruler and frozen pooled v7 grade retained; other three interior packaged frames exact both gears. No degree-angle proof or normal selection.'
e['registration']=json.loads((P/'registration.json').read_text())
e['remaining']='First two views still close. Nearfront shoulder/case silhouette, actual case dimensions, master head/face shading and fullmotion/native/endpoint review open before normal selection.'
(P/'generation-evidence.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
s=json.loads((P/'staging-evidence.json').read_text())
s.update(checks=65,scope='65 staged package checks, including unchanged other interiors and frozen grade; raw v8 source/paired12pose board/browser middlephase3 reviewed; no Godot/native NPC selection',previousGoalTurn='progress:new whole body build/calibration/master width comparison',currentProgress='Locally authored coordinated third body yaw fitted at existing ruler and grade, exact other pose preservation verified',selectedRuntime=False)
for filename in s['sha256']:s['sha256'][filename]=digest(P/filename)
for filename in ['sources/bare-v8.png','sources/prompt-bare-v8.txt','sources/material-grade-v7.json']:s['sha256'][filename]=digest(P/filename)
(P/'staging-evidence.json').write_text(json.dumps(s,indent=2)+'\n',encoding='utf-8')
old='Unselected East/South whole-turn uses newly authored bare-v7 full body source plus\nexisting isolated helmet components.'
new='Unselected East/South whole-turn uses bare-v7 body sources, with only the third\ncell replaced by locally authored bare-v8 coordinated yaw, plus isolated helmets.'
lesson='''
Latest local yaw refinement: third body/face/collar/shoulder/case/stance now turns
more clearly toward front. Same148/682 source ruler; no individual normalization.
Frozen pooled v7 grade applied to all poses. Other three interior frames remain
byte-exact both gears.65package checks pass; raw/paired12pose board/browser middle
phase3 reviewed. No normal selection or new Godot run. First two angles, master
build/face shading and actual case dimensions remain open.

Local pose edits should freeze the established shared grade when preserving
other frames: recomputing pooled material medians can recolor untouched poses.
Adopt only the requested source cell and check packaged pixels, not just source
preservation. A coherent middle pose helps yaw but does not prove loop smoothness.
'''
for filename in ['docs/CURRENT_STATUS.md','docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 path=R/filename;text=path.read_text(encoding='utf-8')
 assert old in text,filename
 text=text.replace(old,new,1)
 marker='## Bill carry-turn build refinement — October 1, 2026\n'
 text=text.replace(marker,marker+lesson,1)
 path.write_text(text,encoding='utf-8')
Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').write_bytes((R/'skills/brinespace-character-pipeline/references/crew-consistency.md').read_bytes())
with (P/'HANDOFF.md').open('a',encoding='utf-8') as out:out.write('\n## Coordinated middle yaw refinement — October 1, 2026\n'+lesson+'\nChanged third staged frame both gears, builder/verifier/source/prompt/registration/grade evidence and maintained references. Next compare case dimensions separately, master shoulder/face/material fit, motion and held endpoint joins before normal matrix/native selection. Full objective remains active/incomplete.\n')
print('65-check staged source evidence and existing current milestone updated.')
