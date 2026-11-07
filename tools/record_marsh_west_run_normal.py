"""Record West staged/native and independent normal full-checkpoint acceptance."""
from pathlib import Path
import json,runpy
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-west-run-material-v1'
MARKER='## Marsh West run02 actor and normal full Continue proof — October 2, 2026'
LESSON='''
## Marsh West run02 actor and normal full Continue proof — October 2, 2026

West02 complete own-master cycle provisionally selected in normal catalog after
held source/actualactor review, not mirrored East art. Rootselection true/provisional
8checkpointverified/fullGoalCompletefalse; dated source/candidate/staged held
flags preserve their scopes. Whole six source files unchanged. Existing p92/172,
184canvas,H148,six100msloop and explicitWeststride.11027027027027027cells retained.
No gameplay/controller/nav/economy/failure/schema changes. Normalcatalog76body/
228states/1190slots coverage only. Body/head/quietwarmgrade closer to selected
31x147Westidle; near/farneutrals33x148/34x147 slightly different profile/sample,
not exactgeometry proof. Bare visible temple/original smallanklebuckles retained.

Fresh stagedactualMarsh.move/main/grid/player on LEFT clear168world furnished
route:444checks/8exactsource-nativecrop pairs/95controlled20ms samples/2wraps/
6actor-playerrestores+pauseholds/normal slowingwalk,0fail/engine0/exit0.77bounded
inputs stable,2931owner nonlogfiles unchanged scratchAPPDATA. FixtureUIDcu2whrunm5v88
paired. Validated physical East interval traversed in reverse: candidate+168start
and targetcandidate, segment_clear checked in actualLEFTdirection, path/progression
signednegativeX,Yfixed. This reverses physical route ONLY, never source identity.
Route-probes.json retains actualcollision samples. All8source/native CROPS in two
boards and whole selectedidle/twoneutrals/walk/contact board inspected. No fullscene
occlusion, continuousfilm or articulated contact claim. Stageactor-review-v1.

Independent normaltest_marsh_west_run_production.gd UIDcv3whrunm6v89 uses actual
normal Marshfactory/main/grid/player/orderedcatalog, no stagedmanifest injection/
custom movement.8fullRunSave checkpoints: selectedidle,sixrunphases,slowingwalk.
Each freshactualTitle._continue_loop waits observable startup AND real loading
Continueenabled/pressed/overlaygone. Wholeactor/player/source/root parity andpause
verified; everyrun resumes normal negativeXroute/distancephase afterunpause.
Retarget scratchrun_save_path afterrestore; neverownerprofile. Normalfreebuild/
disabledfailureflagsfalse, dedicatedfixture room placedfree, not paid-site proof.

Normal audit west-run-normal-native-v1-2026-10-02 terminalexit0:
226checks/8fullsaves/8freshactualvisibleTitleContinues/16captures/8exactbefore-
continuedsourcepairs,0fail/engine0.85bounded inputs stable,2931owner nonlogfiles
unchanged. All8source/before/continuedCROPpairs and correctfour-facing idle/run
whole sourceboard inspected. Body/grade joins improved; contact/pass stance
spacing, continuous soles/naturaltraffic/equipment/fullfamily polish remain open.
Test registeredcompanions/native900 afterlaunch,indexexcluded85freeze; classifier
confirms native. Normal-review-v1/index.html contains scoped evidence and views.
Publisher preserves explicit east/west/north/south matrix when adaptingdirection;
unlike priorEast firstdraft, no duplicated comparison facing.

North own selected references prepared next:10frames (idle0/1,walk0/3PRIMARY,
oldrun6MOTION ONLY), exactsourceSHAs/metadata/commonwhole256p128224 nearest2x.
SelectedNorthoccupied55x146,standingmetadataH148. Bothcompleteguideboards andown
originalnorth-standing-identity-01 inspected. Originalrearbackplate/harness/blond
hairwhorl and smallrighttemple edge retained; no frontface. Raised exposedcharcoal
heel/sole legitimate, distinct fromwarmivory uppers. Oldrunhead/upperbody/plate
scale andgrade need ownmaster review. No newNorthrunsource/native acceptance.
Northguide tool reusesWestguide packager with explicit rearidentity; preserve
bothtool dependency hashes in laterauthoring/nativeprovenance.

Lesson: signed-route/body-envelope checks matter when reversing an actorfixture,
but physical route reversal does not authorize mirroring asymmetric artwork.
NormalSave/visibleContinue must remain independent of stagedsource tests. Whole
neutral/sample differences and sourcecounts are diagnostics, never broadgeometry
or movingcontact acceptance. Keep everycase/pair scoped to the selected direction.

NEXT author full Northrun matching own55x146fittedrearbody/master/camera/grade,
explicit alternating completeleft/rightleg/arm poses andneutral. Preserve legitimate
raisedsoles. Inspectwholemotion,stageactualNorth movement,thenfullnormal8checkpoint
Continue ifaccepted. Carry/remainingheldfamilies/full-set consistency/polish remain.
Full Marsh master/style/camera/size/height/proportion/grade goal ACTIVE/INCOMPLETE.
'''
def main():
    review=BASE/'normal-review-v1';assessment={'normalAdmission':True,'fullGoalComplete':False,'allEightPairsInspected':True,'allFacingRunBoardsInspected':True,'viewScope':'Eight exact source/original/continued framebuffer crops in two boards plus complete four-facing source board. No fullscene or continuous film claim.','appearance':'West02 own fitted head/body/quietwarmgrade closer to selectedidle; bare visibletemple retained. Head/hip/sole spacing and movingcontact provisional.','familyFinding':'East03/West02/South05 normalprovisional improvements retained. Northhead/upperbody/grade next ownmaster review, legitimate raisedcharcoalsoles retained.','remaining':'North run/carry,heldfamilies,full-set motion/equipment/grade/camera/proportion consistency and polish.'};(review/'visual-assessment.json').write_text(json.dumps(assessment,indent=2)+'\n')
    selection=json.loads((BASE/'selection.json').read_text());selection.update(status='provisional complete Westrun02; eight full normal checkpoints/fresh visible TitleContinues verified',normalAdmission=True,fullGoalComplete=False,normalReview='normal-review-v1/index.html');(BASE/'selection.json').write_text(json.dumps(selection,indent=2)+'\n');runpy.run_path(str(ROOT/'tools/publish_marsh_west_run_normal.py'),run_name='__main__')
    maintained=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md';installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md');assert maintained.read_bytes()==installed.read_bytes(),'skillmirrordrift'
    for p in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',maintained]:
        with p.open(encoding='utf-8') as stream:present=any(MARKER in line for line in stream)
        if not present:
            with p.open('a',encoding='utf-8') as stream:stream.write(LESSON)
    installed.write_bytes(maintained.read_bytes())
    handoff='''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Marsh West02 normal run

## Objective and acceptance
Full master-matched set/consistency/polish active/incomplete. West02 normally
selected provisionally,8full checkpoints/freshvisibleContinues verified. Source
wholebody/grade/phase joins improved; final continuous contact/fullfamily polish open.

## Accepted decisions and constraints
OwnWest fittedidle/master, bare near temple,authenticanklebuckles. No Eastmirror/
patch/recolour/perposefit. Sixunchanged whole184canvas sources,p92/172,H148,
100 ms loop/current distance cadence. Normal costs and failures remain enabled;
test-only free-build and disabled-failure flags stay false. Dedicated room site
authored free, not paid-construction proof. Scratch APPDATA.

## Current state and changed files
Normalcatalog append Westcandidate02manifest,rootselectionnormalAdmissiontrue/
provisional8checkpointverified,historicalheldflags preserved. Stageactor-review-v1
eightpairs/rulers/verification,normal-review-v1 sixteenexactcaptures/eightpairs/
two boards/correctall4facingidle-run/assessment/evidence. Newnativefixture+UID/
fingerprint/publisher/rulers;normaltest+UID/install/prepare/fingerprint/publish/
register/record tools. tests/index.jsoncompanions/native900. Pipeline/bible/status/
master-repair mirrors appended. Northsources10selectedwholeguides/metadata/SHAs;
originalrear master/bothguideboards inspected. No Northnewsource/native acceptance.

## Verification and scope
Stage444checks/8views/95controlled20ms samples/2wraps/6restores+pauseholds,77stable
inputs. Normal226checks/8fullsaves/8freshactualvisibleContinues/16captures/8exact
pairs,85stableinputs. Both2931ownerfiles unchanged scratchAPPDATA,0failengine0exit0.
All8stagecropviews,8normalcroppairs,neutral/action/four-facing boards seen. Route
reversedphysically with actualLEFTsegment_clear; identity nevermirrored. No fullscene,
continuousfilm/articulatedcontact,naturaltraffic/equipment/fullfamily acceptance.
Native sessions35862(stage),10083(normal) terminal0. Catalog76/228/1190coverage only.

## Remaining work and next action
Northwhole run matching55x146fittedrearidle/master,head/backplate/camera/grade,
alternating completeleft/rightlegarms+neutral,legitimatecharcoalraisedsoles retained.
Wholecycle review/stagednative/fullnormalContinue ifaccepted. Carry/heldfamilies/
fullconsistency/polish remain. Keepgoalactive. No liveprocess aftermilestone.
'''
    (ROOT/'docs/MARSH_WEST_RUN_NORMAL_HANDOFF_2026-10-02.md').write_text(handoff,encoding='utf-8');print('Recorded Weststaged444+normal226 full8Continue proof; Northownrefsready; skillsmirrored; fullgoal incomplete.')
if __name__=='__main__':main()
