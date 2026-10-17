import hashlib,json,subprocess,re
from pathlib import Path
from milestone_notes import insert_status
root=Path.cwd();bank=root/'character/james-west-carry-walk-keys-v1';base=root/'output/james-release-closeout-v365';review=bank/'release-build-review-v365';package=root/'output/james-windows-package-v365'
build=json.loads((base/'build-validation.json').read_text());release=json.loads((base/'release-validation.json').read_text());cargo=json.loads((root/'output/james-unload-playtest-v365/captures/review.json').read_text());cv=json.loads((root/'output/james-unload-playtest-v365/validation.json').read_text());zip_report=json.loads((package/'validation.json').read_text())
assert build['exitCode']==0 and build['ownerUnchanged']
assert all(r['exitCode']==0 for r in release['checks']) and release['realProfileUnchanged'] and release['qaOverrideRemoved']
assert cargo['failures']==0 and len(cargo['cases'])==8 and cv['exitCode']==0 and cv['ownerUnchanged'] and cv['qaOverrideRemoved']
before=json.loads((root/'output/james-release-closeout-v351/expected-manifest.json').read_text())['files'];after=json.loads((base/'expected-manifest.json').read_text())['files']
old={r['path']:r for r in before};new={r['path']:r for r in after}
changed=[p for p in old.keys()&new.keys() if old[p]['sha256']!=new[p]['sha256']]
allowed={'res://'+r['path'] for r in build['changes']}|{'res://build_info.json'}
assert old.keys()==new.keys() and set(changed)<=allowed,(changed,set(old)^set(new))
for file in review.glob('*.png'):
    attr=subprocess.run(['git','check-attr','filter','--',str(file.relative_to(root))],capture_output=True,text=True,check=True)
    assert attr.stdout.rstrip().endswith(': lfs')
audit=re.search(r'RELEASE ASSET AUDIT: checked=(\d+) missing=(\d+) changed=(\d+) remapped=(\d+) unexpected=(\d+)',(base/'asset-audit.log').read_text())
assert audit and audit.group(2)==audit.group(3)==audit.group(5)=='0'
report={'version':365,'buildId':zip_report['buildId'],'package':zip_report['archive'],'archiveSha256':zip_report['archiveSha256'],'manifestFiles':len(new),'packedAssetsChecked':int(audit.group(1)),'manifestChangedFiles':sorted(changed),'packageHashes':release['hashes'],'cargoChecks':cargo['checks'],'cargoFailures':0,'cargoCases':8,'cargoCaptures':len(cargo['captures']),'ownerUnchanged':True,'published':False,'scope':'V351 tested frozen runtime plus four paired North unload timing manifests; original artwork unchanged. Exact new package audit/startup/Continue/F8 and native workshop lifecycle checked. Broader prior survival/expedition/resume lanes not rerun on this timing-only revision.'}
report['testedCargoFixtureSha256']=hashlib.sha256((review/'cargo_playtest.gd').read_bytes()).hexdigest()
report['nativeFixtureDescriptionNote']='Raw trace retains legacy V351/no-normal-selection boilerplate from its template. Actual V365 executable/PCK hashes and explicit ordinary seven-pose bank/clock checks establish the tested revision and normal selection. Tested script/trace retained; preparation helper corrected for future generation.'
(review/'review.json').write_text(json.dumps(report,indent=2)+'\n')
section=f'''### James seven-pose Windows package — October 4, 2026

V365 build {report['buildId']}: physical V351 tested snapshot plus four paired
North unload timing manifests only;180 original cargo PNGs exact, no later shared
UI/character runtime changes. Established import cache copied; not a clean-import
claim. Maintained exporter completes; same{len(new)}manifest paths and only allowed
timing/build metadata hashes differ. PCK audit checks{report['packedAssetsChecked']}
assets with0missing/changed/unexpected. Actual release New Game,
saved Continue and F8 pass. Normal packaged seven-pose unload (no fixture texture
substitution):{cargo['checks']}checks0, eight layout/gear workshop cases,
{len(cargo['captures'])}native captures; eight boards viewed. Scratch owner unchanged,
QA override removed. Seven-member ZIP byte/integrity verified, unuploaded.
Original crouch/material/arm/case and uninterrupted acceptance limits retained.
Prior broader survival/exterior/disk-resume evidence remains V351-scoped, not a new
V365 claim. Package: output/james-windows-package-v365/{Path(report['package']).name}.
'''
insert_status(root/'docs/CURRENT_STATUS.md',section,'### James North mid-rise timing installed — October 4, 2026')
handoff=f'''# Project handoff

Updated: October 4, 2026 · Project: Brine Space · Task: James timing Windows release

## Objective and acceptance
Wrap James and ship the next version. New verified portable Windows candidate
contains the installed smoother North rise, both gears, at original520ms.

## Accepted decisions and constraints
Use accepted artwork. Preserve exact prior release, owner saves and shared work.
No itch publication or inclusion of later unrelated UI/character work selected.

## Current state
V365 frozen project/export, exact pack/startup/workshop verification, native
captures/boards, portable ZIP and checksums. Build {report['buildId']}.
Package: {report['package']}.

## Verification
Maintained exporter,{len(new)}manifest paths/{report['packedAssetsChecked']}audited assets,
0missing/changed/unexpected; actual release New Game,
saved Continue/F8. Eight normal packaged layout/gear cargo cases:{cargo['checks']}
checks0/{len(cargo['captures'])}captures; eight boards viewed. Four paired manifests
only differ from tested V351 runtime; all original cargo pixels preserved.
Scratch owner unchanged, QA override removed. Seven ZIP members stream-hash/CRC
verified. Source cache reused; no clean-import or full continuous visual acceptance.
Known material/stance/arm/North case limits retained. Prior survival/exterior/resume
evidence not rerun here. Initial copy setup omitted non-runtime registration after
discovering it was absent from frozen selection; no export occurred in that attempt.

## Next action
Final owner playtest or explicitly selected itch.io publication of this package.
Keep current ZIP separate from earlier V358. Later UI/character inclusion requires
a new selected snapshot and validation; do not silently swap in shared checkout.
'''
(package/'HANDOFF.md').write_text(handoff,encoding='utf8');(review/'HANDOFF.md').write_text(handoff,encoding='utf8')
closeout=root/'docs/JAMES_RELEASE_CLOSEOUT.md'
with closeout.open('a',encoding='utf8') as stream:
    stream.write(f'\nV365 replaces the local timing candidate: {report["buildId"]}, portable ZIP at\noutput/james-windows-package-v365/{Path(report["package"]).name}.\nExact package asset/startup/Continue/F8 and eight normal workshop cases pass.\nContains the V364 seven-pose rise; excludes later shared UI/character changes.\nKnown art limits remain, and no publication occurred.\n')
print(json.dumps(report),flush=True)
