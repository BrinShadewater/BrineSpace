from pathlib import Path
import json,hashlib,os,uuid,runpy
from PIL import Image
p=Path(__file__).resolve().parent;r=p.parents[1]
def atomic(path,new):
    old=path.read_bytes();tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(new)
    assert path.read_bytes()==old;os.replace(tmp,path)
guard=json.loads((p/'native_probe-validation.json').read_bytes());assert guard['exitCode']==0 and guard['realProfileUnchanged']
assert any('332 checks, 0 failures, 34 native captures' in s for s in guard['summary'])
review=json.loads((p/'native-review.json').read_bytes());before={name:hashlib.sha256((p/name).read_bytes()).hexdigest() for name in review['pages']}
runpy.run_path(str(p/'review_native.py'))
assert all(hashlib.sha256((p/name).read_bytes()).hexdigest()==v for name,v in before.items()),'Normal captures differ from staged reviewed boards'
pack=json.loads((p/'helmet-manifest.json').read_bytes());decoded=0
for s in pack['states']:
    frames=[Image.open(p/'native'/f'{s["id"]}-{i:03d}.png').convert('RGB') for i in range(int(s['frameCount']))]
    path=p/(s['id']+'-preview.png');frames[0].save(path,save_all=True,append_images=frames[1:],duration=s['frameDurationsMs'],loop=0)
    with Image.open(path) as im:
        assert im.n_frames==len(frames)
        for i,f in enumerate(frames):
            im.seek(i);assert im.convert('RGB').tobytes()==f.tobytes();assert abs(im.info['duration']-s['frameDurationsMs'][i])<.01;decoded+=1
