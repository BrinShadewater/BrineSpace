from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
reports={}
for direction,reference in [('east','veld-helmet-fitting-east-v2/body-underlay-source.png'),('west','veld-carry-west-consistent-v1/source-master-v7.png'),('north','veld-carry-north-consistent-v1/source-v2.png'),('south','veld-carry-south-consistent-v1/source-v3.png')]:
 src=P.parent/f'veld-recover-air-{direction}-coherent-v1';r=json.loads((src/'registration.json').read_text());hr=json.loads((src/'helmet-registration.json').read_text());native=ROOT/f'output/veld-recover-air-{direction}-candidate-native-v1'
 reports[direction]={'provider':r['provider'],'rawSha256':sha(src/r['source']),'promptSha256':sha(src/'sources/prompt-v1.txt'),'selectedBareAuthority':r['idleAuthority'],'selectedBareSha256':r['idleSha256'],'helmetAuthority':hr['donor'],'helmetSha256':hr['donorSha256'],'constructionReference':reference,'constructionReferenceSha256':sha(P.parent/reference),'package':json.loads((src/'validation.json').read_text()),'native':json.loads((native/'validation.json').read_text()),'nativeLogSha256':sha(native/'native.log'),'nativeContactSha256':sha(native/'loaded-water-carry.png')}
 for file in ['manifest.json','helmet-manifest.json','registration.json','helmet-registration.json','material-grade.json']:reports[direction][file+'Sha256']=sha(src/file)
(P/'candidate-evidence.json').write_text(json.dumps({'directions':reports,'familyChecks':json.loads((P/'family-checks.json').read_text()),'sourceBindingsSha256':sha(P/'source-bindings.json'),'status':'staged_candidate','nativeVisualReview':'82px all48poses;148/82paired boards;continuous motion review remains','realJourneyDiskRestoreInstallation':'not yet verified'},indent=2)+'\n')
lesson='''

## Veld cardinal dry recovery candidate — September 30, 2026

Four independent views stage8gear states/48refs. Directional161package and
56consolidation checks pass;372candidate native checks pass across4fixtures.
Native82allposes reviewed;real profile unchanged. Retain actual selected idle
ends,side-specific instruments/vials,one frozen ruler/pooled grade per source,
and authored wholebody bends with planted soles. Source atlases can change shape:
derive row sorting from actual image height, not a hardcoded512 boundary.
Sagittal bends in front/rear views are not sideways image rotation. Rear shell
can follow authored skull foreshortening with native width and fixed collar;
preserve component identity and body below fitted collar. Frontal helmet retains
native component; finer visor/top-shell pitch still requires motion polish review.
Chooser/clock/pixel proof does not establish actual low-air journeys,disk restores,
clearance or selection. Those checks are next. Full life/distress/death/rest and
cross-family polish goal remains. Evidence:
character/veld-recover-air-family-coherent-v1/HANDOFF.md.
'''
for name in ['docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','docs/VELD_ANIMATION_CONTINUATION_2026-09-29.md','skills/brinespace-character-pipeline/references/crew-consistency.md','C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md']:
 f=Path(name) if Path(name).is_absolute() else ROOT/name
 with f.open('a',encoding='utf-8') as stream:stream.write(lesson)
f=ROOT/'docs/CURRENT_STATUS.md';text=f.read_text(encoding='utf-8');heading='''## Veld cardinal dry recovery family staged — September 30, 2026

Eightgear states/48refs from4independent sources,exact selected idle ends,
planted soles,master-matched materials and native directional helmets.161package,
56family consolidation and372candidate native checks PASS;all4native82boards
reviewed,engine errors0,2,914real non-logfiles unchanged. Runtime remains unchanged.
Actual air-trigger journeys,interruptions/disk restores,clearance and complete
motion/helmet pitch review precede selection. Remaining life/rest/distress/death
and broad full-set polish goal active. [Handoff](../character/veld-recover-air-family-coherent-v1/HANDOFF.md).

''';f.write_text(heading+text,encoding='utf-8')
print('Recorded4-view recovery candidate evidence and lessons;runtime unchanged')
