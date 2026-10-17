from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1]
for gear in ['bare','helmet']:
    manifest=json.loads((p/f'{gear}-rise-v4-manifest.json').read_bytes())
    manifest['states'][0]['frameFiles'][6]=f'res://character/james-floor-case-west-v1/standing-body-v2/{gear}/000.png'
    manifest['name']=f'James West unload canonical terminal body v5 {gear}'
    (p/f'{gear}-rise-v5-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
s=(p/'motion_rise_v4.gd').read_text().replace('bare-rise-v4-manifest.json','bare-rise-v5-manifest.json').replace('helmet-rise-v4-manifest.json','helmet-rise-v5-manifest.json').replace('res://character/james-floor-case-west-v1/release_workshop_v6.gd','res://character/james-floor-case-west-v1/body_release_workshop.gd')
s=s.replace('var midpoint_samples:=0','var midpoint_samples:=0;var body_samples:=0')
s=s.replace('\t\t\towned=owned or','\t\t\tif current==player.bank_for(gear)["unload-west"][6]:\n\t\t\t\tbody_samples+=1;check(view.case_enabled and not view.embedded_case and not data.is_empty(),"Canonical terminal body uses single separate case")\n\t\t\towned=owned or')
s=s.replace('\t\tresults.append({"midpointSamples":','\t\tcheck(body_samples>=3,"Canonical body displayed at least60ms")\n\t\tresults.append({"bodySamples":body_samples,"midpointSamples":')
s=s.replace('motion-rise-v4','motion-rise-v5').replace('motion_rise_v4.gd.uid','motion_rise_v5.gd.uid').replace('motion_rise_v4-evidence.json','motion_rise_v5-evidence.json')
s=s.replace('retain original standing5 at6','replace original standing5 with canonical registered idle body at6').replace('exact original unload0..4 and5 with new paired v4 midpoint inserted at5','exact original unload0..4 with paired v4 midpoint5 and canonical registered idle body at6')
s=s.replace('var f:=FileAccess.open(OUT+"motion_rise_v5-evidence.json"','if not FileAccess.file_exists(OUT+"body_release_workshop.gd.uid"):\n\t\tvar uid:=FileAccess.open(OUT+"body_release_workshop.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))\n\tvar f:=FileAccess.open(OUT+"motion_rise_v5-evidence.json"')
(p/'motion_rise_v5.gd').write_text(s)
s=(p/'review_rise_motion.py').read_text().replace('motion_rise_v4','motion_rise_v5').replace('motion-rise-v4','motion-rise-v5').replace('14targeted hashes unchanged.',"'+str(len(inputs))+'targeted hashes unchanged.")
(p/'review_body_motion.py').write_text(s)
prior=json.loads((p/'motion_rise_v4-inputs.json').read_bytes());paths=[r/k for k in prior]+[p/f for f in ['motion_rise_v5.gd','body_release_workshop.gd','bare-rise-v5-manifest.json','helmet-rise-v5-manifest.json','standing-body-v2/bare/000.png','standing-body-v2/helmet/000.png']]
bindings=json.loads((p/'canonical-standing-bindings.json').read_bytes())
paths += [r/b[field] for b in bindings.values() for field in ['source','manifest']]
(p/'motion_rise_v5-inputs.json').write_text(json.dumps({str(path.relative_to(r)):hashlib.sha256(path.read_bytes()).hexdigest() for path in paths},indent=2)+'\n')
print('Canonical terminal body/early separate case replay prepared; explicit original cue4 retained.')
