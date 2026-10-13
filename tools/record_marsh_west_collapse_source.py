"""Record independent West whole-source comparison, with native review pending."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-west-collapse-material-v1'
MARKER='## Marsh West independent whole-collapse sources — October 2, 2026'
LESSON='''
## Marsh West independent whole-collapse sources — October 2, 2026

Own viewed selected West idle/gait, old motion-only guide and originalWest master
freeze independent full source01 exec-0911fb3e-1f30-4630-894e-88a1915ee5e1.
West near temple/ear has NO implant; right-temple hardware is on far side. Never
reflect East artwork or add its visible near-side plate to West. Complete left-
facing adult figures preserve West hair/profile/gear and warm ivory/sage grade.
Source01 single neutral scale .34106728538283065 to selected147occupied rows,
declaredH148 retained. Five poses36x145,59x113,78x87,97x57,157x40; neutral32x147
versus selected31x147. Whole cells/BOX/alpha128/complete translations only.

First145row dip lost only2rows, leaving32row drop into113row crouch. Complete
twofigure correction exec-a3037173-b441-459b-9573-68599dd0b735 uses own selected
West refs without old pose pull. Candidate02 replaces ONLY complete first pose
with44x134; one neutral147 calibration scale .19367588932806323, sampled32x147
neutral, initial idle/fourlater poses byte-exact retained fromsource01. Actual
13row reduction is deeper than requested7; target140NOTforced by per-pose fit.
First-to-next21row reduction is more moderate, but timing/proportion family
acceptance remains open. Both raw original generations, frozen prompts/ordered
refs/SHAs and both candidates retained. No body patches, palette normalization
or pose-specific rescaling. Both whole comparison boards inspected; native actor
review not run at this source milestone, no normal catalog selection/admission.
Final157x40 anatomy/foreshortening remains provisional versus old167x42 guide;
do not stretch its horizontal rectangle to force old width.

Lesson: a generated correction request is not proof its anatomical target was
met. Record measured occupied silhouette and compare adjacent holds; preserve
one neutral scale and admit uncertainty instead of separately fitting the pose.
When adapting a packager, correct literal evidence metadata too: inherited146
neutral/125firstdip/135target labels were corrected to actual147/145/140 BEFORE
any native input interval. Calibrating code correctly while keeping stale recipe
text would misstate the evidence. Current candidate02 recipe agrees with scale.

Review:character/marsh-west-collapse-material-v1/candidate-02/comparison.png.
Next: isolated actual West shutdown study, matching independent coolant/rise,
normal full checkpoint/Continue family, then full-set master/style/proportion/
grade consistency and moving polish. Full Marsh goal remains incomplete.
'''
def main():
    assessment={'normalAdmission':False,'bothSourceComparisonsInspected':True,'guidesAndOriginalMasterInspected':True,'nativeReviewed':False,'selectedIdleOccupied':[31,147],'sampledNeutralOccupied':[32,147],'newFirstDipOccupied':[44,134],'observations':['Own West left-facing identity/bare near temple retained; not reflected East.','Complete intermediate first dip13row reduction versus source01 two; requested7 not forced. Later four whole poses and exact idle retained.','Warm ivory/sage whole adult bodies and ivory boot uppers; prone157x40 perspective/length and moving joins provisional.'],'next':'Actual isolated native actor study, matching white-fluid/rise and normal checkpoint family.'}
    (BASE/'candidate-02/visual-assessment.json').write_text(json.dumps(assessment,indent=2)+'\n')
    maintained=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md';installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md')
    assert maintained.read_bytes()==installed.read_bytes(),'skill mirrors drift'
    for path in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',maintained]:
        with path.open(encoding='utf-8') as stream:present=any(MARKER in line for line in stream)
        if not present:
            with path.open('a',encoding='utf-8') as stream:stream.write(LESSON)
    installed.write_bytes(maintained.read_bytes());print('Recorded West complete-source comparison; native/normal acceptance open.')
if __name__=='__main__':main()
