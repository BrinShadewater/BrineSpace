from pathlib import Path
import json,hashlib,os,uuid,time,subprocess
p=Path(__file__).resolve().parent;r=p.parents[1];sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();records=[]
for name in ['room-journey-v45','room-journey-v46']:
    out=p/name;d=json.loads((out/'inputs.json').read_bytes());assert all(sha(r/f)==v for f,v in d['preLaunchSha256'].items())
    native=json.loads((out/'native-evidence.json').read_bytes());validation=json.loads((out/'native_probe-validation.json').read_bytes());assert native['checks']==2563 and native['failures']==0 and len(native['results'])==2
    assert validation['exitCode']==0 and validation['realProfileUnchanged'] and not validation['profileDelta']
    for row in native['results']:assert sorted(row['observedWalkSlots'])==list(range(49)) and row['freshSceneDiskResume'] and len(row['captures'])==6
    record=dict(nativeChecks=2563,nativeFailures=0,actualRoutes=2,sourceSlotsPerRoute=49,freshSceneDiskResumes=2,reviewedRoomCaptures=12,reviewedRoomBoards=2,normalChanged=False,sourceAcceptance=False,fullGoalComplete=False,realProfileUnchanged=True,continuousVisualMotionReviewed=False,visualFindings=['Partial workbench/backdrop overlap limits case/upper-body assessment; on/off difference alone does not certify unobscured body.'] if name.endswith('45') else ['Open floor route shows entire carrying character and case; bare and helmet journey/paused restore/north unload captures reviewed.', 'Actual arrival directly switches west carry to north unload; this is normal current behavior, not a newly authored/certified carrying turn. Room tint/camera surroundings change after fresh scene; exact source-pixel restore is separate from full rendered scene parity.'],scope='Prescribed collision-clear96world-unit workshop routes through real JamesNPC.update/move/arrive/grid, staged49Westbank explicitly reinstalled before fresh-scene disk restore. Not autonomous scheduler, title fresh-process Continue, pickup/preparation lifecycle or normal adoption/binding.')
    (out/'review-acceptance.json').write_text(json.dumps(record,indent=2)+'\n');records.append(record)
section='''### James staged West cargo room and disk-resume review — October 2, 2026

V45/V46 actual normal JamesNPC.update/move/arrive/grid consume staged V16 paired49
West walking bank on four prescribed collision-clear96world-unit workshop routes.
Each fixture2563/0; all49 source slots observed per route, four actual fresh-scene
midroute disk restores preserve actor/playback/clock/pause/source pixels. Candidate
bank explicitly reinstalled before restore; current cargo checkpoint only binds
unload/settle banks, so this does not prove normal candidate source admission.

All24 room captures reviewed in four boards. V45 route has workbench/backdrop
overlap limiting case/upper-body assessment. V46 picks a lower clear floor route,
shows full character/case, hides fixture hand/card panels. No room/owner furniture
or source art changed. Actor on/off render difference proves contribution, not
whole-body visibility. Source-pixel restore does not prove whole rendered-scene
parity: camera/environment tint differences remain visible after fresh scene.

Code audit identifies runtime wiring gap: dry workshop_pickup sets state idle and
timer520ms; dry animation_state/action_elapsed do not select pickup. Effective
pickup-west already has six70/80/90/100/100/80ms sources in joined material bank.
Existing authored coverage is not controller coverage. Actual arrive immediately
sets north-facing unload after west carry; carrying turn/preparation not exercised.
V44 staged210ms preparation handoff remains unintegrated. Do not call these four
manual routes full cargo lifecycle, autonomous dispatch or title Continue proof.

Both native processes terminal; all owner files unchanged with scratch APPDATA.
Prelaunch source/program/runtime/normal registry hashes stable. Full set unfinished;
normal loader/source/cargo binding unchanged. Next stage existing dry pickup with
simulation clock, preparation and arrival turn through actual workshop lifecycle;
source/material/contact polish, interruptions, checkpoint binding/backcompat and
versioned adoption before complete cardinal/cross-family review.
Evidence:character/james-west-carry-walk-keys-v1/room-journey-v46/review-acceptance.json;
character/james-west-carry-walk-keys-v1/room-journey-v45/review-acceptance.json.
'''
paths=[r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for f in paths:
    old=f.read_bytes();entry=section.encode()
    if entry.split(b'\n',1)[0] in old:continue
    if f.name=='CURRENT_STATUS.md':at=old.index(b'### James carrying preparation handoff clock corrected');new=old[:at]+entry+b'\n'+old[at:]
    else:new=old+b'\n'+entry
    tmp=f.with_name(f.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(new)
    try:
        for attempt in range(5):
            assert f.read_bytes()==old
            try:os.replace(tmp,f);break
            except PermissionError:
                if attempt==4:raise
                time.sleep(1)
    finally:
        if tmp.exists():tmp.unlink()
(p/'room-journey-v46/HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · James actual room cargo walk review

## Objective and accepted decisions
Complete full master-matched James set and consistency polish. Incomplete.
Preserve matte original masters, physical scale/pivot, correct equipment, normal
owner saves and existing source bindings until versioned adoption is proven.

## Current state and changed files
V45/V46 two paired actual NPC/grid workshop route fixtures, input hashes, native
captures, reviews and helpers added. Five guides updated. V45 workbench-overlap
route retained; V46 open-floor route makes entire source visible. No art/normal
loader/cargo binding/furniture changes; no commit/PR/export.

## Verification
Each native2563/0, four routes total. All49 walking slots observed per route;
four real fresh-scene midroute disk saves/restores preserve actor/playback/clock/
pause/source pixels with explicit candidate bank reinstall. All24 captures/four
boards reviewed. Owner whole profile unchanged/scratch APPDATA, processes terminal.
Prelaunch sources/runtime/program hashes exact. No full rendered-scene parity,
pickup/prep lifecycle, autonomous dispatch, normal source admission or title proof.

## Remaining work and next action
Dry workshop pickup currently displays idle during520ms; six authored pickup-west
poses already selected but not reached by dry animation-state/action clock hooks.
Stage that simulation-driven pickup, V44 preparation and carrying arrival turn
through full actual workshop lifecycle. Verify interruptions and checkpoint bank
binding/backcompat before adoption. Chest/case/material/sole contact and full
cardinal/cross-family master polish remain open. Candidate remains unselected.
''',encoding='utf-8')
with (p/'HANDOFF.md').open('ab') as f:f.write(b'\n'+section.encode())
rasters=[f.relative_to(r).as_posix() for name in ['room-journey-v45','room-journey-v46'] for f in (p/name).rglob('*.png')]
attrs=subprocess.run(['git','check-attr','-z','filter','--stdin'],cwd=r,input=b'\0'.join(x.encode() for x in rasters)+b'\0',capture_output=True,check=True).stdout.split(b'\0');assert all(v==b'lfs' for v in attrs[2:-1:3])
print(json.dumps(dict(nativeChecks=5126,failures=0,actualRoutes=4,sourceSlotsPerRoute=49,diskResumes=4,reviewedCaptures=24,reviewedBoards=4,guidesUpdated=5,lfsRasters=len(rasters),normalChanged=False,fullGoalComplete=False)))
