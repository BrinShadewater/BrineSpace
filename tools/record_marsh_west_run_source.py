"""Source-only own-West whole cycle and explicit extraction/acceptance limits."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-west-run-material-v1'
MARKER='## Marsh West own-master whole run source studies — October 2, 2026'
LESSON='''
## Marsh West own-master whole run source studies — October 2, 2026

West run remains UNSELECTED; normal selected catalog unchanged after East03.
Two complete own-West authored sources retained with exact frozen prompts,
ordered ref/source SHAs, built-in execution IDs, originals and raw hashes:
run01 exec-18ce8756-64cb-4a2f-a4fd-d86cb2787e38 (seven figures requested),
half02 exec-02cac5df-b5f2-493b-a51d-46c95a0ac2df (four figures requested).
Primary selected31x147Westidle single unchanged nearest4x guides fitted adult
anatomy/camera/grade; own original West master identity/hardware. Visible near
temple BARE, implant hidden FAR/right; no East mirroring. Original authentic
ankle buckles retained. Initial six-running request repeats near-leading legs
in both halves; distinct images are not alternation proof.

Initial run01 strict7column-group packager FAILED before packing: raw alpha128
column groups6 because figures3/4 lack clean vertical gutter (joined group511..1045
in1774x887raw). Failed assertion preserved; no false seven-cell manifest/native
proof. Full raw retained unchanged. Extracted ONLY separated complete figures
1/2/5/6/7 using whole cells outside joined group; joined two figures OMITTED.
Five packed cells near-contact/near-passing/duplicate-near-passing/near-flight/
neutral,ONE neutralBOXscale .27476635514018694, sizes73x143/51x143/60x142/78x134/
ruler33x148(target147). No cutting through adjacent limbs, region stencil/patch,
mirroring/recolour or perposefit. Duplicate pass retained but not selected into
sixcycle. Complete no-clipping alpha counts checked; no new fullcycle01manifest.

Half02 orders single selectedWestwalk3 first ONLY for exact foreground-trailing
whole thigh/knee/boot arrangement, singleidle second PRIMARYanatomy/material,
originalthird. Four complete separated cells; one neutralBOXscale
.2300469483568075,farcontact89x145/farsupportpass78x145/farkneeflight88x140/
ruler34x147. Foregroundivorythigh trailsRIGHT, darkerpartlyhiddenfarleg leadsLEFT;
far passing's rearnearboot clearlylifted above flat frontfarsole. Farcontact may
have both soles near plane; planted footprint/actual movement remains unverified.
Whole source body/head/grade and bare temple inspected in both raw/packed boards.

Candidate02 six EXACT byte-identical complete184canvas frames: near01contact,
near01passing,far02flight,far02contact,far02passing,near01flight. Whole p92/172,
H148,six100msloop, explicit existingrun-Weststride.11027027027027027cells. Ground
contact/passingbottom172,source-relative flightclearance preserved. SourceAPNG
sixdecodedframes exactly match,loop0 illustrative only. Complete currentselected
idle/oldrun vsnew wholecycle board reviewed. Fitted head/body/material now closer
to selectedWestidle and ownmaster, far/near opposition clearer. Neutral widths
33/34vsselected31 diagnostics, no equal-width/exactgeometry claim. Halfjoins,
hip/root registration, contact phase quality and continuous motion still need
actualactor review. Oldselected comparison explicitly labels phase UNVERIFIED,
does not borrow newcycle labels as proof of old limb phases.

No Godot test/probe or ownerprofile access this source-only milestone. No West
native proof,normalcatalog admission,fullSave/TitleContinue or fullfamily/master
acceptance. East03normal226/8checkpoint proof remains scoped to East. NewWest
source manifests/recipes preserve normalAdmissionfalse/fullGoalCompletefalse.

Lesson: author generous completefigure gutters and verify they exist before
cell cuts. A rendered sevenfigure sheet can have fewer separable column groups.
Retain joined source and use only independently complete separated cells; don't
split through a neighbouring boot to satisfy a grid count. Correct selected whole
stance as first guide helped far-leg overlap here; inspect thigh-knee-boot and
soleclearance anyway. Master matching includes hidden asymmetric hardware and
authentic ankle detail. Whole neutral calibration is not full stance acceptance.

NEXT stage complete West02 in actual normal move/main/grid/player on clear
horizontal LEFT route, review body/head/hip/contact/grade joins against selected
idle/walk and original, refine complete poses if needed. Then normalcatalog/full
eightcheckpoint visibleContinue verification ifaccepted. Northrun/carry, held
families/full-set consistency/polish remain; full Marsh goal ACTIVE/INCOMPLETE.
'''
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    for name in ['run-01','half-02']:
        req=json.loads((BASE/'sources'/f'{name}.request.json').read_text());assert sha(BASE/'sources'/f'{name}.prompt.txt')==req['promptSha256']
        for r in req['orderedReferences']:assert sha(ROOT/r['path'])==r['sha256']
        assert sha(BASE/'sources'/f'{name}.raw.png')==req['rawSha256']
    for folder in ['near-half-01-unselected','far-half-02-unselected','candidate-02']:
        recipe=json.loads((BASE/folder/'recipe.json').read_text());assert recipe['normalAdmission'] is False
        for r in recipe['records']:assert sha(BASE/folder/r['file'])==r['sha256']
    assessment={'normalAdmission':False,'fullGoalComplete':False,'rawSourcesInspected':True,'packedHalfBoardsInspected':True,'wholeCycleComparisonInspected':True,'identity':'OwnWest bare near temple preserved, authentic anklebuckles. No Eastmirror.','appearance':'Fitted head/body and quiet warm grade closer to selected31x147idle than oldrun. Neutral33/34width diagnostic, not exactgeometryproof.','phaseReview':'Clearer near/far thigh-knee-boot order; farpassrearnearbootraised. Initialraw repeated nearleading; joined figures3/4omitted whole, not split.','limits':'Held source only, no native motion/contact/root/normalSave or fullfamily acceptance.'};(BASE/'candidate-02/review.json').write_text(json.dumps(assessment,indent=2)+'\n')
    maintained=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md';installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md');assert maintained.read_bytes()==installed.read_bytes(),'skill mirror drift'
    for p in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',maintained]:
        with p.open(encoding='utf-8') as stream:present=any(MARKER in line for line in stream)
        if not present:
            with p.open('a',encoding='utf-8') as stream:stream.write(LESSON)
    installed.write_bytes(maintained.read_bytes())
    handoff='''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Marsh West run source

## Objective and acceptance
Full master-matched set/consistency/polish active/incomplete. West02 is held
unselected whole cycle; fitted anatomy/grade and clearer opposition. No native/
normalcatalog or full-family art acceptance. East03 remains normally selected.

## Accepted decisions and constraints
OwnWest original/selected31x147idle authority; bare near temple, hiddenfarimplant,
authentic anklebuckles. No mirror/patch/recolour/perposefit. One neutral scale per
sheet,184canvas,p92/172,H148,six100msloop/currentWeststride retained.

## Current state and changed files
character/marsh-west-run-material-v1/sources: exacttwofrozenrequests/raws/original
IDs/hashes, whole selected singleidle/walk3guides. Nearhalf01fivewholecells and
farhalf02fourcells/recipes/comparisons. Candidate02sixbyte-identical sources/
manifest/recipe/APNG/old-newcomparison/review. New prepare-run01/build-run01/
extract-nearhalf01/prepare-half02/build-half02/assemble02/recordsource tools.
Pipeline/bible/status/master-repair mirrors appended. No normalcatalog/controller
or gameplay changes.

## Verification and limits
Raw/packedhalf/currentselectedvsnewcycle boards visuallyinspected. No-clipping
wholealpha counts, exactprompts/5orderedrefs/raw/frameSHAs andsixAPNGframes checked.
Strictinitial7group builderassert failed:twofigures sharecolumnextent. Joined raw
retained; onlyindependently complete5cells used,joinedfigures3/4omitted. Initial
nearleadingphasesrepeat, correctedfarhalf completeposes. Nearscale.27476635514018694,
far.2300469483568075; rulers33x148/34x147vsselected31x147.Noheight/widthfitting.
No Godot/ownerprofileaccess/native orfullSave/Continue thissource-onlymilestone.

## Remaining work and next action
StageWest02 on actual normal horizontalLEFTroute, review body/head/hip/sole/camera/
grade joins and movingphase quality. Refinecompleteposes asneeded, thennormal
catalog/full8checkpointvisibleContinues ifaccepted. Northrun/carry,heldfamilies,
fullconsistency/polish remain. No liveprocess. Goal active/incomplete.
'''
    (ROOT/'docs/MARSH_WEST_RUN_SOURCE_HANDOFF_2026-10-02.md').write_text(handoff,encoding='utf-8');print('Recorded ownWest whole source02 and explicit gutter/phase/native limits; skills mirrored; goal incomplete.')
if __name__=='__main__':main()
