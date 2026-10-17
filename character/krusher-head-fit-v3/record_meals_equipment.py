from pathlib import Path
import json

R=Path(__file__).resolve().parents[2]
H=Path(__file__).resolve().parent
packs=['krusher-meal-family-v3','krusher-helmet-transition-v3','krusher-meal-service-v3']
details={}
for pack in packs:
    P=R/'character'/pack
    details[pack]={
        'independent':json.loads((P/'independent-validation.json').read_text()),
        'native':json.loads((P/'review/native/report.json').read_text()),
        'run':json.loads((P/'review/native/run-verification.json').read_text()),
        'media':json.loads((P/'review/preview.json').read_text())}
    assert not details[pack]['independent']['errors'] and not details[pack]['native']['errors']
    assert details[pack]['run']['engineExit']==0 and not details[pack]['run']['ownerFilesChanged']
    source=list((P/'review/source').glob('heads-*.png'))
    review={'sourceBoards':[str(p.relative_to(P)).replace('\\','/') for p in source],
            'allSourceContextsReviewed':True,
            'scope':'All source head/collar contexts visually inspected. Representative real-display prescribed poses inspected at large and game-size scale; not continuous station playback or owner acceptance.',
            'nativeViews':{'krusher-meal-family-v3':['eat-east-02.png','drink-west-03.png','drink-south-03.png'],
                           'krusher-helmet-transition-v3':['equip-helmet-east-05.png','equip-helmet-east-06.png','equip-helmet-east-11.png'],
                           'krusher-meal-service-v3':['pose-21.png','pose-22.png']}[pack]}
    (P/'review/visual-review.json').write_text(json.dumps(review,indent=2)+'\n')

handoff='''# Project handoff

Updated: October 3, 2026 · Project: Brine Space · Task: Krusher meal and equipment head correction

## Objective and acceptance
Complete Krusher's animation library with attached bare heads, clean brown hair and fuller helmet identity. Goal active/incomplete. Old v2 head construction remains owner rejected; these are revised candidates, not final owner or station acceptance.

## Accepted decisions and constraints
Krusher Dom / System Administrator / AI & Robotics. James utility suit with matte muted cyan #527C80. Original bodies, pixel density, clocks, aliases and pivots retained. Station test first; no normal crew or owner save installation.

## Current state
New meal-family-v3, helmet-transition-v3 and meal-service-v3:106states/612frame references/147unique records/104revised. Original v1 complete manifest bytes exact. Complete H3 head/neck masters replace bare portrait cutouts; original food/cup/hand foreground preserved. Helmet face fills original visor aperture, shell alpha exact. Equipment poses0/11 join canonical-v6 exactly; pose5 protects raised arm and held shell. Meal service reuses exact shared corrected meal drawings and retains indexed aliases;9South pickup poses use complete authored bowed/deep/fully-bowed heads, original lower body preserved.
New builtin raw generated-meal-pitch.png, exact meal-pitch-prompt.txt, extract_meal_pitch.py and meal-pitch-extraction.json record the two transparent pitched masters and hashes. No generated body/shell reused. Build_meals_equipment.py and validate_meals_equipment.py retain reproducible composition/proof.
Mobile overview:meal-equipment-head-fit-sheet.png. Per-pack full-body sheets, local HTML/MP4/ZIP previews generated from current corrected frames. Existing selected complete bank/package deliberately still old until all families form one coherent bank.

## Verification
Independent checks:meal726/equipment130/service765 (1621total0);49complete bare source/contact checks and100exact idle joins. Six source boards/all147contexts inspected, overview inspected, native large/small food/cup, helmet partial/equipped and deep South pickup views inspected.
Native real-display prescribed pose checks:meal641/48captures/7.50s;equipment172/24captures/7.07s;service3167/492state rows/39unique captures/8.19s.3980checks0,engine0/noerrors; scratch APPDATA and2930owner nonlog files unchanged each run. Their own .gd UID companions generated. Native selection of every source slot is not continuous world motion acceptance.
Source-hold native capture replays:meal18.00s/equipment4.383333s/service7.20s, each within one60fps frame of original summed holds. Service video covers8base states, all80indexed returns independently/native checked but not shown as separate video chapters. LFS PNG/MP4 filters confirmed; no commits. Residual yellow department shoulder trim remains pending palette pass.

## Next action
Remaining cargo/rest/water-cargo/interruption/death/recovery migration, rear/quarter identity and cyan shoulder audit. Rebuild coherent bank/package, retarget strict West cue hashes, diagnose staged West service-loss returns with actual per-frame state, and refresh changed actual station/bare-water/full-library checks. No live process, blocker or approval gate.
'''
(H/'MEALS_HANDOFF.md').write_text(handoff,encoding='utf-8')
for pack in packs:(R/'character'/pack/'HANDOFF.md').write_text(handoff,encoding='utf-8')
p=R/'character/krusher-complete-animation-v1/progress.json'
d=json.loads(p.read_text())
v=d['visualReview'];v['status']='head-construction-v3-water-canonical-inspection-actions-meals-equipment-partial'
v['remaining']='Remaining cargo/rest/water-cargo/interruption/death/recovery head migration; rear/quarter identity and residual yellow shoulder cyan palette pass; coherent full bank/package; strict West cues/service-loss and changed actual station/bare-water/full-library closeout.'
v['headConstructionV3']['mealsEquipment']={
    'manifests':['res://character/krusher-meal-family-v3/bare-manifest.json','res://character/krusher-meal-family-v3/helmet-manifest.json','res://character/krusher-helmet-transition-v3/manifest.json','res://character/krusher-meal-service-v3/bare-manifest.json'],
    'states':106,'frameReferences':612,'uniqueRecords':147,'changedUnique':104,
    'independentChecks':1621,'nativeChecks':3980,'bareSourceContactChecks':49,'exactIdleJoins':100,
    'sourceBoardsReviewed':6,'ownerFilesUnchangedEachRun':2930,
    'scope':'Partial revised candidates; original manifests/body motion and utensils protected. Prescribed native captures/source-hold replays only. Selected bank unchanged; full goal incomplete.',
    'handoff':'res://character/krusher-head-fit-v3/MEALS_HANDOFF.md'}
