from pathlib import Path
import json,hashlib,os,uuid
p=Path(__file__).resolve().parent;r=p.parents[1]
data=json.loads((p/'checkpoint_probe_v2-evidence.json').read_bytes());guard=json.loads((p/'checkpoint_probe_v2-validation.json').read_bytes());review=json.loads((p/'checkpoint-v2-review.json').read_bytes());inputs=json.loads((p/'checkpoint_probe_v2-inputs.json').read_bytes())
assert data['failures']==0 and guard['exitCode']==0 and guard['realProfileUnchanged'] and not guard['timedOut']
cases=[x for x in data['results'] if x.get('checkpoint')];assert len(cases)==10
assert {(x['mode'],x['phase']) for x in cases}=={(g,s) for g in ['bare','helmet'] for s in ['before','after','midpoint','terminal','idle']}
assert all(x['sourceExact'] and x['floorRestored'] and x['completed'] for x in cases)
assert len([x for x in data['results'] if 'label' in x])==30 and review['nativeSourceWorldPairs']==30
assert len(inputs)==47 and all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in inputs.items())
def atomic(path,new):
    old=path.read_bytes();temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');temp.write_bytes(new);assert path.read_bytes()==old;os.replace(temp,path)
review.update(visualReviewPending=False,reviewed='All30 saved/restored/completed source/native room pairs inspected in ten boards. New case7 renderer retains material/contact in both gears at all five phases, including body-only midpoint and terminal. Immediate whole source RGBA/clock/foot/plan/room exact; paused fresh-scene restore then finite completion. No normal title/new-process Continue or full future trajectory acceptance.')
atomic(p/'checkpoint-v2-review.json',(json.dumps(review,indent=2)+'\n').encode())
acceptance={'selected':False,'fullGoalComplete':False,'nativeChecks':data['checks'],'failures':0,'actualCarryReturns':10,'freshMainRestores':10,'nativeSourceWorldPairsReviewed':30,'targetedInputsUnchanged':47,'ownerProfileUnchanged':True,'contract':'checkpoint_v2 version2/james-west-return9-rise6-floor7','bankScope':'Both gears unload-west7 and carry-settle-west6 whole RGBA,pivot,H148,row timing; mandatory even idle. Not all normal character banks.','caseScope':'Actual submitted renderer texture RGBA plus named V7PNG file hash/source7/p128224/H148; source7 room payload.','negativeTrials':['Changed serialized casePNG/caseRGBA/midpoint binding rejected.','Actually substituted loaded case texture and loaded midpoint rejected, including idle.','Wrong binding/version type/missing marker/altered plan clock/source hash/actor-floor/expired plan/absent released ownership rejected as applicable.'],'ordinaryLoaderRejectsCandidate':True,'normalTitleContinueAccepted':False,'remaining':['Actual ordinary unload actor execution/full V9 native motion/collar-head polish.','Normal state/render/bank/checkpoint admission and normal title/disk/new-process Continue.','Natural scheduling, all cardinal/context masters/full-family and cross-family polish.']}
(p/'checkpoint-v2-acceptance.json').write_text(json.dumps(acceptance,indent=2)+'\n')
section=f'''## James revised rise/case paired disk contract verified — October 2, 2026

New staged checkpointV2/version2 binding return9-rise6-floor7; new floor payload
source7 and actor/player/renderer companions/UIDs. Actual case submitted RGBA plus
named V7PNG file hash/p128224/H148 bound, not just cosmetic source label. Full
paired unloadWest7 and carry-settleWest6 RGBA/pivots/H148/durations bound even when
saved return plan is empty/idle. Active plan still rebuilt canonically against
loaded bank and exact original release4 hash. Old staged contract unchanged.

Ten actual carry returns/both gears × before/after release/midpoint/terminal/idle.
{data['checks']}native checks0fail/engine0/owner unchanged/47targeted input hashes unchanged.
Actual candidate disk write/read, ten fresh normal main scenes with actual normal
SAVE.restore_staged base restore, then revised candidate actor/player/renderer.
Immediate whole sourceRGBA/clock/foot/plan/room payload exact, restore paused,
finite completion retains case.30saved/restored/completed source/native room pairs
inspected in ten boards. No new artwork/grade/geometry or normal selection change.

Changed serialized casePNG/RGBA/midpoint bindings rejected. Actually substituted
loaded case texture and midpoint rejected in every phase, including idle; restored
correct selections re-admitted. Prior malformed plan/marker/clock/source/ownership
guards retained. Mandatory unadmitted marker makes ordinary loader reject these
candidate saves; this is NOT normal title/new-process Continue admission. Whole
normal bank/future trajectory/natural scheduling/master motion not proven here.

Lesson: labels and active-row hashes do not protect an idle checkpoint from later
wrong-bank/floor-art loading. Bind admitted future clips and submitted prop pixels
even when no return is active; prove rejection with actual substituted textures.
Keep normal station base restore and candidate extension gates distinct until
production admission, rather than silently dropping unselected lifecycle fields.
Next ordinary/full-return native motion/collar-head, normal state/render/catalog/
checkpoint integration and actual title/new-process Continue, all directions/full
master/cross-family polish. Goal active/incomplete. No commit/export.
Evidence:character/james-floor-case-west-v1/checkpoint-v2-acceptance.json,
checkpoint_probe_v2-evidence.json,checkpoint-v2-review.json.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() not in old:atomic(path,section.encode()+b'\n'+old if path.name=='CURRENT_STATUS.md' else old+b'\n\n'+section.encode())
handoff=f'''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James revised rise/case saves

## Objective and acceptance
Full James set matching original masters/style/camera/height/proportions/matte
grade, then cross-family polish. Incomplete; candidate not normal-selected.

## Accepted decisions and constraints
Exact original cue4 retained; body-only midpoint/canonical terminal intentionally
revised. Source7/V7original case crop, p128224/H148. Owner/geometry/normal selection
preserved; candidate marker still rejects ordinary loader admission.

## Current state
checkpoint_v2.gd/version2 binds actual casePNG/submittedRGBA and both complete
admitted West unload7/bridge6 banks/timing even idle. New checkpoint_floor_state/
actor/player_v2 and checkpoint_workshop_v2.gd, pairedUIDs, checkpoint_probe_v2.gd,
47input freeze/log/guard/evidence and ten reviewed boards. Five guides updated.
Old checkpoint files/evidence retained. No commit/export.

## Verification
{data['checks']}native checks0fail/ten actual returns/ten fresh-main staged disk restores,
30source/world pairs reviewed/47hashes unchanged/engine0/owner unchanged. Five
phases × both gears, paused exact whole source/clock/foot/plan/room then completion.
Actual wrong loaded case/midpoint and serialized bindings rejected even idle.

## Next action
Actual ordinary unload actor path/full V9 native return/collar-head polish; normal
state/render/catalog/checkpoint admission then actual normal title/disk/new-process
Continue; natural scheduling/all directions/master/context/cross-family review.
This candidate codec/base-station restore is not normal Continue. Goal incomplete.
'''
atomic(p/'HANDOFF.md',handoff.encode())
print('Revised paired bank/case checkpoint milestone recorded;'+str(data['checks'])+'checks/30reviewed pairs; five guides updated.')
