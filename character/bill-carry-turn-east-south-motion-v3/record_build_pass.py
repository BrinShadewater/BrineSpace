from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1]
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
e=json.loads((P/'generation-evidence.json').read_text())
for key,execution in [('bare-v6','exec-fd279c19-b8a1-4222-9e3a-8dff534e1c90'),('bare-v7','exec-4ac31650-e446-48bb-b8d3-46d933326022')]:
 e['outputs'][key]=execution
 for bucket,filename in [('prompts',f'sources/prompt-{key}.txt'),('rawSources',f'sources/{key}.png')]:e[bucket][key]={'file':filename,'sha256':digest(P/filename)}
e['candidates']['bare-v6']='Rejected for staging: source stature grew to663/664/664/660 despite requested595. Independent fixed-ruler diagnostic gave only modest width improvement; v7 closer.'
e['candidates']['bare-v7']='Staged new whole-body strip. Source density changed:682/688/685/686, so new fixed148/682 first-complete-figure ruler applies toall4 without individual normalization. Shoulder/case bands narrower; native heights148/149.30/148.65/148.87. Still broader than exact masters, early yaw clustering/head/case/detail matching open.'
e['registration']=json.loads((P/'registration.json').read_text())
e['remaining']='Near-front shoulder58vs53master; arm/waist/case band63vs57master. Early head/body yaw clusters. Check actual case dimensions separately from the aggregate silhouette; panel/face/material and native whole-motion/endpoint joins remain before normal selection.'
(P/'generation-evidence.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
s=json.loads((P/'staging-evidence.json').read_text())
s.update(checks=58,scope='58 staged package checks; raw sources/fixed-density comparison/paired12pose board and browser nearfrontphase4 reviewed; no Godot/native NPC selection',previousGoalTurn='progress:isolated helmets fitted and master component calibration verified',currentProgress='Whole-body slimming source authored; new independent shared source ruler; measured master band comparison and preserved rejects',selectedRuntime=False)
for filename in s['sha256']:s['sha256'][filename]=digest(P/filename)
for filename in ['sources/bare-v6.png','sources/bare-v7.png','build-width-audit.json','build-source-comparison.json','build-source-comparison.png']:s['sha256'][filename]=digest(P/filename)
(P/'staging-evidence.json').write_text(json.dumps(s,indent=2)+'\n',encoding='utf-8')
note='''## Bill carry-turn build refinement — October 1, 2026

Unselected East/South whole-turn uses newly authored bare-v7 full body source plus
existing isolated helmet components. Slimmer shoulder/arm/case silhouette: near
front shoulder62->58px and waist/arm/case band69->63px; canonical front53/57px,
so still needs refinement. Measurements are alpha image bands, not separate
anatomy or case dimensions. Raw v6/v7 edits enlarged source stature despite fixed
coordinates. v6 retained rejected. v7 density682/688/685/686 uses one complete
first-figure148/682 ruler across all4; native148/149.30/148.65/148.87px, no per-pose
normalization. This supersedes prior v4upper/v5lower staging; old review retained.
Helmet sheet retains shared pooled canonical component ruler. Paired body pixels,
exact selected endpoints and original clocks preserved.58package checks pass.
Raw sources, independent-density diagnostic board, paired12pose/crops and browser
near-frontphase4 reviewed. Normal matrix-v5/inventory unchanged; no native NPC,
room contact/Continue or full-set acceptance claim. Early yaw, shoulder build,
face/head/case scale/detail and material/endpoint continuity still open.

Lesson: explicit source coordinate prompts can still change source density.
Measure before adopting. Independently regenerated strips may use one recorded
complete-figure ruler across every pose; never normalize each pose independently
or silently keep an unrelated prior density. Aggregate arm/case width diagnostics
do not prove the carried object's own size or anatomical consistency.

'''
for filename in ['docs/CURRENT_STATUS.md','docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 path=R/filename
 if not path.read_bytes().startswith(note.encode('utf-8')):path.write_bytes(note.encode('utf-8')+path.read_bytes())
Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').write_bytes((R/'skills/brinespace-character-pipeline/references/crew-consistency.md').read_bytes())
with (P/'HANDOFF.md').open('a',encoding='utf-8') as out:out.write('\n'+note+'Next: match shoulder/arm build and actual case dimensions independently, improve early head/body yaw and master face/material match, then native whole-motion comparison before normal selection. Full goal active/incomplete. Changed staged builder/verifier/frames/calibration/review/evidence, two sources/prompts, band/source diagnostics, maintained docs and installed skill mirror.\n')
print('58-check staging evidence and master-width findings recorded.')
