from pathlib import Path
import hashlib,json,os,uuid

p=Path(__file__).resolve().parent;r=p.parents[1]
native=json.loads((p/'actor-return-v7-evidence.json').read_bytes())
guard=json.loads((p/'actor-return-v7-validation.json').read_bytes())
inputs=json.loads((p/'actor-return-v7-inputs.json').read_bytes())
cases=[x for x in native['results'] if not x.get('diagnostic')]
assert native['checks']==991 and native['failures']==0 and len(cases)==6
assert sum(len(c['trace']) for c in cases)==48
assert guard['exitCode']==0 and not guard['timedOut'] and guard['realProfileUnchanged']
assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in inputs.items())
refs=json.loads((p/'reference-evidence.json').read_bytes())
assert all(hashlib.sha256((r/c['path']).read_bytes()).hexdigest()==c['sha256'] for c in refs['sources'])
package=json.loads((p/'package-v7-evidence.json').read_bytes())
assert package['protectedCandidateRgbaChecks']==411648

def atomic(path,data):
    old=path.read_bytes();tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp')
    tmp.write_bytes(data);assert path.read_bytes()==old;os.replace(tmp,path)

review_path=p/'actor-return-v7-review.json'
review=json.loads(review_path.read_bytes())
review.update(visualReviewPending=False,
    reviewed='All48 changing native source/world pairs inspected in six boards, plus14 registered source/master presentations. Whole-body intermediates rotate hips/knees/boots with shoulders and retain level case/goggles. Later two interiors over-rotate toward viewer and appear bulkier than original unload endpoint; shared helmet improves but remains a few native pixels lower/smaller than original endpoint. Final source seam and continuous motion/material/master polish remain unaccepted.',
    continuousNativeMotionAcceptance=False,fullMasterMatchAcceptance=False,
    completeReturnAcceptance=False)
atomic(review_path,(json.dumps(review,indent=2)+'\n').encode())
report={'selected':False,'fullGoalComplete':False,'authoring':'built-in image_gen',
    'rawSources':['west-bridge-generated-v6.png','west-bridge-generated-v7.png'],
    'prompts':['west-bridge-prompt-v6.txt','west-bridge-prompt-v7.txt'],
    'sources':[{'file':name,'sha256':hashlib.sha256((p/name).read_bytes()).hexdigest()} for name in ['west-bridge-generated-v6.png','west-bridge-generated-v7.png','west-bridge-reference-close.png']],
    'nativePackageScope':'V6 wholebody intermediates at one shared148/408 ruler. V7 only helmet y0..109 replaces V6 candidate. All bare pixels and helmet lower-body pixels protected against candidate, not original masters.',
    'protectedCandidateRgbaChecks':411648,'nativeChecks':991,'nativeFailures':0,
    'actualPrescribedReturns':6,'sourceWorldPosesReviewed':48,
    'registeredSourceMasterPresentationsReviewed':14,'targetedFrozenInputsUnchanged':21,
    'originalReferenceHashesUnchanged':6,'ownerProfileUnchanged':True,
    'completeVisualJoinAccepted':False,
    'remaining':['Last two new poses turn too far toward viewer and look bulkier than original unload endpoint.','Helmet still needs exact original proportion/entry match.','Continuous native motion/master/material polish.','Authored floor-case/standing disposition and paired ordinary Continue.','Remaining cardinal contexts, West tablet edges and full cross-family consistency.']}
(p/'study-review-v7-evidence.json').write_text(json.dumps(report,indent=2)+'\n')
section='''## James coherent whole-body West bridge v6/v7 candidate — October 2, 2026

Two built-in source edits/prompts retained. V6 four-interior/both-gear whole-body
study restores forehead goggles, clean contours and rotating hips/knees/boots.
V6 native shared148/408scale avoids per-frame height/grade normalization; exact
original carrying/unload endpoints referenced. Registered board exposed undersized
generated helmet. V7 generated helmet/head repair admitted only y0..109 window
using V6 recorded anchors; bare row and helmet lower body retained candidate RGBA
exact411648checks. Protection is against V6 candidate, not original master.

Actual prescribed workshop returns through fixture-only v7 injection pass991checks/
0fail across six pickup/carry/late-unload cases/both gears. All48changing source/
world poses in six boards plus14registered source/master presentations reviewed.
Whole-body turn removes frozen-leg issue, but later two interiors over-rotate toward
viewer and look bulkier than original unload endpoint. Helmet improves but remains
a few native pixels below/smaller than original shell. Visual join/master/material
and continuous motion acceptance remain pending. No production selection change.

Both package runs and actual return run engine0/no timeout/owner profile unchanged
under scratch APPDATA. All21targeted prelaunch actor-run hashes and six original
reference hashes unchanged; not a whole-world dependency freeze. LFS filter verified
for new raw sources/representative interior. Ordinary return Continue and final
floor-case/idle disposition remain unsupported/unaccepted; full objective incomplete.

Lesson: registered side-by-side review catches shared-helmet shrink concealed by
raw-sheet scale. Preserve the candidate's reviewed body when correcting head size,
and distinguish that pixel protection from original-master fidelity. Test coherent
whole-body changes through actual footprint union rather than only source manifest.
Next correct late-interior orientation/width and exact helmet match, continuous
native source joins, floor handoff/Continue and full James/context/cross-family polish.
Evidence: character/james-cargo-return-bridges-v1/study-review-v7-evidence.json,
actor-return-v7-evidence.json and bridge-v7-registered-review.png.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',
    r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',
    r/'skills/brinespace-character-pipeline/references/crew-consistency.md',
    Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() not in old:
        atomic(path,section.encode()+b'\n'+old if path.name=='CURRENT_STATUS.md' else old+b'\n\n'+section.encode())
handoff='''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James cargo return/whole-body bridge

## Objective and acceptance
Full James master/style/perspective/height/proportion/matte animation set, then
cross-family consistency. Full objective active/incomplete; candidate unselected.

## Accepted decisions and constraints
Original endpoints/master authority; one shared scale, no per-frame grade/height
normalization. Needs/safety live, changing-pose union clearance required. Keep
owner geometry/profile intact. Unsupported return snapshot rejects normal saves.

## Current state
V5 rejected. V6 coherent body improves turn and preserves goggles; v7 fixes helmet
only above y110 with exact v6 candidate lower-body/bare preservation. Raw edits,
prompts, native packages/UIDs, paired joined manifests and reviews retained.
Original selected James library/controller unchanged. Five guides updated.

## Verification
V7 actual six prescribed power-loss returns991checks0fail,48native source/world
poses reviewed;14registered master/source presentations. Engine0/owner unchanged
scratch.21targeted prelaunch hashes/six originals unchanged.411648candidate pixel
protection checks. Earlier v4 priority151checks/12cases passes; separate art interval.
These captures do not prove continuous native film or whole-world natural scheduling.

## Next action
Correct last two interiors: too frontal/bulky versus original unload. Exact shared
helmet size/entry match still needed. Then continuous joins, authored crate floor/
standing handoff, paired RunSave/Continue and production admission. Remaining
cardinal/layout contexts, West tablet edges and full master/cross-family polish.
No commit/export. Do not restore whole shared files from historical backups.
'''
atomic(p/'HANDOFF.md',handoff.encode())
print('V7 candidate991checks/48poses/14master presentations recorded;21inputs unchanged;five guides/handoff updated. Full goal incomplete.')
