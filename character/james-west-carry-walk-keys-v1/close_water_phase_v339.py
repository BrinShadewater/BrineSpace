from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'water-phase-probe-v339'
validation=json.loads((o/'probe-validation.json').read_bytes());assert validation['exitCode']==0 and validation['realProfileUnchanged'] and not validation['timedOut']
d=json.loads((o/'traces.json').read_bytes());assert d['checks']==242 and d['failures']==0 and len(d['traces'])==48
inventory=json.loads((p/'selected-family-audit-v333/selected-inventory.json').read_bytes())
matched=0
for x in d['traces']:
 gear=x['gear'] or 'bare';rows={z['key']:z for z in inventory['gears'][gear]}
 for file,key,slot in [(x['before'],'swim-'+x['direction'],x['swimSlot']),(x['after'],'swim-stop-'+x['direction'],x['stopSlot'])]:
  im=Image.open(o/file).convert('RGBA');assert hashlib.sha256(im.tobytes()).hexdigest()==rows[key]['pixelHashes'][slot];matched+=1
boards=[]
for gear,name in [('', 'bare'),('diving-helmet','helmet')]:
 for direction in ['east','south','west','north']:
  board=Image.new('RGB',(512,1800),(48,59,64));draw=ImageDraw.Draw(board)
  rows=[x for x in d['traces'] if x['gear']==gear and x['direction']==direction]
  for j,x in enumerate(rows):
   draw.text((5,j*300+4),f"swim {x['swimSlot']} -> stop {x['stopSlot']} / equal {x['pixelsEqual']}",fill='white')
   for col,key in enumerate(['before','after']):
    im=Image.open(o/x[key]).convert('RGBA');board.paste(im,(col*256,j*300+20),im)
  filename=f'{name}-{direction}-comparison.png';board.save(o/filename);boards.append(filename)
assert (o/'probe.gd.uid').is_file()
media=list(o.glob('*.png'));attrs=subprocess.run(['git','check-attr','--stdin','-z','filter'],input=b''.join(str(f.relative_to(r)).replace('\\','/').encode()+b'\0' for f in media),cwd=r,capture_output=True,check=True).stdout.split(b'\0')
assert len(media)==104 and all(attrs[i]==b'lfs' for i in range(2,len(attrs)-1,3))
report=dict(checks=242,failures=0,scenarios=48,pixelOutputsMatchedPriorSelectedInventory=matched,sourceMismatches=sum(not x['pixelsEqual'] for x in d['traces']),stopEntrySlots=sorted(set(x['stopSlot'] for x in d['traces'])),boardsActuallyViewed=boards,normalChanged=False,sourceAcceptance=False,fullGoalComplete=False,ownerProfileUnchanged=True,scope=d['scope'],finding='All swim phases select stop0; phase1..4 changes pose abruptly in every direction/both gears. Technical checks intentionally establish the actual behavior, not a continuity pass.',next='Create James-specific phase-preserving stop handoff from exact selected poses, with finite clocks, clearance for whole bridge, pause/interrupt/equipment changes and saved playback/whole-run continuation; preserve existing master art and shared crew behavior.')
report['postRunCodeBindings']={f:hashlib.sha256((r/f).read_bytes()).hexdigest() for f in ['scripts/crew_sprite_player.gd','scripts/james_cargo_player.gd','scripts/grid_canvas.gd','character/james-cargo-return-bridges-v1/return_player.gd',str((o/'probe.gd').relative_to(r))]}
report['prelaunchFreeze']=False
(o/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
section='''### James actual swim-stop phase discontinuity — October 3, 2026

V339 actual normal Grid replacement loader/JamesCargoPlayer headless with isolated
APPDATA:242checks0,48all-swim-phase/four-direction/both-gear scenarios. Requested
phase reached through real distance gait advancement, then swim->tread transition
with clearance permission. All48select stop0;32 phase1..4 pairs change source pose,
16neutral0/5 joins match. Player snapshot/restore reproduces each stop entry.
96returned CPU texture images match exact v333 selected RGBA slots. All8pair boards
viewed: visibly instant arm/leg posture reset at phase1..4.104LFS images, paired
probeUID, real owner's profile unchanged. Post-run code hashes retained; no
prelaunch freeze, native drawing/full-scene route/whole-run Continue claim.

This green diagnostic establishes discontinuity; it is not a continuity pass.
Earlier32phase-zero exactjoins did not establish arbitrary locomotion-phase stop
continuity. Next James-specific phase-preserving stop handoff using exact selected
poses, finite clocks, whole bridge clearance and pause/restart/interruption/gear/
snapshot/whole-run validation. Do not globally alter other crew or delay physics
without evidence. Existing art/material/proportion issues remain; no new generated
art or production selection/controller change here. Full goal active/incomplete.
Handoff: character/james-west-carry-walk-keys-v1/water-phase-probe-v339/HANDOFF.md.
'''
record_guides(r,section,'### James cargo-swim original-source trace and material trial — October 3, 2026')
(o/'HANDOFF.md').write_text('# Project handoff\n\n## Objective and acceptance\nFull James set following original masters, then all-family consistency/polish; incomplete.\n\n## Accepted decisions\nPreserve actual current pose at transitions, original art/grade/tools, independent physical motion and collision clearance.\n\n## Current state\n'+section+'\n## Changed files and checks\nwater-phase-probe-v339 probe.gd/pairedUID/log/validation/traces/96CPU texture outputs/eight viewed boards/review; close_water_phase_v339.py;five guides/root handoff/ledger.242checks0,96exact source slots,104LFS media,owner-profile unchanged. No production changes.\n\n## Remaining work\nRepair and visually verify all-phase stop/start/interruption handoffs and whole-scene/Continue behavior; hazard/death/rest contact/core material/proportion/master fidelity and polish.\n',encoding='utf-8')
with (p/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n'+section)
ledger=p/'material-repair-progress.json';old=ledger.read_bytes();data=json.loads(old);data['waterPhaseProbe']=dict(version=339,file=str((o/'review.json').relative_to(r)),checks=242,failures=0,phaseDiscontinuities=32,normalChanged=False)
assert ledger.read_bytes()==old;ledger.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
print('V339:48 phases,32 discontinuities,242 diagnostic checks0;96exact selected source images/104LFS media; five guides updated.')
