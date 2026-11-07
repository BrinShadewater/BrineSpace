"""Freeze a whole source correction, preserving the phase-mismatched draft."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-south-run-material-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    sources=BASE/'sources';req=json.loads((sources/'run-01.request.json').read_text())
    correction='''CRITICAL MOTION CORRECTION: Six poses must use this exact SCREEN-SPACE phase order, with no duplicated held pose. In the following descriptions LEFT and RIGHT mean the viewer's left and right, not the character's. Bent forward forearm on one side pairs with forward leg on the OPPOSITE side. Phase0: viewer RIGHT knee raised/forward, viewer LEFT leg flexed back; LEFT forearm pumps forward across chest, RIGHT forearm back/down. Phase1: viewer LEFT leg reaches forward/down for landing, RIGHT leg folds back with raised trailing heel; RIGHT forearm forward, LEFT arm back/down. Phase2: viewer RIGHT forward leg extends farther DOWN after the raised-knee phase, LEFT leg trails flexed behind; LEFT forearm forward, RIGHT arm back/down. Phase3: viewer RIGHT knee rises forward again during push-off, LEFT trailing foot folds upward; LEFT forearm forward but a distinct recovery angle from0, RIGHT arm back. Phase4: viewer LEFT leg reaches down/forward, RIGHT leg folds back, RIGHT forearm forward and LEFT arm back/down, with a distinct compression/bounce from1. Phase5: viewer LEFT forward leg extends downward after its knee lift, RIGHT leg trails bent up; RIGHT forearm forward, LEFT arm back. The guide is an existing stylized cycle: preserve its exact six pose order and opposite arm/leg relationship rather than inventing a new left/right order. Distinguish phases through coherent knee/ankle/forearm progression and torso bounce; do not repeat the same lifted knee pose for every frame. Seven COMPLETE bodies, unchanged common anatomy scale, last figure neutral ruler.'''
    prompt=(sources/'run-01.prompt.txt').read_text().strip()+'\n\n'+correction
    path=sources/'run-02.prompt.txt';assert not path.exists();path.write_text(prompt+'\n',encoding='utf-8')
    for r in req['orderedReferences']:assert sha(ROOT/r['path'])==r['sha256']
    for key in ['generationId','originalGeneratedPath','rawSha256']:req.pop(key,None)
    req.update(status='frozen whole phase correction before generation',promptSha256=sha(path),priorDraft='candidate-01; retained unselected, phase mismatch in held review')
    (sources/'run-02.request.json').write_text(json.dumps(req,indent=2)+'\n')
    (BASE/'candidate-01/review.json').write_text(json.dumps({'normalAdmission':False,'heldSourceReviewed':True,'nativeMotionAcceptance':False,'findings':['Neutral59x147 versus selected58x147 improves scale join; sampling width is not exact anatomy proof.','Several opposite arm/leg phases differ from existing guide; successive poses insufficiently distinct.','Complete whole-source correction required before actor tests.'],'fullGoalComplete':False},indent=2)+'\n')
    print('Retained rejected motion draft; frozen exact whole-source correction.')
if __name__=='__main__':main()
