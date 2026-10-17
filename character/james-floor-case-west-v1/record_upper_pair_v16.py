from pathlib import Path
import json,hashlib,os,uuid
p=Path(__file__).resolve().parent;r=p.parents[1];b=r/'character/james-cargo-return-bridges-v1'
def atomic(path,old,new):
    assert path.read_bytes()==old
    temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');temp.write_bytes(new)
    assert path.read_bytes()==old;os.replace(temp,path)
guard=json.loads((p/'full_return_upper_v16-validation.json').read_bytes())
evidence=json.loads((p/'full_return_upper_v16-evidence.json').read_bytes())
assert guard['exitCode']==0 and guard['realProfileUnchanged'] and not guard['timedOut']
assert evidence['checks']==1317 and evidence['failures']==0
freeze=json.loads((p/'full_return_upper_v16-inputs.json').read_bytes())
assert len(freeze)==70 and all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in freeze.items())
audit=json.loads((b/'selected-join-audit-v9/audit.json').read_bytes())
assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in audit['inputs'].items())
reviewpath=p/'full-return-upper-v16-review/review.json';old=reviewpath.read_bytes();review=json.loads(old)
assert review['pairs']==102 and review['decodedRgbAndDurationChecks']==200
review.pop('evidenceScopeCorrection',None)
review.update(visualReviewPending=False,continuousPlaybackWatched=False,fullVisualAcceptance=False,preferredNormalSelectionChanged=False,
    reviewed='All ten boards/all102 source-native presentations inspected chronologically, both gears including changed bridge row11, adjacent row12, full release/rise/standing and departure. Collar/identity closer than full-figure V13/14, case lifecycle coherent. Helmet crown step remains2native pixels and moves from bridge2-to3 to3-to4; source upper-region largest step essentially unchanged. Single-interior trial is insufficient; no normal admission.',
    scope='Prescribed power-loss cargo returns with staged injected actor/player/shared-case view on current main/native renderer.20ms actor updates, all20finite source row identities per gear plus departure. Not natural scheduling, normal save/title admission of new trial, continuously watched motion or full master/cardinal acceptance.')
atomic(reviewpath,old,(json.dumps(review,indent=2)+'\n').encode())
path=b/'existing-upper-source-review/review.json';old=path.read_bytes();sources=json.loads(old)
assert len(sources['sources'])==30
assert all(hashlib.sha256((r/x['source']).read_bytes()).hexdigest()==x['sha256'] for x in sources['sources'])
sources.update(visualReviewPending=False,finding='All six boards/30 source presentations and enlarged upper crops inspected. Sampled existing East-West/reverse/South-West cargo turns repeat outgoing heads or other view angles; no suitable intermediate for this source join found in these samples. Not an exhaustive library search or master acceptance.')
atomic(path,old,(json.dumps(sources,indent=2)+'\n').encode())
for version,mode in [(15,'bare'),(16,'helmet')]:
    package=json.loads((b/f'upper-v{version}-package.json').read_bytes())
    assert package['protectedOriginalPixels']==61476 and package['translation']==[96,56]
    assert (b/f'package-upper-v{version}.gd.uid').exists()
    path=b/f'upper-v{version}-source-review.json';old=path.read_bytes();source=json.loads(old)
    assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in source['inputSha256'].items())
    source.update(visualReviewPending=False,selected=False,pairedNativeReview='full-return-upper-v16-review/review.json',
        verdict='Enlarged crop retains closer registration/material/identity than previous whole-figure edits. Unselected: single-interior edit insufficient to distribute head/helmet step across neighbors. See native review and transition diagnostics.')
    atomic(path,old,(json.dumps(source,indent=2)+'\n').encode())
diagnostic=json.loads((b/'upper-v16-transition-diagnostics.json').read_bytes())
assert diagnostic['gears']['helmet']['stagedPair16']['maxCrownStep']==2
verdict={'selected':False,'normalV9Unchanged':True,'nativeChecks':1317,'nativeFailures':0,'sourceNativePairsReviewed':102,'inputHashesUnchanged':70,'apngRgbDurationChecks':200,
    'method':'Built-in image_gen, separate bare15/helmet16 edits of original80square upper crop enlarged8x; raw1254square, native Godot uniform80/1254resample and original96/56crop origin; no grade or pose normalization.',
    'finding':'Closer collar/source registration but temporal join not resolved. Helmet crown156,156,156,156,158,158 delays original2px rise one frame. Largest upper-region premultiplied pixel step190505 vs190487 normal. Bare peak117943 vs118680; neither pixel diagnostic proves anatomical motion. Need adjacent articulated intermediate poses, not single-frame cleanup.',
    'protectedPixelsEach':61476,'scope':'Staged paired complete prescribed return; no candidate normal save/title or full natural/master acceptance.',
    'raw':['upper-crop-v15/raw.png','upper-crop-v16/raw.png'],'prompts':['upper-crop-v15/prompt.txt','upper-crop-v16/prompt.txt']}
