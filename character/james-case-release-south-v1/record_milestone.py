"""Record current South runtime evidence without rewriting older reports."""
from pathlib import Path
import hashlib, json, os
from PIL import Image
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
def atomic(path, transform):
    old=path.read_bytes();new=transform(old);temp=path.with_name(path.name+'.james-south.tmp')
    temp.write_bytes(new);assert path.read_bytes()==old, f'Concurrent modification: {path}';os.replace(temp,path)
def dump(path,value):path.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
w=json.loads((P/'native-world-evidence.json').read_text());i=json.loads((P/'native-indexed-evidence.json').read_text())
assert (w['checks'],w['failures'])==(4304,0) and (i['checks'],i['failures'])==(3980,0)
assert len(i['matrix'])==12 and w['journeys'][0]['caseRestored']
frames=[Image.open(ROOT/s['native'].removeprefix('res://')).convert('RGB') for s in w['journeys'][0]['contactSamples']]
assert len(frames)==21
frames[0].save(P/'native-world-review.gif',save_all=True,append_images=frames[1:],duration=[350]+[90]*19+[700],loop=0,disposal=2)
status='selected_runtime_south_empty_case_release'
atomic(P/'build.py',lambda old:old.replace(b'staged_south_empty_case_release',status.encode()))
for name in ['registration.json','bare-manifest.json','helmet-manifest.json']:
    value=json.loads((P/name).read_text());value['status']=status;dump(P/name,value)
dump(P/'selection.json',{
    'status':status,'ownerVisualAcceptance':False,
    'scope':'South pickup1..5 cancellation. Exact selected reverse sources, five independently authored empty-handed full bodies, new complete detached case, exact selected empty swim0. Four cardinal release packs now integrated; full James goal active.',
    'assetHashes':{name:hashlib.sha256((P/name).read_bytes()).hexdigest() for name in ['source.png','source-v2.png','case.png','bare-manifest.json','helmet-manifest.json','registration.json']},
    'productionFiles':['scripts/branforth_npc.gd','scripts/grid_canvas.gd','scripts/james_case_deposit.gd'],
    'evidence':{'package':'contract-evidence.json','actualReturnContinue':'native-world-evidence.json','indexedBranches':'native-indexed-evidence.json'},
    'limitations':['Actual exterior dispatch uses helmet; paired bare evidence is normal-loader source/clock only.','12 controlled branches share one actual arrival with actor-only restores/site resets, not12 full trips/Continues.','Both actual fixtures strict owner-profile guards failed, last_session.json delta; cause unproven, no owner rollback.','World invalidation/depletion/new attempt/death/traffic and full-set master/height/proportion/material/motion polish remain.']})
