from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1]
for gear in ['bare','helmet']:
    original=json.loads((r/'character/james-cargo-material-joined-v1'/f'{gear}-manifest.json').read_bytes())
    row=next(s for s in original['states'] if s['id']=='unload-west').copy()
    row['frameFiles']=[f'res://character/james-cargo-material-joined-v1/frames/{gear}/unload-west/{i:03d}.png' for i in range(5)]+[f'res://character/james-floor-case-west-v1/rise-v4/{gear}/000.png',f'res://character/james-cargo-material-joined-v1/frames/{gear}/unload-west/005.png']
    row['frameCount']=7;row['frameDurationsMs']=[80,100,100,90,80,80,70]
    for field in ['facings','waterKinds','waterPoses','depthOffsets']:
        if field in row:row[field].insert(5,row[field][4])
    manifest={k:v for k,v in original.items() if k!='states'}
    manifest.update(name=f'James West unload paired rise v4 {gear}',states=[row],status='unselected_native_motion_review_pending')
    (p/f'{gear}-rise-v4-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
s=(p/'floor_state.gd').read_text().replace('bank.get("unload-west",[]).size()!=6','bank.get("unload-west",[]).size()!=7')
(p/'rise_floor_state.gd').write_text(s)
for name in ['floor_actor','floor_player']:
    s=(p/(name+'.gd')).read_text().replace('res://character/james-floor-case-west-v1/floor_state.gd','res://character/james-floor-case-west-v1/rise_floor_state.gd')
    (p/('rise_'+name+'.gd')).write_text(s)
s=(p/'motion_v6.gd').read_text()
s=s.replace('res://character/james-floor-case-west-v1/floor_state.gd','res://character/james-floor-case-west-v1/rise_floor_state.gd').replace('res://character/james-floor-case-west-v1/floor_actor.gd','res://character/james-floor-case-west-v1/rise_floor_actor.gd').replace('res://character/james-floor-case-west-v1/floor_player.gd','res://character/james-floor-case-west-v1/rise_floor_player.gd')
needle='\tgame.grid_view.branforth_player=player;npc.preview_player=player'
s=s.replace(needle,'\tplayer.load_manifest("res://character/james-floor-case-west-v1/bare-rise-v4-manifest.json",true)\n\tcheck(player.load_equipment_manifest("diving-helmet","res://character/james-floor-case-west-v1/helmet-rise-v4-manifest.json"),"Paired rise override loads")\n'+needle)
s=s.replace('var owned:=false;var separate:=false;var embedded:=false','var owned:=false;var separate:=false;var embedded:=false;var midpoint_samples:=0')
s=s.replace('\t\t\towned=owned or', '\t\t\tvar gear:String="" if mode=="bare" else "diving-helmet"\n\t\t\tvar current:Texture2D=game.grid_view._get_branforth_frame(game)\n\t\t\tif current==player.bank_for(gear)["unload-west"][5]:\n\t\t\t\tmidpoint_samples+=1;check(view.embedded_case and not view.case_enabled and not data.is_empty(),"Midpoint owns case without duplicate prop")\n\t\t\towned=owned or')
s=s.replace('\t\tresults.append({"motion":true','\t\tcheck(midpoint_samples>=3,"Actual return displays authored midpoint for at least60ms")\n\t\tresults.append({"midpointSamples":midpoint_samples,"motion":true')
s=s.replace('motion-v6','motion-rise-v4').replace('motion_v6.gd.uid','motion_rise_v4.gd.uid').replace('motion_v6-evidence.json','motion_rise_v4-evidence.json')
s=s.replace('V6 separate prop, original embedded unload frames.','V6 separate prop, exact original unload0..4 and5 with new paired v4 midpoint inserted at5. Original release4 retained; midpoint case suppression verified.')
(p/'motion_rise_v4.gd').write_text(s)
s=(p/'review_motion.py').read_text().replace('motion_v6-evidence.json','motion_rise_v4-evidence.json').replace('motion_v6-inputs.json','motion_rise_v4-inputs.json').replace('motion-v6','motion-rise-v4').replace('motion-review.json','motion-rise-v4-review.json')
(p/'review_rise_motion.py').write_text(s)
prior=json.loads((p/'motion_v6-inputs.json').read_bytes())
paths=[r/k for k in prior]+[p/f for f in ['motion_rise_v4.gd','rise_floor_state.gd','rise_floor_actor.gd','rise_floor_player.gd','bare-rise-v4-manifest.json','helmet-rise-v4-manifest.json','rise-v4/bare/000.png','rise-v4/helmet/000.png']]
(p/'motion_rise_v4-inputs.json').write_text(json.dumps({str(path.relative_to(r)):hashlib.sha256(path.read_bytes()).hexdigest() for path in paths},indent=2)+'\n')
print('Prepared paired7-frame unload override preserving cue4/original endpoints;22targeted inputs frozen.')
