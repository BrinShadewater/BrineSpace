import json, os
from pathlib import Path
root=Path.cwd(); out=root/'character/james-meal-pickup-south-v1'
reports={}
for name in ['native-service-sides','native-front-regression']:
 report=json.loads((out/(name+'-validation.json')).read_text())
 assert report['exitCode']==0 and not report['timedOut'] and report['realProfileUnchanged']
 log=(out/(name+'.log')).read_text(encoding='utf8')
 assert 'ERROR:' not in log
 warnings=[line for line in log.splitlines() if 'WARNING:' in line]
 assert all('Loaded resource as image file' in line and 'res://brineui/hull-ui-v1/icons/' in line for line in warnings)
 report['fixtureRawIconWarnings']=len(warnings)
 evidence=json.loads((out/(name+'-evidence.json')).read_text())
 assert evidence['failures']==0
 reports[name]=evidence
assert len(reports['native-front-regression']['results'])==8
assert all(row['restorePixelsExact'] for row in reports['native-front-regression']['results'])
selection_path=out/'selection.json'; selection=json.loads(selection_path.read_text())
selection['status']='staged_source_fit_rear_service_context_unsupported_not_installed'
selection['counterContact']['reason']='Raised rear cabinet/backboard makes this a front-served counter. Explicit artwork service_facings now prevents the invalid rear fallback; South source remains uninstalled, pending an appropriate supported contact.'
selection['counterContact']['historicalNativeScope']='234 candidate checks and source captures describe the prior unrestricted rear fallback. That custom fixture no longer exposes a valid South service with current registration.'
selection['serviceSideCorrection']={'installed':True,'artwork':['sp-galley-2','sp-galley-4'],'allowedFacings':['north'],'geometryChecks':reports['native-service-sides']['checks'],'journeyChecks':reports['native-front-regression']['checks'],'actualJourneys':8,'scope':'Four default geometry rotations, blocked-front/saved-copy and legacy compatibility; eight normal seeded front service trips with fresh-scene disk Continue. Fixture caches exact raw new UI icon pixels pending concurrent editor import. No owner layout/art/collision change.'}
selection_path.write_text(json.dumps(selection,indent=2)+'\n',encoding='utf8')
lesson=f"""
## James galley artwork service sides - September 30, 2026

South source contact review exposed an invalid service fallback: sp-galley-2/4
have raised rear cabinets/backboards, so clear rear navigation is not access to
their serving surface. Registration now declares service_facings:[north]; the
shared provider honors it through saved copies while unregistered legacy counters
retain their existing two-side fallback. Defaults stay front-served in all four
quarters. No owner placement, artwork scale, collision, or James pose was altered.
{reports['native-service-sides']['checks']} geometry/contact and {reports['native-front-regression']['checks']} actual journey checks PASS, eight normal
meal/helmet inspection trips and eight fresh-scene disk Continues; scratch real
profile unchanged. Native front contact reviewed. Fixture caches exact raw newly
created UI icons until editor import; no UI source change. The full-trip log
contains only expected raw-icon export warnings from this fixture cache, with
zero engine errors; it is a source-native run, not an export check. Initial fixtures had
off-floor legacy assumptions and obsolete loop-only meal state assertions; failed
logs retained, checks corrected to installed full bowl/cup handoff timings.
The progressing full trip run exceeded the old240s harness; terminal rerun uses
480s and writes per-journey progress. No engine error is treated as a pass.
South source v3 remains staged: anatomy/material fit is valid, historical rear
contact is unsupported. It needs appropriate front-facing furniture/contact before
installation; do not warp arms, slide actor feet or remove blockers to force it.
Other South meal choreography, exterior cancellation stow/return, full-set motion
and owner visual acceptance remain open. Full James goal remains active.
"""
for target in ['docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md','C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md']:
 p=Path(target); before=p.read_bytes(); after=before+lesson.encode('utf8'); tmp=p.with_name(p.name+'.james-service.tmp');tmp.write_bytes(after);assert p.read_bytes()==before;os.replace(tmp,p)
p=Path('docs/CURRENT_STATUS.md'); before=p.read_bytes(); intro=(lesson+'\n[Handoff](JAMES_GALLEY_SERVICE_SIDES_HANDOFF_2026-09-30.md).\n\n').lstrip().encode('utf8');tmp=p.with_name(p.name+'.james-service.tmp');tmp.write_bytes(intro+before);assert p.read_bytes()==before;os.replace(tmp,p)
Path('docs/JAMES_GALLEY_SERVICE_SIDES_HANDOFF_2026-09-30.md').write_text("""# Project handoff

Updated:2026-09-30 - Project:Brine Space - Task:James galley service sides

## Objective and acceptance
Full James animation/master/motion consistency remains active. Resolve actual
contact before installing South acquisition; owner visual acceptance is separate.

## Accepted decisions and constraints
Master matte palette/proportions and permanent belt wrench. Whole authored poses,
one ruler. Preserve owner layouts, furniture scale/collisions and selected North
work. Clear rear floor does not permit reaching through raised counter backboards.

## Current state
rooms/station-props-v2/props.json: sp-galley-2/4 explicit North service facing.
scripts/crew_room_activity.gd: honor registered service sides, including copies;
legacy default remains two-sided. South candidate remains uninstalled. Historical
234-check rear-contact fixture is now an unsupported service context, retained
as evidence. Candidate selection, pipeline, bible and both skills updated.

## Verification
"""+'Defaults stay'+lesson.split('Defaults stay')[1].split('South source v3')[0]+"""
Native front contact reviewed. No owner profile changes or live native processes.
Reports/scripts/captures in character/james-meal-pickup-south-v1.

## Next action
Find appropriate supported South contact/artwork before new meal handoffs; keep
staged anatomy candidate. Next independent James polish: actual late exterior
recall captures, safe torch stow/empty return without delaying low-air response.
South cup/returns/interrupts, full mortality/cross-family motion and owner review
remain. No commit/export or full goal completion.
""",encoding='utf8')
print(json.dumps({k:v['checks'] for k,v in reports.items()}))
