from pathlib import Path
import json
H=Path(__file__).resolve().parent;R=H.parents[1]
e=json.loads((H/'route-evidence-v1.json').read_text());assert e['routeChecks']==2403 and e['narrowChecks']==50
title='Veld staged cargo clearance and furnished turn routes — September 30, 2026'
body='''All 48 staged cargo/action/turn states (336 references) measured against the actual movement and action gates. Conservative candidate profile expands 24 bounds without shrinking old coverage; 778 envelope/hash checks pass. Actual five-room furnished graph: 24 turn cases pass 2403 checks, all phases and exact completion/arrival. One obstructed swept-turn route passes 50 safe cancellation/arrival checks. Engine errors and owner profile changes zero. Corrected east/west bare and north/south helmet room captures visually reviewed; legacy Bill preview removed from fixture. Initial narrow fixture selected a clear route and failed its cancellation expectation; archived and corrected to require obstructed swept clearance. [Evidence/handoff](../character/veld-swim-carry-turn-matrix-coherent-v1/CLEARANCE_HANDOFF.md). Full exterior/airlock/sample/return/unload journeys, interruptions/save and promotion remain; runtime unchanged and full goal active.
'''
for rel in ['docs/CURRENT_STATUS.md','docs/VELD_ANIMATION_CONTINUATION_2026-09-29.md']:
    p=R/rel;old=p.read_bytes()
    if title.encode() not in old:p.write_bytes(('## '+title+'\n\n'+body+'\n').encode()+old)
lesson='''
## Cargo clearance gates and route fixture ownership — September 30, 2026

Trace the real renderer gate before comparing envelopes: Veld cargo turns use
CrewLife .life cargo-turn bounds, while swimming movement uses .swim and sample
actions use .actions. Keep separate effective comparisons and conservative unions;
do not shrink older coverage to fit a candidate. A narrow cancellation probe must
select geometry where movement is clear but the swept turn envelope is obstructed;
omitting a safe-route filter does not prove obstruction. Remove legacy test-walker
cell/expedition state before native captures: inactive actors can still draw through
preview predicates. Preserve failed intervals, bind route proof to exact fixture,
profiles, manifests and frames, and review corrected captures. Forced flooding and
explicit candidates do not certify full expedition, airlock, traffic or save behavior.
Evidence: character/veld-swim-carry-turn-matrix-coherent-v1/CLEARANCE_HANDOFF.md.
'''
for p in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    if b'Cargo clearance gates and route fixture ownership' not in p.read_bytes():
        with p.open('ab') as out:out.write(lesson.encode())
print('Cargo clearance/route milestone and pipeline/bible/skill lessons recorded.')
