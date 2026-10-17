from pathlib import Path
from PIL import Image
import json,hashlib,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'water-motion-review-v341';source=p/'water-stop-bridge-v340'
v=json.loads((source/'playback_probe-validation.json').read_bytes());assert v['exitCode']==0 and v['realProfileUnchanged'] and not v['timedOut']
report=json.loads((o/'review.json').read_bytes());assert report['rows']==96 and report['slots']==496 and report['uniquePixels']==80
for name in report['animatedBoards']:
    im=Image.open(o/name);assert im.is_animated and im.n_frames>1
report.update(staticBoardsActuallyViewed=report['staticBoards'],browserReview={'direction':'west','speed':0.25,'observedMs':[67,200],'scope':'Intermittent advancing/paused captures only; not complete continuously observed clips.'},sourceAcceptance=False,fullGoalComplete=False,ownerProfileUnchanged=True,prelaunchFreeze=False)
report['finding']='All chronological source rows inspected at82px: equipment retained, registered natural rise/reverse. Stop latency varies560..1040ms by entry phase; this is not actor physical stopping time. Source material remains coarser than original master. No full-motion or route acceptance claimed.'
report['postRunCodeBindings']={str(f.relative_to(r)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [source/'phase_player.gd',source/'playback_probe.gd',source/'playback.html',p/'build_water_motion_v341.py']}
media=list(o.glob('*.png'))+list((source/'playback-frames').glob('*.png'))
attrs=subprocess.run(['git','check-attr','--stdin','-z','filter'],input=b''.join(str(f.relative_to(r)).replace('\\','/').encode()+b'\0' for f in media),cwd=r,capture_output=True,check=True).stdout.split(b'\0');assert len(media)==101 and all(attrs[i]==b'lfs' for i in range(2,len(attrs)-1,3))
(o/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
section='''### James staged swimming chronology and gameplay-size previews — October 3, 2026

V341 actual normal loader sources cloned into V340 staged player; isolated native
export96finite rows/496pose slots/80unique exactRGBA images. Owner profile unchanged.
12APNG boards replay full exported clocks at148/82/54/27rulers, terminal700ms review
hold and loop explicitly added; eight chronological82px source boards all viewed.
Sources retain equipment and registered authored rise/reverse. No new art or grade.
Browser West quarter-speed samples67ms and paused200ms viewed/saved; source-clock
advancement and stepping observed, not complete continuously observed playback.
Full transition temporal quality is still unaccepted.101LFS media; paired probeUID.

Stop display duration varies560..1040ms with entry stroke. Exact entry matching
does not prove responsiveness, independent physical stopping, whole bridge collision
clearance or direction/equipment interruption behavior. Preserve these as separate
checks before normal installation; do not stop physics merely to satisfy pictures.
Existing coarse quilt/master fidelity and remaining family polish persist.
Normal source/controller selection unchanged. Full goal active/incomplete.
Handoff: character/james-west-carry-walk-keys-v1/water-motion-review-v341/HANDOFF.md.
'''
record_guides(r,section,'### James staged all-phase swimming stop and restart — October 3, 2026')
(o/'HANDOFF.md').write_text('# Project handoff\n\nUpdated: October 3, 2026 · Task: James swimming motion review\n\n## Objective and acceptance\nFull James set matching original masters, then consistency/polish. Incomplete.\n\n## Accepted decisions and constraints\nExact selected source pixels and metadata; fixed whole-canvas rulers. Staged only; keep physics independent.\n\n## Current state\n'+section+'\n## Verification\n96rows/496slots/80exactRGBA exported;12animated files decode;8static full chronology boards viewed;limited browser West progression/stepping viewed;101LFS media,owner unchanged.\n\n## Next action\nComplete temporal playback review, direction/gear interruption audit and actual renderer full-bridge clearance/NPC/save-Continue checks. Then select only a satisfactory repair and continue missing-family/fidelity/polish work. Local viewer server execsession28287 on127.0.0.1:8899; poll same handle to check liveness, not historical notes.\n',encoding='utf-8')
with (p/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n'+section)
ledger=p/'material-repair-progress.json';old=ledger.read_bytes();data=json.loads(old);data['waterMotionReview']={'version':341,'file':str((o/'review.json').relative_to(r)),'rows':96,'slots':496,'normalChanged':False,'fullMotionActuallyViewed':False};assert ledger.read_bytes()==old;ledger.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
print('V341:96rows/496slots;8chronology boards viewed;12APNG previews/101LFS media;five guides updated;staged only.')
