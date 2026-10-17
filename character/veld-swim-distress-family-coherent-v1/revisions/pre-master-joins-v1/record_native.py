"""Bind actual cardinal candidate playback; distinguish synthetic geometry from world proof."""
from pathlib import Path
import hashlib,json,re
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-swim-distress-family-candidate-v1'
result=json.loads((O/'validation.json').read_text());assert result['passed'] and not result['realProfileChanges']
log=(O/'native.log').read_text();match=re.search(r'FAMILY CANDIDATE: (\d+) checks,0 failures',log);assert match
assert int(match[1])==555
files=[R/'tests/test_veld_swim_distress_family_candidate.gd',R/'tests/test_veld_swim_distress_family_candidate.gd.uid',R/'tools/run_veld_swim_distress_family_candidate.py']+[f for f in O.iterdir() if f.is_file()]
e={'checks':int(match[1]),'result':result,'boundFiles':{f.relative_to(R).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'geometry':'synthetic blockers with actual original selected clearance; not furnished room proof','scenarios':'four directions,two gears,two arbitrary visual offsets; low-air threshold history,all slots/wrap,cargo rendered interruption from interior slot2 and reentry0,restored wet air and second episode0,safe-air exit,actual water-death dispatch','candidateOnly':True,'remaining':'furnished world,disk restore,continuous motion/handoffs,normal selection'}
(P/'native-evidence.json').write_text(json.dumps(e,indent=2)+'\n')
lesson='''

### Cardinal distress rendered interruptions — September 30, 2026
555 actual candidate/controller/renderer checks pass using original selected
clearance for all4 directions/2gears/2clock offsets. Explicit interior slot2,
rendered cargo replacement,then distress reentry0 proves the interruption;
restored wet air and second low-air episode also reset entry0. Earlier523-check
interval lacked the rendered cargo sample and is retained as weaker evidence.
The first strengthened interval rewound the clock and correctly reset playback;
retain its16 failed slot assumptions. Corrected clock advances monotonically.
Scratch owner profile unchanged. Synthetic blocker proof is not real furniture
or disk restore; those and continuous joins remain before normal selection.
'''
for name in ['docs/VELD_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md','C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md']:
 f=Path(name) if Path(name).is_absolute() else R/name
 if b'### Cardinal distress rendered interruptions' not in f.read_bytes():
  with f.open('ab') as stream:stream.write(lesson.encode())
f=P/'HANDOFF.md';s=f.read_text(encoding="utf-8")
s=s.replace('## Next action','Cardinal follow-up:555 actual life/controller/renderer checks PASS; original selected clearance retained. Interior slot2 → rendered cargo → distress0, restored wet air → second distress0 verified across16 direction/gear/clock cases. Earlier523-check interval retained with its weaker cargo sampling. Native family board reviewed. No owner profile changes. Synthetic geometry only; disk restore and furnished room proof remain.\n\n## Next action') if 'Cardinal follow-up:' not in s else s
f.write_text(s,encoding="utf-8")
f=R/'docs/CURRENT_STATUS.md';data=f.read_bytes();needle=b'64 exact\nconsolidation checks and byte-exact two-manifest/48frame rebuild.'
replacement=needle+b' Cardinal555\nnative checks verify original selected clearance and rendered cargo/air reentry. '
if b'Cardinal555' not in data:f.write_bytes(data.replace(needle,replacement,1))
print(f'Bound {match[1]} cardinal checks; recorded rendered-interruption scope and limits')
