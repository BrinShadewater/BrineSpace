from pathlib import Path
import json,re
R=Path(__file__).resolve().parents[2]
progress=R/'character/krusher-complete-animation-v1/progress.json'
d=json.loads(progress.read_text());v=d['visualReview']
for family in ['repair','torch','seated']:
 for gear in ['bare','helmet']:
  p=f'res://character/krusher-{family}-family-v2/{gear}-manifest.json'
  if p not in v['correctedCandidates']:v['correctedCandidates'].append(p)
v['remaining']='Correct helmet transitions, meals, cargo, rest, water, interruption, death and recovery families and shared joins before replacing the full candidate bank; refresh changed station contexts and finish full-library visual review.'
progress.write_text(json.dumps(d,indent=2)+'\n')
for family in ['repair','torch','seated']:
 P=R/f'character/krusher-{family}-family-v2'
 rev=json.loads((P/'revision.json').read_text());media=json.loads((P/'review/media.json').read_text())
 native=json.loads((P/'review/native/report.json').read_text());render=json.loads((P/'review/render/report.json').read_text())
 h=f'''# Project handoff

Updated: October 3, 2026. Project: BrineSpace. Task: Krusher {family} head fit.

## Objective and acceptance
Owner correction: human face too small inside helmet; bare side heads appear
disconnected. Full animation goal remains active/incomplete.

## Accepted decisions and constraints
Krusher Dom, System Administrator, AI & Robotics, James utility body, matte muted
cyan #527C80. Station test first; no normal roster installation. Existing independent
pitched heads retained. Exact previous Krusher body outside recorded head mask,
helmet alpha, whole root/state metadata and source clocks retained.

## Current state
New staged paired manifests/poses/head-fit masks in this folder. Builder:
character/krusher-head-fit-v2/revise_actions.py. Bare East/West existing heads moved
back 2/down 2 native pixels with collar, markings and cool foreground protected.
Helmet visible-direction faces enlarged within bounded original visor; North rear
unchanged. Standing endpoints reuse canonical-v5. {len(rev['records'])} unique poses,
{sum(q['changedPixels']>0 for q in rev['records'])} changed. No generated body pixels used.

## Verification
{rev['checks']} composition checks, 0 errors. Independent review {media['checks']}
checks, 0 errors, including 16 exact canonical standing joins. Native source admission
{native['checks']} checks/0 errors/{native['slots']} slots. Render fixture {render['checks']}
checks/0 errors/{len(render['captures'])} native snapshots. Each run scratch APPDATA;
2930 real non-log owner files unchanged, engine exit 0, no script/art errors.
All changed-head chronology boards and 8-view source sheet inspected; representative
native large and 92px views inspected. Paired replay preserves all {media['pairedSlots']}
source slots and original holds ({media['sourceSeconds']:.3f}s); source replay, not continuous
station recording. Does not establish furniture occlusion or new world lifecycle.

## Next action
Propagate fit through remaining helmet transition/meal/cargo/rest/water/interruption/
death/recovery packs and joins, then coherently refresh selected full bank and portable
package. Refresh changed station contexts; West service-loss return diagnostic and bare
water contexts remain open. Candidate list extended only; full bank still selects old
versions. No live process or blocker.
'''
 (P/'HANDOFF.md').write_text(h)
summary='''## Krusher action head-fit candidates - October 3, 2026

Goal active/incomplete. Repair-v2, torch-v2 and seated-v2 carry owner correction
through 96 paired states/1710 pose refs/972 unique outputs,648 changed. Existing
pitched identities retained; bare side heads back2/down2 with protected collars,
marks and foreground; visible helmet faces enlarged inside bounded visor. North
rear unchanged. Exact original root/state clocks;48 canonical-v5 standing joins.
1560composition/2511independent/12075native admission checks0. Native render10770
checks0/288snapshots. All runs scratch APPDATA;2930owner nonlog files unchanged.
Changed-head chronology boards,source sheets and native large/92px views reviewed.
Three paired all-source-hold replays: repair12.668s,torch12.468s,seated30.640s;
source replays,not continuous station capture or new world contact acceptance.
New packs listed in visualReview.correctedCandidates only. Full bank/package
remain old while helmet transitions/meals/cargo/rest/water/interruption/death/
recovery and joins need coherent correction. See new pack HANDOFF.md files.
No live process or blocker. West service-loss/bare water/world closeout remain.

'''
P=R/'character/krusher-head-fit-v2'
src=(R/'character/krusher-station-lifecycle-v1/update_moving_fit_status.ps1').read_text()
start=src.index("    $krusherHeader = @"+chr(39))+len("    $krusherHeader = @"+chr(39))
end=src.index('\n'+chr(39)+'@',start)
src=src[:start]+'\n'+summary+src[end:]
src=src.replace('CURRENT_STATUS.krusher-moving-fit.tmp','CURRENT_STATUS.krusher-actions-fit.tmp')
(P/'update_actions_status.ps1').write_text(src)
for path in [P/'HANDOFF.md',R/'character/krusher-complete-animation-v1/HANDOFF.md']:
 existing=path.read_text() if path.exists() else ''
 path.write_text(summary+'\n'+existing)
print(json.dumps({'correctedCandidateManifests':len(v['correctedCandidates']),'fullBankSelection':'unchanged; correction pending','handoffs':3}))
