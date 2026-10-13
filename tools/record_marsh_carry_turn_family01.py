"""Record complete staged turn source matrix and exact native scope,not admission."""
from pathlib import Path
import hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-carry-turn-material-v1';S=B/'sources'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((S/'west-north-01.request.json').read_text());assert r['generationId']=='exec-fbe58206-f450-4c1f-a619-da99a2c00536' and sha(S/'west-north-01.prompt.txt')==r['promptSha256'] and sha(S/'west-north-01.raw.png')==r['rawSha256']==sha(Path(r['originalGeneratedPath']))
for q in r['orderedReferences']+r['sourceFrames']+r['guideDependencies']:assert sha(ROOT/q['path'])==q['sha256']
for audit,checks,views,samples,restores,inputs in [('carry-turn-west-north-01',482,12,140,5,125),('carry-opposite-east-west-01',570,16,160,9,215)]:
    A=ROOT/f'output/marsh-animation-audit/{audit}-2026-10-02';r=json.loads((A/'report.json').read_text());assert r['checks']==checks and r['failures']==0 and len(r['captures'])==views and len(r['samples'])==samples and r['actorRestores']==restores
    for name,total in [('inputs',inputs),('owner',2931)]:
        before=json.loads((A/f'{name}-before.json').read_text());assert before==json.loads((A/f'{name}-after.json').read_text()) and len(before)==total
    assert (A/'native-exit.txt').read_text().strip()=='0' and 'ERROR:' not in (A/'native.log').read_text()
