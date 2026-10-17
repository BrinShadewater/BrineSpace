from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parents[1]
def atomic(path,fn):
 before=path.read_bytes();after=fn(before);tmp=path.with_name(path.name+'.james.tmp');tmp.write_bytes(after)
 if path.read_bytes()!=before:tmp.unlink();raise RuntimeError('Concurrent update '+str(path))
 tmp.replace(path)
note='''

### North retained-berth visibility correction - 2026-09-30
The original midpoint depth38 hid pose2 behind the bedside cabinet, also hiding
reversed rise pose3 despite successful loader/pillow metadata checks. North lie
depths now [0,19,58,58,77,96], rise exact reverse, both modes. Other directions,
timings and body art stay selected. All36 updated contacts visually reviewed;
each rendered slot also compares actor-on versus actor-off room pixels.830
retained-berth checks and744 installed-loader checks PASS; profile unchanged.
See character/james-lying-family-v1/native-all-berth-contact.png. Before-correction
contact retained as native-berth-before-depth-correction.png. This is a specific
native visibility repair, not proof of cross-set continuous-motion polish.
'''
for rel in ['docs/JAMES_LYING_HANDOFF_2026-09-30.md','docs/JAMES_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 path=R/rel
 if b'### North retained-berth visibility correction - 2026-09-30' not in path.read_bytes():atomic(path,lambda b:b+note.encode())
path=R/'docs/CURRENT_STATUS.md';atomic(path,lambda b:b.replace(b'checks and794 retained-berth',b'checks and830 retained-berth').replace(b'36 native q0 north berth',b'North midpoint draw depth corrected38 to58 after cabinet hid a pose; actor-on/off\nvisibility checked for every slot.36 native q0 north berth'))
path=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')
if b'### North retained-berth visibility correction - 2026-09-30' not in path.read_bytes():atomic(path,lambda b:b+note.encode())
path=P/'selection.json'
def selected(b):
 m=json.loads(b);m['checks']['nativeRetainedBerth']=830;m['depthCorrection']={'northLie':[0,19,58,58,77,96],'rise':'Exact reverse','reason':'Midpoint cabinet occlusion','evidence':'native-all-berth-contact.png','visibility':'Actor-on/off image comparison for all36 rendered slots'};return (json.dumps(m,indent=2)+'\n').encode()
atomic(path,selected)
print('North draw-depth visual repair and final native evidence recorded')
