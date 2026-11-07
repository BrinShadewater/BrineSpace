"""Publish source evidence without implying a stationary or integrated gait join."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-south-start-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    request=json.loads((BASE/'sources/start-01.request.json').read_text());recipe=json.loads((BASE/'candidate-02/recipe.json').read_text())
    assert sha(BASE/'sources/start-01.raw.png')==request['rawSha256']==recipe['rawSha256']
    assert sha(BASE/'sources/start-01.prompt.txt')==request['promptSha256']
    for ref in request['orderedReferences']:assert sha(ROOT/ref['path'])==ref['sha256']
    assert recipe['gaitJoinSupportDepthDeltaDense']==6
    out=BASE/'review';out.mkdir(exist_ok=True)
    evidence={'normalAdmission':False,'generation':request,'registration':recipe,'scope':'Static source comparison; four generated figures, one shared neutral scale, three interiors plus exact idle/gait4 endpoints. Native root/controller/grade/continuous motion/save/title not verified. Raw source reverses requested lead. Earlier load registration failure preserved.','inputs':{str(p.relative_to(ROOT)):sha(p) for p in [BASE/'candidate-02/recipe.json',BASE/'candidate-02/manifest.json',ROOT/'tools/build_marsh_south_start.py']}}
    (out/'verification.json').write_text(json.dumps(evidence,indent=2)+'\n')
    html='<!doctype html><meta charset="utf-8"><title>Marsh South walking-start source</title><style>body{background:#17282c;color:#e4e7dd;font:17px system-ui;margin:30px auto;max-width:1200px}img{max-width:100%;image-rendering:pixelated}</style><h1>South walking start: unselected source study</h1><p>Built-in imagegen, original South identity master plus selected idle/gait references. Raw four figures retained; common neutral-ruler scale, whole figures only, no grading/anatomy patching. Source advances anatomical LEFT/viewer RIGHT instead of requested opposite foot; staged toward selected gait slot4, not a claim of right-leading source.</p><h2>Corrected two-foot registration</h2><img src="../candidate-02/comparison.png"><p>The weight-load anchor averages separately measured boot centroids; selecting only the lowest sole row had shifted the whole body sideways12pixels. Final support differs6dense pixels from exact gait4. A stationary-root start would visibly pop: bridge with source-aware root advance of'+str(round(recipe['gaitJoinRootAdvanceWorld'],3))+'world units before admission. Proposed gait join.48s. Five80ms presentation slots, three generated interiors; neutral ruler is a reference, not another action pose. Native motion and actual controller remain pending; torso grade/identity and joins need native comparison.</p><h2>Rejected first extraction</h2><img src="../candidate-01/comparison.png"><h2>Untouched raw result</h2><img src="../sources/start-01.raw.png"><p><a href="../sources/start-01.prompt.txt">Exact prompt</a> · <a href="verification.json">Ordered reference hashes and registration evidence</a></p>'
    (out/'index.html').write_text(html);print('Unselected South source review saved;6dense/%.3fworld join remains to bridge'%recipe['gaitJoinRootAdvanceWorld'])
if __name__=='__main__':main()
