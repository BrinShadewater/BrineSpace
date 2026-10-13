"""Record actual quarter-turn evidence and frozen next own-facing source."""
from pathlib import Path
import hashlib,json,subprocess,sys
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-carry-turn-material-v1';S=B/'sources';A=ROOT/'output/marsh-animation-audit/carry-turn-east-south-01-2026-10-02'
MARKER='## Marsh East-South carry quarter turn on actual path corner — October 2, 2026'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((S/'east-south-01.request.json').read_text());assert r['generationId']=='exec-876013eb-69c1-4a78-b7e1-c80e78d3c01f' and sha(S/'east-south-01.prompt.txt')==r['promptSha256'] and sha(S/'east-south-01.raw.png')==r['rawSha256']
assert sha(Path(r['originalGeneratedPath']))==r['rawSha256']
for q in r['orderedReferences']+r['sourceFrames']+r['guideDependencies']:assert sha(ROOT/q['path'])==q['sha256']
p=json.loads((B/'east-south-01-unselected/recipe.json').read_text());assert p['exactEndpointCopies']==4 and p['apngExactDecodedFrames']==5
for q in p['stagedEndpoints']:assert sha(ROOT/q['path'])==q['sha256']
report=json.loads((A/'report.json').read_text());assert report['checks']==482 and report['failures']==0 and len(report['captures'])==12 and len(report['samples'])==140 and report['actorRestores']==5
for name,total in [('inputs',90),('owner',2931)]:
    before=json.loads((A/f'{name}-before.json').read_text());assert before==json.loads((A/f'{name}-after.json').read_text()) and len(before)==total
    assert json.loads((A/'failed-parse'/f'{name}-before.json').read_text())==json.loads((A/'failed-parse'/f'{name}-after.json').read_text())
