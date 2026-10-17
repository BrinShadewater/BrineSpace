from pathlib import Path
import json,hashlib,subprocess,sys,urllib.request
P=Path(__file__).resolve().parent;R=P.parents[1];D=P/'north-west-candidate-v4';S=P/'candidate-v7'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def package(d):return list((d/'frames').rglob('*.png'))+[d/'bare-manifest.json',d/'helmet-manifest.json',d/'registration.json',d/'paired-turn-contact.png']
for d,args in [(D,['north-west','4']),(S,[])]:
    paths=package(d);before={str(p):sha(p) for p in paths};assert len(before)==16
    subprocess.run([sys.executable,str(P/'build_candidate.py')]+args,check=True,capture_output=True)
    assert before=={str(p):sha(p) for p in paths},'Package rebuilt differently: '+str(d)
# Shared West is a WHOLE canonical frame in both independent quarter families.
for gear in ['bare','helmet']:
    canonical=R/f'character/veld-cargo-west-master-family-v1/frames/{gear}/unload-west/000.png'
    assert sha(D/f'frames/{gear}/005.png')==sha(S/f'frames/{gear}/005.png')==sha(canonical)
e=D/'native-review-evidence.json';data=json.loads(e.read_text(encoding='utf-8'));assert data['validation']['passed'] and data['decodedNativeSamplesExact']==104
data.update(visualReview='All4chronological native boards/104source-native samples viewed; all12pairedwholefigures/6enlargedhelmet views and6source/head/grip/equipment views inspected. Smaller original proportions, correct rear-to-left sequence, planted adjacent feet and gear occlusion retained. Sampled source/registration review accepted for continued candidate work.',continuousNativeMotionReviewed=False,normalAdoption=False,deterministicPackageFiles=16,previousSouthWestPackageFilesUnchanged=16,sharedWestWholeFrameAliasesExact=True)
e.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
source=P/'north-west-v4-study/review-evidence.json';a=json.loads(source.read_text(encoding='utf-8'));a['visualReview']='All6 source/head/grip/equipment details viewed: coherent smaller head projections23/24/26/28/29/29, planted adjacent feet/rear-to-left angle order and equipment occlusion. Canonical whole West alias retained in paired package; not normal/gameplay acceptance.';source.write_text(json.dumps(a,indent=2)+'\n',encoding='utf-8')
heading='## Veld paired North–West master turn candidate — October 2, 2026'
block=heading+'''

Unselected character/veld-cargo-turns-master-family-v1/north-west-candidate-v4
adds independent authored rear-to-left turn matching original North master and
corrected West family. V1/2 edits retain oversized31pxWest head/tuckedcase,
rejected. V3 direct master authoring improves projections but rear boots spread,
rejected; V4 narrow wholefigure foot repair restores adjacent planted stance.
All6source/detail views inspected; projections23/24/26/28/29/29 through rear/side.
SinglefirstNorth148ruler, shared West material recipe; no perpose anatomy scale.

Existing shared North/West angular helmet source/recipe and exactNorthshell,
whole corrected Westheld bare/equipped aliases.12exports/4quarterstates retain
800msfinite/reverse metadata.32source/22pairchecks,16deterministicfiles stable;
previousSouthWest16packagefiles also unchanged after generalized localbuilder.
Bothfamilies/gearWestendpoints byte-identical to correctedheld wholeframes.

Standalone actualCrewSpritePlayer649nativechecks0fail8.36s/104prescribedsamples,
bothdirections/gears/all6slots/terminal/sourcebinding/47/93/148rulers.107targeted
inputs/2931owner non-logfiles unchanged/scratchAPPDATA;engine0/cleanlog. All4
chronologicalboards/104source-nativepairs and12pairedwhole/6helmetdetailviews
inspected;104exactRGBdecodebindings/866mspreview includes terminalhold/reset.
No full continuous/nativecadence/world/controller/ownership/Continue/normal
adoption or full-set acceptance. No production controller/room/selection change.

Lesson: direct masters can restore the master's wider standing stance while
violating accepted turn feet-together stance. Keep identity/proportion and action
stance constraints separate; author a narrow wholefigure repair and review all
angles again. One shared canonical endpoint is a wholepose, not a pastedhead or
case strip. Remaining East/South/Northheld/cardinalseams and halfturns need full
master review before actual cargo lifecycle/normal installation; full Veld set
and cross-library polish remain active/incomplete. Evidence/HANDOFF in turnstudy.

'''
refs=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for p in refs:
    original=p.read_bytes();text=original.decode('utf-8')
    if heading in text:continue
    tmp=p.with_name(p.name+'.veld-north-turn.tmp');tmp.write_text(block+text,encoding='utf-8');assert p.read_bytes()==original,'Concurrent edit '+str(p);tmp.replace(p)
