from pathlib import Path
import json,hashlib,os,uuid
P=Path(__file__).resolve().parent;R=P.parents[1]
def atomic(p,data):
    t=p.with_name(p.name+'.'+uuid.uuid4().hex+'.tmp');t.write_bytes(data);os.replace(t,p)
def write(p,obj):atomic(p,(json.dumps(obj,indent=2)+'\n').encode('utf-8'))
startup=json.loads((P/'runtime-input-startup.json').read_bytes());after={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in startup};assert after==startup
write(P/'runtime-input-after.json',after)
guards={f:json.loads((P/(f+'-validation.json')).read_bytes()) for f in ['validate','regression','bill_compat']}
for f,g in guards.items():
    assert g['exitCode']==0 and not g['timedOut'] and g['realProfileUnchanged'] and not g['profileDelta']
    assert 'ERROR:' not in (P/(f+'.log')).read_text(encoding='utf-8')
assert 'WARD REPAIR: PASS' in (P/'bill_compat.log').read_text(encoding='utf-8')
e=json.loads((P/'native-evidence.json').read_bytes());reg=json.loads((P/'regression-evidence.json').read_bytes());review=json.loads((P/'review-evidence.json').read_bytes())
assert e['failures']==reg['failures']==0
old=json.loads((R/'character/james-ward-cardinal-v1/west/native-evidence.json').read_bytes());old_sources={(r['key'],r['index']):r['sourceHash'] for r in old['records']}
assert all(old_sources[r['key'],r['index']]==r['sourceHash'] for r in e['records'])
contact_comparison={}
for c in reg['cases']:
    direction=c['facing'];path=R/('character/james-ward-lifecycle-v1/native-evidence.json' if direction=='north' else 'character/james-ward-cardinal-v1/'+direction+'/native-evidence.json')
    original=json.loads(path.read_bytes())['records'][0]['foot'];assert original==c['contact'];contact_comparison[direction]={'before':original,'after':c['contact'],'exact':True}
review['visualReview']={'nativeBoardsReviewed':2,'sourceBoardsReviewed':3,'masterReviewed':True,'beforeAfterReviewed':True,'assessment':'Raised torch area clears original crate at new physical workpoint throughout captured West draw/held/stow; original matte body/master scale and standing joins retained. All88 RGBA sources also exact against prior cardinal records. This proves the dedicated static West fixture, not all moving furniture or full silhouette clearance.'}
write(P/'review-evidence.json',review)
selection={'status':'installed_ward_tool_clearance_native_fixture_reviewed_owner_review_pending','runtimeChanged':True,'productionFiles':['scripts/branforth_npc.gd','scripts/ward_repair.gd','scripts/james_construction_motion.gd'],'sourcesChanged':False,'newDrawings':0,'newSourceStates':0,'fullSetComplete':False,'native':{k:v for k,v in e.items() if k!='records'},'regression':reg,'otherFacingContactComparison':contact_comparison,'billCompatibility':'Original tests/test_ward_repair.gd passes under scratch profile. Wrapper UID path corrected afterward; native regression generated missing paired UID.','review':'review-evidence.json','guards':guards,'inputHashes':'runtime-input-startup.json / runtime-input-after.json: nine match, sampled during initial West startup before compatibility launches; no prelaunch/full-interval frozen claim','archive':'before-teardown-fix: first regression checks passed but fixture detached scenes before pending camera callbacks. Final fixture waits for observable render/camera settling before removal, final log clean. No production camera changes.','scope':review['scope']}
write(P/'selection-review.json',selection)
for relative in ['character/james-ward-cardinal-v1/selection-review.json','character/james-ward-lifecycle-v1/selection-review.json','character/james-torch-material-residue-v2/selection.json']:
    p=R/relative;obj=json.loads(p.read_bytes());obj['wardToolClearanceReview']='character/james-ward-clearance-v1/selection-review.json';write(p,obj)
