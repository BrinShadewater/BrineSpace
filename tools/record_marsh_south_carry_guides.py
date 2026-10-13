"""Record reviewed whole carry guides, without claiming new authored motion."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
S=ROOT/'character/marsh-south-carry-material-v1/sources'
guide=json.loads((S/'guide-provenance.json').read_text())
for r in guide['primarySourceFrames']+guide['guideSourceFrames']+guide['guideArtifacts']+[guide['originalOwnMaster']]:
    assert hashlib.sha256((ROOT/r['path']).read_bytes()).hexdigest()==r['sha256']
(S/'guide-review.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'wholePrimaryAndCarryBoardsInspected':True,'originalOwnMasterInspected':True,'finding':'Old South carry head/upper body broader and denser than selected fitted58x147 idle; cargo correctly supported in both hands across waist. Preserve slate crate/two latches/hand occlusion while matching selected adult body/elevated camera/quiet warm grade.','limits':'Eight unchanged complete guide frames only, no newly authored carry pose/native acceptance. Cargo extent is not body calibration; legacy manifest missing canvas declarations is recorded separately from decoded image dimensions.'},indent=2)+'\n')
marker='## Marsh South carry own-master guides ready — October 2, 2026'
note=f'''
{marker}

Next family prepared after North03 normal eight-Continue acceptance. South carry
sources now have eight complete unchanged guides: selected idle0/1 and walk0/2
PRIMARY for adult body/camera/grade; old carry0..3 for cargo geometry and motion
ONLY. Exact frame/manifest metadata and source/guide/original-master SHAs frozen.
Whole common256,p128224 translations, nearest2x boards and selected single idle
nearest4x; no anatomy edits, clipping, mirroring, patches or recolour. Both boards
and own original South master inspected. Selected idle58x147,H148; old carry
combined silhouettes67x149/67x147/68x149/67x146. Cargo extent is not body scale.

Old carry head/upper body is broader and denser than the fitted selected body.
Preserve slate waist-held crate, two visible latches, supported hands and occlusion
while authoring adult proportions, elevated camera and quiet warm matte grade.
Guide helper initially expected legacy frameWidth declarations; corrected to
record actual decoded image dimensions and separate absent declarations, preserving
metadata uncertainty rather than inventing a manifest value. No Godot run needed
for unchanged reference preparation. No new carry source/runtime acceptance yet.

Changed: tools/prepare_marsh_south_carry_guides.py and this recorder;
character/marsh-south-carry-material-v1/sources guide boards/provenance/review.
Next author four complete alternating cargo-walk phases plus neutral standing
ruler against selected South body and original own master. Retain cargo support;
inspect entire body/crate joins before native validation. Carry turns/other held
families and full-set consistency/polish remain. Full goal active/incomplete.
'''
maintained=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md'
installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md')
assert maintained.read_bytes()==installed.read_bytes(),'skill mirror drift'
for p in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',maintained]:
    with p.open(encoding='utf-8') as stream:present=any(marker in line for line in stream)
    if not present:
        with p.open('a',encoding='utf-8') as stream:stream.write(note)
installed.write_bytes(maintained.read_bytes())
p=ROOT/'docs/MARSH_NORTH_RUN_NORMAL_HANDOFF_2026-10-02.md'
with p.open('a',encoding='utf-8') as stream:stream.write('\n## Next family reference preparation\nSouth carry own-master guides ready: eight unchanged complete references with\nexact SHAs/metadata, two boards and original master inspected. Old head/body\nbroader/denser; preserve slate waist crate/two latches and hand support. Selected\nSouth58x147 is PRIMARY; cargo extent is not body calibration. No new carry source\nor runtime acceptance. See character/marsh-south-carry-material-v1/sources.\n')
print('Recorded reviewed South carry guides and next whole-source task; skill mirrors equal; no carry admission.')
