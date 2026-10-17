from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
note='''
Bill south seated breathing/reading staged — September30,2026. Fourgear
states/24refs,960ms loops, exact breathing joins to south sitting endpoint,
six authored tablet-reading poses,shared current idle matte grade/density-aware
hair/face/burgundy masks,native helmet/body preservation.74package and157native
candidate checks pass10.18sec;native82 reviewed;2,914owner non-logfiles unchanged.
South runtime unchanged. Initial2px boot error came from theoretical registration
before alpha resampling; register the resized opaque boot after one fixed atlas
resize,translate only,retain original anatomy/ruler. Validate native again after
registration changes. Reading keeps its prop throughout; loop evidence does not
prove tablet appearance/removal at stage boundaries. Next actual observation sofa,
tool entry/exit,interruption/diskrestore,remaining life/rest and final fullset polish.
Full goal active. Handoff: character/bill-seated-loops-south-v1/FAMILY_HANDOFF.md.
'''
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 with (ROOT/name).open('a',encoding='utf-8') as f:f.write(note)
status=ROOT/'docs/CURRENT_STATUS.md';status.write_bytes(('## Bill south seated loops staged — September30,2026\n'+note+'\n').encode('utf-8')+status.read_bytes())
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(note)
files=[P/'build.py',P/'bare-manifest.json',P/'helmet-manifest.json',P/'registration.json',P/'material-grade.json',P/'frame-hashes.json',P/'verification.json',P/'sources/breathing-v1.png',P/'sources/reading-v1.png',P/'sources/prompt-breathing.txt',P/'sources/prompt-reading.txt',P.parent/'bill-seated-south-coherent-v1/frames/sit-down-south/005.png',P.parent/'bill-seated-helmet-south-coherent-v1/frames/sit-down-south/005.png',P.parent/'bill-seated-helmet-south-coherent-v1/sources/canonical-head.png',P.parent/'crew-runtime-matte-v1/bill/frames/idle-south-matte-v2/000.png',ROOT/'tests/test_bill_seated_loops_south_candidates.gd',ROOT/'tools/run_bill_seated_loops_south_candidate_validation.py']
native=ROOT/'output/bill-seated-loops-south-candidate-native-v1'
data={'status':'staged_candidate','generations':{'breathing':'exec-f025a3f9-f637-4439-a458-5abcab16e672','reading':'exec-3b2ab593-0897-4fc6-8b73-51c2ebbcefde'},'native':json.loads((native/'validation.json').read_text(encoding='utf-8')),'hashes':{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'nativeScreenshotSha256':hashlib.sha256((native/'loaded-water-carry.png').read_bytes()).hexdigest(),'scope':'sprite-plane/life chooser/cosmetic looping;actual sofa/tablet stage joins/selection pending'}
(P/'candidate-evidence.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8');print('Recorded south seated loops and resampled boot registration lesson')
