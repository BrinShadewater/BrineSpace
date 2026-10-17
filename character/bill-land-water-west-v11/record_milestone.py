from pathlib import Path
from PIL import Image
from scipy.ndimage import label
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent;R=P.parent.parent;A=P.parent/'bill-west-water-proportion-audit-v1'
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
review=json.loads((P/'review.json').read_text(encoding='utf-8'));audit=json.loads((A/'audit.json').read_text(encoding='utf-8'))
for report in [review,audit]:
    assert all(sha(R/'character'/f)==h for f,h in report['inputSHA256'].items())
prior=np.array(Image.open(P.parent/'bill-land-water-west-v10/sources/prone-flat-v3.png').convert('RGBA'))
current=np.array(Image.open(P/'sources/prone-legs-v4.png').convert('RGBA'))
roi=np.ones(prior.shape[:2],dtype=bool);roi[350:650,800:1536]=False
diagnostic=dict(alphaExact=bool(np.array_equal(prior[:,:,3],current[:,:,3])),changedRGBAPixelsOutsideLegDiagnosticROI=int((np.any(prior!=current,axis=2)&roi).sum()),scope='Leg-only instructions are not protected-pixel proof; whole-source replacement.')
c=current[100:390,330:560];rgb=c[:,:,:3].astype(float);r,g,b=rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]
mask=(c[:,:,3]>180)&(r>=40)&(r<=160)&(r>g*1.15)&(g>b*1.2);lab,_=label(mask);counts=np.bincount(lab.ravel());y,x=np.where(lab==np.argmax(counts[1:])+1)
box=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
assert box[0]>0 and box[1]>0 and box[2]<c.shape[1] and box[3]<c.shape[0]
head=dict(roi=[330,100,560,390],bounds=box,width=box[2]-box[0],height=box[3]-box[1],componentTouchesROIEdge=False,scope='Bounded brown head proxy; not anatomical acceptance.')
widths=[]
for folder in ['bill-land-water-west-v10','bill-land-water-west-v11']:
    a=np.array(Image.open(P.parent/folder/'bare/frames/land-swim-west/005.png').convert('RGBA'));yy,xx=np.where(a[:,:,3]>180)
    widths.append(dict(bank=folder,width=int(xx.max()+1-xx.min()),scope='Occupied extent diagnostic, not segment-length proof.'))
