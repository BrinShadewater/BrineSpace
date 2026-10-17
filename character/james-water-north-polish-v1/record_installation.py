from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parents[1]
for name in ['native-staged','native-staged-routes','native-installed','native-installed-routes']:
    v=json.loads((P/(name+'-validation.json')).read_text());assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'],name
e=json.loads((P/'native-installed-routes-evidence.json').read_text());assert e['failures']==0 and len(e['results'])==2 and all(r['arrived'] for r in e['results'])
assert sum(len(r['captures']) for r in e['results'])==50
def atomic(path,fn):
    before=path.read_bytes() if path.exists() else b'';after=fn(before)
    if before==after:return
    tmp=path.with_name(path.name+'.north-water.tmp');tmp.write_bytes(after)
    if (path.read_bytes() if path.exists() else b'')!=before:tmp.unlink();raise RuntimeError('Concurrent edit '+str(path))
    tmp.replace(path)
def selection(b):
    m=json.loads(b);m.update(status='installed_owner_review_pending',runtimeInstalled=True,fullSetComplete=False,
                           packageChecks=211,nativePlayerChecks=427,installedPlayerChecks=186,
                           stagedRouteChecks=503,installedRouteChecks=502,installedRouteCaptures=50,
                           installedRouteEnvelopeSamples=50,
                           visualReview='Full paired pose boards,50 final native route captures and updated tread/start/stop four-direction master comparisons reviewed')
    m['pending']=['West water death limb seam','Workstation-specific facing transitions','Full furniture/meal/equipment/exterior journeys','Owner and full-set acceptance']
    return (json.dumps(m,indent=2)+'\n').encode()
atomic(P/'selection.json',selection)
note='''### James North water polish installed — September 30,2026

Paired tread/start/stop now use the slim master-only v6 atlas plus independently
authored v7 bent-elbow lead-in. Keep the initial arm reach beside the ribs before
overhead extension; a correct final swimming join cannot excuse an abrupt first
arm raise. V7 cranial188px matches v6 cranial66px at fixed148/478 atlas scale:
calibrate different source densities, not each pose's silhouette height. Material
curve remains tied to unchanged neutral; all source prompts/hashes preserved.

211 package,427 staged player,503 staged route,186 installed player and502 final
installed route checks PASS. Two furnished North routes,bare/helmet;50 final
native captures and50 alpha-envelope samples reviewed/check clear,zero prop
overlaps. Actual chooser, move/arrival and normal grid loader exercised; scratch
owner profiles unchanged. Use connected south room pair in reverse for North:
the original north door pair is unreachable with old/current profiles. Ordinary
water clearance keys compared; later life keys are outside this fixture scope.
Existing clocks,clearance,swim loop/endpoints and other directions unchanged.
Updated tread/start/stop master comparison pages reviewed. Full route traffic,
exterior/furniture/meal/equipment journeys and owner acceptance remain open.
See docs/JAMES_NORTH_WATER_POLISH_HANDOFF_2026-09-30.md. Full James goal active.
'''
for path in [R/'docs/JAMES_ANIMATION_CONTINUATION_2026-09-29.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    atomic(path,lambda b:b if note.encode() in b else b+b'\n\n'+note.encode())
headline='''## James North water proportions and arm lead-in installed — September30,2026

Slimmer master-based boots/calves and bent-elbow lead-in now selected for paired
North tread/start/stop.211 package/186 installed player/502 installed route checks
PASS;two furnished routes,50 native captures reviewed,zero prop overlaps and
profile changes. Updated master comparisons reviewed. Existing clocks,clearance
and swim loop retained. [Handoff](JAMES_NORTH_WATER_POLISH_HANDOFF_2026-09-30.md).
West water death limb seam and full motion/journey polish remain;goal active.

'''
atomic(R/'docs/CURRENT_STATUS.md',lambda b:b if headline.encode() in b else headline.encode()+b)
handoff='''# Project handoff

Updated:2026-09-30 · Project:Brine Space · Task:James North water polish installed

## Objective and acceptance
Full James set/master matching and consistency polish. North3-state paired
revision installed for owner review. Full-set motion/journey goal active.

## Accepted decisions and constraints
Matte graphite/gold, slim master calves/boots, straight rear lean, belt wrench.
Fixed atlas density and independent cranial-calibrated lead-in; no per-pose
height fitting,mirrored bodies or limb splicing. Exact selected swim joins,
current clocks,clearances,other directions and save behavior preserved.

## Current state
character/james-water-north-polish-v1 paired3-state36-reference pack selected
through literal paths in scripts/grid_canvas.gd and character/ACTIVE_ASSETS.json.
Source-polish-v6 plus source-lead-in-v7 and exact prompts/origins preserved in
james-water-north-v1. Rejected v5 retained. V7 whole-pose bent-elbow edit removes
initial overhead snap. V6 scale148/478; v7 equals66*atlasScale/188 by skull ruler.
Builder preserves installed status and all36 frame hashes through rebuild.
Pipeline,bible,continuation,canonical+installed skills and review ledger updated.

## Verification
211 package PASS;427 staged player,503 staged route,186 actual normal-grid
installed player and502 installed route checks PASS. Two real furnished North
routes,bare/helmet,complete start/swim/stop/tread.50 final native captures
reviewed;50 actual alpha-envelope samples clear blockers,zero prop overlaps.
Scratch owner profiles unchanged in every run. Updated tread/start/stop master
pages reviewed; selected swim/source endpoints preserved. Route uses connected
south pair reversed because original northern door is unreachable with both
retained and current clearance. Other layouts/concurrent traffic/exterior unproven.

## Next action
Review West water death projected limb length and neighboring death/swim frames.
Prove workstation-facing changes and full furniture/meal/equipment/exterior
dispatch/airlock/cargo-return journeys. All41 families have revised sources but
representative boards and scoped fixtures do not establish full-set acceptance.
No running native processes. Goal active.
'''
atomic(R/'docs/JAMES_NORTH_WATER_POLISH_HANDOFF_2026-09-30.md',lambda b:handoff.encode())
path=R/'character/james-animation-coverage-2026-09-30/consistency-review/review-ledger.json'
def ledger(b):
    m=json.loads(b);m['remaining']=[x for x in m['remaining'] if x!='North ordinary water tread/start/stop boot proportions']
    item='North ordinary water slim calves/boots and bent-elbow early reach'
    if item not in m['corrected']:m['corrected'].append(item)
    m['northWaterRevision']=dict(pack='character/james-water-north-polish-v1',installedRouteChecks=502,finalNativeCapturesReviewed=50,ownerReviewPending=True)
    return (json.dumps(m,indent=2)+'\n').encode()
atomic(path,ledger)
print('Installed North water polish recorded:211 package,186 installed player,502 installed routes; full goal active')
