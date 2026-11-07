"""Record alternating complete carry cycle, with explicit join/native limits."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-east-carry-material-v1';S=B/'sources'
MARKER='## Marsh East carry02 complete source assembly — October 2, 2026'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for name in ['passing-05','near-06']:
    r=json.loads((S/f'{name}.request.json').read_text());assert sha(S/f'{name}.prompt.txt')==r['promptSha256'];assert sha(S/f'{name}.raw.png')==r['rawSha256']
    for q in r['orderedReferences']+r['sourceFrames']:assert sha(ROOT/q['path'])==q['sha256']
a=json.loads((B/'candidate-02/assembly.json').read_text())
for q in a['sources']:assert sha(ROOT/q['path'])==q['sha256']
a.update(visualReviewed=True,allFourCompletePosesInspected=True,findings='Near06 foreground near leading/support and far04/05 opposite thighs now alternate. Near passing raises rear far boot; far passing raises rear near boot. Crate inset panel/single visible right latch concept consistent; projected width and body/hand registration vary between separately generated sheets, especially narrower far-contact crate. Neutral widths36/37/38 versus selected32 remain diagnostics, not accepted anatomical matching. Far-contact sole clearance remains provisional. Native motion and whole-cycle joins still need validation/polish.',remaining='Stage actual East workshop carry movement, inspect source/native pairs and registration/cargo joins; retain unselected until review. West carry, turn/held joins, normal saves/visible Continues, full consistency/polish remain.')
(B/'candidate-02/assembly.json').write_text(json.dumps(a,indent=2)+'\n')
maintained=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md'; installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md');assert maintained.read_bytes()==installed.read_bytes(),'skill mirror drift'
lesson='''

## Marsh East carry02 complete source assembly — October 2, 2026

Passing05 generated exec-a2734a27-25e4-462c-927b-d2805582751e from frozen
whole far-contact04/selected idle/own East original references. Correct far flat
support under pelvis and foreground near knee/rear raised boot LEFT. Two complete
alpha128 cells, one neutral147 BOX scale .1777509068923821:85x146,ruler38x147.
Near06 generated exec-fdd5fddf-e75f-4039-b86d-114cf92dd814 from frozen selected
near stance FIRST,selected idle PRIMARY second,whole far05 cargo-only third,own
East original fourth. Correct near-leading/contact and near-support passing with
darker far rear boot raised. Three complete cells, one neutral147 BOX scale
.2061711079943899:89x146,85x146,ruler36x147. Exact prompts/ordered ref and source
hashes/raw generation IDs/original paths retained and revalidated. Raw figures,
packed comparisons and used whole guides inspected. No clipped opaque pixels.

Candidate02 is FOUR byte-identical whole PNG copies:near06contact/near06passing/
far04contact/far05passing.184canvas,p92/172,H148,four180ms loop and explicit
carry-east stride .0827027027027027 unchanged. APNG four decoded copies exact.
Whole old/new comparison inspected; opposite support now alternates. Current
inset-panel/single-right-latch crate variant intentionally matches its concept,
but projected width varies, particularly narrower far-contact crate. Head/body/
hand horizontal registration and sheet grade/neutral width remain provisional.
Neutral widths36/37/38 versus selected32 are diagnostic, not anatomical acceptance.
Far-contact boot projection/clearance remains provisional. One scale per sheet
does not guarantee identical rigid-object dimensions across separate generations.
Inspect the complete cycle; do not correct these with crate/limb patches, mirror,
per-pose/cargo-width fits or false bbox-based sole certification. Whole integer
registration may address alignment only; material/design differences need complete
source correction. Source assembly is reviewable, not final coherent acceptance.

No native East carry run or new owner/profile fingerprint interval in this source
milestone. Normal catalog remains unchanged; South/North native evidence does not
transfer. Next stage actual own East workshop carry, inspect held source/native
pairs and motion/registration/cargo joins, then polish complete sources as needed.
West carry,carry-turn/held joins,independent normal full saves/visible Continues,
full-set consistency/polish remain. Full goal active/incomplete. No live job.
'''
for p in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',maintained]:
    with p.open(encoding='utf-8') as f:present=any(MARKER in line for line in f)
    if not present:
        with p.open('a',encoding='utf-8') as f:f.write(lesson)
installed.write_bytes(maintained.read_bytes())
(ROOT/'docs/MARSH_EAST_CARRY02_ASSEMBLY_HANDOFF_2026-10-02.md').write_text('''# Project handoff

Updated: October 2, 2026 · BrineSpace · Marsh East carry02 source assembly

## Objective and acceptance
Full master-matched set and consistency/polish active/incomplete. Four opposite
East cargo poses assembled and visually reviewed; unselected, native pending.
No normal catalog or gameplay change. No live process/tool handle.

## Accepted decisions and constraints
Selected East adult body PRIMARY, authentic visible implant/ankle buckles and
elevated side camera. Current inset-panel single-right-latch crate variant explicit.
Complete figures only; one neutral147 calibration per sheet, no opaque clipping,
mirror, limb/crate patch, recolour or per-pose/cargo-width fitting. Runtime timing,
stride,184canvas,p92/172,H148 retained. Owner saves untouched by source work.

## Current state and changed files
build_marsh_east_carry_passing05.py,prepare_marsh_east_carry_near06.py,
build_marsh_east_carry_near06.py,assemble_marsh_east_carry02.py and milestone
recorder. Source raw/prompt/request SHA provenance and complete guides;
passing05-unselected,near06-unselected,candidate02 four exact source PNGs,
manifest/APNG/comparison/assembly assessment. Pipeline,bible,current status and
maintained/installed master-repair skill appended; other-actor notes preserved.

## Verification and limits
Both new raw sources,used guides and packed comparisons seen. Far05 correct far
support/near rear lift;near06 correct near support/far rear lift. One scale per
source:far05 .1777509068923821,85x146/ruler38x147;near06 .2061711079943899,
89x146/85x146/ruler36x147. Four unchanged PNG copies and four exact APNG decoded
frames at180ms. Whole comparison seen. Crate projected width changes,especially
narrower far-contact;horizontal head/body/hand registration and grade provisional.
Neutral widths differ from selected32; not anatomical acceptance. Far-contact
sole clearance provisional. No actual East native/moving-contact/full-save/Title
Continue acceptance or new profile fingerprint interval. No normal admission.

## Remaining work and next action
Build East carry02 actual workshop-carry fixture from South/North carry six-view
fixture, using validated East positiveX 168 clear route from EastRun03. Scratch
APPDATA and fresh owner/native fingerprints mandatory. Inspect all held source/
native pairs and phase/restore/pause behavior; polish complete source/cargo joins
before admission. West carry,turn/held joins,independent normal save/Continue,
full-set consistency/polish remain. Do not declare full set from coverage counts.
''',encoding='utf-8')
print('Recorded complete East carry02 source assembly; skill mirrors equal; native and join polish pending.')
