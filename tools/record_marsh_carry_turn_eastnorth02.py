"""Record rear-turn source/native proof and freeze remaining own quarter."""
from pathlib import Path
import hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-carry-turn-material-v1';S=B/'sources';A=ROOT/'output/marsh-animation-audit/carry-turn-east-north-02-2026-10-02'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
ids={'east-north-01':'exec-ec352c97-3fc8-4a52-a0c0-23f71dbdd053','east-north-nearback02':'exec-d219ff3e-e994-4dad-986e-1f5919fbd434','east-north-nearback03':'exec-28deb541-fb04-4d60-b525-d10e5b76c167'}
for stem,ident in ids.items():
    r=json.loads((S/f'{stem}.request.json').read_text());assert r['generationId']==ident and sha(S/f'{stem}.prompt.txt')==r['promptSha256'] and sha(S/f'{stem}.raw.png')==r['rawSha256']==sha(Path(r['originalGeneratedPath']))
    for q in r['orderedReferences']+r['sourceFrames']+r.get('guideDependencies',[]):assert sha(ROOT/q['path'])==q['sha256']
r=json.loads((A/'report.json').read_text());assert r['checks']==482 and r['failures']==0 and len(r['captures'])==12 and len(r['samples'])==140 and r['actorRestores']==5
for name,total in [('inputs',150),('owner',2931)]:
    before=json.loads((A/f'{name}-before.json').read_text());assert before==json.loads((A/f'{name}-after.json').read_text()) and len(before)==total