(b/'upper-pair-v16-verdict.json').write_text(json.dumps(verdict,indent=2)+'\n')
section='''### James paired enlarged-crop return trial — October 2, 2026

Reviewed30existing cargo-turn/idle sources and enlarged crops; no suitable missing
intermediate in sampled heads. New built-in bare15/helmet16 upper-crop edits retain
raws/prompts/reference hashes:80square at96/56,8xreference enlargement,1254raw,
uniform80/1254native Godot reduction/original crop origin, no grade/pose fitting.
61476original outside pixels exact each. Paired candidate changes only bridge3;
original endpoints/body/case/root preserved; normal V9 bank hashes unchanged.

Staged complete prescribed native returns1317checks0fail/engine0/scratch APPDATA/
owner unchanged,70targeted pre/post hashes stable.141updates per gear at20ms,
all20finite rows,102source-native presentations/all10boards inspected;200decoded
APNG RGB/unequal-duration checks. Injected candidate actor/player/view, not new
normal save/title admission or natural scheduling/continuous/full master acceptance.
Case release/rise/departure behavior coherent; cropped edit closer than V13/14.

Temporal repair still insufficient: helmet crown156,156,156,156,158,158 moves2px
rise one frame later, max step unchanged. Upper-region pixel peak190505 vs190487
normal; bare117943 vs118680. Region pixel metrics are diagnostics, not motion
vectors. Trial unselected. Next revise adjacent head/collar/shoulder intermediates
together; a good-looking isolated crop or delayed pop does not solve continuity.
Keep endpoint identity/physical registration/matte grade, then paired full native
motion and versioned normal save admission. Full set/context/master polish remains.
Evidence: character/james-cargo-return-bridges-v1/upper-pair-v16-verdict.json;
character/james-floor-case-west-v1/full-return-upper-v16-review/review.json.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() in old:continue
    if path.name=='CURRENT_STATUS.md':
        marker=b'### James coherent upper-body trials V13/V14';at=old.index(marker);new=old[:at]+section.encode()+b'\n'+old[at:]
    else:new=old+b'\n\n'+section.encode()
    atomic(path,old,new)
handoff='''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James West upper join

## Objective and acceptance
Full James set matching masters/style/perspective/height/proportions/matte grade,
then cross-family polish. Incomplete; normal West cargo V9/riseV6/caseV7 installed.

## Accepted decisions and constraints
Preserve owner saves/layouts, source registration and concurrent crew work. V10–14
rejected; enlarged upper pair15/16 unselected after temporal review. No commit/export.

## Current state
Normal James actor/player/workshop/checkpoint scripts and main/grid/save hooks
remain selected. New existing-upper-source-review(30sources), upper-crop-v15/16
raw/prompt/hashed references, native packages/UIDs, trial paired manifests16,
full_return_upper_v16 fixture/UID/evidence/70inputs/102pair review/4APNGs.
Transition diagnostics and upper-pair-v16-verdict; five maintained guides updated.

## Verification
New staged complete returns1317checks0fail/102source-native pairs/all10boards
inspected/200decodedRGB-duration checks/70hashes unchanged. Scratch APPDATA,
owner unchanged/engine0.61476outside original pixels exact per upper trial.
Earlier normal checkpoint424/title148/legacy30/ordinary72checks0fail retain their
own scope/revisions; new trial has no normal save/title admission. Temporal join
still fails: helmet2px rise delayed one frame, max jump unchanged. Collar closer;
no continuous playback/full master/natural scheduling acceptance. NormalV9 hashes
unchanged. No live native handle remains after session48811 completed successfully.

## Next action
Author adjacent coherent upper intermediates, preserving face/helmet/badge identity
and original physical registration, distribute orientation/crown changes through
neighbors; then paired complete native motion before versioned normal admission.
Other cardinal/held cargo, room rotations/natural priorities, full directional
master/material/height/proportion/context and cross-family polish remain.
Goal active/incomplete, no blocker.
'''
path=p/'HANDOFF.md';atomic(path,path.read_bytes(),handoff.encode())
print('Paired trial fully reviewed and recorded; normal V9 unchanged; temporal join remains open.')
