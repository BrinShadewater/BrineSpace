import hashlib
import json
import shutil
import zipfile
from pathlib import Path

root = Path.cwd()
base = root / 'output/james-release-closeout-v351'
delivery = base / 'deliverable'
output = root / 'output/james-windows-package-v358'
output.mkdir(exist_ok=True)
expected = json.loads((base / 'release-validation.json').read_text())['hashes']
for name, digest in expected.items():
    with (delivery / name).open('rb') as stream:
        assert hashlib.file_digest(stream, 'sha256').hexdigest() == digest
assert not (delivery / 'override.cfg').exists()
build = json.loads((delivery / 'build_info.json').read_text())
assert build['build_id'] == 'brinespace-5024faab0e485c1a'

(delivery / 'README.md').write_text('''# BrineSpace — Windows playtest candidate

James animation closeout · October 4, 2026
Build: brinespace-5024faab0e485c1a

## Play

Extract the entire ZIP into a folder, then open BrineSpace.exe. Keep
BrineSpace.pck beside it. No editor installation is required.

Choose New Game for a new expedition, or Continue for an existing checkpoint.
This is the normal playable game and uses your BrineSpace save folder.
F7 shows performance information; F8 saves a diagnostic report.

## James changes in this candidate

- Accepted matte James animations, with bare and diving-helmet variants.
- Forward blowtorch work, inward-facing tablet diagnostics and the wrench on his belt.
- Walking, turning, cargo, furniture and underwater animation handoffs.
- Swimming clearance and transitions integrated into normal gameplay.

## Checked

The exact executable and pack passed the packaged-asset audit and release
New Game, Continue and diagnostic-report checks. Follow-up packaged checks
covered cargo, survival/refuge routing, all four exterior airlock orientations,
and eight fresh-scene disk resumes during loaded return and airlock draining.
All four resumed salvage journeys delivered their rewards exactly once.

## Remaining polish and scope

Cargo fabric is still coarser than the original master; the north-facing unload
stance is still wide. The visual review used sampled poses and native captures,
so uninterrupted final visual acceptance remains part of playtesting.

This is the tested frozen James snapshot. Later concurrent character/UI work
in the development workspace is not included. Long-session random-world traffic,
process-restart interruption and Mac gameplay are outside these checks.
Fixture-exit ObjectDB leak warnings remain recorded; long-session memory behavior
has not been certified. Saves remain prototype-level and unversioned.

## Rights and package identity

See NOTICE.md. All rights reserved; this local candidate has not been published.
build_info.json identifies the frozen source. SHA256SUMS.txt identifies the files
in this folder. The font license is included under LICENSES.
''', encoding='utf8')
shutil.copy2(root / 'NOTICE.md', delivery / 'NOTICE.md')
(delivery / 'LICENSES').mkdir(exist_ok=True)
shutil.copy2(root / 'assets/fonts/OFL.txt', delivery / 'LICENSES/Fonts-OFL.txt')
members = ['BrineSpace.exe', 'BrineSpace.pck', 'build_info.json', 'README.md', 'NOTICE.md', 'LICENSES/Fonts-OFL.txt']
hashes = {}
for name in members:
    with (delivery / name).open('rb') as stream:
        hashes[name] = hashlib.file_digest(stream, 'sha256').hexdigest()
(delivery / 'SHA256SUMS.txt').write_text(''.join(f'{digest}  {name}\n' for name, digest in hashes.items()), encoding='utf8')
members.append('SHA256SUMS.txt')
archive = output / 'BrineSpace-Windows-James-2026-10-04.zip'
assert not archive.exists(), 'Preserve an already-created package'
partial = archive.with_suffix('.zip.partial')
assert not partial.exists()
print('Packaging the tested executable, pack and player notes.', flush=True)
with zipfile.ZipFile(partial, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=1, allowZip64=True) as bundle:
    for name in members:
        bundle.write(delivery / name, 'BrineSpace/' + name)
        print('Packed ' + name, flush=True)
print('Verifying all archive contents against the delivery files.', flush=True)
with zipfile.ZipFile(partial) as bundle:
    assert bundle.namelist() == ['BrineSpace/' + name for name in members]
    for name in members:
        with bundle.open('BrineSpace/' + name) as stream:
            digest = hashlib.file_digest(stream, 'sha256').hexdigest()
        with (delivery / name).open('rb') as stream:
            assert digest == hashlib.file_digest(stream, 'sha256').hexdigest()
        assert bundle.getinfo('BrineSpace/' + name).file_size == (delivery / name).stat().st_size
partial.rename(archive)
with archive.open('rb') as stream:
    archive_hash = hashlib.file_digest(stream, 'sha256').hexdigest()
(output / 'SHA256SUMS.txt').write_text(archive_hash + '  ' + archive.name + '\n')
report = {'version': 358, 'buildId': build['build_id'], 'archive': str(archive), 'archiveBytes': archive.stat().st_size, 'archiveSha256': archive_hash, 'members': members, 'memberHashes': hashes, 'verifiedArchiveMembers': len(members), 'exePckUnchanged': all(hashes[n] == h for n, h in expected.items()), 'qaOverrideAbsent': not (delivery / 'override.cfg').exists(), 'packageRebuilt': False, 'published': False}
(output / 'validation.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report), flush=True)
