import hashlib,json,shutil,zipfile
from pathlib import Path
root=Path.cwd();base=root/'output/james-release-closeout-v365';delivery=base/'deliverable'
output=root/'output/james-windows-package-v365';output.mkdir(exist_ok=True)
release=json.loads((base/'release-validation.json').read_text());cargo=json.loads((root/'output/james-unload-playtest-v365/validation.json').read_text())
assert all(r['exitCode']==0 for r in release['checks']) and release['realProfileUnchanged'] and release['qaOverrideRemoved']
assert cargo['exitCode']==0 and cargo['ownerUnchanged'] and cargo['qaOverrideRemoved']
assert not (delivery/'override.cfg').exists() and not (base/'native-qa/override.cfg').exists()
for name,digest in release['hashes'].items():
    with (delivery/name).open('rb') as stream:assert hashlib.file_digest(stream,'sha256').hexdigest()==digest
build=json.loads((delivery/'build_info.json').read_text());assert build['build_id']!='brinespace-5024faab0e485c1a'
(delivery/'README.md').write_text(f'''# BrineSpace — Windows James playtest

October 4, 2026 · Build {build['build_id']}

Extract the whole ZIP, then open BrineSpace.exe. Keep BrineSpace.pck beside it.
No editor is required. New Game starts an expedition; Continue resumes a checkpoint.
The game uses your normal BrineSpace save folder. F7 shows performance; F8 saves a report.

This build adds a smoother North unload rise to the previously tested James snapshot.
It reuses the accepted intermediate pose for both bare and diving-helmet versions.
The action remains520ms; pickups, carries and existing artwork are preserved.
Forward torch work, inward tablet diagnostics, belt wrench, swimming transitions,
turns and furniture actions from that snapshot remain included.

This exact package passed its asset audit, release New Game/Continue/F8 check and
normal workshop pickup/carry/turn/unload in four layouts with both equipment variants.
The prior V351 snapshot also has recorded survival/refuge, exterior delivery and
fresh-scene loaded-return/drain checkpoint evidence; those lanes were not rerun on
this timing-only revision. Sampled native views do not certify every frame in real time.

Known polish: coarse cargo fabric, wide North crouch and remaining arm/material joins.
North persistent floor-case support is not newly added. Later concurrent UI/character
work is excluded. Long-session behavior and Mac gameplay are outside these checks.
Prior fixture-exit ObjectDB warnings remain recorded. Saves are prototype-level
and unversioned. See NOTICE.md for rights; font license is under LICENSES.
This local candidate has not been published. build_info.json and SHA256SUMS.txt
identify the selected source and delivery files.
''',encoding='utf8')
shutil.copy2(root/'NOTICE.md',delivery/'NOTICE.md');(delivery/'LICENSES').mkdir(exist_ok=True);shutil.copy2(root/'assets/fonts/OFL.txt',delivery/'LICENSES/Fonts-OFL.txt')
members=['BrineSpace.exe','BrineSpace.pck','build_info.json','README.md','NOTICE.md','LICENSES/Fonts-OFL.txt']
hashes={}
for name in members:
    with (delivery/name).open('rb') as stream:hashes[name]=hashlib.file_digest(stream,'sha256').hexdigest()
(delivery/'SHA256SUMS.txt').write_text(''.join(f'{digest}  {name}\n' for name,digest in hashes.items()));members.append('SHA256SUMS.txt')
archive=output/'BrineSpace-Windows-James-North-Rise-2026-10-04.zip';partial=archive.with_suffix('.zip.partial')
assert not archive.exists() and not partial.exists()
print('Packaging verified James timing release.',flush=True)
with zipfile.ZipFile(partial,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=1,allowZip64=True) as bundle:
    for name in members:bundle.write(delivery/name,'BrineSpace/'+name)
print('Checking every archived delivery file.',flush=True)
with zipfile.ZipFile(partial) as bundle:
    assert bundle.namelist()==['BrineSpace/'+name for name in members]
    for name in members:
        with bundle.open('BrineSpace/'+name) as stream:digest=hashlib.file_digest(stream,'sha256').hexdigest()
        with (delivery/name).open('rb') as stream:assert digest==hashlib.file_digest(stream,'sha256').hexdigest()
partial.rename(archive)
with archive.open('rb') as stream:archive_hash=hashlib.file_digest(stream,'sha256').hexdigest()
(output/'SHA256SUMS.txt').write_text(f'{archive_hash}  {archive.name}\n')
report={'version':365,'buildId':build['build_id'],'archive':str(archive),'archiveBytes':archive.stat().st_size,'archiveSha256':archive_hash,'verifiedMembers':7,'memberHashes':hashes,'published':False}
(output/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True)
