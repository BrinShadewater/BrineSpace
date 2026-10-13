"""Record seven whole sources, actual West cargo and four-cardinal review."""
from pathlib import Path
import hashlib,json,subprocess,sys
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-west-carry-material-v1';S=B/'sources'
MARKER='## Marsh West carry03 native and four-cardinal staged review — October 2, 2026'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
ids={'carry-02':'exec-745a5620-51b5-4ff9-b043-1d8e78887897','contact-03':'exec-9c21d53b-efb4-469c-bab9-4e15245b3abb','passing-04':'exec-f5f1fe86-8160-45b6-b09d-acf55eb61fe6','passing-05':'exec-e23917c0-5b25-423f-98aa-b8f8ba6c1760','near-06':'exec-d4ddf953-e306-4917-b0f6-db8ab815ca73','near-07':'exec-76ab179a-7594-4320-aca2-0ed69a3d0aa1','near-08':'exec-ce8dcc0e-c84d-4f0a-91ae-d421d0f427c7'}
for name,gid in ids.items():
    r=json.loads((S/f'{name}.request.json').read_text());assert r['generationId']==gid and sha(S/f'{name}.raw.png')==r['rawSha256'] and sha(S/f'{name}.prompt.txt')==r['promptSha256']
    assert sha(Path(r['originalGeneratedPath']))==r['rawSha256']
    for q in r['orderedReferences']+r['sourceFrames']+r.get('guideToolDependencies',[]):assert sha(ROOT/q['path'])==q['sha256']
unused=json.loads((S/'carry-01.request.json').read_text());assert unused['status']=='frozen before generation' and sha(S/'carry-01.prompt.txt')==unused['promptSha256']
audit=ROOT/'output/marsh-animation-audit/west-carry-actor-03-2026-10-02';report=json.loads((audit/'report.json').read_text());assert report['checks']==523 and report['failures']==0 and len(report['captures'])==6 and len(report['samples'])==95 and report['actorRestores']==4 and report['wraps']==2
for name,total in [('inputs',142),('owner',2931)]:
    before=json.loads((audit/f'{name}-before.json').read_text());assert before==json.loads((audit/f'{name}-after.json').read_text()) and len(before)==total
assert (audit/'native-exit.txt').read_text().strip()=='0' and 'ERROR:' not in (audit/'native.log').read_text()
review=B/'actor-review-v1';(review/'visual-assessment.json').write_text(json.dumps({'allSixViewsInspected':True,'viewCount':6,'pairedBoardsInspected':2,'normalAdmission':False,'fullGoalComplete':False,'findings':'Own West bare temple identity and fitted body/camera quieter than old cargo. Four opposite contact/passing poses,crate held with connected arms;selected idle and final paused cargo seen. Source/native pairs exact. Source-sheet head height/grade and divided/plain inset panel details remain provisional.','limits':'Held six source/native pairs and illustrative180ms APNG,not realtime continuous contact,full scene,normal RunSave/TitleContinue,complete pickup/carry/unload or turn/held joins.'},indent=2)+'\n')
subprocess.run([sys.executable,str(ROOT/'tools/publish_marsh_west_carry03_actor.py')],check=True,stdout=subprocess.DEVNULL)
a=json.loads((B/'candidate-03/assembly.json').read_text());a.update(visualReviewed=True,nativeReviewed=True,normalAdmission=False,allFourWholeSourcePosesInspected=True,findings='Near06contact/near08passing/far03contact/far05passing correctly alternate support. Current slate plain/recessed inset side panel and single left block latch concept consistent;far03 divided-panel detail and projected dimensions/grade vary. Whole head-height/registration and body across sheets remain provisional. Four source copies and APNG exact;actual native523 checks/six pairs reviewed.',remaining='Remaster carry turns/held joins against these staged endpoints;cross-cardinal body/crate consistency and normal full saves/visible Continues remain. Full-set consistency/polish incomplete.');(B/'candidate-03/assembly.json').write_text(json.dumps(a,indent=2)+'\n')
records=[]
for folder in ['candidate-02','contact-03-unselected','passing-04-unselected','passing-05-unselected','near-06-unselected','near-07-unselected','near-08-unselected']:
    r=json.loads((B/folder/'recipe.json').read_text());records.append({'folder':folder,'scale':r['commonNeutralScale'],'sizes':[q['size'] for q in r['records']]})
