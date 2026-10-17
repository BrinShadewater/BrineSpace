from pathlib import Path
import json
R=Path(__file__).resolve().parents[2];P=R/'character/krusher-head-fit-v2'
items=[('meal-family',['bare-manifest.json','helmet-manifest.json']),('helmet-transition',['manifest.json']),('meal-service',['bare-manifest.json']),('cargo-family',['bare-manifest.json','helmet-manifest.json']),('cargo-settle-profile',['bare-manifest.json','helmet-manifest.json'])]
progress=R/'character/krusher-complete-animation-v1/progress.json';d=json.loads(progress.read_text());v=d['visualReview']
for family,names in items:
 for name in names:
  path=f'res://character/krusher-{family}-v2/{name}'
  if path not in v['correctedCandidates']:v['correctedCandidates'].append(path)
v['remaining']='Correct rest, water, water cargo turns, interruption, death and recovery families and shared joins; then coherently refresh full bank/package and strict West release hashes. Audit remaining quarter-view shoulder department patches (yellow remains in original reused cargo body), refresh changed station contexts, diagnose West service-loss and finish bare-water/world/full-library visual review.'
progress.write_text(json.dumps(d,indent=2)+'\n')
for family,names in items:
 Q=R/f'character/krusher-{family}-v2'
 if family=='cargo-settle-profile':
  details='Two West settle overrides retain the original root/default nearest filter and state clocks; complete whole paths now point to cargo-family-v2. No additional raster edits. Independent cargo audit and final native cargo render verify this override.'
 else:
  rev=json.loads((Q/'revision.json').read_text());audit=json.loads((Q/'independent-validation.json').read_text());native=json.loads((Q/'review/native/report.json').read_text());run=json.loads((Q/'review/native/run-verification.json').read_text())
  count=len(rev['records']);changed=sum(q['changedPixels']>0 for q in rev['records']);snapshots=native.get('uniqueNativeCaptures',len(native['captures']))
  details=f'{count} distinct recorded poses; {changed} changed. Independent {audit["checks"]} checks/0 errors, {audit["slots"]} source slots. Native {native["checks"]} checks/0 errors/{snapshots} screenshots, engine0/{run["seconds"]}s, no logged errors, scratch APPDATA, all {run["ownerFilesFingerprinted"]} owner non-log files unchanged.'
  if family=='meal-family':details+=' Sixteen exact padded helmet idle joins; all bare foreground utensils/hands and body rows141+ exact. Helmet meal actions remain sealed tablet inspection. Source board and actual native74px/large views reviewed. Native snapshot replay18s/all48paired slots.'
  elif family=='helmet-transition':details+=' Four exact padded canonical-v5 endpoints; original removal sourcePoseIndices exactly reverse the same revised fitting poses. Source12pose board, raised-hand and shell/face native74px/large views reviewed. Native snapshot replay4.383333s/all24slots.'
  elif family=='meal-service':details+=' All39 outputs byte-identical to v1; South/North heads require no side correction. All80 indexed returns end at canonical-v5 padded idle. Initial validator incorrectly pasted hidden transparent RGB; original alpha_composite padding now retained and joins pass. Service board reviewed; replay7.2s/eight service states, not all80 returns.'
  elif family=='cargo-family':details+=' Original full manifests/stride/flags/clocks exact.64join comparisons retain all12 exact old shared joins and52 original source variations. Native includes1920distance gait samples and24automatic turns;150 prescribed captures. Default nearest West settle verified. Four rear-quarter helmet apertures now use existing cardinal Krusher faces where source showed James; rejected warm-metal component candidate retained in review/rejected-rear-quarter-aperture. Final masks clipped to explicit original visor apertures; shell/alpha exact outside masks. All148source boards, revised aperture comparison and actual native74px/large samples reviewed. Paired source replay20.88s/all171paired slots. Release cue/save/world admission not yet rebound to these revised head hashes.'
 h=f'''# Project handoff

Updated: October 3, 2026. Project: BrineSpace. Task: Krusher {family} head fit.

## Objective and acceptance
Complete Krusher animations; owner correction: fuller human head in helmet and
connected bare side necks. Goal active/incomplete, staged source revision only.

## Accepted decisions and constraints
Krusher Dom, System Administrator, AI & Robotics, James utility body, matte muted
cyan #527C80. Station test first; normal roster unchanged. Existing authored head
sources reused. Original suit, hands/tools/cargo and clocks protected.

## Current state
New v2 manifests/poses/masks/review evidence in this folder. Builders in
character/krusher-head-fit-v2: revise_meals_helmet.py or revise_cargo.py;
independent validate_meals_helmet.py and validate_cargo.py. Profile override uses
whole paths. Source root/state metadata retained. Full bank/package not switched.

## Verification
{details}
Replays use prescribed native snapshots or source poses with original holds;
none are continuous station recordings or new world contact acceptance.

## Next action
Correct rest/water/water cargo/interruption/death/recovery and joins. Then rebind
the full bank/package and strict West release hashes, audit residual yellow
department shoulder patches in quarter cargo views, refresh changed station
contexts and finish West service-loss/bare-water/full-library visual closeout.
No live native process or blocker.
'''
 (Q/'HANDOFF.md').write_text(h)
