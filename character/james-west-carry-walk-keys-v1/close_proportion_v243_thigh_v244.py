from pathlib import Path
import json,hashlib,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];audit=p/'proportion-audit-v243';candidate=p/'thigh-construction-phase0-v244';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
a=json.loads((audit/'inputs.json').read_bytes());assert all(sha(r/row['file'])==row['sha256'] for row in a['sources'])
d=json.loads((candidate/'inputs.json').read_bytes())
for group in ['sourceSha256','referenceSha256']:assert all(sha(r/f)==h for f,h in d[group].items())
assert sha(candidate/'prompt.txt')==d['promptSha256']
progress=json.loads((p/'material-repair-progress.json').read_bytes());assert all('lower-material-phase0-v234' in progress['states'][0]['candidateSources'][m]['file'] for m in ['bare','helmet'])
review=json.loads((candidate/'package-review.json').read_bytes());assert all(review[k] for k in ['alphaExact','outerOnePixelRingExact','outsideRectangleExact','pairedBodyBelow110Exact'])
review.update(disposition='unselected_style_foundation_pending_adjacent_pose_consistency',reviewedSourceBoards=['thigh-detail-review.png','paired-neighbor-review.png'],rawVisuallyReviewed=True,nativeIncluded=False,findings=['Original master quilt/seam construction better represented than rectangular panel/parallel stripe source.', '441 opaque interior pixels changed;65095 outside pixels exact. Same admission median54.21to62.50 and95th93.71to90.64: fabric brighter despite restrained peak highlights.', 'New muted yellow seam appears in phase0 but neighbouring selected poses lack it. Coordinate family construction and moving grade before selection. No silhouette/anatomical proportion correction or native acceptance.'])
(candidate/'package-review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
(candidate/'generation.json').write_text(json.dumps(dict(state='terminal_copied',execution='469baa88-698c-4358-a0a2-19367927193c',rawSha256=sha(candidate/'raw.png'),prompt='prompt.txt',referenceRoles=['edit-target','master-quilt-reference']),indent=2)+'\n',encoding='utf-8')
(audit/'review.json').write_text(json.dumps(dict(reviewedComparison='master-normal-carry-comparison.png',comparedPoses=8,browserObserved=dict(originalPlayingPhase=2,quarterPlayingPhase=37,pausedPhase=0,screenshot='browser-master-phase0.png',tab=8,url='http://127.0.0.1:8869/playback-review.html'),findings=['Raised arms/case and separated legs contribute to apparent width; standing whole silhouette is not an equal anatomical measurement.', 'Thigh panels and diagonal striping differ from original-master fine quilting and muted yellow seam; component construction discrepancy independent of body proportions.', 'Perspective/anatomical width remains unresolved; shared row guides are image coordinates, not manually identified joints. Browser sampled playing/paused states do not certify uninterrupted full motion.'],sourceAcceptance=False,continuousVisualMotionAcceptance=False,normalChanged=False,fullGoalComplete=False),indent=2)+'\n',encoding='utf-8')
section='''### James proportion and thigh construction comparison - October3,2026

V243 eight-pose fixed-coordinate board visually reviewed: original master,
normal carry0 and current carrying0/12/24/30/37/48. Raised arms/case and separated
legs contribute to wider silhouette; anatomy cannot be judged by standing bounds.
Visible thigh panels/diagonal striping differ from master's charcoal diamond quilt
and muted yellow seam. Perspective and anatomical width remain unresolved.
V242 browser observed original playing2, quarter playing37, verified paused0;
saved browser-master-phase0.png. Samples are not uninterrupted motion acceptance.

V244 phase0 thigh construction study generated with original-master quilt patch;
raw, protected/detail and paired48/0/1/2 boards reviewed.441 interior pixels change,
65095 outside pixels plus original alpha/rim/shared lower body exact. Quilting and
yellow seam closer to master, but cloth median54.21to62.50,95th93.71to90.64.
Candidate UNSELECTED, no native test: newly visible seam and fabric tone need
adjacent-pose construction consistency before loop admission. Current phase0V234
and normal runtime unchanged. Prompt/reference/source/output hashes frozen.
Lesson: keep suit construction fidelity separate from anatomical perspective;
whole-silhouette width includes equipment and stance. A master seam restored in
one pose creates temporal mismatch until adjacent poses are coordinated.
Next coordinate thigh quilt/seam across the carrying family, resolve actual
master anatomical/perspective differences, moving grade/contact and normal cargo
lifecycle, then all-family consistency/polish. Full objective active/incomplete.
Evidence: character/james-west-carry-walk-keys-v1/proportion-audit-v243/review.json;
character/james-west-carry-walk-keys-v1/thigh-construction-phase0-v244/package-review.json.
'''
guides=record_guides(r,section,'### James current full carrying cycle with opening and knee finish')
for folder in [audit,candidate]:(folder/'HANDOFF.md').write_text('# Project handoff\n\n'+section+'\nChanged: V243 comparisons/frozen inputs/browser screenshot; V244 refs/prompt/raw/protected paired study. Current selection unchanged. Checks: package invariants and frozen hashes; actual visual reviews recorded above.\n',encoding='utf-8')
with (p/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n'+section)
rasters=[f.relative_to(r).as_posix() for root in [audit,candidate] for f in root.glob('*.png')]
attributes=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(rasters)+'\0').encode(),cwd=r,capture_output=True,check=True).stdout.split(b'\0');assert all(attributes[i+2]==b'lfs' for i in range(0,len(attributes)-1,3))
print(json.dumps(dict(comparedPoses=8,study=244,selected=False,guides=guides,lfsRasters=len(rasters),goalComplete=False)))