review='''
## North–West paired milestone — October 2, 2026
Four independent North–West raws/prompts/refs/execution records retained; exact
originalNorthcrop[0,0,512,512] and correctedSouthWestv7Westcrop[1772,0,2126,740]
reference provenance. V1/2oversizedhead/tuckedcase rejected, V3widefeet rejected;
V4 restores feet-together wholefigures.6source/detail/12pairedwhole/6helmet detail
and all4nativeboards/104source-native presentations inspected. Northshared shell
and existingangularheads fitted; canonicalWestwholeframes exact across both
quarterfamilies/gears.32source/22pair/649nativechecks0fail8.36s,107inputs/2931owner
unchanged/scratchAPPDATA,104lossless nativeRGBdecode bindings. North16deterministic
packagefiles stable and previousSouth16unchanged through generalizedbuilder.
Candidate remains unselected; no continuous/nativecadence/world/owneracceptance.
Next remaining quarter/cardinal master seams, halfturns and cargo actualworld
controller/propownership/save lifecycle, then full-library polish.
'''
p=P/'SOURCE_REVIEW.md';old=p.read_text(encoding='utf-8')
if '## North–West paired milestone' not in old:p.write_text(old+review,encoding='utf-8')
handoff='''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Veld cargo master turns

## Objective and acceptance
Finish full master-consistent Veld set then cross-library polish. Actual
controller/room/prop/save lifecycle and visually coherent joins before adoption.

## Accepted decisions and constraints
Authored complete bodies, original anatomy/master detail and matte grade, one
148ruler per independently authored quarter, feet together/planted,800msfinite
and exactreverse. Immutable sharedhelmet construction; wholecanonicalendpoints.

## Current state
SouthWestcandidate-v7 and independentNorthWestnorth-west-candidate-v4 each hold
12pairedexports/4quarterstates plus registration/source/native reviews/APNG/HTML.
SevenSouthWest/fourNorthWest rawsources/prompts/refs/executions retained. Existing
angularhelmet components fitted, exactSouth/Northmasters; bothWestwholeendpoints
byte-identical to correctedWestheld bare/equipped. Both staged/notinstalled.
New paired NorthWest fixture/UID/isolated runner, generalizedlocal builders;
no production selection/controller/room/ownergeometry changes.

## Verification
Each32source/22pairchecks and16stable deterministicpackagefiles. North649native
checks0fail8.36s/104prescribed30Hzsamples bothdirections/gears;South prior6490fail
8.4s/104samples. North107inputs/2931owner non-logfiles unchanged/scratchAPPDATA.
All4Northboards/104source-nativepairs plus12pairedwhole/6helmetdetails reviewed;
104exactRGBdecodebindings/866mspreview(original800msfinite plushold/reset).
South16packagefiles unchanged after generalized builder, sharedWestaliases exact.
No full continuous/cadence/naturaltraffic/world/controller/ownership/Continue or
normal/fullset acceptance. Rejected drafts retain original reasons/evidence.

## Next action
Inspect remaining NorthEast/EastSouth quarters and North/East/South held endpoints
against masters; reconcile allcardinal/sharedhalfturn joins before actualcargo
controller/room/caseownership/freshContinue validation and normal adoption.
Fullset/cross-library fidelity/polish remain active/incomplete.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
url='http://127.0.0.1:8791/character/veld-cargo-turns-master-family-v1/north-west-candidate-v4/?v=paired-master-v4'
r=urllib.request.urlopen(url,timeout=5);assert r.read()==(D/'index.html').read_bytes()
print('North16deterministicfiles/South16unchanged/sharedWest2gearaliases exact;5refs/HANDOFF recorded;previewHTTP200 exactbytes. Fullgoalactive.')
