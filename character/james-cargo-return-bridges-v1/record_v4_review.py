from pathlib import Path
import json,hashlib,os,uuid
p=Path(__file__).resolve().parent;r=p.parents[1]
def atomic(path,new):
 old=path.read_bytes();temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');temp.write_bytes(new);assert path.read_bytes()==old;os.replace(temp,path)
for name in ['package-west-bridge-v4','validate-west-bridge-v4','joined-plan-v4']:
 guard=json.loads((p/(name+'-validation.json')).read_bytes());assert guard['exitCode']==0 and guard['realProfileUnchanged'] and not guard['timedOut']
for mode in ['bare','helmet']:
 for i in [0,1]:assert (p/f'frames-v4/{mode}/{i:03d}.png').read_bytes()==(p/f'frames-v3/{mode}/{i:03d}.png').read_bytes()
refs=json.loads((p/'reference-evidence.json').read_bytes())
assert all(hashlib.sha256((r/x['path']).read_bytes()).hexdigest()==x['sha256'] for x in refs['sources'])
native=json.loads((p/'joined-plan-v4-evidence.json').read_bytes());assert native['checks']==6019 and native['failures']==0 and native['bridgePlans']==46 and len(native['plans'])==328
path=p/'package-v4-evidence.json';package=json.loads(path.read_bytes());package.update({'retainedV3FrameIndices':[0,1],'transformedV4CellsUsed':[2],'unusedTransformedV4Cells':[0,1],'sourceNote':'Script computes all three transformed cells, but only index2 contributes new pixels. First2paired frames are copied/byte-asserted from frames-v3.'});atomic(path,(json.dumps(package,indent=2)+'\n').encode())
path=p/'joined-return-v4-review.json';review=json.loads(path.read_bytes());review.update({'visualReviewPending':False,'reviewed':'All20paired source presentations in both chronological boards plus registered endpoint board inspected. Corrected case level; preserved first2poses/head/shell/lower legs. Shoulder/collar/hip and original unload stance boundary require continuous native motion/world review. GIF created as source-clock replay; not recorded native movie or seamless loop acceptance.'});atomic(path,(json.dumps(review,indent=2)+'\n').encode())
verdict={'selected':False,'fullGoalComplete':False,'caseLevelSourceCorrection':True,'completeBridgeAcceptance':False,'nativeSourceBindingChecks':18,'nativeJoinedPlanChecks':6019,'bridgePlansAdmitted':46,'remainingHeldJoinGaps':186,'registeredIdleFloorCaseJoinsPending':328,'firstTwoPosesByteExact':True,'visualScope':'6registered revised sources and20paired chronological return source presentations reviewed. Source GIF is reconstructed replay, not continuous native/world acceptance.','remaining':['Actual source-bound actor return with live needs/safety and geometry clearance.','Continuous shoulder/collar/hip and transition into original unload stance review.','Floor-crate/standing handoff and ordinary RunSave Continue.','Other directions and full cross-family master/style/height/proportion/material polish.']}
(p/'study-review-v4-evidence.json').write_text(json.dumps(verdict,indent=2)+'\n')
section='''## James level-case West bridge v4 and finite source-plan admission — October 2, 2026

Targeted built-in edit corrects final held-case tilt. Original first2paired v3
poses retained byte-exact; only final torso rectangle uses new v4 pixels. Both
raw outputs/prompts retained. Original head/shared shell/lower-leg pixels outside
80,110,84,69 still exact:358440native protection checks. Paired torso region exact;
staged source-clock/pivot/ruler18checks0fail. No global grade or scale change.
v4 extraction uses pooled bare353ruler/rounded215cell; actual used cell2 and unused
computed cells0/1 explicitly recorded. Normal production selection unchanged.

Joined candidate manifests have5refs per gear: exact old turn endpoint,3interiors,
exact old unload entrance. Staged return_plan admits optional loaded bridge only
when both full-RGBA endpoints bind; excludes bridge as ordinary outgoing cargo.
Candidate injection into normal James bank:328plans/6019checks0fail.46plans now
cross through bridge and finish authored unload;186held joins remain nonidentical,
328registered idle/floor-crate joins pending. Deliberately mismatched endpoint
rejects bridge in both gears. No pre-run broad dependency freeze.

All6revised sources/registered endpoint board and all20paired chronological
return source presentations reviewed. Case now level; first2poses and retained
head/helmet/feet unchanged. Shoulder/collar/hip and original unload stance join
still need continuous native motion/world review. Source GIF uses common palette
and original holds; terminal hold/repeat is viewer reset, not authored loop or
recorded native movie. Complete bridge acceptance pending; all manifests staged.
Three native intervals engine0/no timeout; whole owner profile unchanged under
scratch. Six original reference hashes unchanged at recording.

Lesson: retain unaffected reviewed poses byte-exact during a targeted source edit.
Bind both whole-source bridge endpoints to actual loaded textures and reject
wrong sources; a matching endpoint does not certify anatomical motion or cargo
disposition. Next real finite actor return, geometry/needs/emergency priority,
native motion, floor-case/standing and ordinary Continue. Full James master,
remaining directions/contexts and cross-family polish goal active/incomplete.
Evidence: character/james-cargo-return-bridges-v1/study-review-v4-evidence.json,
joined-return-v4-part1/part2.png and joined-return-v4-review.gif.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 old=path.read_bytes()
 if section.splitlines()[0].encode() not in old:atomic(path,section.encode()+b'\n'+old if path.name=='CURRENT_STATUS.md' else old+b'\n\n'+section.encode())
handoff='''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James level-case West bridge v4

## Objective and acceptance
Full master/style/perspective/size/height/proportion/matte James set then
cross-family polish. Full objective active/incomplete; complete bridge pending.

## Accepted decisions and constraints
Preserve original shell/head/feet outside documented torso rectangle. First two
reviewed poses byte-exact. Bridge endpoints must bind to loaded whole sources.

## Current state
v4 raw/prompt, corrected final case grip; frames-v4 and paired v4 manifests staged.
Paired joined-manifest-v4 has5refs/gear. return_plan.gd in james-east-cargo-heads-v3
now supports optional endpoint-bound bridge; no normal selection/controller change.
All6registered source and20chronological paired presentations reviewed; source
replay GIF created. Five guides updated. Actual power interruption still snaps.

## Verification
358440native protected comparisons,18source player and6019joined plan checks0fail.
328plans,46admit bridge;186other held joins and328registered idle/floor-crate joins
pending. Wrong endpoint rejected in both gears. Three engine0/owner profile
unchanged scratch intervals. Original six refs and retained four pose hashes exact.
No full semantic mask, continuous native/world motion or controller/safety/save
return acceptance; no prelaunch broad dependency freeze.

## Next action
Actual finite return with live needs/safety/geometry and original unload stance
motion review, then floor-case/standing handoff and ordinary Continue. Remaining
cardinal contexts/West tablet edges and full master/cross-family polish stay open.
No commit/export. Source GIF reset is review behavior, not an authored loop.
'''
atomic(p/'HANDOFF.md',handoff.encode())
print('Level-case v4 and46staged bound return plans recorded; real actor/motion/floor/Continue remain open; five guides updated.')
