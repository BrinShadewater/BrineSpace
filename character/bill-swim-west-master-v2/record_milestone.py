from pathlib import Path
from PIL import Image
import json,hashlib,numpy as np
P=Path(__file__).resolve().parent;R=P.parent.parent
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
review=json.loads((P/'review.json').read_text(encoding='utf-8'))
assert all(sha(R/'character'/f)==h for f,h in review['inputSHA256'].items())
a=np.array(Image.open(P/'sources/stroke-sweep-v1.png').convert('RGBA'));b=np.array(Image.open(P/'sources/stroke-sweep-identity-v2.png').convert('RGBA'))
review.update(candidateStatus='partial_stroke_master_revision_pending_full_fidelity',generations=[dict(id='exec-79355fb1-095a-4315-afd4-f3073442dde0',raw='sources/stroke-extend-v1.png',prompt='sources/stroke-extend-prompt-v1.txt',references=['../bill-land-water-west-v11/sources/prone-legs-v4.png','../crew-side-masters-v1/bill-side-master-01.png']),dict(id='exec-495d162f-dec3-45cf-bcf2-4fb672ce9c10',raw='sources/stroke-sweep-v1.png',prompt='sources/stroke-sweep-prompt-v1.txt',references=['sources/stroke-extend-v1.png','../crew-side-masters-v1/bill-side-master-01.png'],status='head grew and chest button design drifted'),dict(id='exec-e8956a81-ab18-41df-8d7b-db5b07223361',raw='sources/stroke-sweep-identity-v2.png',prompt='sources/stroke-sweep-identity-prompt-v2.txt',references=['sources/stroke-sweep-v1.png','../bill-land-water-west-v9/sources/master-head-reference.png','../crew-side-masters-v1/bill-side-master-01.png'],status='selected provisional sweep; complete design still pending')],identityEditDiagnostic=dict(alphaExact=bool(np.array_equal(a[:,:,3],b[:,:,3])),changedRGBAPixels=int(np.any(a!=b,axis=2).sum()),scope='Whole-source replacement, no generated pixel-protection promise.'),visualAcceptance='Original master, V11 near-prone, extended raw and both sweep raws, fixed-density master/entry/old/new stroke and paired partial-stroke boards, both head/collar detail pairs reviewed. Original knee/cuff/boot quilting detail restored relative to old compact bank; head and rectangular chest buttons improve. New strokes and V11 entry closer in body projection, but extension length/material variation and full original anatomy/control layout/perspective remain pending. Canonical helmet/collar fits reviewed, not full moving acceptance.',normalSelected=False,nativeAcceptance=False)
review['sourcePromptSHA256']={f.name:sha(f) for f in (P/'sources').iterdir() if f.is_file()}
(P/'review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
heading='## Bill West original-master extended and down-sweep swim study — October 2, 2026'
note=f'''{heading}

New character/bill-swim-west-master-v2 stages two representative whole-source poses, bare/helmet, not a replacement full swim loop. Extended source edits V11 near-prone with original master; down-sweep follows that source with original identity, then exact master-head crop/control authority repair. Three raw/exact prompts/ordered generation reference IDs retained. Initial sweep enlarged head and changed chest buttons to beads; corrected source restores smaller head and rectangular grid, complete layout/identity still pending. No mirrored views, per-pose height/width fitting or scripted limb changes.

Original148/956 source drawing density,320x320/p160224/H148. Each complete isolated source receives whole-figure translation only; no body geometry/grade edit in packaging. Extended crown[134,200], translation{review['translation']}; sweep translation{review['sweep']['translation']} using bounded hair/face ROI, not whole-silhouette top. Sweep head proxy130x151 clear ROI edges; original137x141 is a proxy comparison, not complete anatomy acceptance. Raised boots can overtake a crown, so independent head registration is required. Head/control instructions did not protect whole source alpha: exact={review['identityEditDiagnostic']['alphaExact']}.

Two canonical40x40 native-scale/rotation0 helmets; protected body outside fitting mask/foreground/below donor exact. Four decoded APNGframes/holds exact320ms/loop1, a finite TWO-pose study only. {len(review['inputSHA256'])} frozen targeted inputs stable. Raw/master/V11-entry/old/new fixed-density boards, complete paired partial study and both neck pairs inspected. Knee/cuff/boot/quilting detail improves against old compact bank and body projection closer to entry; full segment length/material/controls/perspective and continuous joins remain provisional. No native/profile access or normal source selection; old native/resume evidence does not cover this source bank.

Lesson: re-author the working stroke as well as its entry when compressed source anatomy causes the join defect. A fixed head density alone cannot certify body proportions. Separate initial action authorship from original head/control repair; preserve rejected raws. Register a kicking figure from an inspected bounded head region rather than the highest opaque pixel, which may be a boot. Do not label a partial finite study as a finished six-phase loop.

Next remaining recovery/catch/reach phases, full six-phase loop and entry/independent-exit master/grade/segment continuity, then native motion/contact/guards/resume. North/South master repairs, normal admission/cargo lifecycle and full-library consistency/polish remain. Full Bill goal active/incomplete.
'''
files=[R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for f in files:
    with f.open('rb') as s:s.seek(max(0,f.stat().st_size-65536));tail=s.read().decode('utf-8',errors='replace')
    if heading not in tail:
        with f.open('a',encoding='utf-8') as s:s.write('\n\n'+note)
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: Full Bill animations

## Objective and acceptance
Full master-consistent animation set, then entire-library polish/integration. Active/incomplete.

## Accepted decisions and constraints
Original independent directions/physical drawing density. No per-pose fitting/mirroring/scripted limb changes. Preserve normal selection, owner data and concurrent work.

## Current state
West master-v2 extended and down-sweep whole-source pilot, both gears. Three raw/prompts/reference provenance retained; initial sweep identity drift corrected provisionally. build.py then build_sweep.py rebuilds complete two-pose study, not full six-phase loop. Comparison/paired/neck/review and six guidance updates saved.

## Verification
15frozen targeted inputs stable; four decoded APNGframes/holds exact320ms/loop1. Two native40x40 helmet body/foreground fitting protections. Whole painted support preserved, original148/956 density. Raw/master/entry/old/new/neck boards inspected; sweep bounded head130x151 clear ROI edges. Head/control generation not pixel-protected. No native/profile interval or normal admission; full body/grade/control/camera/moving acceptance pending.

## Next action
Recovery/catch/reach source phases then complete six-phase paired loop with master/entry/exit consistency. Native motion/contact/guards/resume, remaining North/South masters, normal admission/cargo lifecycle and full-library polish.
''',encoding='utf-8')
print(json.dumps(dict(frozenInputs=len(review['inputSHA256']),decodedFrames=4,partialMs=320,guidanceFiles=6,normalSelected=False)))
