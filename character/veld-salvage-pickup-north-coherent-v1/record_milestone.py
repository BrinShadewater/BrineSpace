from pathlib import Path
import json

H = Path(__file__).resolve().parent
R = H.parents[1]
for direction, count in [('west', 62), ('north', 64)]:
    folder = R / f'character/veld-salvage-pickup-{direction}-coherent-v1'
    package = json.loads((folder / 'packaging-checks.json').read_text(encoding='utf-8'))
    native = json.loads((folder / 'native-candidate-v1-checks.json').read_text(encoding='utf-8'))
    assert package['checks'] == count and package['failures'] == 0
    assert native['failures'] == 0 and native['real_profile_changed_files'] == [] and native['engine_errors'] == []

title = 'Veld west and north scientific actions staged — September30,2026'
body = '''Independent west/rear-north sample work and finite pickup now staged:48 new bare/helmet references, frozen cargo rulers/material curves and shared directional shells. Each36fit/249native PASS; west62/north64package PASS. Native/master boards and dark/light stow/grip samples reviewed; profiles unchanged. North probe continuity and source-density repairs preserve rejects; crown registration no longer derives scale from noisy hair thresholds. E/W/N now12staged action gearstates/72refs. Runtime/registry/clearance unchanged. South actions, actual controller phase-offset/recall joins, cargo turns, world envelopes/journeys, distress/recovery/death/life and full-set polish remain. [West handoff](../character/veld-salvage-pickup-west-coherent-v1/FAMILY_HANDOFF.md), [north handoff](../character/veld-salvage-pickup-north-coherent-v1/FAMILY_HANDOFF.md). Full goal active.
'''
for rel in ['docs/CURRENT_STATUS.md', 'docs/VELD_ANIMATION_CONTINUATION_2026-09-29.md']:
    q = R / rel
    old = q.read_bytes()
    if title.encode('utf-8') not in old:
        q.write_bytes(('## ' + title + '\n\n' + body + '\n').encode('utf-8') + old)

lesson = '''
## Veld sample source density and persistent props — September30,2026

Keep the specimen case visible and supported through every work/stow/lift cell;
inspect all later pickup phases for a probe that should already be stowed. Tool
removal alone is insufficient when an edited atlas changes density or shortens
legs. Prefer an edit of the reviewed work body that preserves atlas geometry,
then retain the accepted cargo anatomical ruler across paired action sources.
Register crown/axis separately from physical scale. Dark strands and sparse
coloured alpha noise defeated hair-threshold/run-width rulers in north trials;
compare skull, torso, thighs and calves to the master at one shared canvas ruler.
Retain rejected sources and fit reports; verify only the selected final pixels.
Use explicit UTF8 when adapting Python/HTML recipes on Windows; default cp1252
caused mojibake. Guard one-time scaffolds against replacing reviewed builders.
Exact endpoints do not prove arbitrary cosmetic work exit or recall continuity;
controller offsets and complete world routes remain a separate promotion gate.
Evidence: character/veld-salvage-pickup-north-coherent-v1/FAMILY_HANDOFF.md.
'''
for q in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md', R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md', R/'skills/brinespace-character-pipeline/references/crew-consistency.md', Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    if b'Veld sample source density and persistent props' not in q.read_bytes():
        with q.open('ab') as f:
            f.write(lesson.encode('utf-8'))
print('West/north milestone and maintained/installed lessons recorded.')