(B/'source-assessment.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'allSevenRawSourcesInspected':True,'allSevenPackedComparisonsInspected':True,'allUsedGuidesInspected':True,'records':records,'findings':'02 repeats near support;03 correct far contact;04 far support but too extended;05 compact far passing;06 good near contact but requested near passing repeats far;07 near support but too extended;08 compact near passing. Frozen01 was unused,board-position labels corrected in02 before generation.','nativeReview':'candidate03 actual523checks,6pairs,95samples,4restores,2wraps,142stable inputs,2931owner files unchanged;staged only.'},indent=2)+'\n')
C=ROOT/'character/marsh-carry-cardinal-review-2026-10-02';p=json.loads((C/'provenance.json').read_text())
for row in p['rows']:
    for q in row['wholeFrames']:assert sha(ROOT/q['path'])==q['sha256']
(C/'visual-assessment.json').write_text(json.dumps({'bothWholeCardinalBoardsInspected':True,'wholeFigureCount':20,'normalAdmission':False,'fullGoalComplete':False,'findings':'Four selected own cardinal idles plus16staged carry poses reviewed. Identity and elevated facing cameras retained;North crate correctly occluded in front,South frontal two-latch case,East visible implant,West bare visible temple. South has less passing compression thanNorth;East case side projection broader thanWest and body/neutral widths differ. Source-sheet head/body/grade and panel-detail joins need full family polish.','limits':'Each cardinal independent staged native verification;not normal saves/visible Continues,turn/held joins,continuous contact or full-set acceptance.'},indent=2)+'\n')
maintained=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md';installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md');assert maintained.read_bytes()==installed.read_bytes(),'skill mirror drift'
lesson='''

## Marsh West carry03 native and four-cardinal staged review — October 2, 2026

West frozen01 unused: global anatomical LEFT/RIGHT substitution wrongly swapped
guide BOARD positions. Re-viewed whole guide:LEFT figure near-leading,RIGHT far.
Corrected those labels only in frozen02 before generation;01 prompt retained.
Distinguish screen directions,anatomical sides,guide positions and latch positions
when adapting prompts; never globally swap them without re-viewing actual guides.

Seven whole sources retained with exact frozen prompts/ordered refs/frame/tool
SHAs/raw generation IDs/original paths; all raw/packed/used guides inspected:
02 exec-745a5620-51b5-4ff9-b043-1d8e78887897 five figures,scale.2727272727272727,
86x145/71x145/84x145/72x146/ruler36x147,all near support,not accepted loop.
03 exec-9c21d53b-efb4-469c-bab9-4e15245b3abb,correct far contact from selected
far stance first/idle PRIMARY/original,omitting competing near cargo pose;
scale.17583732057416268,89x144/ruler33x147. Crate panel changed,not silently original.
04 exec-f5f1fe86-8160-45b6-b09d-acf55eb61fe6 whole far support but near rear leg
too extended like contact,scale.18058968058968058,85x144/ruler33x148(+1sampling).
05 exec-e23917c0-5b25-423f-98aa-b8f8ba6c1760 compact far passing after explicit
vertical near thigh/low near calf heel recovery,scale.1783980582524272,
77x142/ruler33x147. Correct darker far flat support LEFT/light near rear liftRIGHT.
06 exec-d4ddf953-e306-4917-b0f6-db8ab815ca73 selected near stance/idle PRIMARY/
whole far05 cargo-only/original:good near contact but requested near passing
copies far support,scale.20675105485232068,86x145/76x144/ruler34x147.
07 exec-76ab179a-7594-4320-aca2-0ed69a3d0aa1 whole near contact/idle/original:
near support correct but foreground thigh and dark rear leg too extended,
scale.17970660146699266,84x144/ruler35x147.
08 exec-ce8dcc0e-c84d-4f0a-91ae-d421d0f427c7 explicit foreground near thigh/shin
vertical under pelvis,low dark far knee/calf recovery:compact NEAR passing,
scale.19090909090909092,82x146/ruler32x148(+1sampling). Support identity and
passing joint action are independent; raised boot alone does not prove passing.
Whole opposite-support cargo refs can bias requested legs despite cargo-only text;
use correct same-support whole source for corrections. Causality an inference.

First passing04 pack wrapper targeted underlying contact03 because outer wrapper
had no literal output-path token. Detected from missing passing04 output; restored
contact03 from retained correct original,then corrected direct underlying-source
substitutions and packed passing04 with its actual frozen prompt/request. All seven
current raw IDs/original SHA/prompt/ref provenance revalidated;no native interval
occurred before restoration. Assert target provenance/output path when composing
wrappers; outer source substitution need not alter the code it reads. Whole source
files retain exact authoring provenance; do not disguise sources with wrong request.

Candidate03 FOUR byte-identical whole copies:near06contact/near08passing/
far03contact/far05passing.184p92/172H148,four180ms loop,explicit stride
.0827027027027027;four APNG decoded copies exact. No clipping/mirror/limb/crate
patch/recolour/per-pose or cargo-width body fitting. Whole old/new comparison seen.
Crate now recessed/plain inset-panel/single-left-block-latch concept;far03 divided
panel/grade/projected dimensions and head-height/registration remain provisional.
Own West bare visible temple/far-side implant/authentic ankle hardware retained;
selected31x147 adult PRIMARY,neutral widths32..36 diagnostic,not anatomy fitting.

Actual normal Marsh factory/controller/main/grid/player workshop_carry native
fixture523checks,6exact held source/native views,95controlled20ms samples,
4actor/player restores+pause holds,2wraps,0failures/engine errors,exit0.142 bounded
inputs equal DURING interval;2931 owner nonlog files unchanged under scratch
APPDATA. NegativeX168clear furnished route;no mirrored East art. Normal carry
rate46/run excluded;dedicated free room site only,global economy/failure flags
false,not paid-build proof.95samples cover87.4world units,not full pickup/unload.
All six pairs/two boards seen;held180ms APNG not realtime contact or full scene.
No normal full RunSave/visible TitleContinue or turn/held join acceptance.

Four-cardinal staged board review now retains20complete unchanged figures:
4actual selected idles+16own cargo poses. Two whole boards inspected. North crate
in front correctly occluded;Southfront2latches,Eastsideimplant,Westbaretemple.
South passing compresses less thanNorth;East side crate broader thanWest;body/
neutral widths,head-height/grade and rigid-case panel joins need full family polish.
Each cardinal independently passes its scoped523 native stage;this is NOT normal
catalog/full-set acceptance. Normal catalog unchanged. Full goal active/incomplete.
Next remaster12 carry turns and held joins against staged endpoints,then independent
normal full saves/visible Continues and full cross-family consistency/polish.
No live process or job;West native session71559 terminal0.
'''
for p in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',maintained]:
    with p.open(encoding='utf-8') as f:present=any(MARKER in line for line in f)
    if not present:
        with p.open('a',encoding='utf-8') as f:f.write(lesson)