assert (A/'native-exit.txt').read_text().strip()=='0' and 'ERROR:' not in (A/'native.log').read_text()
p=json.loads((B/'east-north-02-unselected/recipe.json').read_text());assert p['unchangedOriginalFrameCopies']==8 and p['exactEndpointCopies']==4 and p['apngExactDecodedFrames']==5
pending=json.loads((S/'west-north-01.request.json').read_text());assert pending['status']=='frozen before generation; not started' and sha(S/'west-north-01.prompt.txt')==pending['promptSha256']
for q in pending['orderedReferences']+pending['sourceFrames']+pending['guideDependencies']:assert sha(ROOT/q['path'])==q['sha256']
O=B/'east-north-02-actor-review';(O/'visual-assessment.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'allTwelvePairsInspected':True,'viewCount':12,'pairedBoardsInspected':3,'findings':'Selected East idle/initial cargo/all5turn/all4North cargo phases/finalpause inspected. Head/torso turn rear-right,front-held case progressively hidden on screenRIGHT,not box on back. Whole nearback03 viewerLEFT support matches exact North endpoint. First intermediate remains close to East profile;angular progression,head/grade/case/foot joins provisional. Generated neutral58x146 vsselectedNorth55x146 width+3 diagnostic.','limits':'Actual forward positiveX64 then NorthnegativeY96 corner/normal controller-player/5restores+pause only. No actual reverse path/full RunSave/visibleTitleContinue/complete pickup-unload/continuous contact/full-set acceptance.'},indent=2)+'\n')
subprocess.run([sys.executable,str(ROOT/'tools/publish_marsh_carry_turn_eastnorth02_actor.py')],check=True,stdout=subprocess.DEVNULL)
maintained=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md';installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md');assert maintained.read_bytes()==installed.read_bytes(),'skill mirror drift'
marker='## Marsh East-North rear cargo quarter and weight reference — October 2, 2026'
lesson='''

## Marsh East-North rear cargo quarter and weight reference — October 2, 2026

EastNorth01 exec-ec352c97-3fc8-4a52-a0c0-23f71dbdd053 exact frozen prompt/
four ordered refs/raw original/SHA retained. Own selectedEast/North body PRIMARY,
stagedEast03/North01 endpoints,own originalEast/North identity. Three complete
REAR-RIGHT yaws plus neutralNorth146:oneBOXscale.22154779969650987 yields
76x142/59x143/59x144/ruler59x146 vsselectedNorth55x146. Case stays held IN FRONT
of wearer and progressively becomes occluded by torso on screenRIGHT;never a
box on back. First intermediate is too close to East side profile;angular
chronology/material/body/head/case joins remain for consistency polish.

Source01 third correctly rear-right but viewerRIGHT planted opposite exactNorth
viewerLEFT support. Whole nearback02 exec-d219ff3e-e994-4dad-986e-1f5919fbd434
used PRIMARY idle/action endpoint/old wrong-weight yaw guide/ownNorth original;
it copied wrong weight despite explicit correction. One146BOXscale.18181818181818182,
56x146/ruler60x146. Source retained/rejected,not assembled. Whole nearback03
exec-28deb541-fb04-4d60-b525-d10e5b76c167 excludes wrong-weight guide and puts
correct North cargo endpoint FIRST,bodyPRIMARY SECOND,own originalNorth THIRD.
It plants viewerLEFT boot and raises viewerRIGHT rear sole,near-back rear-right
head/body,hidden front case with small screenRIGHT edge. Scale.16079295154185022,
59x146/ruler58x146 vsselected55x146. Neutralwidth+3 diagnostic only,not fitting.
All three raw sources/used guides/packed comparisons/03neutral seen. No mirror,
limb/case patches,recolour/per-pose or cargo-width fitting. Complete cells alpha128,
ONE neutral scale,whole integer torso-row registration,noclippedopaque pixels.

Lesson: a wrong-weight whole yaw guide can outweigh explicit leg text. Supplying
the correct complete ACTION endpoint first and excluding wrong weight recovered
support here (inference,not controlled causal benchmark). At rear view actorLEFT
is viewerLEFT,unlike frontal actorRIGHT=viewerLEFT. Check supporting shin/lowest
sole/raised rear sole separately from body yaw;describe anatomical and picture
side explicitly. Don't mirror to change weight:implant/gear/case asymmetry remain.
For rear turns,occlusion is deliberate:case held in front can disappear behind
torso;missing visible box is not a licence to draw cargo on back.

Generic correction recipe now reports actual requested neutral target instead of
hardcoded147;North uses146. Existing West artwork/recipes were not rerun. New
EastNorth02 assembly copies original01 first2 figures and complete03 third:
two5frame400ms states,8other PNGs byte unchanged including4exact endpoints,
whole-frame reverse exact,5APNG decodedframes exact. Runtime184,p92/172,H148,
selectedtiming/facing/water/depth retained. Source/normalcatalog unchanged.

Independent actual normal Marsh controller/main/grid/player path EastpositiveX64
then NorthnegativeY96 passed482checks/12exact source-native pairs/140controlled
20ms samples/5movingturn actor-player restores+pause/all5turn+4Northcarry phases/
exactdestinationcarry0return/finalpause,0failures/engineerrors/exit0.150bounded
inputs stable DURING interval,2931owner nonlogfiles unchanged scratchAPPDATA.
All12pairs/3boards inspected;heldAPNG5decodedexact,illustrative crops not realtime
continuousfilm/contact. Normal cargo46/run exclusion/economy-failure flags kept;
dedicatedfree furnishedfixture not paidbuild proof. No actualreversecorner,
fullRunSave/visibleTitleContinue/completepickup-unload/fullscene acceptance.
Native38686 terminal0,no livejob. Only assembly-preparer metadata wording fixed
afterinterval todescribe rear-right/first-angle polish;no artwork/runtime change.
PendingWestNorth request addedafterdated150interval,so do not claimcurrent shared
source/helpertree identical to150freeze.

Threequarterpairs now6staged directedstates and3actualforward path checks;
reverse actualpaths untested. WestNorth01 frozen afterEast native,notgenerated.
OwnWest/North pairedbody/cargo guides and originals seen;REAR-LEFT three yaws,
front-held case occludes on screenLEFT,nearback viewerLEFT supports,North146
neutral. No East mirror:West visibletemple bare,NorthRIGHTimplant viewerRIGHT.
RemainingWestNorthpair+4opposite9frame chains through exactcardinalendpoint,
reverse/opposite native/heldpickup-unload joins/normalfullsave-visibleContinues/
fullcross-family consistency/polish. Full goal active/incomplete;normalcarry
selections stay old pending coherent family/native adoption gates.
'''
for path in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',maintained]:
    with path.open(encoding='utf-8') as f:present=any(marker in line for line in f)
    if not present:
        with path.open('a',encoding='utf-8') as f:f.write(lesson)
