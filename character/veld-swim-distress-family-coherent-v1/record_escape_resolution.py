"""Record measured corridor silhouette correction and full cardinal route proof."""
from pathlib import Path
import hashlib,json,shutil
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-distress-escape-v1';G=R/'output/veld-corridor-swim-regressions-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
result=json.loads((O/'validation.json').read_text());report=json.loads((O/'journey-checks.json').read_text());reg=json.loads((G/'validation.json').read_text())
assert result['passed'] and not result['realProfileChanges'] and report['checks']==713 and report['failures']==0
assert reg['passed'] and not reg['realProfileChanges'] and len(report['cases'])==8
assert all(r['crossedDryAlive'] and r['safeRecoveryObserved'] and r['minimumAir']<r['initialAir'] for r in report['cases'])
assert sum(r['allowedCrossRoomEdges'] for r in report['geometryDiagnostics'])==16
old=P/'escape-investigation.json';archive=P/'revisions/vertical-escape-investigation-v1';archive.mkdir(parents=True,exist_ok=True)
if old.exists() and not (archive/old.name).exists():shutil.copy2(old,archive/old.name)
files=[f for f in O.iterdir() if f.is_file()]+[f for f in G.iterdir() if f.is_file()]+[R/'scripts/bill_npc.gd',R/'scripts/bill_npc.gd.uid',R/'tools/review_veld_distress_escape_v1.gd',R/'tools/review_veld_distress_escape_v1.gd.uid',R/'tools/run_veld_distress_escape_validation_v1.py',R/'tools/run_veld_corridor_swim_regressions_v1.py',R/'character/dr-veld-v2/clearance.json']
e={'status':'cardinal_physical_escape_verified_candidate_art','checks':713,'physicalRoutes':8,'guardedDoorwayEdges':16,'doorLockFireAndWallGuardChecks':64,'nativeResult':result,'regressions':reg,'boundFiles':{f.relative_to(R).as_posix():sha(f) for f in files},'rootCause':'_swim_floor_clear called can_stand for silhouette samples,adding10-unit walking floor margin and padded props again. Actual north/south57-unit body failed72-unit corridor mouth; first rejected sample radius10false/radius2true.','fix':'Corridor samples use2-unit floor margin after exact full-silhouette furniture sweep; closed sockets,locks,fire and legacy behavior retained. No artwork/profile/layout edits.','runtimeArtSelected':False,'remaining':'normal-loader selection,continuous-motion/first-interior/arbitrary-exit polish; full-set death/rest/life/consistency'}
(P/'escape-evidence.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
lesson=f'''

## Veld cardinal physical escape verified — September 30, 2026

Resolved vertical corridor failure without shrinking artwork,clearance or editing
room dressing. Cross-room graph edges existed. Diagnostic first north sample at
local(-28.229,-188.792) failed Corridor.contains_foot radius10 but passed radius2;
south sample(-27.347,190.376) had same result. The full57-unit swim silhouette
already included measured width; _swim_floor_clear then called can_stand,adding
walking floor margin10 and padded props again at the72-unit doorway mouth.
Corridor floor samples now use2-unit swim margin after existing exact silhouette
furniture sweep. Closed sockets/global and local locks/fire/legacy rules remain.
Single-corridor fast path stays conservative; rejected fast paths use corrected
sampled check. Changed scripts/bill_npc.gd only in this helper;UID preserved.

Fresh713 native checks PASS{result['seconds']}s: all8 actual direction/gear routes move
through authored flooded corridor/storage doorways,consume real air and enter
safe-air recovery alive. Actual candidate entry pixels checked. All16 permitted
door edges additionally reject global lock,local lock,fire and24-unit sideways
wall displacement (64negative checks). Scoped native flood-retreat and wet-door
integration regressions pass;2914 owner non-logfiles unchanged in scratch runs.
Balanced case/pose contact reviewed; generated source frames/master donors and
clearance profile unchanged. Failed investigation/diagnostic intervals retained.

Treat full-silhouette clearance samples as envelope edges,not new standing feet;
apply one explicit safety margin. Preserve exact obstacle sweep and negative
door/fire/wall tests when replacing a generic standing predicate. Real geometry
failure can be an inflated gate rather than oversized art. Keep candidate art
selection separate from navigation correction and full continuous-motion
acceptance. Family remains staged;normal selection and broad full-set work remain.
'''
for name in ['docs/VELD_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md','C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md']:
 f=Path(name) if Path(name).is_absolute() else R/name
 if b'## Veld cardinal physical escape verified' not in f.read_bytes():
  with f.open('ab') as stream:stream.write(lesson.encode('utf-8'))
f=P/'HANDOFF.md';s=f.read_text(encoding='utf-8')
if 'Escape resolution:' not in s:
 s=s.replace('## Next action',f"Escape resolution:713 native checks PASS{result['seconds']}s; all8 actual physical routes consume air and recover alive. Corrected corridor double walking padding after diagnostic radius10false/radius2true.64 lock/fire/wall negatives and native flood-retreat/wet-door regressions pass; owner profile unchanged. Failed investigation retained under revisions/vertical-escape-investigation-v1; escape-evidence.json is current authority. Balanced native case contact reviewed.\n\n## Next action")
 s=s.replace('Probe vertical doorway graph connections and selected per-edge swim clearance versus authored furniture. Resolve cardinal low-air escape before normal selection; first-interior/arbitrary-phase exit motion remains open.','Normal-loader selection verification and continuous-motion/first-interior/arbitrary-phase exit polish. Cardinal low-air escape is now proven for these eight authored-room journeys; crowd/exterior and locker-completion evidence remain distinct.')
 f.write_text(s,encoding='utf-8')
f=R/'docs/CURRENT_STATUS.md';current=f.read_bytes()
if b'## Veld cardinal escape verified after corridor margin correction' not in current:
 f.write_bytes(f'''## Veld cardinal escape verified after corridor margin correction — September 30, 2026

713 native checks PASS{result['seconds']}s:all8 actual bare/helmet cardinal flooded-room
routes cross physically,consume air and recover alive. Vertical failure was
double walking padding around measured swim silhouette at corridor mouth;
scripts/bill_npc.gd samples corridor floor with2-unit margin after exact obstacle
sweep. Artwork/profile/owner furniture unchanged.64 lock/fire/wall negatives
and native flood-retreat/wet-door integration regressions pass. Owner2914
non-logfiles unchanged; balanced native case contact reviewed. Failed diagnostic
intervals retained;escape-evidence.json supersedes open investigation.
Candidate family remains staged. Next normal-loader selection and continuous
first-interior/arbitrary-exit polish,then remaining death/rest/life/full-set
consistency. Full goal active;no export,commit or push.
[Handoff](../character/veld-swim-distress-family-coherent-v1/HANDOFF.md).

'''.encode('utf-8')+current)
print('Bound713 cardinal escape checks/64 negatives and two native regressions; updated status,pipeline,bible and both skills')
