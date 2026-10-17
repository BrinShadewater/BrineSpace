"""Record reviewed staged sources separately from normal installation."""
from pathlib import Path
import json,re
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-sofa-fall-south-staged-v1'
n=json.loads((O/'validation.json').read_text());v=json.loads((P/'native-review-evidence.json').read_text());q=json.loads((P/'package-checks.json').read_text())
reg=json.loads((R/'output/veld-sofa-fall-south-regressions-v1/validation.json').read_text());b=json.loads((R/'output/veld-bunk-current-death-regression-v1/validation.json').read_text())
assert n['passed'] and q['failures']==0 and len(v['boards'])==12 and b['passed']
assert all(x['passed'] for x in reg['results'] if x['test']!='test_veld_bunk_death.gd')
assert not reg['realProfileChanges'] and not reg['frozenInputChanges']
v['visualReview']='All twelve boards and paired source/master sheet inspected. Exact whole incoming pose retained; no upright reset; connected matte body slides/low-braces before relaxed floor poses. Head/shared native shell stays attached through pitch/tilt. Full sofa and floor contact visible in fixed extended native crop. Owner full motion acceptance remains open.'
(P/'native-review-evidence.json').write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
checks=int(re.search(r'VELD SOUTH SOFA FALL STAGED: (\d+) checks,0 failures',(O/'native.log').read_text())[1])
heading='## Veld South sofa reader fall authored and staged - October 2, 2026'
note=f'''
New character/veld-sofa-fall-south-v1 retains built-in raw/prompt/execution and
paired6pose manifests/12PNG. Exact current seated tablet entrance, three authored
slump/lean/low-brace interiors, two retained coherent South floor endpoints.
One H148/474ruler,256x272/p128,224,1.52s finite clock; pooled master skin/brown
hair/science-charcoal grade. Connected opaque components exclude generated
backdrop haze. Existing native25degree pitched shared shell fits new necks with
0/25/50degree screen tilts; no new shell design or per-pose body normalization.
61package/source/endpoint/binding checks and byte-identical rebuild pass.

CrewSpritePlayer and VeldDeathMotion add opt-in South reading-fall metadata,
strict current reader/gear/contact binding and saved sofa recipe validation.
Keep exact whole incoming source180ms, then supported slump. Sofa offset holds
through360ms and releases gradually by780ms; authored floor poses use natural
depth. Navigation foot fixed. Other families retain their selector paths.
No normal fall loader/ACTIVE_ASSETS admission, owner geometry/save-rule change.

Staged actual actor API: {checks}checks0fail/{n['seconds']}s/engine0/cleanlog,
6distinct reading entrances×2gears=12mortality contexts;48same-clock actor-file
restores,48malformed guards. Independent six-source clock and support/floor checks.
78targeted inputs/all2931owner non-log files unchanged under scratch APPDATA.
All12native boards/108source-native pairs and master sheet visually reviewed:
attached body/arms, matte canonical palette and shell through seat-to-floor fall.
Fixed extended crop shows complete floor body. This is prescribed default sofa,
paused world and actor-level mortality, not world roster/hazard/ordinary RunSave
future Continue. Earlier exact-boundary floating-point fixture failure retained;
samples1msinside phases fix the oracle, no production timing change.

Focused shared-controller regressions: water entrance and North partial lounge
pass; current normally selected held bunk also passes separately. Original
regression aggregate remains FAILED because historical bunk probe injects an
older death pack against current master sleeper and compares unequal silhouettes.
Retained original probe/report; new paired-UID current bunk probe removes that
old artwork injection. No weakening of stature/contact assertion. Initial8targeted
regression inputs/owner2931 unchanged; current bunk run records profile protection
separately and has no dependency-freeze claim.

Lesson: author supported collapse from the exact current seated body and reuse
native equipment, keeping body ruler/palette fixed across pitched interiors.
Separate source geometry, registered support and actor/world save evidence.
Historical staged probes must not mix former death bodies with current masters.
Next actual world mortality and ordinary disk/future Continue across reader poses,
then normal paired admission. Earlier/later South sit/rise falls need their own
source/context coverage; remaining families/world cadence/full-library polish
and owner acceptance remain open. Full Veld goal active/incomplete.
Review: character/veld-sofa-fall-south-v1/review.html.
'''
for target in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]:
    old=target.read_text(encoding='utf-8')
    if heading not in old:target.write_text(heading+'\n'+note+'\n'+old if target.name=='CURRENT_STATUS.md' else old.rstrip()+'\n\n'+heading+'\n'+note,encoding='utf-8')
(P/'HANDOFF.md').write_text(f'''# Project handoff

Updated: 2026-10-02 - Project: BrineSpace - Task: Veld South sofa reader fall

## Objective and acceptance
Full master-matched Veld set and cross-family polish active/incomplete. New South
reader fall is staged, visually reviewed; normal/world/save-future admission open.

## Accepted decisions and constraints
Exact current reader entrance, one H148 ruler, fixed matte master palette/native
shared shell. Capture whole live source/root/depth before die clears the stage.
Keep owner sofa layout, foot/navigation and ordinary save eligibility unchanged.

## Current state
Raw/prompt/provenance, build/manifests/12PNG/grade/registration/source+native review.
Guarded parser/selector/sofa snapshot/root/depth path in crew_sprite_player and
veld_death_motion. New paired-UID staged test/runner; no normal loader admission.
Current bunk regression preserves historical staged test in a separate interval.

## Verification
61package checks;{checks}staged native0fail/{n['seconds']}s;12actor deaths/
48actor-file restores/48malformed guards.78inputs/owner2931unchanged; all12boards
and108source-native pairs reviewed. Native full sofa/floor visibility, matte body
and pitched shell consistent. Existing water/North partial regressions pass;
current normally loaded bunk passes. Historical mixed-source bunk aggregate stays
failed and retained separately. No world roster/RunSave/future death proof yet.

## Next action
Use current staged pair for actual world deaths with paid survivor/normal save
eligibility, ordinary disk/fresh-main future equivalence, interrupted read-exit
cases. Then normal loader/registry admission, other South seated partial entrances
and all remaining family/material/perspective/ruler/motion consistency work.
''',encoding='utf-8')
print(json.dumps({'nativeChecks':checks,'sourceChecks':q['checks'],'boardsReviewed':12,'normalSelection':False,'lessonTargets':5}))
