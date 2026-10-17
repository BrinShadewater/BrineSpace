from pathlib import Path
import hashlib,json
from PIL import Image

ROOT=Path(__file__).resolve().parent
MASTERS=ROOT.parent/'kris-krug-masters-v1'
contract=json.loads((MASTERS/'manifest.json').read_text(encoding='utf-8'))
east=next(v for v in contract['views'] if v['direction']=='east')
atlas=Image.open(MASTERS/'source-atlas.png').convert('RGBA')
body=atlas.crop(east['source_bounds'])
input=Image.new('RGB',(896,1024),'#00ff00')
position=(448-body.width//2,920-body.height)
input.paste(body,position,body)
common='Locked static camera, exact same full-body man and right-facing east profile throughout, both boots fully visible. Preserve glasses, long beard, receding tied-back hair, wrap suit, pale collar, shoulder markings, tablet and wafer pouch. Same stature and graphite matte colors throughout. Solid uniform bright green chroma background, no floor, shadow, camera movement or zoom. '
prompts={
 'idle-east':common+'He stands still with both boots planted. Only very subtle relaxed chest breathing and one natural blink; head and body stay steady. No stepping, turning, gesturing or speaking. Finish in the same neutral standing pose.',
 'walk-east':common+'He walks naturally in place toward screen-right at a steady unhurried ordinary walking pace. Show at least two complete alternating left and right step cycles, feet lifting and contacting a consistent ground line, coordinated restrained arm swing, believable weight transfer, tiny body sway. Neither running nor shuffling. Keep full gait including both legs and all equipment coherent; no sliding on one fixed foot.',
 'tablet-east':common+'From relaxed standing, he draws the rugged tablet from his anatomical left hip, raises it comfortably in front of his waist, looks down slightly and uses the opposite glove to tap the screen twice deliberately, checking conflicting directives. Then lowers and returns the same tablet to the same left hip holster, hands returning to relaxed standing. Boots remain planted, no turning or walking. One continuous clear raise, inspect, tap, lower, holster sequence; no duplicated tablet, no extra equipment.'
}
for state,prompt in prompts.items():
    dest=ROOT/state;dest.mkdir(parents=True,exist_ok=True)
    assert not (dest/'generation.json').exists(), 'Existing ledger; never overwrite/re-submit'
    input.save(dest/'master-input.png')
    (dest/'prompt.txt').write_text(prompt,encoding='utf-8')
(ROOT/'input-contract.json').write_text(json.dumps({'canonical_master':'res://character/kris-krug-masters-v1/rotations/east.png',
 'atlas_sha256':hashlib.sha256((MASTERS/'source-atlas.png').read_bytes()).hexdigest(),
 'whole_source_bounds':east['source_bounds'],'input_size':[896,1024],'body_position':position,
 'states':list(prompts),'scope':'Representative raw source motion study; no normal runtime integration',
 'budget':'Three ordinary Fast2.3 6s768P attempts, estimated USD0.57 total; not verified billing'},indent=2),encoding='utf-8')
print('Prepared three exact shared-identity inputs and distinct action prompts; no provider submission yet.')