installed.write_bytes(maintained.read_bytes())
(ROOT/'docs/MARSH_CARRY_TURN_EASTNORTH02_HANDOFF_2026-10-02.md').write_text('''# Project handoff

Updated: October 2, 2026 · BrineSpace · Marsh East-North rear carry turn

## Objective and acceptance
Full master-matched Marsh set and consistency/polish active/incomplete.
EastNorth02 staged actual forward path source/native reviewed;normalcatalog
unchanged,no actualreverse/fullsave-visibleTitleContinue/complete delivery proof.

## Accepted decisions and constraints
Own selectedbody PRIMARY,stagedEast03/North01 endpoints exact. Builtinimagegen
complete figures only,one neutral146BOXscale,whole integer torso registration,
no mirror/limb-crate patch/recolour/per-pose fitting. ScratchAPPDATA/ownerSHA.
Rear case held in FRONT and hidden by torso;correct endpoint support independent
from head/body yaw. No box on back. Unknowns remain explicit.

## Current state
Three retained sources:EastNorth01 four-cell three-yaw sheet;nearback02 copied
wrongsupport,rejected;nearback03 endpointFIRST withoutwrong-weightguide correct.
east-north-02-unselected retains first2whole01 figures+whole03 third,8unchanged
PNG copies/4exactendpoints/two5frame400ms states/reversewholeorder/5APNGframes.
Preparer/build/correction/assembly/nativefixture+UID/fingerprint/publisher/recorder
tools,east-north-02-actor-review12pairs/3boards/verification/assessment. Generic
correction recipe actualneutral target fixed,existingWest artwork notrerun.
Pipeline/bible/status/bothskillmirrors appended. WestNorth01 frozen,notgenerated,
allfourrefsseen. No livejob;native38686 terminal0.

## Verification
ActualEastX+64/NorthY-96 path:482checks/12exactpairs/140samples/5restores+pause/
all5turn+4Northphases/exactNorth0return/finalpause,0failures/engineerrors/exit0.
150inputs stableDURINGinterval/2931ownerfilesunchanged. All12pairs/3boards and
raw/wholecomparison/neutral seen.03scale.16079295154185022,59x146/ruler58x146
vsselected55x146. Originalfirstintermediate close to side,second143height vs
neutral146,head/torso/grade/case/feet joins provisional. Source03 nearback correct
viewerLEFT support;frontheldcase only screenRIGHTedge.No actualreversepath/full
RunSave/TitleContinue/completepickup-unload/continuouscontact/fullscene acceptance.
Westrequest and metadata-only preparerwording changed AFTERdated150interval;
currenthelper/sharedsource tree is broader/different,datedequality stillvalid.

## Next action
Generate exact frozen west-north-01.prompt.txt with four ordered refs in request;
retain returnedID/original/rawSHA then genericbuilder --pair west-north --source
west-north-01 --generation-id ID. InspectREAR-LEFT progression,case screenLEFT
occlusion,bareWesttemple/RIGHT rearimplant,nearback viewerLEFTsupport,body/head/
camera/grade,thenactualWestnegativeX→NorthnegativeY corner. Thisfinishes authoring
fourquarterpairs only;opposite4nineframe chains/reverse-opposite native/heldjoins/
independentnormalfullsaves-visibleContinues and fullconsistency-polish remain.
''',encoding='utf-8')
print('Recorded EastNorth02 actual482/12,150inputs/2931ownerstable;three raws retained;WestNorth frozen;goal incomplete.')
