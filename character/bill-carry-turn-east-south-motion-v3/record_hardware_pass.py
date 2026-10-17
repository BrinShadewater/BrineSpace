from pathlib import Path
import json, hashlib
P=Path(__file__).resolve().parent
R=P.parents[1]
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
e=json.loads((P/'generation-evidence.json').read_text())
for key,execution in [('bare-v5','exec-00d0770b-b5d1-47ba-88b7-67216c35920e'),('helmet-v2','exec-3dc8d5b9-5593-4d4b-9cb4-2c830cc362be')]:
 e['outputs'][key]=execution
 for bucket,filename in [('prompts',f'sources/prompt-{key}.txt'),('rawSources',f'sources/{key}.png')]: e[bucket][key]={'file':filename,'sha256':digest(P/filename)}
e['candidates']['bare-v5']='Lower source rows630 onward used over exact v4 upper source; slimmer soles and elongated knee hardware. Whole generated upper body excluded. Still staged.'
e['candidates']['helmet-v2']='Reference only, rejected for adoption: modest angle progression but larger shell, altered body proportions and density. Helmet-v1 components remain staged; angle repair still needed.'
e['registration']=json.loads((P/'registration.json').read_text())
e['remaining']='Master helmet angle/silhouette fit, quarter motion and native review before normal selection; full animation goal remains open.'
(P/'generation-evidence.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
s=json.loads((P/'staging-evidence.json').read_text())
s.update(scope='47 staged package checks; raw sources and paired12pose native-size/crop board reviewed; no new browser or Godot runtime review this pass',currentProgress='Targeted authored lower hardware fitted below source row630; exact upper source retained; enlarged helmet attempt retained as rejected reference',selectedRuntime=False)
for filename in s['sha256']: s['sha256'][filename]=digest(P/filename)
s['sha256']['sources/bare-v5.png']=digest(P/'sources/bare-v5.png')
s['sha256']['sources/helmet-v2.png']=digest(P/'sources/helmet-v2.png')
(P/'staging-evidence.json').write_text(json.dumps(s,indent=2)+'\n',encoding='utf-8')
note='''## Bill carry-turn hardware refinement — October 1, 2026

Unselected East/South whole-motion candidate now fits built-in authored bare-v5
lower hardware from source row630 onward over exact bare-v4 upper source pixels.
Boot soles are slimmer and knee plates longer; the fixed148/595 ruler, planted
feet, paired suit pixels and exact held endpoints remain.47package checks pass;
raw sheets and paired12pose/native crop board reviewed. Helmet-v2 attempt is
retained as a rejected reference: modest angle progression but enlarged shell
and changed body density. Helmet-v1 remains staged; angle and master build fit
still open. Normal matrix-v5/selected inventory unchanged. No Godot/native NPC
or new browser motion review this pass. No full-set or owner acceptance claim.

Lesson: use only the requested generated hardware region when a targeted edit
also changes protected anatomy. Head angle progress does not justify adopting
a larger shell or changed source density. Preserve rejected source and prompt.

'''
for filename in ['docs/CURRENT_STATUS.md','docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 path=R/filename; old=path.read_bytes(); path.write_bytes(note.encode('utf-8')+old)
installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')
installed.write_bytes((R/'skills/brinespace-character-pipeline/references/crew-consistency.md').read_bytes())
with (P/'HANDOFF.md').open('a',encoding='utf-8') as out:
 out.write('\n'+note+'Next: correct helmet angles at canonical shell size, then review motion/master fit before native selection. Changed build.py, staged frames/registration/grade/review/evidence, two raw sources/prompts, maintained docs and skill mirror. No normal loader changes.\n')
print('Source evidence, staged hashes, handoff and current pipeline references updated.')
