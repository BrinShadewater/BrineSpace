from pathlib import Path
import json,hashlib,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'water-playback-v336'
d=json.loads((o/'inputs.json').read_bytes())
for f,h in d['sourceBindings'].items():assert hashlib.sha256((r/f).read_bytes()).hexdigest()==h
for frames in d['bank'].values():
 assert len(frames)==6 and all(f['duration']>0 for f in frames)
 for f in frames:assert hashlib.sha256((o/f['src']).read_bytes()).hexdigest()==Path(f['src']).stem
shots=['west-quarter.png','west-advancing.png','east-normal.png','north-normal.png','south-normal.png']
assert all((o/f).is_file() for f in shots)
media=list(o.rglob('*.png'));attrs=subprocess.run(['git','check-attr','--stdin','-z','filter'],input=b''.join(str(f.relative_to(r)).replace('\\','/').encode()+b'\0' for f in media),cwd=r,capture_output=True,check=True).stdout.split(b'\0')
assert all(attrs[i]==b'lfs' for i in range(2,len(attrs)-1,3))
review=dict(sourceSlots=192,uniqueSourceFiles=120,sourceBindingsStable=True,reviewScreenshotsViewed=shots,actualBrowserAdvance=dict(westNormalMs=6596,westQuarterMs=[14,3025],westCargoQuarterPoses=[0,3],eastNormalMs=79,northNormalMs=75,southNormalMs=73),fullContinuousObservation=False,ordinaryControllerSimulation=False,normalChanged=False,sourceAcceptance=False,findings=['West cargo shoulder bulk remains apparent at sampled advancing kick phases.','Bare/helmet loops use same source clock and maintain selected gear in observed views.','All four directions have functioning comparison playback; source sequence uses phase-zero swim entry and two loops, not an actual controller trace.'],next='Inspect actual game water transition phase selection/interruptions and isolate cargo shoulder/cloth proportion against masters before authoring replacement; hazard/death and full set polish still open.')
(o/'review.json').write_text(json.dumps(review,indent=2)+'\n')
section='''### James swimming playback comparison — October 3, 2026

V336 exact selected-source viewer includes normal/quarter speed, four directions,
paired bare/helmet swim and cargo loops, start/two-swim-loops/stop source sequence.
192 selected slots,120 byte-exact PNG copies; source/copy hashes rechecked and
all125 source/screenshot PNG LFS attributes verified. No anatomy/grade edits.
Actual browser clock/pose advancement observed: West normal6596ms; quarter14→
3025ms and cargo0→3. East/North/South normal views captured and viewed. Five full
page screenshots retained. Original tab disappeared; recreated on same browser,
existing confirmed live server, without rebuilding or restarting source work.

West cargo shoulder bulk remains visible across sampled kicks. Gear retained in
observed views. These intermittent screenshots do not certify continuous whole
motion or ordinary game water behavior. Sequence is explicit phase-zero source
composition, not a phase-aware controller trace; no cadence/master acceptance.
Next inspect real player transition phases/interruptions and isolate cargo cloth/
shoulder proportion before replacement. Hazard/death, rest furniture, carry/unload
support/material and full-family master/gameplay polish remain. Full goal active.
Handoff: character/james-west-carry-walk-keys-v1/water-playback-v336/HANDOFF.md.
'''
record_guides(r,section,'### James selected swimming chronology comparison — October 3, 2026')
(o/'HANDOFF.md').write_text('# Project handoff\n\n## Objective and acceptance\nFull James set/master fidelity and all-family polish; incomplete.\n\n## Accepted decisions\nExact selected art, source clocks and metadata. Browser source replay is distinct from game controller/continuous motion acceptance.\n\n## Current state\n'+section+'\n## Changed files and checks\nbuild_water_playback_v336.py, close_water_playback_v336.py, local viewer,192 source slots/120PNG copies, five viewed screenshots, reports; five guides, root handoff/ledger. Sources/copies unchanged;125LFS media. No Godot run or owner save access.\n\n## Remaining work\nPhase-aware in-game water transitions, interruptions, targeted cargo material/proportion repair; hazards/death/rest contacts/core repairs and full-family master fidelity.\n')
with (p/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n'+section)
ledger=p/'material-repair-progress.json';old=ledger.read_bytes();data=json.loads(old)
data['waterPlaybackReview']=dict(version=336,file=str((o/'review.json').relative_to(r)),sourceSlots=192,actualBrowserAdvancement=True,continuousMotionAcceptance=False,normalChanged=False)
assert ledger.read_bytes()==old;ledger.write_text(json.dumps(data,indent=2)+'\n')
print('192 exact source slots; five playback captures reviewed; five guides updated. Full goal active.')
