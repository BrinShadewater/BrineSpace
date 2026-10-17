import hashlib,json,py_compile,subprocess
from pathlib import Path
from PIL import Image
from milestone_notes import insert_status
root=Path.cwd();bank=root/'character/james-west-carry-walk-keys-v1';out=bank/'north-unload-installed-rise-v364'
installed=json.loads((out/'installation.json').read_text());native=json.loads((out/'normal-evidence.json').read_text());validation=json.loads((out/'normal-validation.json').read_text())
assert native['checks']==136 and native['failures']==0 and native['captures']==7
assert validation['exitCode']==0 and validation['ownerUnchanged'] and not validation['profileDelta']
for key in ['sourceFrameHashes','joinedSourceFrameHashes']:
    assert all(hashlib.sha256((root/f).read_bytes()).hexdigest()==h for f,h in installed[key].items())
for folder in ['james-cargo-north-v1','james-cargo-material-joined-v1']:
    for name in ['build_pickup.py','build.py','verify.py','unload_timing.py']:
        file=root/'character'/folder/name
        if file.exists():py_compile.compile(str(file),doraise=True)
images=[Image.open(out/f'normal-{i:02}.png').convert('RGB') for i in range(7)]
images[0].save(out/'installed-motion.png',save_all=True,append_images=images[1:],duration=[80,100,100,90,40,40,720],loop=0,disposal=0,blend=0)
source=bank/'north-unload-reused-rise-v363'
(out/'playback.json').write_bytes((source/'playback.json').read_bytes())
page=(source/'index.html').read_text().replace('unselected seven-pose timing study','installed seven-pose timing').replace('Accepted unload on the left','Previous unload on the left')
page=page.replace("ctx.fillText(row.gear+' '+row.direction", "ctx.fillText(row.gear.replace('current','previous').replace('candidate','installed')+' '+row.direction")
(out/'index.html').write_text(page,encoding='utf8')
for file in out.glob('*.png'):
    attr=subprocess.run(['git','check-attr','filter','--',str(file.relative_to(root))],capture_output=True,text=True,check=True)
    assert attr.stdout.rstrip().endswith(': lfs')
report={'version':364,'selected':True,'normalLoaderVerified':True,'newArtwork':0,'sourceImagesUnchanged':180,'totalMs':520,
    'pythonChecks':{'northSource':160,'matchedMaterial':1029},'normalLoaderChecks':136,'failures':0,
    'normalCapturesViewed':7,'pairedEquipmentSizes':[148,82,54,27],
    'nativeWorkshopEvidence':'V363 exact V351 package fixture-only resequencing:1912checks0/eight layout-gear cases. Normal installed-loader proof is this V364 current-project probe, not a rebuilt package.',
    'failedSetupPreserved':'first-overridden-run: base manifest edit was overridden by matched-material bank; final admission updates both layers. Failed probe stopped after error, owner unchanged.',
    'ownerUnchanged':True,'packageRebuilt':False,
    'limits':'Known crouch/material/arm and North floor-case limits remain. Builders syntax checked, not fully regenerated. Native capture phases do not certify uninterrupted real-time visual acceptance.',
    'next':'Freeze a new selected James release snapshot and export/audit the timing change before including it in a shipped package; exclude unrelated concurrent source changes unless selected.'}
(out/'review.json').write_text(json.dumps(report,indent=2)+'\n')
section='''### James North mid-rise timing installed — October 4, 2026

V364 normal paired North unload now seven poses520ms: reuses approved mid-rise
before standing, splitting original80ms return hold40+40; last crown rise31px becomes
13+18px. Source North and final matched-material override manifests updated with
exact existing file references.180 original PNGs unchanged. Builders reproduce
reuse paths without replacing old endpoint files; verifiers160+1029checks0.
Current normal Grid selected loader136checks0, all seven native paired gear/four-size
captures viewed; scratch owner unchanged. First overridden-loader attempt retained
under first-overridden-run; source-only edit had been superseded by material bank.
V363 actual workshop eight-case lifecycle proof retains fixture scope. No new art,
recolour, case behavior or export; V358 ZIP lacks this timing change. Known material,
stance/arm/case and continuous acceptance limits remain. Next freeze/export selected
James timing revision, keeping unrelated shared work out unless owner-selected.
Evidence: character/james-west-carry-walk-keys-v1/north-unload-installed-rise-v364/.
'''
insert_status(root/'docs/CURRENT_STATUS.md',section,'### James reused North unload rise — October 4, 2026')
ledger=bank/'material-repair-progress.json';data=json.loads(ledger.read_text());data['northUnloadInstalledRise']=report;data['nextVisualRepair']=report['next'];ledger.write_text(json.dumps(data,indent=2)+'\n')
(out/'HANDOFF.md').write_text('''# Project handoff

Updated: October 4, 2026 · Project: Brine Space · Task: James North rise admission

## Objective and acceptance
Finish James and prepare the next release. Seven-pose North return now installed
in actual selected source/material banks with matching helmet and original timing.

## Accepted decisions and constraints
Reuse approved artwork, preserve exact source pixels, pickups/carries, foot pivot
and520ms total. Keep staged generated alternatives out. Owner saves isolated.

## Current state
Paired North source and matched-material manifests; source timing helper/builders/
verifiers; matched-material registration; V364 install/probe/run/close helpers,
before-state backups, native evidence/validation, seven captures and playback movie.
CURRENT_STATUS, closeout and ledger updated. No production script or image changes.

## Verification
160 source and1029 material checks0. Normal Grid selected loader136checks0;
seven native poses in both gears at148/82/54/27 viewed.180 source PNGs unchanged.
First overridden probe preserved; final loader check addresses actual final bank.
Scratch owner unchanged. V363 eight-case real workshop evidence retains fixture
scope. Builders syntax checked, not regenerated. Continuous movie supplied, not
continuously watched. Existing stance/material/arm/North case limits unchanged.

## Next action
Freeze new James release revision with only these selected changes, export and
audit before shipping. Existing V358 ZIP contains earlier six-pose timing. Later
concurrent UI/character inclusion and itch publication remain owner choices.
''',encoding='utf8')
print(json.dumps({'selected':True,'normalLoaderChecks':136,'pythonChecks':1189,'failures':0,'sourceImagesUnchanged':180,'packageRebuilt':False}))