note='''## James ward torch furniture clearance installed — October 1, 2026

character/james-ward-clearance-v1 resolves the West static storage/cryo fixture
overlap found in cardinal review. Ward.approach retains original desired point,
candidate distance ordering, genuine graph/routes and MAX_ROUTES3; optional James
hook filters clear foot candidates by raised torch-to-door rays. Measured selected
flame offsets, original physical foot and registered visible prop rectangles with
2world-unit margin; floor pieces, wall attachments and overhead shelves excluded.
Dry bare James only; original behavior for other actors/gears. No owner furniture,
source artwork, body/pivot/ruler/palette, paid18seconds/8Metal or rewards changed.
Three production files:branforth_npc,ward_repair,james_construction_motion.

Diagnostic probe records original foot7344.2378,7840.2378 and crate rect
(-182.7,-96,42.2012,49.1599), confirming the raised flame area intersects the crate.
Normal approach now chooses7344.8740,7872.0; two native boards/88 captured original
source poses and three clean source boards, master and before-after views reviewed.
Raised tool area is clear in the captured West lifecycle; exact prior RGBA88/88,
same148/p92,172 master size/matte grade and standing endpoints retained.

7683 native checks0failures/88 views, three paused real disk fresh-scene Continues
at draw/held/stow, original cost/progress/source/player/cache exact.9717 actual
North/East/South paid job checks0failures; all three physical contacts exactly match
prior evidence. Original Bill ward test passes. Three final engine0/no-timeout
guards and strict owner profile unchanged, logs clean. Nine inputs match startup
and after snapshots; first snapshot was during initial West startup before
compatibility launches, not a full prelaunch-frozen interval claim. Initial
regression green counts had detached-scene camera errors; archived before fixture
awaited observable render/camera settling. No production camera changes.

Lesson: standable feet do not prove raised equipment clearance. Filter ordinary
worksite candidates using the accepted source's contact height and actual prop
registration; fix placement rather than repainting/rescaling anatomy or moving
owner furniture. This is conservative rectangle/ray clearance, not pixel-exact
full silhouette proof. Review native worksite and source/master match separately.
native-source-order.gif is50ms per unique source capture, simplified pose order,
not continuous18-second gameplay. Owner acceptance pending.

Remaining: moving furniture invalidation/currently claimed points, full silhouette
and alternate owner-layout acceptance, ward gears/kinds, power/door/critical flood/
incoming-worker contexts; wider full-set/master/cross-family/furniture/rotation/
owner/export polish. Full animation goal active/incomplete.

'''
guides=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for i,p in enumerate(guides):
    data=p.read_bytes();assert note.splitlines()[0].encode() not in data
    atomic(p,note.encode('utf-8')+data if i==0 else data.rstrip(b'\r\n')+b'\n\n'+note.rstrip().encode('utf-8')+b'\n')
handoff='''# Project handoff

Updated: 2026-10-01 · Project: Brine Space · Task: James ward tool clearance

## Objective and acceptance
Full James motion set continuously matching masters/style/perspective/size/
height/proportions/grade, then cross-family polish. This milestone fixes a
native West furniture/torch overlap; full goal remains incomplete.

## Accepted decisions and constraints
Original matte artwork148/p92,172; original paid18seconds/8Metal. Preserve owner
furniture/save and concurrent Bill/Veld changes. Static dedicated fixture; owner
review pending. No per-pose rescale/repaint or actor pose/path/collision overrides.

## Current state
Three production files:branforth_npc.gd,ward_repair.gd,james_construction_motion.gd.
Optional dry bare James ward approach ray clearance at selected flame height.
Original candidate ordering/routes/MAX_ROUTES retained; original other-actor/gear
behavior. Evidence, before-after view, native/source boards and paired fixture
UIDs here. Five guides and three parent selections updated; no new source states.

## Verification
7683 West lifecycle checks0failures/88 captures,3 real disk fresh Continues;
exact prior source RGBA88/88, original paid job completes once.9717 other-facing
paid checks0failures, same prior North/East/South contacts; original Bill ward
test passes. All native/source/master/before-after views reviewed. Three final
engine0/no-timeout/profile guards, logs clean. Nine startup/after hashes match;
startup snapshot was after initial West launch, no whole-interval frozen claim.
First regression detached-scene camera errors archived; fixture settling fixed.
Native GIF simplified50ms/unique pose, not continuous real-time gameplay.

## Next action
Moving furniture/claimed-point invalidation and fuller silhouette/owner-layout
clearance. Ward gears/kinds, power/door/critical flood/incoming workers; wider
full-set/master/cross-family/furniture/rotation/owner/export polish. Goal active.
'''
atomic(P/'HANDOFF.md',handoff.encode('utf-8'))
print(json.dumps({'checks':e['checks']+reg['checks'],'nativeCaptures':88,'freshContinues':3,'otherContactsExact':3,'guidesUpdated':5,'hashesMatch':9}))
