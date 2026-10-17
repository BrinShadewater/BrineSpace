from pathlib import Path
import json,hashlib,os,uuid
p=Path(__file__).resolve().parent;r=p.parents[1]
for name in ['early','late','meter']:
    inputs=json.loads((p/(name+'-inputs.json')).read_bytes());assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==h for k,h in inputs['preCallSha256'].items())
    path=p/(name+'-review.json');data=json.loads(path.read_bytes());assert data['protectedOutsideExact']
    data.update(visualReviewPending=False,sourceAcceptance=False,selected=False,disposition='provisional_local_source_repair',findings=(['Raw/full/head comparisons inspected. Crown76/sole224 restored by generated roof-band pixels;65288outside pixels exact.','Admission roof also includes upper forehead-goggle edges; do not claim complete goggles byte-exact. Face/ears/collar/body/case/feet outside region unchanged.','Fixed contour is not whole head/master anatomy or temporal/gear acceptance.'] if name!='meter' else ['Actual late/West belt crop comparison exposes extra lower grey/yellow-screen box. Raw/full/detail repair views inspected; lower copy removed, retained upper partial meter unchanged.','65440pixels outside8x12rectangle exact, including head repair, case/feet/upper retained meter. No dark cavity or blank alpha hole in repaired hip.','Single corrected late pose; remaining source-family tool design/occlusion needs full-family review.']))
    path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
