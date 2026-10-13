"""Record the actually reviewed movement evidence and provisional detail edits."""
from pathlib import Path
import hashlib, json

ROOT = Path(__file__).resolve().parents[1]
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
movement = ROOT / 'character/marsh-movement-joins-v1/review.json'
d = json.loads(movement.read_text())
assert d['states'] == 34 and d['slots'] == 170
for path, digest in d['inputs'].items():
    assert sha(ROOT / path) == digest, path
for entry in d['boards'] + d['nativeDensityPages']:
    assert sha(ROOT / entry['path']) == entry['sha256']
    entry['reviewed'] = True
    entry['reviewScope'] = ('Full held-source board; North/South tall overviews were also inspected in exact unscaled three-page crops. No continuous cadence or native acceptance.')
d['findings'] = [
    'Native density and recorded pivot alignment preserve differing184/256 canvases without resizing anatomy; all visible alpha fits review cells.',
    'East walking collar/harness construction is weaker than original directional material authority and current idle. Original master visible temple treatment differs from current ownidle; current ownidle remains governing animation join.',
    'West profile remains broadly coherent in this held comparison; fine hair/face/suit detail still varies. No final visual acceptance inferred.',
    'North/South held views preserve authored foot/crown movement; North step transfer rise is not labelled body shrinkage from absolute screen position alone.',
    'South corrected step phase3 remains selected; no registration or animation changes in this pass.'
]
movement.write_text(json.dumps(d, indent=2) + '\n')
comparison = ROOT / 'character/marsh-east-walk-detail-v1/comparison.json'
c = json.loads(comparison.read_text())
assert len(c['candidates']) == 2
for entry in c['candidates']:
    for prefix in ['raw', 'frame']:
        assert sha(ROOT / entry[prefix + 'Path']) == entry[prefix + 'Sha256']
    entry['reviewed'] = True
    entry['decision'] = ('Rejected: conspicuous riveted visible temple plate conflicts with current ownidle despite explicit negative prompt.' if entry['candidate'] == '01' else
        'Provisional whole-pose source: clearer collar/strap/seam construction; conspicuous riveted plate absent, gray temple/hair patch remains. Brighter ivory and stronger panel contrast differ from current neighboring walking frames. Crown+1/sole-1 must be evaluated with gait/contact; not admitted.')
c['wholeNeighborhoodReviewed'] = True
c['reviewScope'] = 'Native whole master/idle/before/two candidates and all six current/provisional walk neighbors inspected. Enlarged overview also seen but tool display resized it; native board establishes actual-density comparison. No cadence/native acceptance.'
comparison.write_text(json.dumps(c, indent=2) + '\n')

note = '''

## Marsh four-direction movement joins and East detail study — October 3, 2026

Current normal catalogue revalidated against post-South-contact inventory:
228body states/1190slots/89body manifests retained. New pivot-aligned held review
covers34dry movement states/170slots: all four idle/start/walk/short-step/run and
every authored stop bank. All four complete boards actually inspected; North/South
tall overviews also inspected in six exact unscaled pages.184/256canvases aligned
by recorded pivots only, no occupied-bound/body fitting. All visible alpha fits
cells; original directional masters shown at fixed historical147/1232display
scale.241frozen inventory/catalogue/manifest/master/selected-frame inputs unchanged.
Evidence character/marsh-movement-joins-v1/review.json. Held review proves this
comparison scope, not full-set acceptance, continuously watched cadence or native
route/contact/save/Continue behavior. No engine/profile run this pass.

East walk phase3 lost some fine collar/harness/seam detail compared with original
material master and ownidle. Two built-in whole-pose edits retained in
character/marsh-east-walk-detail-v1 with exact prompts, hashed refs, raw images and
whole-neighborhood comparison.01(67672637)rejected for conspicuous riveted temple
plate against current East ownidle, despite negative instruction.02(edc6b5e7)
uses unpainted original collar/suit crop(340,375,660,805), no master head, while
same target/ownidle guide canvases govern identity. Conspicuous riveted plate
absent; gray temple/hair patch remains. Collar/harness/panel construction clearer,
but brighter ivory/stronger contrast differs from six-frame walking neighborhood.
02PROVISIONAL/UNSELECTED: coordinated family grade, head/detail joins and physical
contact/cadence remain. Neither revision changes normal selection.

Both raw1254square outputs receive one fixed184/1254whole-canvas resampling,
no alpha repair/recolour/anatomy splice/pivot/occupied-pose fitting. Both opaque
height146vs148(98.65%),crown+1,sole-1;IoU01.95215/02.94566. That geometry alone
does not certify contact or style. Whole master/ownidle/before/candidates and all
six current/provisional neighbors actually inspected; native board establishes
density. Enlarged overview was display-resized, not claimed as an exact2xview.
No gameplay/room/save/runtime/art catalogue changes, commit/export. Full goal active.

Lesson: a full identity master supplied only for suit detail can override a
current ownidle facial/equipment constraint even with explicit negatives. Preserve
the current accepted join, keep original master authority visible in review, and
try an unpainted material-only support crop for a coherent whole-pose retry.
One retry is evidence for this case, not a universal guarantee. A clearer isolated
pose can introduce a brightness/ink pulse in its unchanged neighbors; compare
the complete family before admission, then validate real contact and motion.
Next coordinated East six-phase walking detail/material pass, exact gait and idle/
start/stop joins, native normal movement/contact/cadence. Other directions, water,
equipment/furniture/construction and natural/full-save verification remain open.
'''
canonical = ROOT / 'skills/brinespace-character-pipeline/references/master-repair.md'
installed = Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md')
assert canonical.read_bytes() == installed.read_bytes()
for p in [ROOT / 'character/ANIMATION_PIPELINE.md', ROOT / 'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md', ROOT / 'docs/CURRENT_STATUS.md', canonical]:
    with p.open('a', encoding='utf-8', newline='\n') as f:
        f.write(note)
installed.write_bytes(canonical.read_bytes())
print('34states/170slots held review and two provisional whole-pose receipts recorded;241inputs stable; four maintained notes updated and skill mirror exact')
