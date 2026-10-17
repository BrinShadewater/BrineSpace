from pathlib import Path
import json,hashlib,os,uuid
p=Path(__file__).resolve().parent;r=p.parents[1]
d=json.loads((p/'full_return_v6-evidence.json').read_bytes())
guard=json.loads((p/'full_return_v6-validation.json').read_bytes())
reviewpath=p/'full-return-v6-review/review.json'
review=json.loads(reviewpath.read_bytes())
assert d['checks']==1277 and d['failures']==0
assert guard['exitCode']==0 and guard['realProfileUnchanged'] and not guard['timedOut']
assert review['pairs']==94 and review['decodedRgbAndDurationChecks']==184
inputs=json.loads((p/'full_return_v6-inputs.json').read_bytes())
assert len(inputs)==40 and all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in inputs.items())
def atomic(path,old,new):
    tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(new)
    assert path.read_bytes()==old;os.replace(tmp,path)
review.update(visualReviewPending=False,continuousPlaybackWatched=False,normalInstalled=False,reviewed='All94 chronological source/native pairs in eight boards inspected. Case ownership and first departure preserved. Visible head/collar orientation switch between V9 interiors1/2; shoulder/body changes remain abrupt. Revised rise reaches exact canonical terminal; full smoothness/master acceptance remains incomplete.',visualAcceptance=False)
atomic(reviewpath,reviewpath.read_bytes(),(json.dumps(review,indent=2)+'\n').encode())
bridge=r/'character/james-cargo-return-bridges-v1'
package=json.loads((bridge/'collar-v10-package.json').read_bytes())
cg=json.loads((bridge/'package-collar-v10-validation.json').read_bytes())
assert package['protectedOriginalPixels']==63184 and cg['exitCode']==0 and cg['realProfileUnchanged']
verdict={'selected':False,'accepted':False,'reason':'Generated head skin/forehead is warmer/brighter; badge and shoulder detail change within edit rectangle. Current drawing retained.','reviewed':'Four whole source poses plus four enlarged head/collar crops. No candidate native motion or helmet pair.','protectedOriginalPixels':63184,'raw':'collar-repair-v10-raw.png','prompt':'collar-repair-v10-prompt.txt','method':'Built-in image_gen edit; native uniform256/1254 downsample, original pixels protected outside104/72/49/48. No grade or translation.','rawSha256':hashlib.sha256((bridge/'collar-repair-v10-raw.png').read_bytes()).hexdigest(),'promptSha256':hashlib.sha256((bridge/'collar-repair-v10-prompt.txt').read_bytes()).hexdigest(),'firstFailure':'Expected1280square but actual1254square; preserved first log/guard, then inspected actual dimensions and corrected.','ownerProfileUnchanged':True}
(bridge/'collar-v10-verdict.json').write_text(json.dumps(verdict,indent=2)+'\n')
section='''## James full West return reviewed; collar repair rejected — October 2, 2026

Full prescribed East-to-West carry power-loss return now captured through V9
bridge, revised riseV6/unload7, and first departure, both gears.1277native checks,
0failures/engine0;14120ms updates per gear,20 admitted row identities each,
94 source-change/texture-change native/source pairs reviewed in eight boards.
40 prelaunch input hashes unchanged; scratch APPDATA/owner profile unchanged.
Four lossless APNGs verify184decoded RGB/unequal-duration checks. Adjacent equal
images may coalesce with accumulated duration; actual timestamps retained, final
620ms hold is viewer-only. No continuously watched playback claim. Native evidence
scope retains obsolete no-full-V9 wording; review explicitly corrects it from
actual row coverage, without upgrading fixture evidence to natural scheduling.

Case remains fixed through rise and departure, canonical terminal body joins idle.
Visible head/collar switch between V9 interior1/2 and abrupt shoulder/body changes
still prevent full visual acceptance. Built-in targeted bare collar V10 raw/prompt
saved; native package protects63184 original pixels outside104/72/49/48. One
raw-dimension assumption failed(1280expected/1254actual), first evidence retained;
corrected inspected uniform256/1254 packaging passes, owner unchanged. Four source
poses and enlarged collars reviewed: face warmer/brighter, shoulder badge/detail
changed. Candidate rejected; normal selection and preferred staged V9 unchanged.
No paired helmet repair, candidate motion, normal installation or title Continue.

Lesson: protecting pixels outside a rectangular collar edit does not protect a
badge inside it or prove facial material continuity. Require consecutive-source
review of identity, shoulder markings and neck before pairing/admitting a repair.
Read actual raw dimensions; never infer them from displayed image size. Lossless
animation verification must handle identical frames coalescing with summed holds.
Next coherent collar/shoulder repair with protected identity/badge, full motion
recheck, normal state/render/save integration/title Continue, directional/master/
context and cross-family polish. Full goal incomplete. No commit/export.
Evidence:character/james-floor-case-west-v1/full-return-v6-review/review.json;
character/james-cargo-return-bridges-v1/collar-v10-verdict.json.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() not in old:atomic(path,old,section.encode()+b'\n'+old if path.name=='CURRENT_STATUS.md' else old+b'\n\n'+section.encode())
handoff='''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James full West return review

## Objective and acceptance
Full James set matching masters/style/camera/size/height/proportions/matte grade,
then cross-family polish. Incomplete; revised West lifecycle remains staged.

## Accepted decisions and constraints
Paired V9 bridge/riseV6/unload7/caseV7 and staged checkpointV2 retained. Exact
original release4, canonical terminal, fixed room case. Owner saves untouched.

## Current state
Full return fixture/evidence/40input freeze, eight boards/four lossless APNGs and
review_full_return_v6.py.94paired presentations inspected. V10bare collar raw,
exact built-in prompt/native package/UID/review/verdict saved in bridge folder;
candidate rejected for facial material/badge drift. Five maintained guides updated.

## Verification
1277native checks0fail/both gears/20row identities each/141updates each,
94source/world pairs/184lossless RGB-duration checks/40hashes unchanged.
Owner unchanged. One rejected collar candidate63184protected original pixels,
native package engine0/owner unchanged; first raw-size failure retained.

## Next action
Repair V9collar/shoulder join while preserving face palette and badge; pair helmet
and review complete return. Normal actor/player/render/catalog/save installation,
normal title/new-process Continue, ordinary unload/natural scheduling, all cardinals/
master/context/cross-family polish remain. Do not infer full acceptance from checks.
No commit/export. Goal active/incomplete.
'''
atomic(p/'HANDOFF.md',(p/'HANDOFF.md').read_bytes(),handoff.encode())
print('Full-return review and rejected collar candidate recorded; five guides and handoff updated.')
