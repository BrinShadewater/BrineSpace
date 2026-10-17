import json
import subprocess
from pathlib import Path

from milestone_notes import record_guides

root = Path.cwd()
bank = root / 'character/james-west-carry-walk-keys-v1'
output = root / 'output/james-windows-package-v358'
report = json.loads((output / 'validation.json').read_text())
assert report['verifiedArchiveMembers'] == 7 and report['exePckUnchanged'] and report['qaOverrideAbsent']
assert not report['packageRebuilt'] and not report['published']
archive = Path(report['archive'])
assert archive.is_file()
ignored = subprocess.run(['git', 'check-ignore', str(archive.relative_to(root))], capture_output=True, check=False)
assert ignored.returncode == 0, 'Local binary distribution must stay outside source tracking'
section = f'''### James Windows download packaged — October 4, 2026

V358 single local ZIP ready: output/james-windows-package-v358/{archive.name}.
Build {report['buildId']}; {report['archiveBytes']} bytes. Seven archive members
verified by streamed SHA256/ZIP integrity against the delivery folder: EXE, PCK,
build_info, player README, rights notice, font license and file checksums. ZIP
checksum beside it. Exact V351 tested EXE/PCK retained; no rebuild, QA override,
Godot probe, owner-save access or publication. Binary distribution is gitignored.

README gives extraction/play instructions, James changes and tested scope, known
cargo texture/North unload stance polish, sampled visual evidence and recorded
fixture-exit leak warnings. This frozen James snapshot excludes later concurrent
UI/character authoring changes. Existing V351–V357 gameplay evidence retains its
original bounds; packaging is not another gameplay acceptance claim.

Local Windows delivery is now concrete and portable. Next useful step is final
owner playtest or an explicit publication request for a selected build. Do not
rebuild or add redundant fixtures just to continue this completed packaging work.
'''
handoff = '''# Project handoff

Updated: October 4, 2026 · Project: Brine Space · Task: James Windows package

## Objective and acceptance
Wrap James and prepare the next game version. Tested James Windows snapshot now
available as a verified single ZIP, with player instructions and identity checks.

## Accepted decisions and constraints
Accepted artwork and exact tested executable retained. Known cargo texture and
North unload stance polish explicit. No publication or approval inferred.

## Current state
V358 packaging/closeout helpers; README, rights notice, font license and checksums
added beside V351 deliverable. New ZIP/checksum/validation under output. Source
runtime, art, owner saves and tested EXE/PCK unchanged.

## Verification
'''+section+f'''
Archive SHA256: {report['archiveSha256']}

## Next action
Final owner playtest or explicit publication of a selected build. The ZIP covers
the frozen James snapshot and excludes later concurrent UI/character changes.
Uninterrupted visual acceptance, long-session random-world traffic, process-restart
interruption and Mac gameplay remain outside the completed checks.
'''
(output / 'HANDOFF.md').write_text(handoff)
record_guides(root, section, '### James loaded expedition Continue — October 4, 2026')
with (bank / 'HANDOFF.md').open('a', encoding='utf8') as stream:
    stream.write('\n' + section)
f = bank / 'material-repair-progress.json'
old = f.read_bytes()
ledger = json.loads(old)
ledger['windowsDownloadPackage'] = report
assert f.read_bytes() == old
f.write_text(json.dumps(ledger, indent=2) + '\n')
f = root / 'docs/JAMES_RELEASE_CLOSEOUT.md'
old = f.read_bytes()
text = f.read_text()
text += '\nV358 portable Windows ZIP: output/james-windows-package-v358/' + archive.name + '.\nSeven members verified byte-for-byte; player instructions, rights/font notices and\nchecksums included. Exact tested EXE/PCK retained, no rebuild or publication.\nThis frozen James snapshot excludes later concurrent UI/character authoring changes.\n'
assert f.read_bytes() == old
f.write_text(text)
print(json.dumps({'version': 358, 'archiveBytes': report['archiveBytes'], 'verifiedMembers': 7, 'exePckUnchanged': True, 'published': False}))
