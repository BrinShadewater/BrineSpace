"""Record the staged quarter-turn milestone without replacing existing notes."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
D = Path(__file__).resolve().parent
request = json.loads((D / 'source-request-v1.json').read_text())
request.update(status='selected_staged_not_installed', selection='source-selection-v1.json', provenance='source-provenance.json')
(D / 'source-request-v1.json').write_text(json.dumps(request, indent=2) + '\n')
checks = json.loads((D / 'native-candidate-v1-checks.json').read_text())
checks.update(checks=773, failures=0, scope='All four paired swimming quarter families: exact loaded pixels, metadata, every phase, pause, finite completion and selected destination loop0. Explicit candidates on normal Veld base; not actual route or owner acceptance.')
(D / 'native-candidate-v1-checks.json').write_text(json.dumps(checks, indent=2) + '\n')
handoff = '''# Project handoff

Updated: September 30, 2026 · Project: BrineSpace · Task: Veld north/east swimming turns and quarter matrix

## Objective and acceptance
Complete Veld against the directional masters, followed by full-set consistency and polish. This milestone completes staging of four paired ordinary swimming quarter families; motion/route and owner visual acceptance remain open.

## Accepted decisions and constraints
Exact selected cardinal swim frame0 joins;256 canvas,128 pivot,148 physical standing ruler;520ms finite quarter turns. Fixed overhead prone camera, anatomicalRIGHT scanner/anatomicalLEFT cylinders, matte master materials and smooth closed helmet. Independent source angles; reverse without mirroring. Runtime selection and owner saves unchanged.

## Current state
character/veld-swim-turn-north-east-coherent-v1 holds four states/24refs, original sources/exact prompts/provenance, explicit source selection, reproducible extraction/material fitting/build/validation scripts, finite paired review and all-quarter matrix. Corrected near-north atlas cell and independent later diagonal replace clustered first-pass headings. Calibrated per-source density rulers and one pooled material curve preserve head/hair and hardware. Four helmet angles fit skull/collar landmarks with protected body outside the component support; enlarged selected prone masters supersede the historical exposed-bun reference.

tools/review_veld_swim_turn_north_east_v1.gd and paired UID exercise all four quarter families on normal Veld base with explicit candidates. quarter-matrix.html compares eight directions,16gearstates and96turnrefs against selected source/destination loops. No installation, commit or export.

## Verification
59 paired packaging checks PASS;773 native checks PASS,0failures,engine_errors[],real_profile_changed_files[] under scratch APPDATA.16 candidate alpha envelopes fit effective selected transition/swim bounds. Native148/82/54 sheets and all-quarter contact boards reviewed; near-north dark, middle/reverse light82/54/27 browser captures retained. These checks cover loaded geometry/clocks/pause/completion/joins, not furnished/exterior/traffic routing or owner acceptance. Projected leg bulk, straighter turning legs versus loop stroke, and angular pacing still need full-matrix motion judgment.

## Next action
Inspect half-turn contracts, derive paired half routes through exact cardinal joins and review full twelve-direction swimming turn matrix before coherent promotion. Check actual water turn-route behavior. Remaining water cargo/actions/salvage/distress/recovery/death, inherited crew-life and full-set polish remain. Full Veld goal active.
'''
(D / 'FAMILY_HANDOFF.md').write_text(handoff, encoding='utf-8')
note = '''## Veld swimming quarter matrix staged — September 30, 2026

North/east completes four paired ordinary swimming quarter families: eight directions,16gearstates,96turnrefs with exact selected cardinal joins. Explicit visual source selection replaces clustered headings; calibrated source rulers and protected pooled material curves retain master identity. Closed prone helmet angles exclude the historical external bun.59 N/E packaging and773 combined native checks PASS; engine errors[] and real profile changed[] under scratch APPDATA.16 alpha envelopes covered. Combined native/contact/browser review retained. New turns remain staged; half routes, leg/stroke proportions, angular pacing, actual route evidence and owner visual acceptance remain before promotion. See [family handoff](../character/veld-swim-turn-north-east-coherent-v1/FAMILY_HANDOFF.md) and [combined review](http://127.0.0.1:8791/character/veld-swim-turn-north-east-coherent-v1/quarter-matrix.html?v=quarters-v1). Full Veld goal active.

'''
for rel in ['docs/CURRENT_STATUS.md', 'docs/VELD_ANIMATION_CONTINUATION_2026-09-29.md']:
    p = ROOT / rel
    if note.encode() not in p.read_bytes():
        p.write_bytes(note.encode() + p.read_bytes())
lesson = '''
### Veld north/east quarter matrix lesson — September 30, 2026

Prompt angle labels do not establish visual body headings. Select by actual whole-body axis: retain an explicit corrected near-north cell and independent later diagonal when an atlas clusters headings. Preserve rejected originals and exact selection/provenance. Pool one material curve over selected poses, protect full head/hair and hardware, and calibrate a fixed ruler for each source density rather than normalizing pose height. Rear views require full-skull anchors, not a missing skin landmark. Enlarged selected prone helmet masters govern camera, closed shell and collar; a historical high-density reference with an exposed bun is superseded. Extract connected opaque support to remove source alpha halos without a broad grade. Combined phase/pixel/clearance gates do not certify leg bulk, stroke cadence, angular pacing, actual world turn routes or owner acceptance. Evidence: character/veld-swim-turn-north-east-coherent-v1/FAMILY_HANDOFF.md (773 native checks,16covered envelopes; staged).
'''
for p in [ROOT / 'character/ANIMATION_PIPELINE.md', ROOT / 'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md', ROOT / 'skills/brinespace-character-pipeline/references/crew-consistency.md', Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    if lesson.encode() not in p.read_bytes():
        p.write_bytes(p.read_bytes() + lesson.encode())
print('Recorded staged quarter milestone, reports and four pipeline lessons.')
