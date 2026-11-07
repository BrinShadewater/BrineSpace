"""Record source-only South running milestone without motion acceptance."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageSequence
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-south-run-material-v1'
MARKER='## Marsh South run source scale and alternating-phase study — October 2, 2026'
LESSON='''
## Marsh South run source scale and alternating-phase study — October 2, 2026

Source-only study, all drafts unselected: character/marsh-south-run-material-v1.
Selected South idle/gait and original front master visually inspected, old run
used initially as motion-only guide. Selected idle58x147 occupied,184canvas,
pivot92/172, declaredH148. Old six100ms run loop retained in draft metadata;
normal runtime/catalog unchanged. Held source scale/material join improved,
but no family motion acceptance or native actor/save/Continue evidence here.

Three whole seven-figure sheets retain exact frozen prompts, ordered reference
SHAs, generation IDs, raw sources and originals. Each is packaged with ONE
neutral BOX scale, binaryalpha128, whole translations retaining neutral-relative
foot clearance, no per-pose fitting, limb patches, mirroring or palette mapping.
Candidate01 scale.26582278481012656, neutral59x147; candidate02 scale
.2832369942196532, neutral57x147; candidate03 scale.28053435114503816,
neutral61x147. Sampling widths differ from selected58: not exact anatomy proof.
All three held comparison boards inspected against idle and original master.

01 has repeated/incorrect arm-leg phases.02 repeats the same leading knee in
both contact and flight half strides.03 omits old pose guide from generation:
its opposite contact and raised-knee poses are distinguishable, but both passing
figures support the same screen-side foot. Do not admit a cycle solely because
it has six frames, matching neutral height and better material/proportion joins.
Prompted phase order is not evidence of generated phase order. Inspect actual
support foot, forward knee, opposite arm, compression and flight across wrap.

Separate complete passing04 plus neutral attempted missing viewer-RIGHT support:
generation exec-746cff84-13c0-4677-b551-1b8d73a18979 produced viewer-LEFT support.
Whole output retained passing-04-unselected, commonneutral scale
.21181556195965417, passing67x141/ruler59x147. Raw and packed comparison seen.
Do not mirror this to correct the side: asymmetric implant/harness identity and
whole-source constraints still apply. Unexecuted02 phase draft also preserved;
actual executed02 prompt was refined before its generation, exact SHA retained.

No Godot tests/probes launched; no owner save interaction. Source hash/metadata,
binaryalpha/noclip and six decodedAPNG frame equality checked for all3cycles.
SourceAPNG is a packaged animation, not actor/realtime/browser acceptance.
Next: use a clear correct screen-RIGHT support whole-pose reference to author a
complete missing passing pose plus neutral, review full alternating stride,
then native actual actor/cadence/root/contact/transition evidence with scratch
APPDATA and owner fingerprints. Full set has68unreviewed family boards in the
current held inventory pass; normal73manifests/228states/1190slots remain coverage
counts. Full Marsh master/style/camera/size/height/proportion/grade and polish
objective active and incomplete.
'''
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    checks=0
    for number in ['01','02','03']:
        sources=BASE/'sources';req=json.loads((sources/f'run-{number}.request.json').read_text());out=BASE/f'candidate-{number}';recipe=json.loads((out/'recipe.json').read_text());manifest=json.loads((out/'manifest.json').read_text())
        assert sha(sources/f'run-{number}.raw.png')==req['rawSha256'];assert sha(sources/f'run-{number}.prompt.txt')==req['promptSha256'];checks+=2
        for r in req['orderedReferences']+req['guideProvenance']['primarySourceFrames']+req['guideProvenance']['guideSourceFrames']:assert sha(ROOT/r['path'])==r['sha256'];checks+=1
        assert manifest['states'][0]['frameDurationsMs']==[100]*6 and manifest['states'][0]['loop'] and manifest['standingHeight']==148;checks+=1
        for r in recipe['records']:
            p=out/r['file'];assert sha(p)==r['sha256'];a=np.array(Image.open(p).convert('RGBA'));assert set(np.unique(a[:,:,3])).issubset({0,255});assert not a[0,:,3].any() and not a[-1,:,3].any() and not a[:,0,3].any() and not a[:,-1,3].any();checks+=3
        decoded=[f.convert('RGBA').copy() for f in ImageSequence.Iterator(Image.open(out/'source-motion.apng'))];assert len(decoded)==6
        for i,f in enumerate(decoded):assert np.array_equal(np.array(f),np.array(Image.open(out/f'{i:03d}.png').convert('RGBA')));checks+=1
    assessment={'normalAdmission':False,'fullGoalComplete':False,'heldSourceReviewed':True,'nativeMotionAcceptance':False,'findings':['Opposite contact and flight poses now distinct.','Passing phases1/4 both use viewer-LEFT support: missing viewer-RIGHT support phase.','Head/torso/material join is promising but neutral61x147 vs selected58x147 is not exact anatomy proof.','Do not admit or mirror/patch; review corrected full cycle before native actor tests.']}
    (BASE/'candidate-03/review.json').write_text(json.dumps(assessment,indent=2)+'\n')
    (BASE/'study-validation.json').write_text(json.dumps({'sourceChecks':checks,'cycles':3,'decodedApngFrames':18,'normalAdmission':False,'godotTestsRun':False,'ownerSaveInteraction':False,'fullGoalComplete':False},indent=2)+'\n')
    maintained=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md';installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md');assert maintained.read_bytes()==installed.read_bytes(),'skill mirrors drift'
    for path in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',maintained]:
        with path.open(encoding='utf-8') as stream:present=any(MARKER in line for line in stream)
        if not present:
            with path.open('a',encoding='utf-8') as stream:stream.write(LESSON)
    installed.write_bytes(maintained.read_bytes())
    handoff='''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Marsh South run source study

## Objective and acceptance
Full master-matched animation set/consistency/polish remains active/incomplete.
South run source scale improved; no draft passed coherent stride acceptance.

## Accepted decisions and constraints
Whole authored bodies, selected idle147occupied neutral calibration/H148metadata,
one BOX scale per authored source sheet, no per-pose fit, mirror, anatomy patch or
recolour. Preserve asymmetric identity. Six100ms loop timing retained in drafts.

## Current state
character/marsh-south-run-material-v1 has frozen source01/02/03 requests/raws,
candidate01/02/03 complete six-frame184/p92,172 manifests, rulers/comparison/APNGs,
and rejected complete passing04. New tools prepare guides/requests, build/review
and record evidence. Pipeline/bible/status/installed skill mirror appended.
Normal catalog/runtime unchanged; rejected sources preserved with exact provenance.

## Verification
All3comparison boards plus passing04 inspected against selected/original master.
Source SHA/metadata/binaryalpha/noclip and18decodedAPNG frames match. No Godot
tests/probes, owner save interaction, actor/cadence/contact/moving acceptance.
01/02 repeated phases;03 has distinct opposite contact/flight but both passing
poses support viewer LEFT. Separate passing04 also used wrong support side.

## Next action
Provide clear correct viewer-RIGHT support whole-pose reference for a complete
passing replacement + neutral, then review full alternating stride before native
actual actor/source/cadence/root/contact/transition checks in scratchAPPDATA.
Continue68remaining held family boards and full-set consistency/motion polish.
'''
    (ROOT/'docs/MARSH_SOUTH_RUN_SOURCE_HANDOFF_2026-10-02.md').write_text(handoff,encoding='utf-8')
    print(json.dumps({'sourceChecks':checks,'cycles':3,'decodedApngFrames':18,'normalAdmission':False,'docsRecorded':True,'skillMirrorExact':maintained.read_bytes()==installed.read_bytes()}))
if __name__=='__main__':main()
