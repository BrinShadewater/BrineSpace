"""Retain inspected East whole-source findings, without native/art acceptance."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-east-collapse-material-v1'
MARKER='## Marsh East whole-collapse source study — October 2, 2026'
LESSON='''
## Marsh East whole-collapse source study — October 2, 2026

Complete right-facing sixfigure source01 exec-a2764187-5722-4f22-9b24-cb9493e2cc87
retained with exact frozen prompt, ordered viewed refs and rawSHA. Primary selected
East idle/gait, old whole-motion guide only, originalEast standing master. Whole
cells/BOX/alpha128 at ONE scale .3202614379084967 calibrated to selected147occupied
height, metadataH148 unchanged. First slot exact selected idle32x147. Five complete
poses occupy37x140,52x115,83x91,109x53,171x41; sampled neutral30x147 versus selected
32x147. First dip7rows versus old11, provisional milder articulation. No per-pose
fit, anatomical patch, mirror or palette mapping. Source comparison inspected:
head/detail size closer to selected narrow East adult than old lowered guide;
warm ivory/sage body and complete connected side-view figures retained. Prone
length/boot material/camera and moving joins await actual native/family acceptance.

Lesson: animation canvas is per selected manifest, not per facing. East selected
idle/gait/death use184canvas p92/172 although East short-step uses256canvas. Guide
helper's initial256canvas assertion failed before producing guides; corrected by
whole translation to a common256preview p128/224, asserting no clipping. Never
scale the narrow side silhouette to rear width or change runtime canvas because
another action uses a larger registration envelope. Independently adapted native
fixture preserves actual north_step_draw_offset method name; there is no invented
east_step_draw_offset runtime API. Study fixture prepared but NOT RUN at this
milestone; no native acceptance claim, no normal catalog selection.

Review:character/marsh-east-collapse-material-v1/candidate-01/comparison.png.
Next: isolated actual East shutdown native study, white-fluid/rise preserving
complete bodies, full normal admission/checkpoint family, West and moving polish.
Full Marsh objective remains active and incomplete.
'''
def main():
    assessment={'normalAdmission':False,'sourceComparisonInspected':True,'guidesAndOriginalMasterInspected':True,'nativeReviewed':False,'sourceStatus':'Complete East candidate01 provisional; actual actor study prepared but not run.','observations':['Selected side neutral32x147, sampled ruler30x147. One occupied-height calibration; no forced width.','Milder first dip140rows, adult head/detail size closer to selected idle than old guide.','Warm ivory/sage complete right-facing anatomy retained. Final171x41 foreshortening, boots and moving joins remain open.']}
    (BASE/'candidate-01/visual-assessment.json').write_text(json.dumps(assessment,indent=2)+'\n')
    maintained=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md';installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md')
    assert maintained.read_bytes()==installed.read_bytes(),'skill mirrors drift'
    for path in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',maintained]:
        with path.open(encoding='utf-8') as stream:present=any(MARKER in line for line in stream)
        if not present:
            with path.open('a',encoding='utf-8') as stream:stream.write(LESSON)
    installed.write_bytes(maintained.read_bytes())
    print('Recorded East inspected whole-source study; native and normal admission pending.')
if __name__=='__main__':main()
