from pathlib import Path
import json,hashlib,os,uuid
p=Path(__file__).resolve().parent;r=p.parents[1];b=r/'character/james-cargo-return-bridges-v1'
codec=json.loads((p/'production-codec-evidence.json').read_bytes())
guard=json.loads((p/'probe_production_checkpoint-validation.json').read_bytes())
assert codec['checks']==190 and codec['failures']==0 and guard['exitCode']==0 and guard['realProfileUnchanged']
inputs=json.loads((p/'production-codec-inputs.json').read_bytes())
assert all(hashlib.sha256(Path(k).read_bytes()).hexdigest()==v for k,v in inputs['sha256'].items())
assert hashlib.sha256((r/'scripts/james_cargo_checkpoint.gd').read_bytes()).hexdigest()==inputs['contractSha256']
assert hashlib.sha256((p/'probe_production_checkpoint.gd').read_bytes()).hexdigest()==inputs['probeSha256']
motion=json.loads((p/'full_return_collar_v12-evidence.json').read_bytes());mg=json.loads((p/'full_return_collar_v12-validation.json').read_bytes())
assert motion['checks']==1277 and motion['failures']==0 and mg['exitCode']==0 and mg['realProfileUnchanged']
freeze=json.loads((p/'full_return_collar_v12-inputs.json').read_bytes())
assert len(freeze)==46 and all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in freeze.items())
comparison=json.loads((p/'collar-v12-comparison.json').read_bytes())
assert comparison['equal']=={'source':93,'world':93}
def atomic(path,new):
    old=path.read_bytes();temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');temp.write_bytes(new)
    assert path.read_bytes()==old;os.replace(temp,path)
reviewpath=p/'full-return-collar-v12-review/review.json'
review=json.loads(reviewpath.read_bytes())
review.update(visualReviewPending=False,continuousPlaybackWatched=False,pairedRepair=False,fullVisualAcceptance=False,reviewed='Changed bare row11 source/native pair and adjacent rows in boards00/12 inspected.93other source/world pairs match earlier fully reviewed V6 RGBA byte-exact. Face, ochre cap/badge/body below110 remain original. Local collar edge cleaner than broad V11 patch, but fixed head switch/shoulder articulation still unresolved; not preferred/normal-selected.',scope='Both prescribed full native returns with one bare collar interior trial; helmet unchanged. No normal hooks/title Continue or full master/cross-family acceptance.')
atomic(reviewpath,(json.dumps(review,indent=2)+'\n').encode())
verdict={'selected':False,'preferredStagedSelectionChanged':False,'v11':'Rejected broad collar window produces shoulder/chest cut.','v12':'Narrow collar alternative preserves face above100, all body below110 and38original ochre pixels inside edit.651? See exact package counts:65314 original pixels protected,222 admitted collar pixels. Minor local edge cleanup; complete head/shoulder join remains unresolved.','nativeMotionChecks':1277,'pairs':94,'pairsByteExactToPriorReviewed':93,'newPairReviewed':1,'raw':'collar-repair-v11-raw.png','prompt':'collar-repair-v11-prompt.txt','method':'Built-in image_gen; native uniform256/1254 resize, no translation/grade. Both alternative packages retain same raw.','productionCodecChecks':190,'productionHooksInstalled':False}
verdict['v12']=verdict['v12'].replace('651? See exact package counts:','')
(b/'collar-v11-v12-verdict.json').write_text(json.dumps(verdict,indent=2)+'\n')
section='''## James protected collar trial and reusable save extension — October 2, 2026

Built-in V11 collar-only raw/exact prompt preserved. Broad420pixel window package
protects65116original pixels but creates shoulder/chest cut; rejected. Alternative
V12 uses same raw,108/100/26/10 window with38 original ochre pixels protected:
65314 original pixels exact,222 admitted collar pixels. All below110/above100,
badge/case/gloves/boots retained. Actual1254raw read before uniform256/1254resize;
no grade/translation. Four source poses plus enlarged collars reviewed. V12 gives
minor local edge cleanup, not coherent head/shoulder motion acceptance; preferred
staged V9 and normal selection unchanged. No new helmet repair.

V12 single bare interior exercised in both complete prescribed native returns:
1277checks0fail,20 row identities/14120msupdates per gear;94source/world pairs.
46prelaunch input hashes unchanged, engine0/owner unchanged/scratch APPDATA.
93source AND native world pairs equal prior fully reviewed V6 byte-exact; changed
bare row11 and adjacent board00/12 presentations inspected.184decoded RGB/unequal
APNGduration checks. Full fixed-head switch/shoulder articulation remains open;
no continuously watched/natural scheduling/master acceptance.

New scripts/james_cargo_checkpoint.gd/UID prepares normal-shaped optional
james_cargo_return extension/version2 with actual actor stage, full paired banks,
casePNG/RGBA and strict clock/plan validation. No RunSave preload/circular callback;
base station validation separate. Staged marker/field rejected even matching idle
markers; generic player rejected before accessing missing lifecycle methods.
Ten prior actual staged scratch saves converted:190checks0fail/engine0/owner
unchanged; normal checksum reader and normal base schema plus separate strict
extension/loaded bank/case gates. Actually substituted loaded case/midpoint and
wrong clocks rejected; correct textures re-admitted. Ten disk bytes/helper/probe
hashes unchanged; not a whole-normal-bank prelaunch freeze. First140-check pass
retained, then strengthened marker/generic/actual-substitution cases rechecked.

This helper is NOT wired to normal capture/factory/renderer/restore or title
Continue. No new actor restoration/new-process Continue proven. Next connect the
normal actor/player, shared workshop renderer binding and optional checkpoint
hooks together, preserving legacy saves, then exercise actual title Continue.
Coherent collar/shoulder/full directional/master/context and cross-family polish
remain. Lessons: protect semantic ochre/face separately from a rectangular edit;
small pixel preservation proves identity protection, not motion quality. Isolate
checkpoint schema from base codec to avoid recursive validation during integration.
Evidence:character/james-floor-case-west-v1/production-codec-evidence.json,
full-return-collar-v12-review/review.json; bridge/collar-v11-v12-verdict.json.
Goal active/incomplete. No normal installation, commit/export.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() not in old:atomic(path,section.encode()+b'\n'+old if path.name=='CURRENT_STATUS.md' else old+b'\n\n'+section.encode())
handoff='''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James collar/save integration