handoff='''# Project handoff

Updated: 2026-10-01 · Project: Brine Space · Task: James South empty case release

## Objective and acceptance
Full James set and continual master/style/perspective/size/height/proportions/grade checks remain active. All four cardinal case-release packs now integrated; owner visual acceptance pending. Remaining life/rest/mortality contexts and full cross-family polish are not complete.

## Accepted decisions and constraints
Independent South front-overhead prone bodies, trailing boots image-top/empty gloves below face. Permanent wrench image-left/torch holstered image-right. Original South case touches its glove, so do not extract a clipped case or fabricate missing hand pixels; author complete separated case with the bodies at one .25 ruler. Preserve exact selected entrances and swim0 endpoint. Shared native South helmet changes only cranial ownership.

## Current state
New pack has source.png (exec5b32c764-bf58-4335-9ed1-8361077eac70) plus exact prompt. Initial later poses retained excessively bent legs. source-v2.png (exec6411b2bc-b089-4159-a1d5-f84a2335d28e) reauthors entire cells0/3/4 for glove clearance/progressive leg extension; exact prompt-v2 retained. Original whole cells1/2 and separate case preserved. Five whole poses, fixed .25 ruler/selected cranial anchor, pooled per-source-atlas neutral/gold/skin grades; original/revised neutral gains .933333/.756757 avoid mixed-atlas flashes. No per-frame anatomy normalization. Case41x30 at[111,187], South native helmet at[107,122]. Ten profiles480..680ms: exact selected reverse index..1, authored0..4, exact selected empty swim0. Main actor/normal grid loader/case helper now support East/West/North/South. Site-owned case captured before movement and drawn in crew pass. No route/economy/extraction rule changes. Current negative fixtures use diagonal as invalid direction. Native scripts have Godot-generated paired UIDs; earlier newly created North noncanonical UID strings corrected by engine round-trip check, no existing production UID regeneration.

## Verification
69package checks pass: fixed ruler/finite pooled grade, complete new case dimensions, paired exact full body outside head, release glove/core clearance, ten paired exact input/reverse/empty endpoints/clocks/native plane. Native-world4,304 checks pass: one actual South normal dispatch/recall/airlock return, indexed source2 release, moving return/empty join, fixed world case, no extraction/credit, paused fresh-scene disk Continue and dry alive completion. Normal loader checks all ten paired sources/finite endpoints. Native-indexed3,980 checks pass:12 controlled work/pickup branches from one actual arrival, all six naturally advanced indexes/action, exact entrances/empty joins, actor-only restores/site resets, physical movement; pickup1..5 place cases. Not12 full journeys/Continues or actual bare exterior dispatch. Both fixtures terminal0/clean/no timeout/scratch resolved. Both strict full owner-profile guards FAILED with last_session.json delta; cause unproven/no owner restore/no clean-guard retry. UID utility also0, same strict guard delta. Paired fitted sheet and actual scene samples04/11 visually reviewed;21 authoritative contactSamples.native captures form runtime GIF. Metadata148 is not anatomical master-height acceptance.

## Next action
World case invalidation/depletion/new attempt/death/traffic/hazard checks. Remaining South meal/cup context, life/rest/mortality coverage, then full-set cross-family master/height/proportion/material/motion polish and owner review. Goal active; no commit/export requested.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
note='''\n## James South empty case release — October 1, 2026

South pickup1..5 release integrated; all four cardinal releases now have independent empty-handed followthroughs. Five complete South front-overhead bodies and detached case at common .25 ruler, permanent wrench image-left/torch image-right. Original case touches glove, so new complete case authored rather than clipped. Source-v2 corrects whole cells0/3/4 for glove clearance and progressive trailing-leg extension; original whole cells1/2/case retained. Two source-atlas pooled matte grades avoid a mixed-source flash, no per-pose sizing. Case41x30 at[111,187], native South helmet/head anchor, exact reverse sources/empty swim0,480..680ms clocks. Three production files updated; negative fixtures now use diagonal. New native UID pairs generated by Godot; earlier new North noncanonical IDs corrected after engine round-trip check.
69package/4,304actual-world/3,980indexed checks pass. One actual South normal return/fresh-scene Continue; ten paired normal-loader source/clock contracts;12 controlled branches from one actual arrival with actor-only restore/site resets. Bare proof is source/clock only, not exterior dispatch. Paired sheet and scene samples04/11 reviewed,21 authoritative runtime contact captures in native-world-review.gif. Engines0/clean/no timeout/scratch resolved. Strict full owner-profile guards FAILED (last_session.json delta), attribution unproven; no owner restore or rerun seeking a clean interval. Full-set anatomical height/proportions/perspective/material/motion acceptance remains pending.
Lesson: require projected leg extension to approach the actual selected endpoint, not merely matching frame metadata. Preserve known-good complete cells when correcting a sheet, and pool grade separately per authored atlas; one combined gain can dim retained cells after an edited source becomes brighter. A newly authored detached case must share the source physical ruler and match original contact placement. See character/james-case-release-south-v1/HANDOFF.md. Next world interruption/site lifecycle checks and remaining meal/rest/life/mortality contexts, followed by full cross-family polish. Full James goal active; no commit/export or owner layout change.
'''.encode('utf-8')
paths=[ROOT/'docs/CURRENT_STATUS.md',ROOT/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for path in paths:
    if b'James South empty case release' not in path.read_bytes():atomic(path,lambda old:note+b'\n'+old if path.name=='CURRENT_STATUS.md' else old+b'\n'+note)
print(json.dumps({'status':status,'checks':[69,4304,3980],'runtimeFrames':21,'guidanceFiles':5,'ownerProfileGuard':'failed: last_session.json'}))
