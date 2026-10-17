from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1]
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
e=json.loads((P/'generation-evidence.json').read_text());e['outputs']['case-v9']='exec-d2dd0867-c222-4149-b5ea-cb63e11f9236'
for bucket,filename in [('prompts','sources/prompt-case-v9.txt'),('rawSources','sources/case-v9.png')]:e[bucket]['case-v9']={'file':filename,'sha256':digest(P/filename)}
e['candidates']['case-v9']='Only bounded case/glove/lowerforearm native components from cells0/1/2 staged over existing paired bodies at fixed body ruler. Fourth front-facing case too deep; component retained as rejected diagnostic, previous front case kept. Other generated body pixels excluded. Case yaw/pitch/object size continuity still unproven.'
e['skinCorrection']={'recipe':'sources/material-grade-skin-v9.json','scope':'One shared correction for independently regenerated bare heads; same gains all4interiors; all other material gains unchanged. Old frozen gain was from earlier darker source, inappropriate for new body sheets. Post-pass pooled skin165/109/81 vs158/104/77endpoints; threshold populations change,not exact equality.'}
e['registration']=json.loads((P/'registration.json').read_text());e['remaining']='Master shoulder/head proportions and case yaw/pitch/height continuity, early angle spacing and native fullmotion/contact/Continue review before normal selection.'
(P/'generation-evidence.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
s=json.loads((P/'staging-evidence.json').read_text());s.update(checks=74,scope='74 staged package checks; shared skin/non-skin protection and exact bounded case fits first3bothgears; raw/master case crops/diagnostic/currentpairedboard/browser middlephase3 reviewed;no Godot/native NPC selection',previousGoalTurn='progress:coordinated third yaw authored with exact other pose preservation',currentProgress='Stale bare skin grade diagnosed/corrected once for all4; new case/grip source and bounded first3fits; rejected overdeep frontal component retained',selectedRuntime=False)
for filename in s['sha256']:s['sha256'][filename]=digest(P/filename)
for filename in ['sources/case-v9.png','sources/prompt-case-v9.txt','sources/material-grade-skin-v9.json','material-case-audit.json','material-case-review.png','case-fit-diagnostic.json','case-fit-diagnostic.png']+[f'sources/component-case-v9-{i:03}.png' for i in range(1,5)]:s['sha256'][filename]=digest(P/filename)
(P/'staging-evidence.json').write_text(json.dumps(s,indent=2)+'\n',encoding='utf-8')
note='''
Latest material/case refinement: stale brightening gains from earlier dark bare
heads were reused after whole-source changes. Shared bare skin correction now
applies0.8/0.859504/0.875 to prior RGB gains across all4interiors; other material
gains unchanged. Pooled graded skin197.5/121/88 ->165/109/81 versus canonical
158/104/77. Mask threshold populations change; not exact material/lighting proof.
Authored case-v9 bounded glove/case/lowerforearm components adopted for first3
interiors both gears at existing body ruler. Fourth generated frontal case too
deep; retained rejected diagnostic and original near-front case kept.74package
checks pass; protected pixels/alpha outside intentional head and case edits,
exact fit components, paired bodies, endpoints/clocks/soles verified. Raw/native
case crops/fit diagnostic/paired12pose board and browser middlephase3 reviewed.
Normal selection unchanged; no Godot/native NPC/contact/Continue acceptance.
Case pitch/size/hold-height continuity and master body/head build remain open.

Lesson: freezing an old shared grade protects local same-palette edits but is
wrong after independently regenerated material populations change. Re-audit
source family, recalibrate once for the whole set, preserve all non-target gains.
Case silhouette must be judged with hands and perspective; larger depth in side
view does not justify the same increase in the front view. Preserve rejected
components and keep visual acceptance separate from protected-pixel checks.
'''
marker='## Bill carry-turn build refinement — October 1, 2026\n'
for filename in ['docs/CURRENT_STATUS.md','docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 path=R/filename;text=path.read_text(encoding='utf-8');assert marker in text;path.write_text(text.replace(marker,marker+note,1),encoding='utf-8')
Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').write_bytes((R/'skills/brinespace-character-pipeline/references/crew-consistency.md').read_bytes())
with (P/'HANDOFF.md').open('a',encoding='utf-8') as out:out.write('\n## Shared face material and bounded case refinement — October 1, 2026\n'+note+'\nChanged staged builder/verifier/frames, shared skin recipe and audit/diagnostics, generated case source/prompt and components, source/registration/hashes/current milestone references. Next master head/body build and coherent case pitch/dimensions/hold heights through all angles, then actual native whole-motion before normal selection. Full goal active/incomplete.\n')
print('74-check staged material/case source provenance and current milestone updated.')
