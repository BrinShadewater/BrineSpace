"""Record full normal South damage admission while keeping family art work open."""
from pathlib import Path
import json,runpy
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-south-injury-material-v1'
def append_once(path,marker,text):
    with path.open(encoding='utf-8') as stream:exists=any(marker in line for line in stream)
    if not exists:
        with path.open('a',encoding='utf-8') as stream:stream.write(text)

def main():
    review=BASE/'normal-review-v1'
    assessment={'allTwentyPairsInspected':True,'allThreeFacingFamilyBoardsInspected':True,'pairedBoards':[f'paired-{i}.png' for i in range(4)],'familyBoards':[f'family-{a}.png' for a in ['death-ground','injury-ground','injury-rise']],'artStatus':'Provisional selected South improved matte ivory/sage body and white fluid; whole-family moving/identity polish remains open.','observations':['All20original/Continued pairs show unobscured complete South figures, retained warm suit/boot uppers and exact source geometry.','Shutdown is dry; injury white fluid at glove/floor; floor handoff and recovery/normal idle remain visually coherent in held views.','North early collapse widths71,72,73 versus selected idle55; South65,63,69 versus idle58. Articulation can expand occupied width, so these are review targets, not automatic errors.','Older East/West/North head/shoulder/detail/grade joins differ from selected idle and new South in this common148 density sheet. Do not force equal perspective widths or normalize occupied height.','North final feet expose dark soles toward camera; dark sole-facing surfaces are legitimate. Judge boot uppers separately before any material repair.'],'pending':'Other-facing whole-body master/material review, remaining action coverage and full-set motion/consistency/polish. Browser/realtime motion, articulated contact and natural moving traffic not accepted by this checkpoint proof.'}
    (review/'visual-assessment.json').write_text(json.dumps(assessment,indent=2)+'\n')
    runpy.run_path(str(ROOT/'tools/publish_marsh_south_damage_normal.py'),run_name='__main__')
    evidence=json.loads((review/'verification.json').read_text())
    for folder in ['marsh-south-collapse-material-v1','marsh-south-injury-material-v1']:
        path=ROOT/'character'/folder/'selection.json';selection=json.loads(path.read_text())
        selection.update(status='normal provisional material source; full normal save/visible Continue verified; family art polish open',normalAdmission=True,fullGoalComplete=False,latestNormalEvidence={'path':'character/marsh-south-injury-material-v1/normal-review-v1/verification.json','checks':356,'fullCheckpoints':20,'freshVisibleTitleContinues':20,'exactOriginalContinuedPairs':20,'ownerFilesUnchanged':2931,'nativeVisualReview':True,'familyVisualReview':True})
        path.write_text(json.dumps(selection,indent=2)+'\n')
    lesson='''
## Marsh South normal damage family admission and full Continue — October 2, 2026

Normal ordered catalog appends exact South dry-collapse material01 and injury/
recovery material01 manifests. Three existing six180ms states now select improved
complete warm ivory/sage body; shutdown dry, injury separate white fluid. Initial
idle and recovery endpoint remain exact selected idle0. Art selection PROVISIONAL:
head/torso/prone foreshortening and moving/family polish remain open. Generation
raws/recipes unchanged; separate selection.json carries current admission/evidence.

356native checks pass:20full RunSave checkpoints,20fresh actual visible Title
Continues,40native/source captures,20exact original/restored pairs. Six shutdown
holds plus20secsettled, sixfall/sixrise, completion saved before first normal idle
draw. Whole actor/player snapshot/source/root parity, restored pause, finite
nonfatal completion/fresh idle0 and dead settled hold verified. Actual transmission
Continue acknowledged and overlay gone before capture; normal factory/catalog,
no study manifest injection or actor subclass. Normal costs/failures unchanged,
prescribed clear furnished site and peers/world paused.84bounded inputs stable;
2931owner non-log files unchanged under scratchAPPDATA,exit0/engine0. All20pairs
on four boards and all three four-facing family sheets inspected.

Test tests/test_marsh_south_damage_production.gd plus pairedUIDcc2shdamn7v70
registered companions/native lane with900s timeout; classification verified.
tests/index.json metadata was added after native launch and is explicitly outside
the84input runtime/source interval. No native repeat needed for that metadata.
Current catalog67body manifests,228selectedstates,1190slots are coverage counts,
not evidence of full master quality. Earlier staged249dry/404injury proofs retain
their dated scope; normal full Continue is new/current evidence.

Family review targets: North early collapse occupied71/72/73width versus selected
idle55; newSouth65/63/69versusidle58. Articulation widens silhouettes, so do not
assert width equality or rescale each pose to standing height. Older East/West/
North head/shoulder/detail/grade joins differ in these sheets; judge them against
their own accepted master and camera. North final feet face dark SOLES toward
camera; darkness there is legitimate, not evidence the ivory boot uppers need
whitening. Preserve perspective and sole material while repairing whole figures.
Held source/Continue pictures do not prove realtime/browser moving acceptance,
natural moving traffic, articulated limb contact or full-family style completion.

Review:character/marsh-south-injury-material-v1/normal-review-v1/index.html.
Next: North whole-collapse identity/density/material comparison and corrections,
then East/West damage family joins and remaining full-set consistency/polish.
Full Marsh objective stays active and incomplete.
'''
    marker='## Marsh South normal damage family admission and full Continue — October 2, 2026'
    maintained=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md'
    installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md')
    assert maintained.read_bytes()==installed.read_bytes(),'skill mirror drift; preserve both'
    for path in [ROOT/'docs/CURRENT_STATUS.md',ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',maintained]:append_once(path,marker,lesson)
    installed.write_bytes(maintained.read_bytes())
    handoff='''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: normal South damage family

## Objective and acceptance
Full master-matched Marsh animation set, then family consistency/polish. Active/
incomplete. This milestone admits improved South dry/injury/rise provisionally and
proves full normal disk/fresh visible Title Continue, not full family art quality.

## Accepted decisions and constraints
Complete warm ivory/sage body, dry shutdown, WHITE injury fluid, exact idle0
endpoints. No anatomical painting, per-pose height fits or palette normalization.
Black soles facing camera are legitimate; don't whiten them indiscriminately.
All probes scratchAPPDATA with owner before/after fingerprints. No exports/commits.

## Current state
character/marsh-v2/catalog.json adds two exact manifests for3six180ms states:
marsh-south-collapse-material-v1/candidate-01 and marsh-south-injury-material-v1/
candidate-01. Both rootselection.json normal/provisional with latest normal proof.
Normal-review-v1 under injury package has40captures/20pairs and3facing-family
sheets. New full-save native test+UIDcc2shdamn7v70; companions/native900s index
entry. Installer/fixture scaffold/fingerprint/publish/record tools added. Prior
grid_canvas injury cosmetic key reset remains; actor/save schema unchanged.
Pipeline/bible/current status/skill exact mirror updated by append; latest status
milestone near tail. Historical recipes/raw requests remain dated unselected study.

## Verification
356checks,20full checkpoints,20fresh actual visible TitleContinues,40native/source
views,20exact original/restored pairs. Whole actor/player/root/source equality;
pause, finite injury completion/fresh idle and20secdeath final hold.84bounded
inputs stable;2931ownerfiles unchanged,exit0/engine0. All4pairedboards/20pairs and
3four-facing family sheets inspected. Native test lane classified correctly.
Indexmetadata added after runtime launch, excluded from frozen interval. No
whole-family style, articulated limb contact, natural traffic or browser/realtime
motion acceptance. Catalog67manifests/228states/1190slots is coverage only.

## Next action
Compare North damage body against accepted North idle/master: early widths71–73
versus55idle and head/shoulder/detail joins are review targets, not proof by bounds.
Repair complete poses at common master density/camera, preserving black soles
where exposed. Then coherent North fluid/recovery, East/West joins, remaining
full coverage and whole-family polish. Keep full goal active.
'''
    (ROOT/'docs/MARSH_SOUTH_DAMAGE_NORMAL_HANDOFF_2026-10-02.md').write_text(handoff,encoding='utf-8')
    print('Recorded normal South damage family/Continue proof; skill mirrors exact; full goal remains active.')
if __name__=='__main__':main()