review=json.loads((p/'native-review.json').read_bytes());review.update(visualReviewPending=False,normalLoaderVerified=True,normalBoardsByteIdenticalToReviewedStagedBoards=True,decodedPreviewRGBAndDurationChecks=decoded,selected=True,continuousPlaybackWatched=False)
atomic(p/'native-review.json',(json.dumps(review,indent=2)+'\n').encode())
cap=json.loads((p/'cap-review.json').read_bytes());cap.update(visualReviewPending=False,selected=True,normalAdmission='Four equipped turn states only, selected through final normal grid load order; face/collar/body unchanged. Native332checks0fail. Continuous/native natural-world cadence pending.')
atomic(p/'cap-review.json',(json.dumps(cap,indent=2)+'\n').encode())
pack['status']='selected_normal_loader_checked_helmet_cap_polish_cadence_pending'
atomic(p/'helmet-manifest.json',(json.dumps(pack,indent=2)+'\n').encode())
active=r/'character/ACTIVE_ASSETS.json';data=json.loads(active.read_bytes());data['actionOverrides'].pop('branforth-turn-helmet-cap',None);data['equipmentActionOverrides']['branforth-turn-helmet-cap']='character/james-helmet-turn-dip-v1/helmet-manifest.json'
atomic(active,(json.dumps(data,indent=2)+'\n').encode())
audit=json.loads((r/'character/james-selected-turn-master-audit-v1/review.json').read_bytes())
unchanged=[k for k,v in audit['inputSha256'].items() if k!='scripts/grid_canvas.gd' and hashlib.sha256((r/k).read_bytes()).hexdigest()==v]
assert len(unchanged)==len(audit['inputSha256'])-1
evidence={'selected':True,'normalLoaderChecks':332,'failures':0,'pairedNativePresentationsReviewed':34,'decodedRGBAndDurationChecks':decoded,'normalBoardsExactToStagedReviewedBoards':True,'priorAuditSourceInputsUnchanged':len(unchanged),'intentionalRuntimeChange':'grid_canvas final four-state equipment cap override','realProfileUnchanged':True,'stagedFirstFixtureFailure':'332checks4fail fixed .8s assumption for1.6s halfturns, source unchanged','normalValidation':'native_probe-validation.json','prompt':'prompt.txt','raw':'raw.png','capSource':'candidate-cap.png','protectedOriginalPixels':64536,'scope':'Narrow helmet crown repair selected. No natural-world cadence, full master/context or complete James acceptance.'}
(p/'selection-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
section='''### James helmet cap dip corrected and selected — October 2, 2026

Enlarged SouthWest shell/collar views isolate undersized crown in row2, not body
height. Original builder fits angular shells with independently changing width
scales (.313,.283,.269 neighboring rows), exposing silhouette-size variation.
Built-in imagegen narrow crown source retains raw1254/exact prompt/pre-call hashes.
Uniform64/1254 crop reduction; generated cap framing overshoots2px, explicit cap
attachment(96,58) seats new cap at neighbor crown. OnlyRect10264..15284 admitted:
64536original pixels exact, face/collar/shoulders/body/case/feet protected, no grade
or wholebody move. Diagnostic154dip→156 matches neighboring156; not anatomy proof.
Cap and whole comparisons inspected; correct shell contour without face redesign.

Reuse same cap at SouthWest2/reverse3/EastWest7/reverse3 with all endpoints/holds
intact. Staged native332checks0fail/34paired captures; normal grid final equipment
override independently332checks0fail/engine0/owner profile unchanged under scratch
APPDATA. All34paired presentations reviewed/four contactboards; normal boards
byte-identical to reviewed staged boards.34APNG decoded RGB/duration checks/actual
manifest holds, no added viewer hold. Continuous watched/natural world cadence
still pending. First fixture332/4fail preserved: quarter .8s assumption wrongly
applied to1.6s halfturns; fixture corrected, source unchanged.224prior audit inputs
unchanged excluding intentional grid addition. ACTIVE_ASSETS and final equipment
manifest updated after tests (status metadata only). Body bank not overridden.

Lesson: trace shell-fit scale and collar seat before altering whole anatomy.
Authored equipment cap can fix crown silhouette while protecting original face
and entire body; make source registration compensation explicit, not hidden pose
normalization. Propagate once to exact quarter/half/reverse aliases and test actual
final normal load order. Save/native/pixel evidence does not certify continuous
motion/full master matching. Next normal cadence/context review, remaining West
return join and cross-family polish. Five guides updated; full goal incomplete.
Evidence: character/james-helmet-turn-dip-v1/selection-evidence.json and HANDOFF.md.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() in old:continue
    if path.name=='CURRENT_STATUS.md':
        at=old.index(b'### James selected dry-turn master comparison');new=old[:at]+section.encode()+b'\n'+old[at:]
    else:new=old+b'\n\n'+section.encode()
    atomic(path,new)
handoff='''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James helmet turn polish

## Objective and acceptance
Full James set matching masters/style/camera/height/proportions/matte grade, then
cross-family polish. Incomplete; normal V9 return/riseV6/caseV7 unchanged.

## Accepted decisions and constraints
Correct equipment shell silhouette while preserving canonical face/collar/body.
No wholebody normalization, owner-profile mutation, commit or export.

## Current state
character/james-helmet-turn-dip-v1 raw/prompt/inputs/source/cap package/review,
4state equipment manifest and paired bare test manifest, native probe/UID/34
captures/four APNG previews. Normal grid final helmet override and ACTIVE_ASSETS
updated. Five guides updated. Cap selected, full set not accepted.

## Verification
64536original pixels outside cap exact; crown154→156, body/face/collar unchanged.
Staged332/0 and independent normal332/0, owner unchanged/scratchAPPDATA/engine0.
All34paired native presentations reviewed; normal contactboards exact to staged.
34APNG RGB/duration checks;224prior targeted sources unchanged. First fixture
332/4fail duration-assumption interval retained; fixed for actual halfturn1.6s.
Native test predates manifest status-only/ACTIVE metadata update. No continuous
watched cadence/natural context/master or full-set acceptance. No live job.

## Next action
Review normal turn cadence/context and remaining shell rebound, West return
head/collar join, other families/context/master/grade/proportions. Goal active,
incomplete; no blocker. Preview: carry-turn-south-west-preview.png.
'''
(p/'HANDOFF.md').write_text(handoff,encoding='utf-8')
print(json.dumps(evidence))