summary='''## Krusher meals, equipment and dry cargo head fit - October 3, 2026

Goal active/incomplete. New meal-family-v2:96refs/60changed,468independent/641native
checks0,16exact padded helmet idle joins, foreground hands/cups/utensils protected.
Helmet-transition-v2:24refs/12unique revised,99independent/172native checks0,
four exact idle endpoints and original exact reversal. Meal-service-v2:492refs/
39unique outputs all byte-identical;779independent/3167native checks0,80idle joins.
Padding validator repaired to retain original alpha_composite semantics for hidden
transparent RGB; no anatomy change needed in South/North service heads.

Cargo-family-v2:342refs/148unique/106changed,367composition/1245independent checks0.
Final native4478checks0/150snapshots/9.45s, distance carrying/24automatic turns;
original manifests/strides/clocks and64joins (12exact/52original variations) retained.
West nearest settle overrides retargeted in cargo-settle-profile-v2. Four rear-quarter
helmets had visible James faces: now use existing Krusher cardinal face sources
clipped to registered visor apertures. Rejected warm-metal segmentation painted
hardware in two rear views; comparison/raw candidates retained, final masks reviewed.
Source boards and native large/74px samples reviewed. All native runs scratch
APPDATA,2930owner nonlog files unchanged/engine0/noerrors. Replays: meals18s,
equipment4.383333s,service7.2s,cargo20.88s; prescribed source/snapshot replays only.

New candidates listed only; full bank/package still old while rest/water/water
cargo/interruption/death/recovery and joins need correction. Strict West release
hashes must be rebound when selecting revised cargo. Residual yellow department
shoulder panels observed in reused quarter cargo body: final palette audit remains.
Changed world contexts, West service-loss diagnostic, bare-water and full-library
closeout remain. See new pack HANDOFFs. No live process or external blocker.

'''
for path in [P/'HANDOFF.md',R/'character/krusher-complete-animation-v1/HANDOFF.md']:
 previous=path.read_text() if path.exists() else '';path.write_text(summary+'\n'+previous)
src=(R/'character/krusher-station-lifecycle-v1/update_moving_fit_status.ps1').read_text();marker="    $krusherHeader = @"+chr(39);start=src.index(marker)+len(marker);end=src.index('\n'+chr(39)+'@',start)
src=(src[:start]+'\n'+summary+src[end:]).replace('CURRENT_STATUS.krusher-moving-fit.tmp','CURRENT_STATUS.krusher-meals-cargo-fit.tmp');(P/'update_meals_cargo_status.ps1').write_text(src)
(P/'padding-audit-repair.json').write_text(json.dumps({'initialAudit':'80 service returns differed from direct-paste canonical by hidden transparent RGB; displayed alpha unchanged','resolution':'Use the original alpha_composite registration, at36,52; all80 exact canonical-v5 joins pass. Original39 service outputs retained byte-for-byte.'},indent=2)+'\n')
print(json.dumps({'correctedCandidateManifests':len(v['correctedCandidates']),'fullBankSelection':'unchanged; remaining correction pending','handoffs':5}))
