from pathlib import Path
import json
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
r=json.loads((P/'review.json').read_text(encoding='utf-8'))
d=json.loads((P/'source-edit-diagnostic.json').read_text(encoding='utf-8'))
assert r['frozenInputsStable']==31 and r['unchangedDecodedFramesExact']==10
heading='Bill West extended-authority pull source refinement - October 2, 2026'
body=f'''Sibling character/bill-swim-west-master-v4 replaces only swim phase2 both gears. Primary extended whole-body source, original standing master secondary; built-in generation exec-871a536c-aee0-4e74-a858-bdb63d1abd6c. Head refinement exec-ab44c714-a881-4bf6-b2e0-a309642da9cb uses new pull first/exact original head crop second. Both raws/exact prompts/ordered references retained in generation-jobs.json. Clear open gloves/wrists, less barrel chest and flatter torso improve relativeV3; completely flat master body/head/grade still NOT accepted.

Original148/956 density,352x320/p160224/H148,whole-source translation[70,163] retained from extended authority rather than recentering new head. Actual crown[115,203] versus extended[134,200]; head/shoulder displacement remains visually noticeable and must be judged with hips/spine. No local limb transforms, mirroring or posed-height normalization. Ten unaffected decoded frames exactV3. Twelve APNGdecoded frames/160ms holds exact960ms/loop0, all painted support preserved, six40x40 canonical helmets with bounded body/foreground protections;31frozen inputs stable. LFS filters confirmed.

Head semantic proxy157x171 before edit ->166x153 after versus original137x141. Shorter component but wider, so neither prompt nor proxy establishes original head match. Source head-only edit changes {d['RGBAChangedOutsideDiagnosticHeadROI']} RGBApixels outside diagnostic ROI and alpha exact=False; no generated body protection claim. Same2x original/before/after head board inspected: new head remains wider/brighter and face highlights differ from original. Candidate remains provisional.

Reviewed both raws, master, full paired stroke/neck/entry-wrap and neighboring before-after pull boards. Browser play/step sampled, paused new pull both gears screenshot saved; not full continuous native motion/contact acceptance. No native/profile interval or normal selection. Full body/hip/head chronology, recovery/reach progression, hardware/face matte grade and entry/independent exit still pending; no old native evidence transferred.

Lesson: changing primary authoring reference from drifted pull to neighboring flatter body improves wrists/torso, but can still enlarge and relocate head. Keep shared body registration separate from head edit, inspect actual crown displacement and hips, and disclose it. A shorter head proxy can coexist with greater width; do not report full size repair from a requested shrink or height alone. When source head edits repeatedly drift identity/material, evaluate reuse of original same-orientation head at fixed original density with bounded collar/foreground protections, while keeping body and moving joins independently provisional.

Next original-head/material fitting study against all six, then spine/hip/limb progression and restrained suit hardware; reconcile entry/exit and refresh native motion/contact/resume before normal admission. North/South master repairs and full-library consistency/polish remain. Full Bill objective active/incomplete.'''
targets=[ROOT/'docs/CURRENT_STATUS.md',ROOT/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md',ROOT/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for path in targets:
    with path.open('rb') as f:
        f.seek(max(0,path.stat().st_size-131072));tail=f.read().decode('utf-8',errors='replace')
    if heading not in tail:
        with path.open('a',encoding='utf-8') as f:f.write('\n\n## '+heading+'\n\n'+body+'\n')
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 - Project: BrineSpace - Task: Bill full master-consistent set

## Objective and acceptance
Complete full Bill set, continually match masters/identity/anatomy/camera/physical size/matte grade, then cross-family consistency and polish with appropriate moving/native verification.

## Accepted decisions and constraints
Original148/956 source density,352x320/p160224/H148. Whole-source translation only, no local anatomical fitting or mirrored views. Canonical40x40 helmet. Reversible authoring authorized; current normal selection preserved.

## Current state
This sibling changes swim phase2 both gears only. Open wrists/less broad torso from extended primary authority; head edit provisional. Sources/exact prompts/generation-jobs.json, build.py, two paired manifests/APNGs, review.json, source-edit-diagnostic.json, four comparison boards plus head board/browser-review.png. Six guidance targets appended.

## Verification
31 frozen inputs stable,10 untouched frames exactV3,12 decoded APNG frames/holds exact960ms loop0, all support retained, six bounded helmet protections pass, LFS filters confirmed. Raw/master/head/full/neck/entry-wrap/before-after/browser sampled views reviewed. Head proxy157x171->166x153, original137x141: head match unproven, brighter face highlights remain. Source-only head prompt changes1485128 outside-ROI RGBApixels; not protected-body generation. No new native/profile interval or normal adoption.

## Next action
Evaluate fixed-density original head reuse for same orientation with bounded collar protections across six. Check hips/spine and limb progression independently, then restrained hardware grade and entry/independent exit. Refresh native moving/contact/resume before guarded admission; North/South and full-library polish remain.
''',encoding='utf-8')
print('Recorded six guidance targets and handoff; goal active/incomplete.')
