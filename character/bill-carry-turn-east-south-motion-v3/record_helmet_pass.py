from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1]
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
e=json.loads((P/'generation-evidence.json').read_text())
key='helmet-components-v3'
e['outputs'][key]='exec-0df46584-797a-4d2f-8bba-f3459cf3be12'
for bucket,filename in [('prompts',f'sources/prompt-{key}.txt'),('rawSources',f'sources/{key}.png')]:e[bucket][key]={'file':filename,'sha256':digest(P/filename)}
e['candidates'][key]='Isolated full head/collar strip staged over exact existing candidate bodies; clearer later frontal progression. First two angles remain close. One complete first-head ruler calibrated to pooled canonical east/south component heights; no per-pose normalization.'
e['candidates']['helmet-v1']='Prior clustered helmet components superseded in staging by isolated components-v3; raw reference retained.'
e['registration']=json.loads((P/'registration.json').read_text())
e['remaining']='Body/shoulder build remains broader than masters; early body/head angles close. Further whole-turn master silhouette, material and cadence polish before normal selection/native NPC review.'
(P/'generation-evidence.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
s=json.loads((P/'staging-evidence.json').read_text())
s.update(checks=57,scope='57 staged package checks; raw isolated helmets and paired12pose/crop board reviewed; browser phase3 at148 andphase4 at82; no Godot/native NPC selection',previousGoalTurn='progress:lower hardware authored and fitted, rejected helmet source preserved',currentProgress='New isolated helmet source authoring, canonical component calibration, paired fit, visual browser checks and maintained evidence',selectedRuntime=False)
for filename in s['sha256']:s['sha256'][filename]=digest(P/filename)
for filename in ['sources/helmet-components-v3.png','sources/helmet-master-crops.png','sources/prompt-helmet-components-v3.txt','index.html']:s['sha256'][filename]=digest(P/filename)
(P/'staging-evidence.json').write_text(json.dumps(s,indent=2)+'\n',encoding='utf-8')
note='''## Bill carry-turn isolated helmet fit — October 1, 2026

Staged East/South whole-motion candidate now uses four built-in authored isolated
helmet/face/collar components rather than regenerated full equipped figures.
Later angles progress more clearly toward front; first two remain close.
Body ruler148/595 unchanged. Independent head sheet uses one complete first-head
ruler against the pooled median height of exact current East/South canonical
helmet components (38/42px ->40px); all four heads share that scale. No per-pose
normalization. Upper bare-v4/lower bare-v5 bodies stay identical between gears
outside bounded head fit. Original selected cardinal endpoints/clocks unchanged.
57package checks pass. Raw source, paired12pose/crop board and browser phase3
at148/phase4 at82 reviewed. Candidate remains unselected; shoulders/body still
broader than masters and early angles need polish. Normal matrix-v5/inventory
unchanged; no new Godot/native NPC/contact/Continue or owner acceptance evidence.

Lesson: isolated head authoring avoids adopting unrelated body drift. Independently
authored component sheets need a recorded complete canonical component ruler,
shared across all angles, rather than an inherited unrelated whole-body density.
Correct size and paired pixel protection do not certify silhouette or smooth yaw.

'''
for filename in ['docs/CURRENT_STATUS.md','docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 path=R/filename
 if not path.read_bytes().startswith(note.encode('utf-8')):path.write_bytes(note.encode('utf-8')+path.read_bytes())
Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').write_bytes((R/'skills/brinespace-character-pipeline/references/crew-consistency.md').read_bytes())
with (P/'HANDOFF.md').open('a',encoding='utf-8') as out:
 out.write('\n'+note+'Next: authored body/shoulder silhouette repair at unchanged source stature; review earlier yaw spacing, material continuity and endpoint joins before matrix/native selection. Full set objective remains incomplete. Changed staged build/verify/frames/registration/grade/review/evidence, source/prompt/reference builder, maintained docs and skill mirror.\n')
print('57-check staging evidence, source provenance and current handoff recorded.')
