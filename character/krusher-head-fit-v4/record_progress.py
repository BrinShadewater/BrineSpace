from pathlib import Path
import json
R=Path(__file__).resolve().parents[2];P=R/'character/krusher-complete-animation-v1/progress.json'
q=json.loads(P.read_text());q['headVisualRevision']['canonicalCandidate']={'bare':'res://character/krusher-james-canonical-v7/bare-manifest.json','helmet':'res://character/krusher-james-canonical-v7/helmet-manifest.json','states':24,'frameReferences':2122,'status':'native canonical candidate, unselected; complete propagation and selected fresh station contexts verified','review':'res://character/krusher-head-fit-v4/standing-review-mobile.png'}
s=json.loads((Path(__file__).resolve().parent/'scope-progress.json').read_text())
q['headVisualRevision']['scopedCandidates']={'scopeProgress':'res://character/krusher-head-fit-v4/scope-progress.json','states':s['coveredStates'],'requiredStates':s['requiredStates'],'remainingStates':len(s['remainingStateKeys']),'packs':s['scopePacks'],'status':'unselected repaired head candidates; all 586 states propagated, native loader and selected fresh station contexts verified','review':'res://character/krusher-head-fit-v4/mobile-head-review.png'}
P.write_text(json.dumps(q,indent=2)+'\n');print('Progress records unselected v4 scope; full-bank selections preserved.')