p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
original=(H/'update_actions_status.ps1').read_text()
start=original.index('    $krusherHeader = @'+chr(39))
end=original.index('\n'+chr(39)+'@',start)+3
header='''## Krusher meal, pickup and equipment complete-head candidates - October 3, 2026

Full animation goal active/incomplete. Meal-family-v3, helmet-transition-v3,
meal-service-v3:106states/612refs/147unique records/104revised. Original v1
whole manifests exact; complete H3 heads/necks, original food/cup/hand foreground,
helmet alpha and lower bodies preserved. New deeper South head masters retain
builtin raw/prompt/alpha extraction/hashes.1621independent checks0/49bare source
contacts/100exact idle joins. All147source contexts across6boards reviewed,
plus representative native large/small meals, partial/equipped helmet and pickup.
3980native checks0:meal641/48captures/7.50s,equipment172/24/7.07s,
service3167/492rows/39unique captures/8.19s. All engine0/noerrors/scratchAPPDATA;
2930owner nonlog files unchanged each interval. Source-hold native pose replays
18.00/4.383333/7.20s within1frame; not continuous station acceptance. Updated
mobile overview/full sheets/HTML/MP4/ZIP delivered. Selected full bank stays old.
Remaining cargo/rest/water-cargo/interruption/death/recovery head migration,
rear/quarter identity and residual yellow shoulder cyan pass, coherent bank,
strict West cues/service-loss and actual changed station/bare-water closeout.
Handoff:character/krusher-head-fit-v3/MEALS_HANDOFF.md. No approval gate/live job.

'''
new=original[:start]+'    $krusherHeader = @'+chr(39)+'\n'+header+chr(39)+'@'+original[end:]
new=new.replace('CURRENT_STATUS.krusher-head-construction-actions.tmp','CURRENT_STATUS.krusher-head-construction-meals.tmp')
(H/'update_meals_status.ps1').write_text(new,encoding='utf-8')
print(json.dumps({'handoff':'character/krusher-head-fit-v3/MEALS_HANDOFF.md','candidateBankChanged':False,'status':'active-incomplete'}))