review.update(generationMode='built-in image_gen edit',generation=dict(id='exec-2cdba42c-0086-4b4e-b8f4-a90e1f24a2ef',raw='sources/prone-legs-v4.png',prompt='sources/prone-legs-prompt-v4.txt',references=['../bill-land-water-west-v10/sources/prone-flat-v3.png','../crew-side-masters-v1/bill-side-master-01.png']),sourceEditDiagnostic=diagnostic,headProxy=head,extentDiagnostic=widths,frozenInputsStable=len(review['inputSHA256']),candidateStatus='provisional_leg_proportion_revision',visualAcceptance='Original standing/swim sources, all six selected swim poses and V10/V11 common-physical-density comparisons reviewed. New thighs/shins visually shorter with knee/cuff/boot hardware retained, small head and separated hands readable; canonical helmet/collar connected. Complete paired bank/all neck pairs and paused browser reviewed. Existing swim bank remains compressed/different in lower-leg detail and new pose remains longer. Full projected anatomy/perspective/grade/contact/continuous-motion acceptance pending.',browserEvidence=dict(file='browser-review.png',poseIndex=5,timeMs=350,scope='Paused source only, no native continuous motion.'),normalSelected=False,nativeAcceptance=False)
review['sourcePromptSHA256']={f.name:sha(f) for f in (P/'sources').iterdir() if f.is_file()}
(P/'review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
audit.update(visualAcceptance='All common-density master/current idle/V10 entry/six selected swim/detail and V11 leg-revision boards inspected. Fixed .27 swim scale and exact padded endpoint verified. Old swim authored body visibly more compressed with less distinct original knee/lower-leg hardware, while V10 legs were extended; V11 reduces that extension but does not resolve full endpoint consistency. Both families need original segment/detail/camera/grade review; no occupied-width fitting.',remaining='Re-author swim pose0 with original anatomical segments/hardware, then complete six-pose stroke and paired helmet review alongside entry/exit. Refresh native evidence only after source fidelity.')
(A/'audit.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8')
heading='## Bill West full stroke proportion audit and near-prone leg revision — October 2, 2026'
note=f'''{heading}

New character/bill-west-water-proportion-audit-v1 compares original standing/current normal idle, V10/V11 entry and all six selected West swim poses at common H148. Fixed existing atlas .27 factor across six frames; source hash matches registration, padded entry6 exact selectedswim0. All31 targeted inputs stable. No per-pose width/height fitting or source mutation. Boards reviewed: older swim source body visibly compressed and knee/lower-leg detail less distinct than original; V10 newly authored legs also too extended. This is visual proportion diagnosis, not full anatomical measurement or native motion proof.

Sibling character/bill-land-water-west-v11 revises pose5 alone through built-in whole-source edit against original master, exec-2cdba42c-0086-4b4e-b8f4-a90e1f24a2ef. Raw/exact prompt and ordered references retained. Thigh/shin segments visually shorten while knee/cuff/boot hardware remains, small head and two hands readable. Original148/956 density and preceding crown[131,188], whole-figure translation[69,151]; no occupied-width normalization or limb transforms. Occupiedwidth {widths[0]['width']}→{widths[1]['width']} is diagnostic, not proof of requested15percent segment change. Bounded head proxy {head['width']}x{head['height']}, clear ROI edges; not whole anatomy acceptance. Leg-only edit alpha exact={diagnostic['alphaExact']}, {diagnostic['changedRGBAPixelsOutsideLegDiagnosticROI']}RGBApixels outside leg diagnostic ROI changed; no generated body protection claim.

Twelve unaffected poses exactV10;14APNGframes/holds exact500ms/loop1, five canonical40x40 scale1/rotation0 head-fitting body/foreground protections. {len(review['inputSHA256'])} frozen bank inputs stable. Raw, registered original/levelling/V10/V11, complete paired bank/all neck pairs and paused browser pose5 at350ms reviewed. Helmet/collar connected in inspected pose. New pose still longer than current swimming endpoint; full segment/camera/grade/contact/motion acceptance pending. No native/profile interval, normal source selection or runtime scale change. Older WestV4 native/resume/Continue does not cover new revisions.

Lesson: common head/hardware density and fixed per-bank factors cannot certify torso/thigh/shin lengths across source families. Inspect the whole selected stroke bank, both source authorities and neighboring transition poses before assigning all mismatch to a new pose. Restore authentic knee/ankle detail and anatomy through source authoring, not shrink-to-fit, or global swim-scale adjustment that enlarges its head. Keep requested percentage separate from measured proof.

Next original-master West swim0 anatomical/hardware repair, complete six-pose paired stroke and entry/exit chronology/grade/reach; North/South masters, refreshed native contact/motion/resume, normal admission/cargo lifecycle and full-library polish. Full Bill goal active/incomplete.
'''
files=[R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for f in files:
    with f.open('rb') as s:s.seek(max(0,f.stat().st_size-65536));tail=s.read().decode('utf-8',errors='replace')
    if heading not in tail:
        with f.open('a',encoding='utf-8') as s:s.write('\n\n'+note)
handoff='''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: Full Bill animations

## Objective and acceptance
Full master-consistent set then cross-family polish and game integration. Active/incomplete.

## Accepted decisions and constraints
Original masters, independent directions and physical density. No per-pose fitting, global endpoint-scale workaround or scripted limb alterations. Preserve selections/owner/concurrent work.

## Current state
West full six-stroke/entry/master proportion audit and V11 source near-prone thigh/shin revision. Old swim source compressed/lower-leg details differ; V11 less extended but full join remains unresolved. Source/raw/prompt, build/frames/manifests/exports, comparison/fullpaired/neck/browser evidence/reports and six guidance records updated.

## Verification
31audit inputs stable; fixed swim .27/source hash and exact padded endpoint verified. V11 twelve unaffected poses exactV10;14APNGframes/holds exact500ms/loop1/five canonical protected equipment fits, frozen bank inputs stable. All boards/raw/neck/paused browser inspected. Generated edit treated as whole-source. No native/profile interval or normal selection; no full anatomy/motion acceptance.

## Next action
Original-master swim0 anatomy/hardware repair, then complete six-pose paired swim bank with entry/exit consistency. Complete West grade/reach/contact and North/South masters, refresh native/resume, normal admission/cargo lifecycle and full-library polish.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8');(A/'HANDOFF.md').write_text(handoff,encoding='utf-8')
print(json.dumps(dict(auditInputs=31,bankInputs=len(review['inputSHA256']),unchangedPoses=12,decodedFrames=14,headProxy=head,extentDiagnostic=widths,guidanceFiles=6)))
