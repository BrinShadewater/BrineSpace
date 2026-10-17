from pathlib import Path
import json,hashlib,os,uuid,time,subprocess
p=Path(__file__).resolve().parent
r=p.parents[1]
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
inputs=json.loads((p/'selected-inputs.json').read_bytes())
assert all(sha(r/f)==v for f,v in inputs['preLaunchSha256'].items())
for stem in ['edge-study','validate','validate-selected','native-arrival-continue']:
    validation=json.loads((p/(stem+'-validation.json')).read_bytes())
    assert validation['exitCode']==0 and validation['realProfileUnchanged'] and not validation['profileDelta']
route=json.loads((p/'native-arrival-continue-evidence.json').read_bytes())
assert route['failures']==route['mismatches']==0 and len(route['results'])==8
assert (p/'route-review-acceptance.json').is_file()
room_review=json.loads((p/'route-review-acceptance.json').read_bytes())
assert room_review['reviewedCaptures']==24
normal=json.loads((p/'validate-selected-evidence.json').read_bytes())
assert normal['failures']==0
inventory=r/'character/james-full-set-review-2026-10-02/current-selection-v31/source-inventory.json'
inv=json.loads(inventory.read_bytes())
assert all(sha(r/f)==v for f,v in inv['sourceSha256'].items())
compare=json.loads((p/'effective-selection-comparison.json').read_bytes())
assert compare['allOtherEffectiveSourcePathsExact'] and len(compare['changedSourceStates'])==12
review=json.loads((p/'review-acceptance.json').read_bytes())
assert all(sha(r/f['path'])==f['sha256'] for f in review['reviewedBoards'])
capture=json.loads((p/'selected-capture-comparison.json').read_bytes())
assert capture['exactPixelsMatchReviewedStagedCaptures']
selection=json.loads((p/'selection-evidence.json').read_bytes())
selection.update(normalValidationPending=False,routeContinuePending=False,normalChecks=normal['checks'],routeChecks=route['checks'],roomCapturesReviewed=24,roomFreshSceneRestores=8,wholeRealProfileUnchanged=True,currentPrimaryInventory=inventory.relative_to(r).as_posix(),effectiveSourceStatesChanged=12,allOtherEffectiveSourcesExact=True,sourceMaterialReviewComplete=True,continuousVisualMotionReviewed=False,fullGoalComplete=False,scope='Selected edge-only South/North/West diagnostics correction; authored poses/silhouettes/clock/pivots retained, later East correction and effective meal sources retained. All864 source frames and twelve native four-size paired captures reviewed. Eight explicit generic dry maintenance-room arrivals and fresh-scene midpoint disk restores verified;24 actual room captures reviewed. No autonomous scheduler, actual locker changes, workstation rotation, title fresh-process Continue or full James motion/owner acceptance claim.')
(p/'selection-final-evidence.json').write_text(json.dumps(selection,indent=2)+'\n')
rasters=[f.relative_to(r).as_posix() for f in p.rglob('*') if f.suffix.lower() in ['.png','.apng']]
attrs=subprocess.run(['git','check-attr','-z','filter','--stdin'],cwd=r,input=b'\0'.join(x.encode() for x in rasters)+b'\0',capture_output=True,check=True).stdout.split(b'\0')
assert len(attrs)==len(rasters)*3+1 and all(x==b'lfs' for x in attrs[2:-1:3])
section='''### James three-direction diagnostic edge cleanup selected — October 2, 2026

V30 South/North/West diagnostics edge material bank selected in both normal grid
and ACTIVE_ASSETS, keeping the later V26 East correction and original effective
meal aliases. All864 source frames reviewed across18 chronological boards. Native
green-only correction changes852 sources;12 standing endpoints byte-exact.
Alpha/R/B and all pixels outside the byte-defined green-edge selector remain
exact. Clocks/counts/pivot92,172/canvas184/H148 unchanged. This correction does
not change authored head movement, anatomy, tablet perspective or equipment.
Numeric green admission is not semantic material classification; original opaque
interiors and warm equipment colors outside admission are preserved.

Staged normal-player check7568/0 and actual normal selection7566/0. Twelve paired
148/82/54/27 native captures reviewed; normally selected captures match the
reviewed staged pixels exactly. Initial combined-pack append failed helmet
compatibility because later meal overrides had already loaded; failure archived.
Lesson: stage only targeted states on an already-loaded player, or reproduce the
original catalog slot. Do not append an older combined bank after newer aliases
and mistake rejected equipment loading for a source-art defect. Normal selection
replaces the original combined slot and preserves its later East override.

Eight explicit dry generic maintenance-room arrivals and fresh-scene midpoint
disk restores pass, exact actor/playback/clock/pause/pose and normal6s completion;
24 room captures reviewed. North retains partial workshop-backdrop overlap;
these generic contacts do not certify every furnishing contact or depth sort.
All runs use scratch APPDATA; whole owner profile
unchanged. Fresh V31 primary inventory retains338bare/248helmet states and143
manifest loads, zero source/count/clock defects. Exactly12 effective source IDs
change (inspect/interact,3directions,2gears); every other effective source path,
state count/clock/canvas/pivot/ruler stays exact. V27 remains historical prior
selection evidence. LFS checked. No autonomous scheduler, actual locker changes,
workstation rotations, title fresh-process Continue or uninterrupted motion/owner
acceptance inferred. Full goal incomplete: cargo stance/case joins, full cardinal
and cross-family master matching and continuous/context polish still required.
Lossless paired APNG previews for all3 directions retain each original6s clock;
decoded source RGBA and durations verified. Preview creation does not imply
uninterrupted motion viewing.
Evidence:character/james-diagnostics-edge-matte-v30/selection-final-evidence.json.
'''
paths=[r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for f in paths:
    for attempt in range(3):
        old=f.read_bytes();entry=section.encode()
        if entry.split(b'\n',1)[0] in old:break
        if f.name=='CURRENT_STATUS.md':
            at=old.index(b'### James diagnostic edge-material representative study')
            new=old[:at]+entry+b'\n'+old[at:]
        else:new=old+b'\n'+entry
        temp=f.with_name(f.name+'.'+uuid.uuid4().hex+'.tmp');temp.write_bytes(new)
        try:
            assert f.read_bytes()==old
            os.replace(temp,f)
            break
        except PermissionError:
            temp.unlink()
            if attempt==2:raise
            time.sleep(2)
        finally:
            if temp.exists():temp.unlink()
handoff='''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James diagnostics edge cleanup

## Objective and acceptance
Full James set matching masters/art style/perspective/size/proportions/matte grade,
then complete cardinal/cross-family polish; maintain pipeline/bible/skills. Incomplete.

## Accepted decisions and constraints
Tablet faces James; wrench stays holstered; blowtorch for repairs/construction.
Preserve authored poses, alpha, clock/pivot and standing master endpoints. Keep
later V26 East grade and existing cargo checkpoint binding. No owner-save writes.

## Current state
V30 combined bare/helmet manifests selected at original continuity catalog slot
in scripts/grid_canvas.gd and character/ACTIVE_ASSETS.json.864 source frames,
18 cycle boards,3 native four-size boards,24 room captures; all reviewed.
V31 current primary source inventory supersedes V27 as current selection authority.
Exact preselection file backups retained. Failed whole-pack append fixture archived;
targeted staging and original normal load order pass. No commit/PR/export.

## Verification
1728 native edge-save checks0; all864 independent source protections pass;
12 endpoints exact. Staged7568/0, normal7566/0; normally selected captures match
reviewed staging exactly. Eight explicit dry direction/gear room arrivals and
fresh-scene midpoint disk restores pass with exact pose/clock/contact/gear and6s
completion. Whole owner profile unchanged. V31 has exactly12 effective source
changes, every other source and all clocks/pivots/rulers exact. Five guides/LFS
updated. selection-final-evidence.json records scope. Uninterrupted motion,
autonomous schedules, locker changes/rotation/title fresh-process not proven.

## Next action
Continue cargo standing/walking stance and case joins from west-carry-walk-keys-v1
HANDOFF and retained V20 leg bridge/V21 rejected upper bridge/V16 full walk.
Then full cardinal/cross-family master/material/height/context and continuous
motion review. Full James owner acceptance remains open.
'''
(p/'HANDOFF.md').write_text(handoff,encoding='utf-8')
for f in [r/'character/james-west-carry-walk-keys-v1/HANDOFF.md',r/'character/james-full-set-review-2026-10-02/HANDOFF.md']:
    old=f.read_text(encoding='utf-8');marker='## V30 selected diagnostics edge cleanup\n'
    if marker not in old:
        at=old.index('## Next action\n')
        old=old[:at]+marker+'''864 South/North/West bare/helmet sources reviewed/selected; alpha/R/B/outside
edge selector exact,12 endpoints exact, authored motion/clocks/pivots unchanged.
Staged7568/0, normal7566/0,8 explicit dry room arrivals/fresh-scene disk restores
pass;24 room captures reviewed, whole owner profile unchanged. V31 current
primary inventory changes only12 diagnostic source IDs; all other effective
sources/contracts exact, later East/meal aliases retained. Five guides/LFS updated.
Full James goal remains open. See james-diagnostics-edge-matte-v30/HANDOFF.md.

'''+old[at:]
        f.write_text(old,encoding='utf-8')
print(json.dumps(dict(normalChecks=normal['checks'],routeChecks=route['checks'],roomRestores=8,guides=5,lfsRasters=len(rasters),fullGoalComplete=False)))