## Objective and acceptance
Full James set matching masters/style/camera/size/height/proportions/matte grade,
then cross-family polish. Incomplete; revised West lifecycle still staged.

## Accepted decisions and constraints
Preferred V9/riseV6/caseV7/checkpointV2 unchanged. V11 broad patch rejected;
V12 minor collar trial not preferred. Owner saves and other crew work preserved.

## Current state
V11 raw/prompt/two native package scripts/UIDs/reviews; V12single-interior manifest,
full_return_collar_v12 fixture/evidence46input freeze/eight boards/four APNGs.
New scripts/james_cargo_checkpoint.gd/UID normal-shaped strict reusable extension,
probe_production_checkpoint.gd/UID/10prior scratch inputs/checks. No normal hooks.
Five maintained guides updated; verdict/source evidence saved. No commit/export.

## Verification
V12native1277checks0fail/94pairs:93whole source/native pairs exact prior reviewed,
changed bare pair/adjacent boards inspected.184APNGchecks/46hashes unchanged.
Codec190checks0fail/10packets/normal checksum read/base schema/separate strict
actual bank/case/clock checks. All native runs scratch APPDATA/owner unchanged.
No complete visual acceptance, normal actor restore or title Continue proof.

## Next action
Wire normal actor/player/room renderer and optional save hooks as one coherent
integration, preserve legacy saves and test actual title/new-process Continue.
V9head/collar/shoulder continuity and ordinary natural unload still open; full
cardinal/master/context/cross-family polish remains. Goal active/incomplete.
'''
atomic(p/'HANDOFF.md',handoff.encode())
print('Collar trial/save extension milestone recorded;190codec/1277motion checks, five guides and handoff.')