O=B/'west-north-01-actor-review';(O/'visual-assessment.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'allTwelvePairsInspected':True,'viewCount':12,'pairedBoardsInspected':3,'findings':'SelectedWestidle/initialcargo/all5West-to-North/all4Northcarry/finalpause inspected. RearLEFT yaw,case held in front progressively hidden on screenLEFT,correct viewerLEFTplant intoNorth. OwnbareWesttemple retained,no mirror. First intermediate close to Westside,neutral59x146 vsselectedNorth55x146 width+4 and adulthead/body/grade/case/feet joins provisional.','limits':'Actualforward negativeX64/NorthnegativeY96 only. No reverse/fullRunSave/visibleTitleContinue/completepickup-unload/continuouscontact/fullsetacceptance.'},indent=2)+'\n')
O=B/'opposite-east-west-01-actor-review';(O/'visual-assessment.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'allSixteenPairsInspected':True,'viewCount':16,'pairedBoardsInspected':4,'findings':'SelectedEastidle/initialcargo/all9oppositephases/all4Westcarry/finalpause inspected. Exact North midpoint whole shared cardinal. Case remains frontheld and disappears then emerges on opposite side. Endpoint pixel/return exact. Quarter1s near side and head/grade/crate/weight joins remain provisional.','limits':'ActualEastpositiveX64/WestnegativeX96 U-turn800ms only,9actor-playerrestores/pause. No actualWestEast/NorthSouth/SouthNorth or reversequarters/fullsave/visibleContinue/continuouscontact/delivery/fullsetacceptance. Raw report inherited phrase quarter turn;actual cycle.8/ninephase evidence establishes opposite scope.'},indent=2)+'\n')
for n in ['publish_marsh_carry_turn_westnorth01_actor.py','publish_marsh_carry_opposite_eastwest01_actor.py']:subprocess.run([sys.executable,str(ROOT/'tools'/n)],check=True,stdout=subprocess.DEVNULL)
O=B/'opposite-01-unselected';recipe=json.loads((O/'recipe.json').read_text());assert recipe['wholeSourceCopies']==recipe['exactDecodedApngFrames']==36 and recipe['familyStates']==12 and recipe['familySlots']==76
for q in recipe['quarterInputs']:assert sha(ROOT/q['path'])==q['sha256']
for q in recipe['sourceParity']:assert sha(ROOT/q['path'])==q['sourceSha256']==sha(ROOT/q['copy'])
for q in recipe['sharedEndpointJoins']:assert sha(ROOT/q['sharedEndpoint'])==q['sha256']==sha(ROOT/q['secondSharedEndpoint'])
family=json.loads((O/'family-manifest.json').read_text());assert len(family['states'])==12 and sum(len(s['frameFiles']) for s in family['states'])==76
(O/'visual-assessment.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'wholeComparisonBoardsInspected':4,'wholeTurnPosesInspected':36,'findings':'EastWest andWestEast route viaNorth;NorthSouth/SouthNorth viaEast matches selectedtiming facings. Midpoint exactsharedcardinal appearsonce at120ms. All source/frame joins inspected;no mirror or rasteredit. Existing quarter angle repeats/bodywidth/head/casepanel/grade/support chronology propagate into halves and remain provisional.','nativeReviewedDirections':['east-west'],'nativePendingDirections':['west-east','north-south','south-north'],'reverseQuarterNativePending':['south-east','south-west','north-east','north-west'],'limits':'12state76slot private family only;fullstate/source count not fullset/art/normalSaveContinue acceptance.'},indent=2)+'\n')
maintained=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md';installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md');assert maintained.read_bytes()==installed.read_bytes(),'skill mirror drift'
marker='## Marsh full staged carry-turn matrix and first opposite path — October 2, 2026'
lesson='''

## Marsh full staged carry-turn matrix and first opposite path — October 2, 2026

OwnWestNorth01 exec-fbe58206-f450-4c1f-a619-da99a2c00536 retained exact frozen
prompt/four ordered refs/raworiginal/SHA. PairedselectedWest/North bodyPRIMARY,
stagedWest03/North01 cargo,ownWest+North originals. Three REAR-LEFT whole yaws
andneutralNorth146,oneBOXscale.21565731166912852 gives71x145/59x146/54x146/
ruler59x146 vsselected55x146. Caseheld IN FRONT progressively occluded on
screenLEFT,viewerLEFT supports nearback intoNorth;bareWest visibletemple retained,
RIGHTimplant viewerRIGHTrear edge. Firstintermediate stillnear side;neutralwidth+4,
head/body/case/pixelgrade/foot chronology provisional. Raw/allusedguides/fivepose/
neutral and12source-nativepairs seen. No mirror/patch/recolour/perposefitting.

Independent normal Marsh negativeX64 then NorthnegativeY96 path passed482checks,
12exactpairs/140controlled20ms samples/5actor-player movingturn restores+pause/
all5turn+4Northphases/exactNorth0return/finalpause,0failures/engineerrors/exit0.
125inputs stable DURING interval/2931owner nonlogfiles unchanged scratchAPPDATA.
All12pairs/3boards seen. Native10335 terminal0. Normal rate46/run exclusion and
economy/failure flags kept,dedicatedfree furnishedsite not paidbuild proof.
No actualreverse/fullRunSave/visibleTitleContinue/continuousfilm/contact/delivery.

Fourquarterpairs now authored:EastSouth01,WestSouth02,EastNorth02,WestNorth01;
8directed5frame400ms states. Newopposite-01-unselected joins COMPLETE whole PNG
quarters at exact sharedcardinal endpoint once:EastWest viaNorth andreverse
WestEast;NorthSouth viaEast andreverseSouthNorth. Match selected opposite route
facings,not an arbitrarilychosen arc. Existinghalf9timing60/90/100/90/120/90/100/
90/60ms=800ms retained,middle120 combines endpoint60+60 without duplicate frame.
36byteexactsourcePNGcopies,36exactdecodedAPNGframes,whole reversepair order exact,
sourceSHA/parity/joins retained. No new rasterauthoring/edits/mirroring. Private
family-manifest.json referenceswhole literal res paths:12states/76slots(all8
quarters+4halves),normalcatalog unchanged. All4whole nineposeboards/36poses seen.
Quarter angle repeats/neutralwidth/head/case/grade/support joins propagate into
halves,not fixed by exactsharedendpoint or count. Sourcecoverage isn't acceptance.

Independent actual normalcontroller/player EastpositiveX64 then WestnegativeX96
U-turn uses800ms opposite:570checks,16exactpairs,160controlled20ms samples,
9movingturn actor-player restores+pause,all9turn+4Westphases/exactWest0return/
finalpause,0failures/engineerrors/exit0.215inputs stable DURING interval/2931owner
nonlogfiles unchanged scratchAPPDATA.All16pairs/4boards seen.Held9phaseAPNG exact
decoded at800ms,not realtimecontinuousfilm/contact. Native46302 terminal0.
Rawreport inherited words quarterturn,but actual cycle.8/ninephase arrays/restores
proveopposite;preparer scope wording corrected afterinterval forfuturegenerated
fixtures,no art/runtime change. Initialpreparerasserted absent all5turn prose,
corrected before fixture/native;one PowerShell quotingattempt failed before edit,
apply_patch repaired. Check parent's exactliteral text before adapting helper;
don't infer nestedtemplate contents or rerun a partiallywritten preparer blindly.

No normalfullsave/visibleTitleContinue/completepickup-unload/fullscene acceptance.
Fourquarter forwardpaths +oneEastWestopposite=5actualdirected turn paths covered;
7remain:SouthEast/SouthWest/NorthEast/NorthWest reversequarter andWestEast/
NorthSouth/SouthNorth opposite. Both native intervals have their own fingerprints;
do not transfer quarterproof to half/reverse. Source/oppositeassembly added outside
West125bounded sourcefolder with no recordedinput changed;datedWest125 equality
valid. Metadata/preparer/assessment updates after215interval don't make current
helper tree that exact215freeze;claim dated interval only. No livejob.

Fullgoal active/incomplete. Next actualremainingreverse/opposite path coverage,
thenheldpickup/unload joins andindependentnormalfullsaves/visibleContinues before
normalcoherentcarry admission. Fullcross-family consistency/polish stillrequired:
12turnsources do not mean fullMarshset finished. Preserve old normalcarry until
family passes scopeappropriate adoption/visual gates;do not shrinkrequestedgoal.
'''
for path in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',maintained]:
    with path.open(encoding='utf-8') as f:present=any(marker in line for line in f)
    if not present:
        with path.open('a',encoding='utf-8') as f:f.write(lesson)
installed.write_bytes(maintained.read_bytes())
(ROOT/'docs/MARSH_CARRY_TURN_FAMILY01_HANDOFF_2026-10-02.md').write_text('''# Project handoff

Updated: October 2, 2026 · BrineSpace · Marsh staged carry-turn matrix

## Objective and acceptance
Full master-matched Marsh set and consistency/polish active/incomplete.
All12carry-turn source states staged;5actualdirectedpaths native reviewed.
Normalcatalog unchanged,notfullset/normal-save/continuouscontact acceptance.

## Accepted decisions and constraints
Ownselectedbody PRIMARY andownmasters,exactstagedSouth01/North01/East03/West03
endpoints. Builtinimagegen completefigures,one neutralBOXscale,wholeinteger torso
registration,no mirror/limb-crate patch/recolour/perposefit. ScratchAPPDATA/SHA.
Frontheld case occluded by body in rear views. Wholeframe reversal allowed.

## Current state
WestNorth01 own3yaws+ruler authored raw/exactprompt/4refs/SHA. west-north-01-
unselected two5frame400ms states/recipe/comparison/neutral. Nativefixture+UID/
preparer/fingerprint/publisher and12pairreview. Newassemble_marsh_carry_opposite01.py
copies quarters through exactsharedcardinal once:EastWest viaNorth/reverseWestEast,
NorthSouth viaEast/reverseSouthNorth. opposite-01-unselected4nineframe800msstates/
36PNGcopies/36decodedAPNGframes/4boards/SHArecipe/family-manifest12states76slots.
EastWestactualfixture+UID/preparer/fingerprint/publisher/16pairreview. Combined
recorder,pipeline/bible/status/bothskillmirrors appended. No livejob.

## Verification
WestNorthactualX-64/Y-96:482checks/12exactpairs/140samples/5restores+pause/all5turn+
4Northphases/exactNorth0return/finalpause,0fail/engineerrors/exit0,125inputs stable/
2931ownerfiles unchanged.Native10335 terminal0.All12pairs/3boards/raw/guides/
fivepose/ruler seen.Scale.21565731166912852,71x145/59x146/54x146/ruler59x146 vs
selectedNorth55x146;firstangleclose toside,head/width/grade/case/feet provisional.
Oppositeall4boards/36poses seen,sourcecopies/reverseexact,midpoints exactonce120ms.
EastWestactualX+64/X-96 Uturn:570checks/16pairs/160samples/9restores+pause/all9turn+
4Westphases/exactWest0return/finalpause,0fail/engineerrors/exit0,215inputs stable/
2931ownerfiles unchanged.Native46302 terminal0.All16pairs/4boards seen.HeldAPNG
illustrative,not continuouscontact. Raw report inherited quarter wording;actual
800ms/ninephases proveshalf. Preparer wording updatedafterinterval,noart/runtime
change;dated215 equality valid,currenthelper tree differs. Initialpreparerfailed
on absentprose before native;literal validationfixed,noGodotfailure.

## Next action
Cover seven actualpaths:SouthEast/SouthWest/NorthEast/NorthWest reversequarters,
WestEast/NorthSouth/SouthNorth opposites. Reuse actualfixture path with ownaxes/
endpoints and5vs9phase timing,ownscratch owner/input interval;publisher5vs9 slot
arrays/12vs16captures mustmatch. Thenheldpickup-unloadjoins,normalfullRunSave/
visibleTitleContinue adoption. Repair knownfirstangle repeats/neutralwidth/head/
torso/grade/cratepanel/footchronology acrossfamily;fullset/cross-familypolish remains.
Do not infer reversepath/fullsave acceptance from wholepixel reversal or counts.
''',encoding='utf-8')
print('Recorded 12stagedturnstates/76slots;WestNorth482/12 andEastWest570/16 native;owner2931stableboth;goal incomplete.')
