from pathlib import Path
import json,hashlib
H=Path(__file__).resolve().parent;R=H.parents[1];O=R/'output/veld-work-pickup-phase-boundaries-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
v=json.loads((O/'validation.json').read_text(encoding='utf-8'));t=json.loads((O/'timeline.json').read_text(encoding='utf-8'))
assert v['passed'] and v['realProfileChanges']==[] and len(t)==96
distinct={}
for d in ['east','west','north','south']:
    for g in ['bare','helmet']:
        rows=[x for x in t if x['name'].startswith(d+' '+g+' nominal')]
        values={x['exits'][0]['previousPixelHash'] for x in rows}
        assert len(values)==6,(d,g,'offsets failed to exercise six work poses',len(values))
        assert all(x['exits'][1]['previousPixelHash']==x['exits'][1]['nextPixelHash'] for x in rows)
        distinct[d+' '+g]=len(values)
bound={str(p.relative_to(R)):sha(p) for p in [R/'tests/test_veld_work_pickup_phase_boundaries.gd',R/'scripts/crew_expedition.gd',R/'scripts/crew_sprite_player.gd',H/'bare-manifest.json',H/'helmet-manifest.json',H/'family-checks.json',O/'native.log',O/'timeline.json',O/'validation.json']}
(H/'controller-evidence.json').write_text(json.dumps(dict(installed=False,validation=v,routes=96,distinctNominalWorkExits=distinct,exactNominalPickupCargoBoundaries=True,hashes=bound,scope='Actual Veld controller/grid candidate action/cargo phase rules and inherited return turns; not visual acceptance or complete world routes'),indent=2)+'\n',encoding='utf-8')
title='Veld sample action family and genuine phase offsets verified — September30,2026'
body='''All4direction bare/helmet work/pickup consolidated:16states/96exact refs,104source checks PASS. Corrected inherited probe clock setup now exercises6distinct work exit poses per direction/gear;96actual controller scenarios PASS, exact nominal pickup/cargo boundaries and recall extraction rules, owner files unchanged. Earlier clock-shift-only evidence archived and superseded. Exit comparison boards reviewed; runtime unchanged. Cargo turn art/world envelopes/full journeys remain before promotion; distress/recovery/death/life/full-set polish remain. [Handoff](../character/veld-salvage-pickup-family-coherent-v1/FAMILY_HANDOFF.md). Full Veld goal active.
'''
for rel in ['docs/CURRENT_STATUS.md','docs/VELD_ANIMATION_CONTINUATION_2026-09-29.md']:
    q=R/rel;old=q.read_bytes()
    if title.encode() not in old:q.write_bytes(('## '+title+'\n\n'+body+'\n').encode()+old)
lesson='''
## Actual cosmetic work offsets — September30,2026

A shifted initial visual clock does not create distinct animation phases:
CrewSpritePlayer resets the clip phase on first entry. Start the clip first,
then advance its cosmetic clock to the chosen offset. Assert each initial pose
and six distinct exit pixel hashes, not only six differently labelled scenarios.
Keep the rejected fixture run, bind corrected evidence to fixture/frame hashes,
and distinguish actual controller rules from visual smoothness and world routes.
Veld controller evidence: character/veld-salvage-pickup-family-coherent-v1/.
'''
for q in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    if b'Actual cosmetic work offsets' not in q.read_bytes():
        with q.open('ab') as f:f.write(lesson.encode())
print('96 real controller scenarios bound;6distinct exits in each of8direction/gear groups; nominal pickup/cargo exact.')
