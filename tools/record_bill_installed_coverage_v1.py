"""Maintain current coverage milestone and a bounded next task."""
from pathlib import Path
import ast,hashlib,json,subprocess
R=Path(__file__).resolve().parents[1];D=R/'character/bill-installed-coverage-2026-10-04'
q=json.loads((D/'review.json').read_text());v=q['nativeSourceValidation'];assert v['passed']
ast.parse(Path(__file__).read_text());q['browserProofSHA256']=hashlib.sha256((D/'browser-coverage.png').read_bytes()).hexdigest()
pngs=[p.relative_to(R).as_posix() for p in D.glob('*.png')];result=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(pngs)+'\0').encode(),capture_output=True,check=True,cwd=R);items=result.stdout.decode().split('\0');assert all(items[i+2]=='lfs' for i in range(0,len(items)-1,3))
q.update(pythonSyntax=8,pairedUniqueUIDs=2,pngLFS=len(pngs));(D/'review.json').write_text(json.dumps(q,indent=2)+'\n')
note=f'''\n\n## Bill installed coverage reconciliation — October 4, 2026

character/bill-installed-coverage-2026-10-04 is the current full selected source
inventory. Actual normal grid loader plus inherited production carry banks:
216 bare/198 helmet states,1,860/1,716 slots,3,128 unique selected source paths.
Older literal-only audit missed inherited carry-start states and latest overrides;
historical212/194 counts remain evidence for their old resolution scope.
Current resolver appends36 inherited manifest loads in actual selection order.
Actual materialized normal-player validation agrees for every key/slot, raw RGBA,
authored timing/loop and declared density:11,974checks/0,11.56s,engine0/clean,
4,974 frozen inputs unchanged,2,936owner non-log files unchanged, scratchAPPDATA.
Headless source audit only, not new motion/world/Continue acceptance. Existing
normal East jobs and Continue evidence stays in bill-master-install-v1 registry.

Explicit131 required keys per gear (ordinary actions,cardinal life/basic water,
cargo starts and all12carry-turn programs,specialEastbunk) are all present.
18 theoretical missing bunk direction/gear combinations are intentional:
major_bill_npc.begin_life_station forcesEast; generic lie/sleep/get-up remains
cardinal. Eight retained helmet eat/drink keys are not a feeding-art repair task:
crew_life.pose selectsinspect for a sealed helmet. Three older specialEastbunk
keys per gear remain selected. No inferred replacement count from folder age.

Eight refreshed representative whole-source boards/80samples actually inspected
at common physicalH148/p160224. All3,311 comparison inputs exact at publication;
North authority remains prepared rear stance, not untouched original master.
Installed bareEast idle/walk/run/reach/carry/weld materially closer; remaining
kneel/repair/stand darker/smoother, swim face/light differs. West remains highest
visual priority: dry face/suit darker/softer than original, swim brighter.
South running cloth and face angle/shading vary; North running/welding quilt
details differ. Static80samples and bare reference do not prove all frames,
continuous cadence or equipped helmet-design acceptance. Full master-matching
objective remains open, despite complete explicit source coverage.

NativeV1 had8,398functional checks/0 but noisy Image.load_from_file warnings;
failure classification retained with all maps. V2 changes only fixture expected
decode to rawPNGbuffer (3,576extra decode assertions), engine clean. No runtime,
artwork,selected bank,owner save or exported-build change in this reconciliation.
EightPython syntax/two paired uniqueUIDs/{len(pngs)}previewPNG LFS. Updated review,
source mapping,native reports/maps,browserproof,REVIEW.md,HANDOFF retained.
HEAD eb1cb03b plus dirty/untracked installation and concurrent work; no commit.

Next concrete work: boundedWest master consistency, review existing48phase study
before authoring again; keep rejected trials unselected and acceptedEast sources
intact. Then judge remaining demonstrated view/pose differences. Coverage limits
are not automatic new generation/export/all-route tasks. Owner wants closeout
soon; do not reopen unrelated historicalTODOs or label full visual objective done.
http://127.0.0.1:8791/character/bill-installed-coverage-2026-10-04/.
'''
paths=[R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']
for base in [R/'skills/brinespace-character-pipeline',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline')]:paths.extend([base/'references/crew-consistency.md',base/'references/source-density.md'])
for p in paths:
 with p.open('a',encoding='utf-8') as f:f.write(note)
(D/'HANDOFF.md').write_text('''# Project handoff

Updated: October 4, 2026 · Project: Brine Space · Task: Bill installed coverage

## Objective and acceptance
Finish Bill master consistency and wrap soon. Complete explicit selected source
coverage is established; full master/style/motion acceptance remains open.

## Accepted decisions and constraints
Preserve installed East, legacy source epochs, other gears/directions and owner
saves. Whole source edits only; no automatic historicalTODO expansion. No commit,
export, new generation or normal runtime/source selection change in this audit.

## Current state
character/bill-installed-coverage-2026-10-04: current normal grid+inherited banks,
216bare/198helmet states,3,576slots,3,128unique source paths. REVIEW.md, native
maps/report/validation, eight cardinal boards/80samples, browserproof. EightPython
tools/builders and two paired native UIDs. All eight maintained records updated.
HEAD eb1cb03b plus dirty/untracked installation and concurrent work preserved.

## Verification
11,974/0 in11.56s: actual loaded RGBA/clock/density for all selected keys/slots;
4,974sourceinputs/2,936owner files exact, scratchAPPDATA,engine0/clean.131explicit
required keys per gear present.18theoretical bunk holes intentionally unused;
sealed helmet meals showinspect. All eight static family boards visually reviewed,
3,311comparisoninputs exact,8Python/2UID/9PNG LFS. V1 warning-bearing fixture
retained; V2 expected images decode rawbuffer. Existing native East jobs/Continue
remain separately authoritative; this is headless source inventory only.

## Next action
Bounded West master consistency. Review existing48phase study before new art;
do not admit rejected trials or overwrite installedEast. West dry face/suit are
darker/softer and swim brighter; remainingEast lowered poses and South/North
detail differences also recorded. Full art objective remains open. Do not convert
every evidence limitation into a new task or claim all-frame/motion acceptance.
''',encoding='utf-8')
print(json.dumps({'maintainedRecords':8,'checks':11974,'missingRequiredKeys':0,'pngLFS':len(pngs),'fullVisualObjectiveComplete':False}))
