from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;R=P.parents[1]
for direction in ['north','east','south','west']:
    original=R/('character/james-ward-lifecycle-v1/validate.gd' if direction=='north' else 'character/james-ward-cardinal-v1/'+direction+'.gd')
    s=original.read_text(encoding='utf-8');old='res://character/james-ward-lifecycle-v1/' if direction=='north' else 'res://character/james-ward-cardinal-v1/'+direction+'/'
    s=s.replace(old,'res://character/james-ward-helmet-v1/'+direction+'/')
    s=s.replace('game.Architects.advance_core(game,10)','game.Architects.advance_core(game,10)\n\tcheck(game.branforth_npc.set_helmet_equipped(true),"Prescribed worn gear through supported API; fitting motion outside scope")')
    s=s.replace('player.frames[key].find(source)','player.equipment_frames["diving-helmet"][key].find(source)').replace('game.grid_view.branforth_player.frames[key].find(source)','game.grid_view.branforth_player.equipment_frames["diving-helmet"][key].find(source)')
    s=s.replace('"footViewport":','"helmet":actor.helmet_equipped,"footViewport":')
    s=s.replace('steps+=1','steps+=1\n\t\tcheck(actor.helmet_equipped,"Worn helmet retained throughout paid work")')
    s=s.replace('check(actor.valid_branforth_snapshot(actor.snapshot()),"Ward snapshot admitted")','check(actor.valid_branforth_snapshot(actor.snapshot()),"Ward snapshot admitted")\n\t\tif failures>0:quit(2);return')
    start=s.index('\tif not FileAccess.file_exists(',s.index('func run():'));end=s.index('\tprint(',start)
    s=s[:start]+f'\tif not FileAccess.file_exists("res://character/james-ward-helmet-v1/{direction}.gd.uid"):\n\t\tvar uid:=FileAccess.open("res://character/james-ward-helmet-v1/{direction}.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()));uid.close()\n'+s[end:]
    s=s.replace('JAMES WARD LIFECYCLE:','JAMES WARD HELMET NORTH:').replace('JAMES WARD '+direction.upper()+':','JAMES WARD HELMET '+direction.upper()+':')
    (P/(direction+'.gd')).write_text(s,encoding='utf-8');(P/direction).mkdir(exist_ok=True)
pause=(R/'character/james-ward-lifecycle-v1/pause.gd').read_text(encoding='utf-8').replace('res://character/james-ward-lifecycle-v1/validate.gd','res://character/james-ward-helmet-v1/north.gd')
pause=pause.replace('game.grid_view.branforth_player.frames[key].find(source)','game.grid_view.branforth_player.equipment_frames["diving-helmet"][key].find(source)').replace('"footViewport":','"helmet":actor.helmet_equipped,"footViewport":')
pause=pause.replace('check(Return.valid(actor.snapshot()),','var bad_gear:Dictionary=actor.snapshot();bad_gear.branforth_hull_return.equipment="";check(not Return.valid(bad_gear),"Reject wrong return equipment")\n\t\t\tcheck(Return.valid(actor.snapshot()),')
pause=pause.replace('var bad:Dictionary=actor.snapshot();','var wrong_gear:Dictionary=actor.snapshot();wrong_gear.branforth_hull_resume.equipment="";check(not Resume.valid(wrong_gear),"Reject wrong resume equipment")\n\t\t\tvar bad:Dictionary=actor.snapshot();')
pause=pause.replace('OUT+"pause.gd.uid"','"res://character/james-ward-helmet-v1/pause.gd.uid"').replace('JAMES WARD PAUSE:','JAMES WARD HELMET PAUSE:')
(P/'pause.gd').write_text(pause,encoding='utf-8')
for fixture in ['hull_regression','bill_compat']:
    s=(R/'character/james-ward-lifecycle-v1'/f'{fixture}.gd').read_text(encoding='utf-8').replace('res://character/james-ward-lifecycle-v1/','res://character/james-ward-helmet-v1/')
    (P/(fixture+'.gd')).write_text(s,encoding='utf-8')
files=['scripts/branforth_npc.gd','scripts/bill_npc.gd','scripts/ward_repair.gd','scripts/james_hull_resume.gd','scripts/james_hull_return.gd','scripts/james_construction_motion.gd','scripts/station_effects.gd','scripts/grid_canvas.gd','character/james-torch-material-residue-v2/bare-manifest.json','character/james-torch-material-residue-v2/helmet-manifest.json','character/james-repair-contact-v1/torch-tip-offsets.json']
(P/'runtime-input-before.json').write_text(json.dumps({f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in files},indent=2)+'\n',encoding='utf-8')
print('Four helmet lifecycle fixtures, pause/gear admission and two compatibility fixtures; ten frozen input hashes')
