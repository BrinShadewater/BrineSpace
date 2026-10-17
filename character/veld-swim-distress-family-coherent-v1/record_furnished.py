"""Bind valid-world furnished/disk evidence without promoting the candidate."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-distress-furnished-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
result=json.loads((O/'validation.json').read_text(encoding='utf-8'));report=json.loads((O/'furnished-checks.json').read_text(encoding='utf-8'))
assert result['passed'] and not result['realProfileChanges'] and report['failures']==0
assert len(report['cases'])==32 and report['diskRestores']==96 and all(r['rejectedGraphNodes']>0 for r in report['cases'])
profile=R/'character/dr-veld-v2/clearance.json';assert sha(profile)==json.loads((P/'clearance-audit.json').read_text())['selectedProfileSha256']
board=Image.new('RGB',(4*340,2*380),'#202a30');draw=ImageDraw.Draw(board)
for d,direction in enumerate(['east','west','north','south']):
 for g,gear in enumerate(['bare','helmet']):
  image=Image.open(O/f'{direction}-{gear}.png').convert('RGB');image.thumbnail((330,345))
  board.paste(image,(d*340+5,g*380+25));draw.text((d*340+5,g*380+5),direction+' '+gear+' furnished frame3',fill='white')
board.save(P/'furnished-contact.png')
files=[f for f in O.iterdir() if f.is_file()]+[R/'tools/review_veld_distress_furnished_v1.gd',R/'tools/review_veld_distress_furnished_v1.gd.uid',R/'tools/run_veld_distress_furnished_validation_v1.py',profile,P/'furnished-contact.png',P/'motion.html',P/'motion-review-bindings.json']
e={'status':'candidate_furnished_and_disk_restore_verified','checks':report['checks'],'cases':32,'diskRestores':96,'nativeResult':result,'acceptedNodeComparisons':sum(r['acceptedGraphNodes'] for r in report['cases']),'rejectedNodeComparisons':sum(r['rejectedGraphNodes'] for r in report['cases']),'boundFiles':{f.relative_to(R).as_posix():sha(f) for f in files},'selectedClearanceChanged':False,'remaining':'full continuous-motion/joins review,normal-loader selection,actual low-air escape journeys and full-set death/rest/life/polish'}
(P/'furnished-evidence.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
lesson='''

## Veld distress furnished rooms and wet checkpoint proof — September 30, 2026

Candidate family passes1007 native checks in40.01s: five authored flooded
maintenance/storage rooms,four rotations,32direction/gear cases,96 current-disk
restores at distress slots1/3/5. Exact pixels,visual clock,oxygen,direction,gear,
wet medium,history and actual furnished gate retained. Graph scans compare30299
accepted and21821 rejected points; all32cases demonstrate real furniture
suppression. Existing profile hash unchanged;2914 owner non-logfiles unchanged
under scratch APPDATA. Eight room captures/contact reviewed; flooded tint and
station comms overlay remain in raw room captures. Review UI pairs actual selected
swim loops with candidate loops at manifest timing and82/148/54px standing scale,
plus illustrative entry/exit sequence and light/dark backgrounds. Browser east
dark and west light join samples reviewed; this is not whole continuous-motion
or actual escape-journey acceptance. Runtime Veld selection unchanged.

The initial custom-world checkpoint fixture cleared architect_run while retaining
generated site_layout/recovery wards. Production correctly rejected that invalid
world; retain failed interval. Preserve the generated version5 roster/wards in
furnished checkpoint fixtures rather than weakening save validation. Successful
art/player fixtures do not make arbitrary fixture worlds valid save games.
Remaining continuous joins,normal selection,actual escape journeys and whole-set
death/rest/life/polish keep the goal active. Handoff:
character/veld-swim-distress-family-coherent-v1/HANDOFF.md.
'''
for name in ['docs/VELD_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md','C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md']:
 f=Path(name) if Path(name).is_absolute() else R/name
 if b'## Veld distress furnished rooms and wet checkpoint proof' not in f.read_bytes():
  with f.open('ab') as stream:stream.write(lesson.encode('utf-8'))
f=P/'HANDOFF.md';s=f.read_text(encoding='utf-8')
if 'Furnished follow-up:' not in s:
 s=s.replace('## Next action','Furnished follow-up:1007 checks PASS40.01s;32 actual flooded direction/gear/rotation cases and96 exact wet disk restores. All cases exercise real furniture suppression,with30299 accepted/21821 rejected node comparisons. Profile hash and2914 owner non-logfiles unchanged. Native room captures/contact reviewed; original roster/wards preserved after initial invalid-world fixture rejection. motion.html supplies selected-swim/candidate timing and illustrative joins; browser samples do not prove whole continuous motion.\n\n## Next action')
 s=s.replace('Real furnished clearance, scratch disk restore, full-speed motion and swim/distress joins before normal-loader selection.','Full continuous-motion and swim/distress joins,then normal-loader selection and actual low-air escape journeys. Furnished geometry and96 wet disk restores are now proven within the fixture scope.')
 f.write_text(s,encoding='utf-8')
f=R/'docs/CURRENT_STATUS.md';current=f.read_bytes()
if b'## Veld swimming distress furnished and checkpoint milestone' not in current:
 f.write_bytes('''## Veld swimming distress furnished and checkpoint milestone — September 30, 2026

Cardinal candidate1007 native checks PASS40.01s across32 actual flooded
direction/gear/rotation cases and96 exact wet disk restores. Five authored rooms;
all cases exercise real furniture suppression.30299 accepted/21821 rejected node
comparisons; profile hash and2914 owner non-logfiles unchanged. Native room
captures/contact reviewed. Initial invalid roster/ward fixture rejected and
retained; production save validator unchanged. Same-clock master/action loops
and illustrative joins now available at82/148/54 on light/dark backgrounds.
Browser samples reviewed; whole continuous motion/joins,normal-loader selection
and actual low-air escape journeys remain. Runtime unchanged; full-set
death/rest/life/cross-family polish goal active.
[Handoff](../character/veld-swim-distress-family-coherent-v1/HANDOFF.md).

'''.encode('utf-8')+current)
print('Bound1007 furnished checks/96 restores; updated handoff,status,pipeline,bible and both skill copies')
