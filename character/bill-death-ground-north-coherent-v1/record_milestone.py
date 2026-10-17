from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parents[1];OUT=ROOT/'output/bill-death-ground-north-candidate-native-v1'
r=json.loads((OUT/'validation.json').read_text());v=json.loads((P/'verification.json').read_text());assert r['passed'] and v['passed'] and not r['realProfileChanges']
summary=f'''Bill north bare ground-collapse candidate — October 1, 2026.
Built-in primary exec-5e039822-5d9e-493f-bc80-8eef5e6e4d0d retained;
selected anatomy correction exec-f4dc6c41-2a38-41b4-8c60-11149244468b,
raw sources and exact prompts in sources/. Corrected final raised-chest/crawl
reading toward settled rear prone pose. Exact selected rear idle entry plus
five authored interiors1..5, six finite slots250/300/350/400/400/300ms,2s;
terminal5 held, never loops. Fixed[.31,.363] source ruler on256plane,
pivot128,224/H148/dry0, centered rear boot/contact axis128,223.
Master neutral/hair/skin/shoulder grading; burgundy sampling excludes dark
outline pixels, preventing extreme pale shoulder gains. Both raw revisions
retained. Native148/82/idle comparison reviewed; fine master details, shoulder
marking remnants, final anatomy/floor contact and cadence remain polish work.
20 package and37 native checks PASS{r['seconds']}s; explicit scratch profile;
{r['realProfileFileCount']:,} owner non-log files unchanged in this interval.
Crowns76/87/109/111/112/118: rear prone foreshortening cannot reuse the
side-collapse constant/monotonic crown rule as physical acceptance.
Exact loaded pixels, finite pacing, dry metadata, held corpse and preserved
old helmet source proven. Staged candidate, not normal mortality selection,
actual kill/clearance/interruption or Continue proof. Earlier meal profile
guard failures remain failures; this clean interval does not certify them.
Next south dry collapse, canonical helmet versions and family/runtime proof;
generic rest, unfinished meal/inspection integration and full-set polish remain.
Full objective remains open. No normal actor, reward, room geometry or export changes.
'''
handoff='''# Project handoff

Updated: October 1, 2026 · BrineSpace · Bill north ground collapse

## Objective and acceptance
Complete Bill's master-consistent animation set, then full cross-animation polish.
North bare death candidate is packaged; owner/runtime acceptance remains open.

## Accepted decisions and constraints
Preserve rear master identity, subdued matte finish, physical density and camera.
Independent source art, exact idle entry, finite terminal hold; scratch profiles only.

## Current state
'''+summary+'''
Changed package: sources, build/prepare/verify, six frame PNGs, manifest,
registration/material grade/hashes, review sheet and index. Native fixture and
runner: tests/test_bill_death_ground_north_candidates.gd (+paired UID),
tools/run_bill_death_ground_north_candidate_validation.py.

## Verification
20 package/37 native checks pass. Full-size and82px native board reviewed.
Raster LFS attributes verified. Fine art acceptance and actual mortality remain.

## Next action
Author south collapse, build canonical helmet variants and paired family, then
prove actual kill/held corpse/restoration/clearance. Keep generic rest, meals,
inspection and full-set polish in scope.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
paths=list(P.glob('*.*'))+list((P/'sources').glob('*'))+list((P/'frames/death-ground-north').glob('*.png'))+[OUT/'validation.json',OUT/'native.log',OUT/'loaded-water-carry.png',ROOT/'tests/test_bill_death_ground_north_candidates.gd',ROOT/'tests/test_bill_death_ground_north_candidates.gd.uid',ROOT/'tools/run_bill_death_ground_north_candidate_validation.py']
e={'status':'staged_candidate','packageChecks':20,'nativeChecks':37,'native':r,'scope':'source/pixel/pacing evidence; final art acceptance, paired helmets, actual mortality/restore pending','sha256':{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in paths if f.is_file() and f.name!='candidate-evidence.json'}}
(P/'candidate-evidence.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
heading='## Bill north ground-collapse candidate — October 1, 2026\n\n'
for relative in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 with (ROOT/relative).open('a',encoding='utf-8') as f:f.write('\n'+heading+summary)
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write('\n'+heading+summary)
f=ROOT/'docs/CURRENT_STATUS.md';f.write_bytes((heading+summary+'\nHandoff: character/bill-death-ground-north-coherent-v1/HANDOFF.md.\n\n').encode('utf-8')+f.read_bytes())
print('Recorded north candidate evidence, source revisions, visual limits and remaining scope')
