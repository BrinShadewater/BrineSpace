"""Record independent native milestone and retained wrong-yaw sources honestly."""
from pathlib import Path
import hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-carry-turn-material-v1';S=B/'sources';A=ROOT/'output/marsh-animation-audit/carry-turn-west-south-02-2026-10-02'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
ids={'west-south-01':'exec-b6c936d8-2b32-4640-9162-b4629aa0998e','west-south-nearfront02':'exec-75f9b583-86de-4cae-b18f-1222b16c75d7','west-south-nearfront03':'exec-54c888df-1998-438f-951d-0cbea0d6438f','west-south-nearfront04':'exec-87c7f370-6f10-4bb2-a305-2e80f450a1ba','west-south-nearfront05':'exec-7bc4c781-4ce7-4d97-aa92-7fe1d9a94dbf'}
for stem,ident in ids.items():
    r=json.loads((S/f'{stem}.request.json').read_text());assert r['generationId']==ident and sha(S/f'{stem}.prompt.txt')==r['promptSha256'] and sha(S/f'{stem}.raw.png')==r['rawSha256']==sha(Path(r['originalGeneratedPath']))
    for q in r['orderedReferences']+r['sourceFrames']+r.get('guideDependencies',[]):assert sha(ROOT/q['path'])==q['sha256']
r=json.loads((A/'report.json').read_text());assert r['checks']==482 and r['failures']==0 and len(r['captures'])==12 and len(r['samples'])==140 and r['actorRestores']==5
for name,total in [('inputs',149),('owner',2931)]:
    before=json.loads((A/f'{name}-before.json').read_text());assert before==json.loads((A/f'{name}-after.json').read_text()) and len(before)==total
assert (A/'native-exit.txt').read_text().strip()=='0' and 'ERROR:' not in (A/'native.log').read_text()
p=json.loads((B/'west-south-02-unselected/recipe.json').read_text());assert p['unchangedOriginalFrameCopies']==8 and p['exactEndpointCopies']==4 and p['apngExactDecodedFrames']==5
pending=json.loads((S/'east-north-01.request.json').read_text());assert pending['status']=='frozen before generation; not started' and sha(S/'east-north-01.prompt.txt')==pending['promptSha256']
for q in pending['orderedReferences']+pending['sourceFrames']+pending['guideDependencies']:assert sha(ROOT/q['path'])==q['sha256']
O=B/'west-south-02-actor-review';(O/'visual-assessment.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'allTwelvePairsInspected':True,'viewCount':12,'pairedBoardsInspected':3,'findings':'Own West side and two original intermediate whole figures progress into whole nearfront05 LEFT-looking pose then exact frontal South. Supporting viewerLEFT boot now agrees with destination;case remains waist-supported. Selected idle/initial cargo/all5turn/all4South phases/finalpause inspected. Nearfront05 neutral64x148 vs selectedSouth58x147 is broader+1 tall,head/body grade and crate panel joins remain provisional.','limits':'Actual forward negativeX64 then South96 path only,normal controller/player5restores+pause. No actual reverse path/full RunSave/TitleContinue/complete pickup-unload/continuous contact/full-set acceptance.'},indent=2)+'\n')
subprocess.run([sys.executable,str(ROOT/'tools/publish_marsh_carry_turn_westsouth02_actor.py')],check=True,stdout=subprocess.DEVNULL)
maintained=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md';installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md');assert maintained.read_bytes()==installed.read_bytes(),'skill mirror drift'
marker='## Marsh West-South carry turn correction and actual path corner — October 2, 2026'
lesson='''

## Marsh West-South carry turn correction and actual path corner — October 2, 2026

Own WestSouth01 source exec-b6c936d8-2b32-4640-9162-b4629aa0998e retained:
three whole yaws+ruler,one neutral147BOXscale.20473537604456823,71x146/
63x147/61x148/ruler59x148. First two poses correctly turn LEFT side toward
front;third overshot RIGHT and planted opposite boot from South endpoint.
Never accept a wrong yaw/support from filename,frame count or alpha bounds.

Whole two-cell replacement attempts retained with exact frozen prompts/ordered
refs/source SHAs/raw originals:nearfront02 exec-75f9b583-86de-4cae-b18f-1222b16c75d7
fixed viewerLEFT support but still looked RIGHT,scale.17294117647058824,
60x147/ruler59x147. Nearfront03 exec-54c888df-1998-438f-951d-0cbea0d6438f used
successful LEFT quarter as first sole yaw guide;LEFT recovered but remained
too oblique,scale.14327485380116958,64x148/ruler59x147. Nearfront04
exec-87c7f370-6f10-4bb2-a305-2e80f450a1ba nearlyfrontal source still looked
RIGHT,scale.17926829268292682,63x147/ruler63x147. Nearfront05 whole-sheet
imagegen edit exec-7bc4c781-4ce7-4d97-aa92-7fe1d9a94dbf changed complete
cargo figure toward LEFT,keeping neutral request;scale.17796610169491525,
64x148/ruler64x148 vsselectedSouth58x147. Model did not preserve neutral
pixels exactly:measure its new whole neutral,do not assume requested unchanged
ruler. +6width/+1height and more frontal torso than head remain provisional.

Repeated text direction alone did not prevent wrong yaw. Correct whole
direction guide recovered LEFT (inference,not controlled causal benchmark),
but copied guide angle stayed too oblique;whole-sheet edit recovered nearfront.
Check nose/eyes/ear,head/chest/hips/case yaw AND supporting anatomical foot
independently. Do not flip pixels to repair yaw:identity implant/ankle/case
asymmetry is load-bearing. Replace one COMPLETE authored figure,not head/leg/
crate pieces. Keep raw failures and explain why each was rejected. Builtin
imagegen only for raster authoring;whole alpha128 cells,one neutralBOXscale,
whole integer torso-row registration,no clipped opaque pixels/per-pose fit.

west-south-02-unselected uses original01 first2 intermediates and whole05
third:two5frame400ms directedstates,8otherPNG files byte unchanged including
4exact West03/South01 endpoint copies,reverse whole order exact,APNG5decoded
frames exact. Packed old/new5pose board and05neutral reviewed. Case front
panel/width,adult head/torso/grade and support chronology/full-family joins
still provisional;normal catalog unchanged. Originalwrong01 and rejected
02/03/04 retained. No per-pose or cargo-width fitting used to hide differences.

Independent actual normal controller/player West negativeX64 then South96
clear furnished path corner:482checks,12exact source/native pairs,140controlled
20ms samples,5movingturn actor/player restores+pauseholds,all5turn and4South
carry phases,exact destinationcarry0return/finalpause,0failures/engineerrors,
exit0.149boundedinputs stable DURING native interval;2931owner nonlog files
unchanged with scratchAPPDATA. All12pairs/3boards seen;held5phaseAPNG decoded
exact,illustrative held crops not continuousfilm. Normal rate46/run exclusion,
economy/failure flags preserved;dedicatedfree furnishedfixture not paidbuild
proof. No fullRunSave/visibleTitleContinue/actualreversecorner/completepickup
unload/continuouscontact/fullscene acceptance. Native27641 terminal0.

EastSouth and WestSouth now4staged directedquarter states with2actualforward
path checks;reverse actual paths and8otherturn states still need authoring/
assembly/native proof. EastNorth01 exact request frozen AFTER West native
interval,notgenerated/nojoblive. Paired own selectedbody/stagedcargo guides
and ownEast/North masters seen. Three REAR-RIGHT yaws+neutralNorth146,case
held IN FRONT and progressively occluded by torso,never a box on back.
New pending files afterdated149interval don'tinvalidate its equality;do not
claim current sharedsource enumeration identical to149freeze. Full goal active:
remainingquarter/opposite turns,heldpickup/unload joins,normalfullsave/visible
Continues and full cross-family consistency/polish. Staged native proof does
not admit new carries into normal catalog or complete the full set.
'''
for path in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',maintained]:
    with path.open(encoding='utf-8') as f:present=any(marker in line for line in f)
    if not present:
        with path.open('a',encoding='utf-8') as f:f.write(lesson)