native=json.loads((p/'native-review.json').read_bytes());assert native['checks']==354 and native['failures']==0 and native['profileUnchanged']
native.update(visualReviewPending=False,sourceAcceptance=False,selected=False,sourceNativePairsReviewed=10,comparisonBoardsReviewed=2,findings=['All10source/native pairs inspected in both prescribed state chronologies at148/82/54/27rulers. Boots remain on baseline; source order/size/case grip as staged.','Software comparison sampler is independent and differs from native filtering; no native RGB equivalence claim.','Standalone bare candidate only; actual crew dispatch, advancing natural world movement/cargo room and fresh Continue untested.'])
(p/'native-review.json').write_text(json.dumps(native,indent=2)+'\n',encoding='utf-8')
path=p/'review.json';data=json.loads(path.read_bytes());assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==h for k,h in data['sourceSha256'].items())
assert all(b[1]==76 and b[3]==224 for b in data['nativeAlpha128Bounds'])
data.update(visualReviewPending=False,sourceAcceptance=False,selected=False,disposition='provisional_bare_source_native_clock_checked',previewDecodeChecks=20,findings=['Raw/local full/head/tool and final whole/upper/legs/station boards inspected. Five distinct intended front-to-left source orientations, two-hand case, planted feet and crown76/sole224 across all five.','Head roofs and upper goggle-edge treatment modified only inside31x8 bands, not a whole-head shift/scale. Late lower duplicate removed only inside8x12hip region.','Both finite800ms forward/reversed candidate manifests retained.20APNG RGB/duration checks cover forward/reverse source playback media, endpoint600ms hold/replay is viewer only.','Bare standalone player354checks/0failures/84prescribed20ms samples and10observed source-change captures; all10source/native pairs reviewed; owner profile unchanged.','Technical/source-frame success does not prove continuously watched cadence, shared helmet proportions, normal carry gait/task joins, actual cargo room contact, fresh Continue, owner or full master/cardinal/context acceptance. Full James/cross-family objective remains incomplete.'])
path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
section='''### James carried head contours and single-meter repair — October 2, 2026

New character/james-carry-headcaps-v1 locally repairs early2pixel and late1pixel
high roofs with built-in imagegen crops. Native64square at96/64,31x8roof bands;
65288outside pixels exact per pose. Band includes upper goggle edges; entire
goggles are not claimed unchanged. Face/ears/collar/body/case/feet outside exact.
Late/West diagnostic confirms extra lower meter; generated40square crop at120128,
8x12admission removes lower copy while retained upper partial meter stays exact;
65440outside pixels protected. Raw/local and final complete source boards reviewed.
All five crowns76/soles224, common148ruler; no per-pose fit/grade/body translation.

Bare standalone player354checks/0failures,84prescribed20ms samples,10observed
post-draw captures; all10source/native pairs reviewed forward/reverse at148/82/
54/27rulers. Source inventory from build before launch stable afterward; owner
profile unchanged under scratch APPDATA, clean engine. Initial fixture parse
failure retained/fixed with explicit filename type.20APNG RGB/duration checks;
reverse preview decodes sequentially then reverses cached images after Pillow
backward seek failed. Runtime800ms versus viewer600ms terminal hold/replay.

Lesson: successful pose should survive localized contour/tool repair, and complete
source/native chronology must be reviewed afterward. Exact roof geometry does
not prove head anatomy or smooth cadence. Frozen raw/prompt/input inventories
stable. Provisional bare candidate only; no shared helmet, normal carry-gait/task
joins, room/Continue/owner or full-master acceptance. Next paired helmet sources
at fixed body density, ordered gear/cadence and actual cargo joins/context checks,
then all cardinal/master/cross-family polish. Full goal active/incomplete.
Handoff:character/james-carry-headcaps-v1/HANDOFF.md.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() in old:continue
    if path.name=='CURRENT_STATUS.md':
        at=old.index(b'### James authored carrying turn angle progression');new=old[:at]+section.encode()+b'\n'+old[at:]
    else:new=old+b'\n\n'+section.encode()
    tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(new);assert path.read_bytes()==old;os.replace(tmp,path)
(p/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James carried roof/tool polish

## Objective and acceptance
Full master/style/perspective/size/height/proportion/matte James animations,
then full cross-family consistency/polish. Active/incomplete. Previous turn progress:
five-pose source progression and known head/tool differences isolated.

## Accepted decisions and constraints
Common256canvas/148standing ruler/pivot128224; no per-pose fit/grade or mirrored
tools. Keep successful body/grip/feet during local source edits. Existing normal
cap/V9/riseV6/caseV7 remain selected. Source/frame checks are limited evidence.

## Current state
Three generated raw/prompt/input pairs and local package helpers. Early/late roof
repairs65288outside exact; late duplicate removal65440outside exact. Both bare
finite800ms candidate states, complete chronology, forward/reverse APNG previews.
Native probe/UID and paired source/native comparison boards; review reports closed
provisional. Five guides updated; no normal loader/actor/save binding changes.

## Verification
All raw/local/final full/upper/legs/station boards inspected. All five crown76/
sole224. Three frozen generation inventories and pre-native built source hashes
stable. Native standalone bare354checks/0failures/84prescribed20ms samples,
10post-draw captures; all10source/native pairs reviewed at148/82/54/27. Original
owner profile unchanged under scratch APPDATA (brine-james-native-xsb78kh2).
Initial parse failure retained in native-first-parse files; explicit String fix.
Engine clean.20APNG RGB/duration checks pass forward/reverse, viewer final hold
600ms differs from800ms runtime. Backward Pillow seek failure corrected by
sequential decode/cache before reversal. New binary sources/previews use LFS.
Roof admission includes upper goggles, not all goggles unchanged. Only source
frames and prescribed player clocks reviewed; no continuous cadence, helmet,
normal dispatcher/gait joins, cargo room, fresh Continue or owner acceptance.

## Next action
Generate shared helmet source projections for all five corrected bare poses,
preserving exact paired bodies at common density and standing master gear endpoints.
Review all gear/turn/cadence and native source pairs, then actual carry gait/task
joins, room contact/interruptions/fresh Continue before versioned normal admission.
Finish full cardinal/context/master set and cross-family consistency/polish.

## Source provenance
Built-in imagegen:early roof exec-ce760d3c-b68f-4706-bb1a-3fd06b3428d8;
late roof exec-2c1c0b8a-e053-4a8b-9713-dd2f630d0813;
meter exec-13e2e521-4fb0-4714-96d8-f544e274a486.
Saved raw/prompt pairs:early-raw.png/early-prompt.txt,
late-raw.png/late-prompt.txt,meter-raw.png/meter-prompt.txt.
''',encoding='utf-8')
print('Three local source repairs and354/0native bare review closed provisional; five guides and handoff updated; full goal incomplete.')
