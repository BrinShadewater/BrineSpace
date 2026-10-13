"""Record six-pose source/native evidence without implying normal admission."""
from pathlib import Path
import hashlib, json
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'character/marsh-east-walk-family-detail-v1'
RUN = ROOT/'output/marsh-animation-audit/east-walk-family-detail-player-v2-2026-10-03'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
reportpath = OUT/'review.json'
d = json.loads(reportpath.read_text())
assert len(d['records']) == 6
for r in d['records']:
    assert sha(ROOT/r['rawPath']) == r['rawSha256']
    assert sha(ROOT/r['framePath']) == r['frameSha256']
    assert sha(ROOT/r['original']['path']) == r['original']['sha256']
    r['reviewed'] = True
    r['decision'] = 'Provisional whole family, unselected; shared muted grade/detail improved, head shading and original gait/contact still require verification.'
for b in d['boards']:
    assert sha(ROOT/b['path']) == b['sha256']
    b['reviewed'] = True
d['findings'] = ['Six raw full figures and complete native-density master/idle/old/revised/start/stop/run board plus exact2xhead board actually inspected.',
    'Restrained shared grade reduces prior isolated-pose brightness change, collar/harness/seam detail clearer. Head/hair/face shading still varies, especially phase5 against phase3 and ownidle.',
    'Whole-canvas geometry: occupied height98..100% of old; crown0..2pixels lower, sole unchanged or1pixel higher. Do not hide residuals by per-pose fit. Contact/normal moving cadence unproven.',
    'No conspicuous riveted temple plates added; gray hair/temple patches remain. Native source/profile success does not decide full identity or grade acceptance.']
reportpath.write_text(json.dumps(d,indent=2)+'\n')
vpath = OUT/'native/verification.json'
v = json.loads(vpath.read_text())
for page in v['pages']:
    assert sha(ROOT/page['path']) == page['sha256']
    page['reviewed'] = True
v['reviewScope'] = 'Both full original-size672x1470three-capture pages inspected; six before/candidate/idle diagnostic native density and65.28station-height triplets. No actual main/grid/world capture or continuous motion.'
v['currentSourceReviewSha256'] = sha(reportpath)
frozen = json.loads((RUN/'inputs-after.json').read_text())
changes = [p for p,h in frozen.items() if sha(ROOT/p) != h]
assert changes == ['character/marsh-east-walk-family-detail-v1/review.json'], changes
v['postNativeMetadataChanges'] = changes
v['otherFrozenInputsStillExact'] = len(frozen)-len(changes)
vpath.write_text(json.dumps(v,indent=2)+'\n')

note = '''

## Marsh East six-phase walking detail/material study — October 3, 2026

Six built-in coherent whole-pose edits from exact current East walking targets,
equal1024square nearest-expanded target/ownidle guides, original unpainted collar/
suit crop. Explicit subdued ownidle grade shared across all six requests; exact
requests/ref hashes/raw output and generation receipts in
character/marsh-east-walk-family-detail-v1. All six raw figures, complete native
master/ownidle/old/revised/start/stop/run board and exact2xhead board inspected.
Collar/harness/seam construction clearer; shared muted grade reduces previous
isolated03brightness jump. Head/hair/face shading still varies (notably05vs03).
No conspicuous riveted temple plate; gray temple/hair patches remain. All six
PROVISIONAL/UNSELECTED. Normal228states/1190slots/89body manifests unchanged.

One whole-canvas184/1254resampling per raw source; alpha preserved, no pose fit,
head/limb splice/recolour/pivot move. Occupied height98..100% of old, crown0..2px
lower,sole0..1px higher;IoU.90107..97957. Geometry not a contact pass. Staged
manifest retains exact original loop/150ms holds/facings/water/depth/stride metadata
and uses whole quoted res paths. Six-frame APNG review media made, not claimed
continuously watched. World contact and natural gait remain pending before admission.

Normal body/equipment player loaded, then only test instances override East walk
with staged candidate:46checks/0failures,6exact source slots/restore holds and six
diagnostic before/candidate/ownidle captures at native density and65.28station
height. Both complete three-capture native pages actually inspected.5364bounded
source/runtime/art inputs and2931owner non-log files stable in scratch APPDATA,
engineexit0,no ERROR/WARNING/SCRIPT ERROR. Initial probe failed parsing because
load_manifest returnsvoid; corrected fixture and failedV1evidence retained with
5364/2931unchanged. V2 terminal. Source review JSON flags/decisions updated after
native interval;5363other frozen inputs still exact, new review hash bound in
native verification. No actual main/grid/world floor/contact, natural actor,
fullRunSave/Continue, continuous cadence or full-set acceptance inferred.

Lesson: a common ownidle grade reference plus explicit subdued material wording
helped this six-pose family reduce a single-source brightness mismatch. Shared
prompts do not lock head shading or registration; inspect complete family, head
neighbors and idle/action joins before selection. Source/player equality does
not settle physical gait/contact. Next actual staged normal-actor moving/contact
review, head/grade seam polish, then admission only when supported. Full goal active.
'''
canonical = ROOT/'skills/brinespace-character-pipeline/references/master-repair.md'
installed = Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md')
assert canonical.read_bytes() == installed.read_bytes()
for p in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',canonical]:
    with p.open('a',encoding='utf-8',newline='\n') as f: f.write(note)
installed.write_bytes(canonical.read_bytes())
print('Six provisional whole poses and46-check native evidence recorded;5363protected inputs exact after review metadata update; four notes/skill mirror updated')
