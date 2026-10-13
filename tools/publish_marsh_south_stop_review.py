"""Bind the rejected South-stop source review to its actual artwork/provenance."""
from pathlib import Path
import hashlib
import json
import numpy as np
from PIL import Image
from build_marsh_south_start import sole

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'character/marsh-south-stop-v1'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    checks = 0
    def check(condition, message):
        nonlocal checks
        assert condition, message
        checks += 1
    for version in ['01', '02', '03']:
        request = json.loads((BASE/f'sources/stop-phase4-{version}.request.json').read_text(encoding='utf-8'))
        check(sha(BASE/f'sources/stop-phase4-{version}.raw.png') == request['rawSha256'], 'raw generation changed')
        for reference in request['orderedReferences']:
            check(sha(ROOT/reference['path']) == reference['sha256'], 'ordered reference changed')
    for record in json.loads((ROOT/'character/marsh-south-walk-material-v1/baseline.json').read_text())['states']:
        check(sha(ROOT/record['path']) == record['sha256'], 'normal South gait changed')
    out = BASE/'candidate-03/phase-4'
    recipe = json.loads((out/'recipe.json').read_text(encoding='utf-8'))
    manifest = json.loads((out/'manifest.json').read_text())
    check([manifest['frameWidth'], manifest['frameHeight'], manifest['pivot'], manifest['standingHeight']] == [184,184,[92,172],148], 'density/pivot contract')
    state = manifest['states'][0]
    check(state['frameDurationsMs'] == [80]*5 and state['loop'] is False, 'finite timing')
    images = [Image.open(out/file).convert('RGBA') for file in state['frameFiles']]
    check(sha(out/'000.png') == recipe['gaitSha256'], 'exact gait endpoint')
    check(sha(out/'004.png') == recipe['idleSha256'], 'exact idle endpoint')
    with Image.open(out/'source-motion.apng') as motion:
        check(motion.n_frames == 5, 'APNG slot count')
        for index, image in enumerate(images):
            motion.seek(index)
            check(np.array_equal(np.array(motion.convert('RGBA')), np.array(image)), 'APNG decoded pose differs')
            check(sha(out/state['frameFiles'][index]) == recipe['frameHashes'][state['frameFiles'][index]], 'packed frame changed')
    contacts = [{'left':sole(image, True), 'right':sole(image, False)} for image in images]
    verdict = {
        'status':'rejected source study; normalAdmission false', 'packagingChecks':checks,
        'normalSouthGaitUnchanged':True, 'sourcePhase':4, 'contacts':contacts,
        'leftBootExtraLiftDense':contacts[0]['left'][1]-contacts[1]['left'][1],
        'rightBootTerminalLateralSeamDense':contacts[-1]['right'][0]-contacts[-2]['right'][0],
        'rightBootTerminalDepthSeamDense':contacts[-1]['right'][1]-contacts[-2]['right'][1],
        'normalAdmission':False,
        'visualDecision':'03 corrects recovering leg but raises it excessively, omits right-foot lateral closing, and exposes master-ivory versus selected-idle dark lower-leg material mismatch. Not accepted for motion/native review.',
        'limits':'Static exact packaging and visual source inspection only. No Godot execution, root/contact controller, arbitrary gait phase, safety, saves or title Continue. No owner profile writes.',
        'next':'Resolve a master-matched staged idle material endpoint and regenerate subtle phase4 recovery/closing with actual sole targets; inspect both feet, head/hips and whole-body scale before native work.'}
    recipe.update(status=verdict['status'], visualDecision=verdict['visualDecision'])
    (out/'recipe.json').write_text(json.dumps(recipe,indent=2)+'\n',encoding='utf-8')
    request_path=BASE/'sources/stop-phase4-03.request.json'
    request=json.loads(request_path.read_text(encoding='utf-8'));request['status']=verdict['status']
    request_path.write_text(json.dumps(request,indent=2)+'\n',encoding='utf-8')
    verdict['boundFiles'] = {path.relative_to(ROOT).as_posix():sha(path) for path in
        [out/'manifest.json',out/'recipe.json',out/'comparison-2x.png',out/'source-motion.apng']+
        [out/file for file in state['frameFiles']]+
        [BASE/f'sources/stop-phase4-{version}.{suffix}' for version in ['01','02','03'] for suffix in ['raw.png','prompt.txt','request.json']]+
        [Path(__file__),ROOT/'tools/build_marsh_south_stop.py']}
    (BASE/'verification.json').write_text(json.dumps(verdict,indent=2)+'\n',encoding='utf-8')
    html='''<!doctype html><meta charset="utf-8"><title>Marsh South stop — rejected studies</title>
<style>body{background:#18272b;color:#e9ece4;font:17px system-ui;max-width:1400px;margin:35px auto;padding:16px}a{color:#badbda}img{max-width:100%;background:#293b40}h1{font-size:28px}table{border-collapse:collapse}td,th{padding:8px;border:1px solid #607174}</style>
<h1>South phase-4 stopping studies — rejected</h1>
<p>Three source attempts retained. No normal admission or native acceptance.</p>
<p>01 and its coherent repair02 lift the wrong foot. 03 fixes the side, but the recovering left boot rises12dense pixels beyond gait4 and the terminal right boot has a7dense-pixel lateral gap (3.088world at the existing scale). The last interior also follows master ivory shins while selected idle has dark lower legs. Repair that family endpoint before accepting a stop.</p>
<h2>Exact gait4 → three authored interiors → exact idle</h2>
<img src="candidate-03/phase-4/comparison-2x.png"><p>Nearest-neighbor2× comparison. Whole-figure shared neutral scale, no anatomy patch or color grade.</p>
<p><a href="candidate-03/phase-4/source-motion.apng">Source animation</a> · <a href="verification.json">Bound evidence and contacts</a> · <a href="candidate-03/phase-4/recipe.json">Extraction recipe</a></p>
<h2>Original South identity master</h2><img style="max-height:600px" src="../marsh-motion-polish-v1/sources/south-standing-identity-01.png">
<h2>Rejected sources and provenance</h2>'''
    for version in ['01','02','03']:
        html+=f'<h3>Source {version}</h3><img src="sources/stop-phase4-{version}.raw.png"><p><a href="sources/stop-phase4-{version}.prompt.txt">Exact prompt</a> · <a href="sources/stop-phase4-{version}.request.json">Ordered references and generation</a></p>'
    html+=f'<p>{checks} packaging/provenance checks passed; five APNG poses match decoded source RGBA. These checks do not override the visual rejection. Existing normal six-frame South gait and idle endpoint unchanged. No Godot tests/probes run for rejected artwork.</p>'
    (BASE/'index.html').write_text(html,encoding='utf-8')
    print(f'{checks} static packaging/provenance checks; source rejected: extra lift12dense, terminal lateral seam7dense; no normal admission')

if __name__ == '__main__':
    main()