installed.write_bytes(maintained.read_bytes())
(ROOT/'docs/MARSH_CARRY_TURN_WESTSOUTH02_HANDOFF_2026-10-02.md').write_text('''# Project handoff

Updated: October 2, 2026 · BrineSpace · Marsh West-South carry turn

## Objective and acceptance
Full master-matched Marsh set and consistency/polish active/incomplete.
WestSouth02 staged forward path-turn source/native reviewed. Normal catalog
unchanged;no full save/visible TitleContinue or complete delivery acceptance.

## Accepted decisions and constraints
Own selected body PRIMARY,stagedWest03/South01 endpoints exact. Builtin imagegen
whole figures only,one neutral BOX scale,integer torso registration,no mirror/
limb-crate patch/recolour/per-pose fitting. ScratchAPPDATA and owner fingerprints.
Correct LEFT yaw AND destination supporting foot;file labels aren't proof.

## Current state
Five retained sources:WestSouth01 three-yaw sheet,nearfront02/03/04/05 two-cell
corrections. Only05 used:original first2 PNGs+whole05 third. west-south-02-unselected
two five-frame400ms states,8unchanged PNGs/4exact endpoints/reverse whole sequence/
5exact decoded APNG frames. Preparation/build/correction/assembly/nativefixture+
pairedUID/fingerprint/publisher/recorder tools added. west-south-02-actor-review
12exact pairs/3boards/evidence/assessment. Pipeline,bible,status,both skill mirrors
appended. EastNorth01 exact prompt/request frozen,not generated;used guides seen.

## Verification
West actual negativeX64/South96 path:482checks/12exact pairs/140samples/
5actor-player restores+pause/all5turn+4destination phases/exactSouth0return/
finalpause,0failures/engineerrors/exit0.149inputs stable during native interval,
2931ownerfiles unchanged.All12pairs/3boards and old/new five-pose/neutral seen.
Source01 wrong3yaw/support;02supportfixed butRIGHT;03LEFT toooblique;04RIGHT;
05LEFT nearfront accepted only provisionally.05scale.17796610169491525,
64x148/ruler64x148 vsselectedSouth58x147:width+6 and height+1 diagnostic.
Head/body yaw/grade/case panel/feet/full family joins need polish. No actualreverse
path/fullRunSave/TitleContinue/continuousfilm/contact/fullscene/completepickup
unload acceptance. Native27641 terminal0,no live job. EastNorth request added
after dated149 interval;current folder enumeration is broader than that freeze.

## Next action
Generate frozen east-north-01.prompt.txt with exact four ordered refs from request;
all seen. Retain returned ID/original/rawSHA then genericbuilder --pair east-north
--source east-north-01 --generation-id ID. Check REAR-RIGHT progression,front-held
case occlusion,adult proportions/grade,then actual positiveX→negativeY corner.
WestNorth own quarter remains;opposite4 derive9frames through exact cardinal
endpoints without mirroring. Reverse/opposite native,held joins,independent normal
fullsaves/visibleContinues and full consistency/polish remain. Goal active.
''',encoding='utf-8')
print('Recorded WestSouth02 actual482/12,149inputs/2931ownerstable;five sources retained;EastNorth frozen;goal incomplete.')
