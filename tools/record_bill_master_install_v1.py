"""Record reviewed normal installation without rewriting historical source manifests."""
from pathlib import Path
import ast,hashlib,json,subprocess
R=Path(__file__).resolve().parents[1];D=R/'character/bill-master-install-v1';T=R/'character/bill-carry-turn-east-seams-v1'
q=json.loads((D/'registry.json').read_text());turn=json.loads((T/'review.json').read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert q['normalAdmission'] and all(v['passed'] for v in q['nativeValidation'].values()) and turn['nativeValidation']['passed']
assert all(sha(R/p)==h for p,h in turn['protectedInputs'].items())
names=['build_bill_carry_turn_east_seams_v1.py','prepare_bill_carry_turn_east_seams_native_v1.py','run_bill_carry_turn_east_seams_native_v1.py','publish_bill_carry_turn_east_seams_v1.py','prepare_bill_master_install_native_v1.py','run_bill_master_install_native_v1.py','run_bill_master_install_native_v2.py','validate_bill_master_install_native_v2.py','prepare_bill_master_title_native_v1.py','run_bill_master_title_native_v1.py','publish_bill_master_install_v1.py','record_bill_master_install_v1.py']
for name in names:ast.parse((R/'tools'/name).read_text(encoding='utf-8'))
uids=['review_bill_carry_turn_east_seams_native_v1','review_bill_master_install_native_v1','review_bill_master_install_native_v2','review_bill_master_title_native_v1']
for name in uids:
 assert (R/f'tools/{name}.gd').is_file()
 uid=(R/f'tools/{name}.gd.uid').read_text().strip();assert sum(p.read_text().strip()==uid for p in (R/'tools').glob('*.gd.uid'))==1
pngs=[p.relative_to(R).as_posix() for folder in [D,T] for p in folder.rglob('*.png')]
result=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(pngs)+'\0').encode(),capture_output=True,check=True,cwd=R);items=result.stdout.decode().split('\0');assert all(items[i+2]=='lfs' for i in range(0,len(items)-1,3))
q.update(visualReviewed=True,visualReview='All nine installation/Title boards reviewed; matching before/after submitted sprites. Paid construction and workshop handoffs retain matte suit, warmer face and readable panel detail. Existing other-direction poses and equipment remain visibly older sources. Sampled captures, not continuous full-game recording.',pythonSyntax=len(names),pairedUniqueUIDs=len(uids),pngLFS=len(pngs),browserProofSHA256=sha(D/'browser-installed.png'))
(D/'registry.json').write_text(json.dumps(q,indent=2)+'\n')
turn.update(normalAdmission=True,visualReviewed=True,findings='Seven native first/middle/last boards reviewed at actual station pixels. Exact whole repaired East pickup10 replaces seven held aliases; 50 existing turn slots and all original timings/geometry retained. Existing intermediate detail/directional shading judged acceptable at station scale. Source comparison boards retained; not all enlarged comparison boards inspected.',installedRegistry='res://character/bill-master-install-v1/registry.json')
(T/'review.json').write_text(json.dumps(turn,indent=2)+'\n')
html=(T/'index.html').read_text();html=html.replace('No new artwork or normal installation.','No new artwork. These seven programs are now selected in the normal bare source bank; <a href="../bill-master-install-v1/">installation and Continue evidence</a>.');(T/'index.html').write_text(html,encoding='utf-8')
note=f'''\n\n## Bill East master family installed — October 4, 2026

Normal selected source version: bill-east-master-family-v1-cardinal-arrival3.
scripts/bill_carry_player.gd loads ten whole-path master manifests for bare East
idle, walk, reach, run, carry, weld, draw/stow, pickup/unload and carry entry,
plus seven shared East turn programs: 18 states/238 unique logical slots,
310 manifest references (72 identical idle holds repeated by the reach bank).
Per-East stride overrides only; three previous source versions retain 22 source
keys with their clocks/strides and both gear rows. Existing helmet and other
sources remain exact. bill_carry_npc default uses new binding; grid_canvas
refreshes retained bare source tables when Continue restores a different bank,
guarded to the selected production player. No mid-pose source migration.

character/bill-carry-turn-east-seams-v1 reuses the repaired whole pickup10 in seven
held alias slots across seven existing programs; 50 intermediate slots untouched,
original 800/1600ms programs/geometry retained. No new art, local grade, stamps or
body transforms. 28 APNGs/228 decoded exact sources and clocks; 22 protected inputs
unchanged. Native 5,040 checks/0, all57 slots on seven prescribed legal segments,
57 retained room/source pairs,37.87s,5,348inputs and2,936owner non-log files exact.
Seven native first/middle/last boards visually reviewed at actual station pixels;
existing intermediate detail/directional shade acceptable at this scale.

Normal installation NativeV2:4,286/0; all310 manifest references exact RGBA,
four real disk carry-entry resumes (legacy/current × bare/helmet) with30 exact
future updates each, paid construction completes all18 draw/weld/stow slots,
workshop pickup visits all11 slots then generated route/arrival/service completion.
44 retained room/source pairs,40.13s,5,807inputs unchanged,2,936owner unchanged.
Fresh normal Title/main scenes in same native process:101/0, two actual Continue
and loading buttons for bare legacy/current saved entry; source/physical root/clock
and pause exact plus30 deterministic future steps each.4 retained pairs,48.59s,
5,807inputs and2,936owner files unchanged. All successful engines0/clean, scratch
APPDATA only. Nine installation/Title boards and published browser proof reviewed.

Historical fixture failures retained: installV1 used nonexistent Save.valid;
stopped after91.46s, owner unchanged, concurrent grid_canvas edit preserved.
InstallV2 native passed but wrapper expected238 rather than310 references;
validation-corrected.json explicitly corrects classification, no test rerun for
that count. Future wrapper corrected. Final Title run includes selected-player
guard and unchanged normal source code. {len(names)} Python syntax checks,
{len(uids)} paired unique native UIDs, {len(pngs)} new preview/evidence PNGs LFS.

Registry/proof: character/bill-master-install-v1. Historical master manifests keep
their authoring statuses; this normal selection registry governs installation.
This is a scoped East installation milestone, not blanket full Bill acceptance.
Other direction/equipment/life/water banks retain selections; natural unforced
goal choice and a new exported build were not tested here. Next: reconcile final
coverage against this installed registry and existing recorded evidence; address
only demonstrated remaining defects, then concise closeout. Do not restart source
repairs or expand optional polish. Owner wants wrap soon. No commit/export requested.
http://127.0.0.1:8791/character/bill-master-install-v1/.
'''
paths=[R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']
for base in [R/'skills/brinespace-character-pipeline',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline')]:paths.extend([base/'references/crew-consistency.md',base/'references/source-density.md'])
for p in paths:
 with p.open('a',encoding='utf-8') as f:f.write(note)
(D/'HANDOFF.md').write_text('''# Project handoff

Updated: October 4, 2026 · Project: Brine Space · Task: Bill East installation

## Objective and acceptance
Wrap Bill animation work soon. Reviewed bare East master family now installed;
scoped integration milestone, no blanket owner acceptance of all Bill states.

## Accepted decisions and constraints
Whole figure sources and exact whole alias reuse. Preserve older checkpoint
source versions, equipment/other directions and concurrent renderer/room changes.
Reversible work authorized; no commit/export. All native work scratch APPDATA.

## Current state
scripts/bill_carry_player.gd, bill_carry_npc.gd, grid_canvas.gd: ten source banks,
new default binding, 22 versioned keys/three legacy epochs, retained draw sync.
character/bill-carry-turn-east-seams-v1: seven repaired whole held aliases and
50 unchanged intermediate slots. character/bill-master-install-v1: registry,
48 retained source/room pairs, nine boards and browser proof. Twelve tools/four
paired native UIDs. All eight maintained records updated.

## Verification
Turns5,040/0 (57slots); normal install4,286/0 (310refs/238unique slots,
4disk resumes, real paid/workshop jobs); fresh normal Title scenes101/0
(2bare source versions, pause,30future steps each). Successful native runs
engine0/clean, all frozen inputs and2,936owner files unchanged. Visual native
turn and install/Title boards reviewed. Wrapper count correction documented;
failed installV1 fixture retained separately. Existing detail variance remains.

## Next action
Final coverage/closeout against registry and existing accepted evidence. Other
direction/equipment/life/water sources retain selections; not a new blanket audit,
unforced job-choice proof or export. Repair only demonstrated defects; avoid
rebuilding completed art or expanding optional polish.
''',encoding='utf-8')
print(json.dumps({'maintainedRecords':8,'pythonSyntax':len(names),'pairedUIDs':len(uids),'pngLFS':len(pngs),'normalAdmission':True,'installationChecks':4387,'turnChecks':5040}))
