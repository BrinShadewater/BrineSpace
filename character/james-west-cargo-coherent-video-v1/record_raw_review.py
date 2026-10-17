from pathlib import Path
import json,hashlib,os,uuid
p=Path(__file__).resolve().parent;r=p.parents[1]
def atomic(path,old,new):
    assert path.read_bytes()==old
    tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(new)
    assert path.read_bytes()==old;os.replace(tmp,path)
ledger=json.loads((p/'generation.json').read_bytes())
assert ledger['status']=='Success' and ledger['task_id']=='448145326813657'
inputs=json.loads((p/'inputs.json').read_bytes())
assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in inputs['sha256'].items())
path=p/'raw-review/review.json';old=path.read_bytes();review=json.loads(old)
assert review['decodedFrames']==141 and review['fps']==24 and review['size']==[768,768]
assert hashlib.sha256((p/'source.mp4').read_bytes()).hexdigest()==review['sourceSha256']
heights=[f['diagnosticHeight'] for f in review['frames']]
review.update(visualReviewPending=False,selected=False,continuousPlaybackWatched=False,sourceAcceptance=False,
    reviewed='All six chronological boards/141raw decoded frames and full-size first/mid/last frames inspected beside same-scale provider input. Face and matte material more coherent than independent crop edits; gentle shoulder/case articulation, late downward gaze. No obvious abrupt source-grade flash in these inspected frames. Foot silhouettes/placement change through shoulder turn; fixed anatomical/foot-contact registration still needs audit before accepting motion. Reference diagnosticH450, raw447..451, not anatomical height acceptance. Case/grip/endpoint exactness and paired helmet/native contexts remain unproven.',
    diagnosticHeightRange=[min(heights),max(heights)],taskTerminal=True)
atomic(path,old,(json.dumps(review,indent=2)+'\n').encode())
verdict={'selected':False,'normalSelectionChanged':False,'taskId':ledger['task_id'],'providerStatus':'Success','decodedRawFramesReviewed':141,'fps':24,'sourceSize':[768,768],'estimatedUSD':0.19,'actualBillingVerified':False,'generationAttempts':1,
    'finding':review['reviewed'],'next':'Fixed single scale/pivot extraction from original reference; audit head/torso material and anatomy, planted ankle/sole landmarks, case grip and outgoing/incoming endpoint mismatch. No per-frame height fitting. Then paired helmet and full native contract if source quality passes.',
    'source':'source.mp4','prompt':'prompt.txt','input':'master-input.png','review':'raw-review/review.json','rawIndependentCropTrials':{'verdict':'../james-cargo-return-bridges-v1/adjacent-bare-v18-review.json','prompts':['../james-cargo-return-bridges-v1/upper-crop-v17/prompt.txt','../james-cargo-return-bridges-v1/upper-crop-v18/prompt.txt']}}
(p/'VERDICT.json').write_text(json.dumps(verdict,indent=2)+'\n')
section='''### James coherent cargo video raw review — October 2, 2026

Single saved MiniMax task448145326813657 terminal Success; source.mp4 downloaded,
no further generation/resubmission. All141raw frames at24fps/768square reviewed
chronologically across six common-scale boards, plus full first/middle/last beside
provider input. More coherent face/matte material and small shoulder/case motion
than separate upper patches; late downward gaze. Foot silhouette/placement changes
through turn still need fixed ankle/sole/contact audit. White-difference diagnostic
height447..451 versus input450 is not anatomical height proof. No obvious abrupt
grade flash in inspected frames; exact case/grip/endpoints and helmet unproven.

Original source/prompt/helper/input hashes unchanged. Source/raw review only;
no extraction/grade/native motion/continuously watched cadence/master or normal
admission. Original V9/riseV6/caseV7 remains selected. Next one fixed reference
scale/pivot extraction, anatomy/material/contact/case and endpoint comparison;
never per-frame height fitting. Then paired helmet/native/save binding if sound.
EstimateUS$0.19, billing unverified, one attempt. No live provider or native job.
Both skills/pipeline/bible reflect failure of independent adjacent head patches,
and why coherent source still needs contact/endpoints. Full goal active/incomplete.
Evidence: character/james-west-cargo-coherent-video-v1/VERDICT.json, generation.json,
inputs.json, prompt.txt, source.mp4, raw-review/review.json. No commit/export.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() in old:continue
    if path.name=='CURRENT_STATUS.md':
        marker=b'### James adjacent source trial and coherent-motion change';at=old.index(marker);new=old[:at]+section.encode()+b'\n'+old[at:]
    else:new=old+b'\n\n'+section.encode()
    atomic(path,old,new)
handoff='''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James coherent cargo motion

## Objective and acceptance
Full James set matching masters, style/perspective/height/proportions/matte grade,
then cross-family polish. Incomplete; normal V9/riseV6/caseV7 remains installed.

## Accepted decisions and constraints
Preserve owner profile/layouts/concurrent crew. Upper10–18 trials unselected;
adjacent17/18 rejected for face/badge drift/crown overshoot. Existing direct-video
route authorized, reserved motion-transfer run untouched. No commit/export.

## Current state
New upper17/18 raw/prompt/reference hashes/native package/UID/source review.
character/james-west-cargo-coherent-video-v1: original Westunload0 provider input,
prompt/pre-call inputs, exclusive generation ledger, task448145326813657 completed,
source.mp4/141raw-frame chronological review/VERDICT. Five maintained guides updated.

## Verification
Upper17/18 packages each61476outside pixels exact/engine0/owner unchanged under
scratch APPDATA. Twelve source/crop comparisons inspected; rejected/no helmet or
actor expansion. New direct source single6s/768P attempt estimated$0.19, actual
billing unverified; taskSuccess/download, input hashes stable. All141raw frames/
six boards + full first/mid/last inspected. Face/material more coherent, but foot
placement changes need contact audit. Raw white-difference height447..451 vs
input450 is diagnostic, not anatomical acceptance. No fixed extraction, paired
helmet/native/title/master acceptance. No live native/provider job remains.
Earlier normal424/title148/legacy30/ordinary72 checks retain their own revisions;
paired upper16 native1317/0 trial remains unselected due delayed helmet pop.

## Next action
Extract coherent clip at ONE fixed reference scale/pivot, inspect whole anatomy/
head/collar/material, sole/ankle contact, case grip and exact endpoint gaps before
selecting interval or normal override. No per-pose height normalization. If source
passes, matched helmet and full native lifecycle/Continue on versioned new banks.
Other cardinals/held joins/natural contexts/master/height/material/cross-family
polish remain. Goal active/incomplete; no blocker.
'''
path=r/'character/james-floor-case-west-v1/HANDOFF.md';atomic(path,path.read_bytes(),handoff.encode())
print('Terminal source and141-frame review recorded; input hashes unchanged; five guides/handoff updated. No selection or full-goal acceptance.')