installed.write_bytes(maintained.read_bytes())
(ROOT/'docs/MARSH_WEST_CARRY03_NATIVE_HANDOFF_2026-10-02.md').write_text('''# Project handoff

Updated: October 2, 2026 · BrineSpace · Marsh West carry03/cardinal cargo review

## Objective and acceptance
Full master-matched set plus consistency/polish active/incomplete. All four own
cardinal carry loops now authored,assembled and independently staged/native
reviewed. West03 unselected,normal catalog unchanged. Full set not accepted.
No live job/session;West native71559 terminal exit0.

## Decisions and constraints
Own selected adult bodies/camera/grade PRIMARY;East implant visible,West bare
visible temple/far-side implant. Complete whole figures,one neutral147 scale per
source,no mirror/patch/recolour/per-pose/cargo-width fitting,no opaque clipping.
184p92/172H148/four180ms/stride.0827027027027027 unchanged. Normal economy/failure
flags untouched;dedicated free site only. Scratch APPDATA/owner fingerprints.

## Current state and changed files
West02 corrected unused01 board labels before generation. Seven raw/prompt/
ordered-reference/frame/tool SHA-provenanced sources and complete packed sheets:
carry02,contact03,passing04/05,near06/07/08. Candidate03 unchanged whole near06
contact/near08passing/far03contact/far05passing,manifest/APNG/comparison/assessment.
Native preparer/fixture+UID/fingerprint/publisher,actor-review-v1 exact6pairs.
Four-cardinal review tools,20whole figures/two boards/provenance/assessment.
Source assessment/milestone recorder,pipeline,bible,current status and both
master-repair skill mirrors appended. No gameplay/catalog/export changes.

## Verification and scope
All7 raw sources,packed comparisons/neutrals/used whole guides seen;exact
generation IDs/originals/raw/prompt/ref SHAs revalidated.02near repeats;03correct
farcontact;04far too extended;05compactfar;06nearcontact good/passingwrongfar;
07near too extended;08compactnear. Four copies and four APNG frames exact.
Initial04 wrapper accidentally targeted03 output; restored03 from correct original
before native,corrected direct wrapper and validated all current provenance.
West native523checks,6exactpairs,95samples,4restores/pauseholds,2wraps,0fail/engine
errors,exit0.142 inputs stable during native interval,2931owner nonlog files
unchanged. All6pairs/2boards reviewed.20figure cardinal boards reviewed.
Held/native scope excludes full saves/TitleContinue,turn/held joins,continuous
contact/full scene and fullpickup/carry/unload. Case panel/grade/width and source
head/body registration provisional;EastcasebroaderWest,SouthlesscompressionNorth.

## Remaining work and next action
Remaster12 carry-turn states and held joins against staged South01/North01/East03/
West03 complete endpoints. Inspect actual ordered catalog selections first.
Adjacent8 have5frames,opposite4have9;existing tests cover old supplemental/bare
reproduction,not current staged master coherence. Preserve four180ms cadence.
Then independent normal full saves/visible TitleContinue and full-set family
cross-reference consistency/polish. Allstagedcarryloops are progress,not completion.
''',encoding='utf-8')
print('Recorded seven West whole sources and native523/6;four-cardinal review retained;skill mirrors equal;goal incomplete.')
