from pathlib import Path
import json, hashlib

P = Path(__file__).resolve().parent
ROOT = P.parent.parent
native = ROOT/'output/bill-reading-entry-east-candidate-native-v1'
report = json.loads((native/'validation.json').read_text())
assert report['passed'] and not report['realProfileChanges']
assert json.loads((P/'verification.json').read_text())['checks'] == 40
note = '''
Bill east tablet take-out/put-away staged — September 30, 2026.
Four gear states/24 references; exact east seated and reading endpoints in both
gear states.40 package/103 native checks PASS9.98sec; full-size/native82 boards
reviewed. Fixed ruler[.235,.263], material density1.1, protected body/native east
helmet, selected matte grade and planted sole223. All2,914 owner non-log profile
files unchanged under scratch APPDATA. Candidate source/player evidence only:
normal selection, NPC interruption/restore and live furniture remain unproved.
East source coverage now includes12 gear states/72 references across sitting,
breathing, reading and tablet transitions. Consolidated selection is next.
Retain the small tablet lift before settling for later motion review. Lesson:
keep exact stage endpoints and distinguish source coverage from activity support.
West, other life/rest and full-set consistency/polish remain; full goal active.
Handoff: character/bill-reading-entry-east-v1/FAMILY_HANDOFF.md.
'''
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md',
             'docs/ASSET_PIPELINE_AND_WORKFLOW.md',
             'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',
             'skills/brinespace-character-pipeline/references/crew-consistency.md']:
    with (ROOT/name).open('a', encoding='utf-8') as f:
        f.write(note)
status = ROOT/'docs/CURRENT_STATUS.md'
status.write_bytes(('## Bill east tablet entry/exit staged — September 30, 2026\n'+note+'\n').encode('utf-8')+status.read_bytes())
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a', encoding='utf-8') as f:
    f.write(note)
files = [P/'sources/entry-v1.png', P/'sources/prompt-entry.txt', P/'build.py',
         P/'bare-manifest.json', P/'helmet-manifest.json', P/'registration.json',
         P/'verification.json', P/'frame-hashes.json', P/'FAMILY_HANDOFF.md',
         P.parent/'bill-seated-east-coherent-v1/grade.py',
         native/'validation.json', native/'loaded-water-carry.png',
         ROOT/'tests/test_bill_reading_entry_east_candidates.gd']
evidence = {'status':'staged_candidate', 'checks':{'package':40,'native':103},
            'native':report, 'scope':'candidate source/player;normal selection,actor restore and furniture unproved',
            'hashes':{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}}
(P/'candidate-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
print('Recorded east tablet entry/exit milestone and evidence')
