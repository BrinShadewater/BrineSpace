from pathlib import Path
import json,os
P=Path(__file__).resolve().parent
g=json.loads((P/'generation.json').read_text());c=json.loads((P/'checks.json').read_text());assert g['status'].lower()=='success' and c['frames']==141 and c['clippedFrames']==0
review={'status':'generated_full_source_pending_material_motion_review','productionInstalled':False,'taskId':g['task_id'],'sourceSha256':c['sourceSha256'],'frames':141,'fps':24,'fixedScale':c['fixedScale'],'offset':c['offset'],'newAuthoredMotion':True,'reference':'reference.json','prompt':'prompt.txt','initialReview':'18 full-body source samples inspected: separate rectangular tablet appears, belt wrench remains visible in sampled lift/read/stow; no source crop loss. Full141-frame prop/motion review remains.','concerns':['Source sample82 appears warmer than neighboring read poses; quantify and review fixed source-level material treatment, never per-pose normalization.','Tablet rear casing too pale versus graphite prompt; material review needed.','Complete source hand/prop/body/head and master ruler comparison','Shared shell fitting and exact selected endpoints','Normal loading/action clocks/generic approaches/disk Continue before selection'],'billing':'Recorded submission estimate only; verified billing unavailable.'}
(P/'source-selection.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
h=P/'HANDOFF.md';s=h.read_text(encoding='utf-8');s=s.replace('New generation pending;','New source generated successfully (141frames/24fps/zero crop loss);').replace('New generation pending;','New source generated successfully;').replace('MiniMax single task in\ngeneration.json.','MiniMax single task succeeded; source.mp4 and141 extracted source frames/full GIF\n/contact and source hash retained.').replace('Poll generation.json same task; inspect complete raw motion.','Task terminal Success; do not resubmit. Inspect complete141-frame raw motion.');s=s.split('\n\n## Initial source review')[0];s+='''

## Initial source review
18 full-body samples inspected: separate broad rectangular tablet is present and
belt wrench remains visible in sampled draw/read/stow, unlike prior transformation.
Still candidate: sample82 warmer than neighboring read poses; rear tablet casing
too pale. Review entire motion and fixed source-level material treatment, one
master ruler, head/body/tools, accepted shell and exact endpoints. No source frame
normalization or reduced-pose substitute. No new runtime selection/native proof.
Source-selection.json has current terminal task/hash and scoped concerns.
''';h.write_text(s,encoding='utf-8')
print(json.dumps({'taskStatus':g['status'],'frames':141,'clippedFrames':0,'productionInstalled':False,'remaining':'full source material/motion/registration and normal native selection'}))
R=P.parents[1]
note='''

## James East separate-tablet source generated — October 1, 2026

Single saved MiniMax task447775814107624 terminal Success; no generation job live.
james-tablet-east-belt-fixed-source-v1 retains raw source3154c6bad3cd14bda20cf1265ce00548219612ae79a9be5566241a2cce9f0b35,
exact master/input/prompt/ledger,141frames at24fps, fixed.25 ruler/-4,-4 offset,
zero crop loss, source GIF/contact.18 sampled full-body poses show separate broad
tablet and visible belt wrench through sampled lift/read/stow. Still unselected:
sample82 warmer than neighbors and tablet rear too pale. Review full141-frame
motion/material/master geometry, one source-level grade, shell fit/endpoints and
normal NPC/Continue before switching. Do not reduce motion to a few stills to hide
defects; do not normalize grade per pose. Old East wrench morph remains installed.
Next: complete source review and matching treatment; full James goal active.
'''
for path in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    data=path.read_bytes()
    if b'## James East separate-tablet source generated' not in data:
        enc=note.encode('utf-8');updated=enc.lstrip(b'\n')+b'\n'+data if path.name=='CURRENT_STATUS.md' else data+enc;tmp=path.with_name(path.name+'.east-tablet-source.tmp');tmp.write_bytes(updated);os.replace(tmp,path)
h=R/'character/james-inspect-material-continuity-v1/HANDOFF.md';s=h.read_text(encoding='utf-8');s=s.replace('Native job terminal; generation\nis separately pending and must be re-polled by its saved task ID.','Native job and generation both terminal. Replacement task Success; full141-frame\nsource retained with initial sampled review. Source remains unselected; source82\nwarmth and pale tablet rear need complete motion/material/geometry review.');h.write_text(s,encoding='utf-8')
