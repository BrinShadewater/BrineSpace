from pathlib import Path
from PIL import Image
import json,hashlib,numpy as np
P=Path(__file__).resolve().parent;R=P.parent.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
report=json.loads((P/'review.json').read_text(encoding='utf-8'))
assert all(sha(R/'character'/f)==h for f,h in report['inputSHA256'].items())
audit=json.loads((P/'head-audit.json').read_text(encoding='utf-8'))
assert all(not item['componentTouchesROIEdge'] for item in audit)
extent=[]
for gear in ['bare','helmet']:
    for i in [4,5,6]:
        a=np.array(Image.open(P/gear/f'frames/land-swim-west/{i:03}.png').convert('RGBA'));y,x=np.where(a[:,:,3]>180)
        extent.append(dict(gear=gear,pose=i,opaqueBounds=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)],width=int(x.max()+1-x.min()),scope='Occupied extent only; not anatomical length or scale acceptance.'))
raw1=np.array(Image.open(P/'sources/prone-master-v1.png').convert('RGBA'))
raw2=np.array(Image.open(P/'sources/prone-head-v2.png').convert('RGBA'))
roi=np.ones(raw1.shape[:2],dtype=bool);roi[100:390,330:560]=False
diagnostic=dict(headEditAlphaExact=bool(np.array_equal(raw1[:,:,3],raw2[:,:,3])),headEditChangedOutsideDiagnosticROI=int((np.any(raw1!=raw2,axis=2)&roi).sum()),scope='No generated protected-body claim; head edit and pose edit treated as whole-source replacements.')
report.update(generationMode='built-in image_gen edit',generations=[
    dict(id='exec-2b55a8cb-3b1d-4567-9451-f9322a358774',raw='sources/prone-master-v1.png',prompt='sources/prone-master-prompt-v1.txt',references=['../crew-side-masters-v1/bill-side-master-01.png'],status='head oversized, lower body too sloped'),
    dict(id='exec-6e7177ae-4ab2-48a6-9daa-cfe68863be02',raw='sources/prone-head-v2.png',prompt='sources/prone-head-prompt-v2.txt',references=['sources/prone-master-v1.png','../bill-land-water-west-v9/sources/master-head-reference.png'],status='head closer; lower body too sloped, preserved head-v2-review.json and head-v2-comparison.png'),
    dict(id='exec-377e2e9f-e6bb-439e-a111-5f98e2111a33',raw='sources/prone-flat-v3.png',prompt='sources/prone-flat-prompt-v3.txt',references=['sources/prone-head-v2.png'],status='flat pose diagnostic candidate; endpoint proportion join needs review')],
    frozenInputsStable=len(report['inputSHA256']),headProxyAudit=audit,neighborExtentDiagnostic=extent,sourceEditDiagnostic=diagnostic,
    candidateStatus='needs_full_body_endpoint_consistency_review',
    visualAcceptance='Original master and all three raws, four common-density head proxies, registered original/levelling/previous/new near-prone comparison, complete fourteen-pose bank and seven neck pairs reviewed. Flat v3 resolves sloped lower body; head133x141 proxy versus original137x141, two hands distinct, canonical collar connected. New near-prone still visibly longer than existing swimming endpoint; full anatomical segment lengths/grade/camera/contact/continuous-motion acceptance remains pending. Do not compress to endpoint occupied width as a repair.',
    browserEvidence=dict(file='browser-review.png',poseIndex=5,timeMs=350,scope='Paused source candidate only, no continuous/native review.'),nativeAcceptance=False,normalSelected=False)
