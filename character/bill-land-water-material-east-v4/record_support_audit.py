from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parent.parent
f=P/'build_contact_player.py';t=f.read_text(encoding='utf-8');t=t.replace('Green dashed line: source ground pivot.','Green dashed line: dry walking registration pivot.').replace('These are registration guides; contact and buoyancy still require visual judgment.','These are registration guides, not a floor-height plane. Bill uses a 2D navigation anchor; swimming silhouettes may extend below the dry pivot. Actual room obstacle clearance is checked separately.').replace('New-bank save/resume and normal gameplay integration remain pending.','All 120 active captured silhouettes fit the admitted collision outline. Smoothness, new-bank save/resume and normal gameplay integration remain pending.');f.write_text(t,encoding='utf-8')
note='''## Bill East planar support-model audit — October 2, 2026

Resolved previous contact-player concern from authoritative actor/draw code:
Bill foot is a2D navigation/depth anchor, not vertical floor height. Textures draw
at actor minus source pivot times65.28/H148; swimming keeps same physical root
with source-specific pose registration. Room swim checks sweep silhouette bounds
against furniture and floor outlines in plan. No separate elevation/buoyancy axis
exists. A boot below the dry source pivot is not proof of floor penetration;
do not translate whole swim poses solely to satisfy a walking guide.

New reproducible build_support_audit.py/support-audit.json binds retained record
SHA and all190 exact source/native capture rows to source alpha extents and actual
entry/exit admission events. All120active captured silhouettes lie inside the
admitted union (1e-4float tolerance, no pixel tolerance). Existing3487check native
interval rechecks union against actual geometry while moving and completes both
finite bridges. This strengthens planar clearance evidence; no new native run,
vertical support simulation or continuous visual acceptance claimed. Contact
player label corrected from ground line to dry walking registration guide.

Next current-V5-bank save/resume/Title proof and visual motion refinement, then
other cardinal bridges/guarded normal integration/full-family master polish.
Full Bill goal active/incomplete. Preserve current source pose/anatomy unchanged.
Audit:character/bill-land-water-material-east-v4/support-audit.json.

'''
heading=note.splitlines()[0]
for rel in ['docs/CURRENT_STATUS.md','docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']:
 p=R/rel;t=p.read_text(encoding='utf-8')
 if heading not in t:p.write_text(note+t,encoding='utf-8')
for p in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 t=p.read_text(encoding='utf-8')
 if heading not in t:p.write_text(t+'\n'+note,encoding='utf-8')
p=P/'HANDOFF.md';t=p.read_text(encoding='utf-8');t+='\n## Planar support audit resolution\nActor foot is2D navigation/depth anchor, not elevation. Dry pivot crossing alone\nis not clipping. New support audit binds190capture rows;120active silhouettes\nfit actual admitted union. Existing native interval continuously rechecked actual\nplanar obstacles. No vertical buoyancy simulation/new native run/continuous visual\nacceptance. Keep artwork unchanged; player guide relabeled. Next current-V5-bank\ncheckpoint/Title proof and other cardinal bridges/full-family polish.\n';p.write_text(t,encoding='utf-8')
e=json.loads((P/'review.json').read_text(encoding='utf-8'));e['planarSupportAudit']={'presentations':190,'activeEnvelopeCoverage':120,'supportModel':'2D navigation/depth anchor, no elevation axis','sourceChanged':False,'newNativeRun':False};e['contactPlayer']['contactAcceptance']='Dry pivot is not floor-height plane. All120 active capture extents inside actual admitted collision union. Full visual motion acceptance pending.';(P/'review.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
print('Recorded planar support resolution in guidance and handoff; source art unchanged.')