assert (A/'native-exit.txt').read_text().strip()=='0' and 'ERROR:' not in (A/'native.log').read_text()
O=B/'east-south-01-actor-review';(O/'visual-assessment.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'allTwelvePairsInspected':True,'viewCount':12,'pairedBoardsInspected':3,'findings':'Selected East idle,initial East cargo,all5 actual East-to-South turn phases,all4 destination South cargo phases and final pause seen. Head/torso/arms/case yaw progresses toward frontal;crate remains supported with visible near hands and latches emerge through yaw. Exact endpoint/return source match. Intermediate3 head still looks slightly right relative nearly frontal torso;head/body/grade/torso registration and continuous physical contact remain provisional.','limits':'Actual native path-corner/player/restore behavior controlled140x20ms;held snapshots/APNG illustration are not realtime continuous film/full scene,reverse path,complete pickup/unload,normal full save/visible TitleContinue or full-set acceptance.'},indent=2)+'\n')
subprocess.run([sys.executable,str(ROOT/'tools/publish_marsh_carry_turn_eastsouth01_actor.py')],check=True,stdout=subprocess.DEVNULL)
pending=json.loads((S/'west-south-01.request.json').read_text());assert pending['status']=='frozen before generation; not started' and sha(S/'west-south-01.prompt.txt')==pending['promptSha256']
for q in pending['orderedReferences']+pending['sourceFrames']+pending['guideDependencies']:assert sha(ROOT/q['path'])==q['sha256']
g=json.loads((S/'guide-provenance.json').read_text());assert len(g['selectedTurns'])==12
(B/'east-south-01-unselected/assessment.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'rawSourceInspected':True,'packedFivePoseComparisonInspected':True,'neutralComparisonInspected':True,'forwardNativeReviewed':True,'reversePixelsVerified':True,'reverseActualPathReviewed':False,'selectedDestinationIdleSize':[58,147],'generatedNeutralSize':[62,147],'limits':'Source ruler width+4 diagnostic only;3head relative torso yaw/foot motion/grade/registration/full family joins provisional. Native forward12pairs only.'},indent=2)+'\n')
maintained=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md';installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md');assert maintained.read_bytes()==installed.read_bytes(),'skill mirror drift'
lesson='''

## Marsh East-South carry quarter turn on actual path corner — October 2, 2026

Current ordered catalog audited:12selected old carry-turn states,8adjacent5frames
at60/90/100/90/60ms(400ms),4opposite9frames at60/90/100/90/120/90/100/90/60ms
(800ms). New staged endpointsSouth01/North01/East03/West03 and selected own idles
frozen with SHA provenance;whole pair guides/old motion-only boards retained.
Old helpers use recolour/per-pose heuristics;do not apply those to current whole
master repair. Existing old supplemental/bare reproduction tests are not proof of
current staged body/turn coherence. Runtime finished-turn resets destination gait
to frame0;verify actual get-frame/player behavior,not just manifest endpoint arrays.

EastSouth01 exec-876013eb-69c1-4a78-b7e1-c80e78d3c01f raw/exact frozen prompt/
four orderedrefs retained:paired selected body PRIMARY,paired staged cargo
endpoints,own originalEast,own originalSouth. Three complete intermediate yaws
plus unobstructedSouth ruler;ONE neutral147BOXscale.203601108033241 gives
67x143/63x146/61x146/ruler62x147 vsselected58x147. Neutral width diagnostic,
not body/cargo-width fitting. Alpha128 whole cells,no clipped opaque pixels,
no mirror,limb/crate patches,recolour or per-pose fit. Endpoints byte-identical
copies in both directed states;return reverses whole frame order only. Forward
APNG5decoded frames exact400ms. Raw/used guides/5posecomparison/ruler seen.
Head/torso/case rotates toward front,implant retained correctly,latches reveal
throughyaw. Intermediate3 head still slightlyright relative near-frontal torso;
material/rigid-case/foot motion/full family joins remain provisional.

Cargo silhouette should not define body registration: builder measures alpha
chest-row midpoint at28%occupiedheight(above case),interpolates target torsoX
from exact staged endpoints,then applies whole integer translation. One common
scale,not independent bbox-centering/torso or limb edits. Row/alpha measures are
registration diagnostics,not anatomical landmarks/sole contact proof. Review
resulting complete pose and rendered join;camera/pivot metadata alone cannot
certify registration. Generic bbox bottom172 remains only packing anchor.

Actual normal Marsh factory/controller/main/grid/player on clearEast64/South96
path corner passed482checks,12exact source/native pairs,140controlled20ms samples,
5movingturn actor/player restores+pauseholds,all5turn phases and4destination
phases,exact destinationcarry0return,finalpause,0failures/engine errors,exit0.
90boundedinputs equal DURING native interval;2931owner nonlog files unchanged
with scratchAPPDATA. All12pairs/3boards inspected. Normal workshop_carry rate46
and run exclusion kept. Dedicated free furnished site only;normal economy/failure
flags unchanged,not paid-build proof. No fullRunSave/TitleContinue,actual reverse
corner,completepickup/unload,continuous contact/fullscene acceptance. Held5phase
APNG uses400ms illustrative crops,not a realtimefilm. Reverse whole pixel order
verified by player but onlyforward actual path tested.

Initial fixturefailed parse beforestartup:dynamic actor segment_clear expression
could not inferclear'stype. Added explicitbool only,retained failed log/fingerprints
underfailed-parse;owner/input files equal infailed interval aswell. Godot exit0
despiteparseerror:require cleanERROR log and report/check counts,not exitcodealone.
Successful native77646 terminal0. No source changed tofixfixture. Publication
helper created separately;90freeze covers runtime/source/fixture duringinterval.
Next request addedafterinterval doesnotinvalidate dated equality,but do not claim
all current sharedsource folder bytes are that90-file frozen tree.

OwnWestSouth01 frozen before generation;PRIMARY paired own body/paired staged
endpoints/ownWest+South originals. WholeWest/Southguides andoldmotionboard seen,
masters alreadyseen andunchangedSHA. BARE Westvisibletemple,implantfarhidden
untilfront,caseleftlatch→front2latches,WestactorLEFTsupport→SouthactorRIGHT
support transferexplicit. PreserveguideboardLEFTWest/RIGHTSouth positions while
changingheading;never globalRIGHT/LEFTswap anatomicalimplant/guidepositions.
GenerationNOTSTARTED,nojob live. EastSouthpair staged/unselected,normalcatalog
unchanged.2directednewquarterstates exist,only1actualpathreview;10turnstates
stillneed sourceassembly,thenreverse/opposite native/heldjoins,independentnormal
fullsaves/visibleContinues andfullcross-family consistency/polish.Goalactive.
'''
for path in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',maintained]:
    with path.open(encoding='utf-8') as f:present=any(MARKER in line for line in f)
    if not present:
        with path.open('a',encoding='utf-8') as f:f.write(lesson)
installed.write_bytes(maintained.read_bytes())
(ROOT/'docs/MARSH_CARRY_TURN_EASTSOUTH01_HANDOFF_2026-10-02.md').write_text('''# Project handoff

Updated: October 2, 2026 · BrineSpace · Marsh carry quarter turns

## Objective and acceptance
Full master-matched set/consistency/polish active and incomplete. EastSouth01
authored/packaged andactual forward path-corner native reviewed. Reverse frame
sequence exact but reverse path not tested. Normal catalog/carries unchanged.
WestSouth01 frozen,not generated. No livejob;native77646 terminal0.

## Decisions and constraints
Own selected idles/body PRIMARY;stagedSouth01/North01/East03/West03 endpoints
exact,no mirror/recolour/limb orcrate patch/per-pose fit.3wholeyaws+one neutral147
BOXscale;184p92/172H148. Interpolate whole torso-row registration from endpoint
chest midpoints;not independent cargo-bbox centering or anatomicalproof.
Selected quarter400ms/half800ms timings remain. ScratchAPPDATA andfingerprints.

## Current state and changed files
prepare_marsh_carry_turn_material_guides.py retains selected12turn metadata and
four ownstagedendpoints/idles/originalmasters;pairedbody/cargoandoldmotionguides.
EastSouth01prompt/request/rawID/original/SHA,fourwholecells,newgenericbuilder,
east-south-01-unselected two5frame directedstates/exactendpoints/reverse/APNG/
comparison/ruler/recipe/assessment. Nativepreparer/fixture+UID/fingerprinter/
publisher,east-south-01-actor-review12pairs/3boards/evidence/assessment.
WestSouth01preparer/frozenprompt/request. Pipeline,bible,currentstatus and both
master-repairskillmirrors appended. No gameplay/catalog/export change.

## Verification and limits
Source exec-876013eb-69c1-4a78-b7e1-c80e78d3c01f exactprompts/ref/source hashes
retained,revalidated. One scale.203601108033241:67x143/63x146/61x146/ruler62x147
vsselectedSouth58x147. Raw/guide/5pose/ruler inspected. Fourbyte-identicalendpoint
copies,reversewholeorder,5exactAPNGdecodedframes. Intermediate3head stillslightly
right relative torso;grade/registration/feet/fullfamily joins provisional.
Actual East64/South96 path corner:482checks/12exactpairs/140samples/5restores/
pauseholds/all5turn+4destinationphases/exactSouth0return/finalpause,0fail/engine
errors/exit0.90inputs equalDURINGinterval,2931ownerfilesunchanged.All12pairs and
3boardsseen. Initialparsefailure retained underfailed-parse,explicitboolfix only;
Godot exit0 wasinsufficient. No fullsave/TitleContinue/reversepath/completepickup
unload/continuouscontact/fullscene acceptance. Sharedsource folder gained pending
West requestafterdated interval;don'tclaim current enumeration identical to90.

## Remaining work and next action
Generate frozen WestSouth01 exactprompt/fourorderedrefs;allusedguides/mastersseen.
Retain original/rawID/SHA immediately,pack genericbuilder --pair west-south
--source west-south-01 --generation-id RETURNEDID. Inspectbody/head/crateyaws/
hidden→visibleimplant/weighttransfer/registration,thenstage ownactualWest→South
pathcorner. NewEastSouth2directed states,10otherturnstates needassembly;all reverse/
opposite paths and held joins,normalfullsaves/visibleContinues andfullconsistency/
polish remain. Full goal active;normal selections unchanged.
''',encoding='utf-8')
print('Recorded actual EastSouth482/12 and exactquarterjoins;WestSouth requestfrozen;skillmirrors equal;goal incomplete.')