report['sourcePromptSHA256']={f.name:sha(f) for f in (P/'sources').iterdir() if f.is_file()}
(P/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
heading='## Bill West near-prone head and flat articulation candidate — October 2, 2026'
note=f'''{heading}

Sibling character/bill-land-water-west-v10 changes only entrypose5 both gears. Original directional master authors whole near-prone; first raw enlarged head and sloped lower body. Exact original head crop reference repairs second raw; third edit articulates spine/hips/legs flat rather than rotating or squeezing a sprite. All three built-in generation raws/exact prompts/ordered reference IDs retained; prior sloped packed review/comparison retained separately. Whole-source148/956 drawing density and crown[131,188] via translation[69,151]. Lowest opaque support248 diagnostic, not floor contact.

Common-density bounded brown head proxies original137x141, first182x192, head edit137x146, flat133x141; all clear ROI edges. Head-only edit alpha exact={diagnostic['headEditAlphaExact']}, changes {diagnostic['headEditChangedOutsideDiagnosticROI']} RGBApixels outside diagnostic ROI; not protected-body generation. Twelve unaffected decoded poses exactV9;14APNGframes/holds exact500ms/loop1, five canonical40x40helmet scale1/rotation0 fitting protection checks. {len(report['inputSHA256'])} frozen inputs stable. Raw/master/head audit/registered and complete paired boards/all neck pairs/paused browser pose5 at350ms inspected.

Flat pose/head/two-hand clarity improves but complete board reveals visible shortening into existing normal swimming endpoint. Candidate needs full body/endpoint consistency review, not accepted production replacement. Occupied extents recorded per gear/pose4..6 are not anatomical lengths. Do not fix this by fitting the new pose to the endpoint bounding width; inspect original swim authority and actual anatomical segments across the bank first. Whole head proxy match and canonical helmet fitting do not certify torso/thigh/shin proportions. Grade, perspective, moving/contact/clearance acceptance remain pending. No native/profile interval or normal selection; older WestV4 native/resume/Continue evidence does not coverV5..V10.

Lesson: a corrected head can coexist with sloping or elongated lower-body projection. Specify anatomical hip/knee articulation and evaluate the complete chronological body against both original standing master and selected swimming authority. Preserve failed intermediate boards; choose common physical density before comparing, and never substitute width normalization for matching anatomy.

Next audit original/current West swim endpoint and late-pose anatomical lengths, repair actual source drift and chronological grade/reach; independent exit context/rise, North/South master repairs, refreshed native motion/contact/resume, normal admission/cargo lifecycle and full-library consistency/polish. Full Bill goal active/incomplete.
'''
files=[R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for f in files:
    with f.open('rb') as stream:
        stream.seek(max(0,f.stat().st_size-65536));tail=stream.read().decode('utf-8',errors='replace')
    if heading not in tail:
        with f.open('a',encoding='utf-8') as stream:stream.write('\n\n'+note)
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: Full Bill animations

## Objective and acceptance
Full master-consistent set and cross-family polish/integration. Goal active/incomplete.

## Accepted decisions and constraints
Original independent directions and physical drawing density; no per-pose occupied-height/width fitting or limb transforms. Preserve normal selections, owner data and concurrent work.

## Current state
West entryV10 pose5 flat near-prone diagnostic candidate, both gears. Smaller original head and clear hands improve; body/endpoint longitudinal mismatch remains. prepare/build/manifests/frames/exports, three raw/prompts, head audit, prior sloped comparison, paired/master/neck/browser evidence/review and six guidance updates retained.

## Verification
12unaffected poses exactV9;14APNGframes/holds exact500ms/loop1, five canonical40x40 fitting protection checks. Frozen inputs stable. Raw/master/common-density head/full paired/neck and paused browser reviewed. Head proxy133x141 versus137x141 is not full anatomy acceptance. No new native/profile interval or normal admission.

## Next action
Inspect original/current West swim authority and anatomical segment lengths for late-pose/endpoint mismatch, then revise actual drift. Complete West chronology/grade/reach, independent exit, North/South masters; refreshed native motion/contact/resume, normal admission/cargo lifecycle and full-library polish.
''',encoding='utf-8')
print(json.dumps(dict(frozenInputs=len(report['inputSHA256']),unchangedPoses=12,decodedFrames=14,guidanceFiles=6,neighborExtents=extent)))
