from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1]
for gear in ['bare','helmet']:
    manifest=json.loads((p/f'{gear}-rise-v5-manifest.json').read_bytes());manifest['states'][0]['frameFiles'][5]=f'res://character/james-floor-case-west-v1/midpoint-body-v1/{gear}/000.png';manifest['name']=f'James West paired body-only rise/shared original case v6 {gear}'
    (p/f'{gear}-rise-v6-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
s=(p/'motion_rise_v5.gd').read_text().replace('bare-rise-v5-manifest.json','bare-rise-v6-manifest.json').replace('helmet-rise-v5-manifest.json','helmet-rise-v6-manifest.json').replace('res://character/james-floor-case-west-v1/body_release_workshop.gd','res://character/james-floor-case-west-v1/shared_case_workshop.gd')
s=s.replace('view.embedded_case and not view.case_enabled and not data.is_empty(),"Midpoint owns case without duplicate prop"','view.case_enabled and not view.embedded_case and not data.is_empty(),"Body-only midpoint uses single original case prop"')
s=s.replace('motion-rise-v5','motion-rise-v6').replace('motion_rise_v5.gd.uid','motion_rise_v6.gd.uid').replace('motion_rise_v5-evidence.json','motion_rise_v6-evidence.json').replace('body_release_workshop.gd.uid','shared_case_workshop.gd.uid')
s=s.replace('V6 separate prop, exact original unload0..4 with paired v4 midpoint5 and canonical registered idle body at6.','V7 exact original cue4 case crop separate prop, exact original unload0..4 with body-only paired midpoint5 and canonical registered idle body6.')
(p/'motion_rise_v6.gd').write_text(s)
s=(p/'review_body_motion.py').read_text().replace('motion_rise_v5','motion_rise_v6').replace('motion-rise-v5','motion-rise-v6').replace('floor-case-west-v6.png','floor-case-west-v7.png')
(p/'review_shared_case_motion.py').write_text(s)
prior=json.loads((p/'motion_rise_v5-inputs.json').read_bytes());paths=[r/k for k in prior]+[p/f for f in ['motion_rise_v6.gd','shared_case_workshop.gd','bare-rise-v6-manifest.json','helmet-rise-v6-manifest.json','midpoint-body-v1/bare/000.png','midpoint-body-v1/helmet/000.png','floor-case-west-v7.png']]
(p/'motion_rise_v6-inputs.json').write_text(json.dumps({str(path.relative_to(r)):hashlib.sha256(path.read_bytes()).hexdigest() for path in paths},indent=2)+'\n')
print('Shared original case through body-only rise and terminal prepared;39targeted inputs frozen.')
