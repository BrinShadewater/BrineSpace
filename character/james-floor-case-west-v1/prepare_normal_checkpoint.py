from pathlib import Path
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1]
s=(p/'checkpoint_probe_v2.gd').read_text()
s=s.replace('preload("res://character/james-floor-case-west-v1/checkpoint_v2.gd")','preload("res://character/james-floor-case-west-v1/normal_checkpoint_facade.gd")')
a=s.index('func install_candidate()');z=s.index('func run()',a)
s=s[:a]+'''func install_candidate()->Dictionary:
	var player=game.grid_view.branforth_player
	player.game=game
	var view=game.grid_view._bill_room_view({"id":"salvage_workshop","pos":ORIGIN})
	check(player.get_script().resource_path=="res://scripts/james_cargo_player.gd","Normal player factory")
	check(view.get_script().resource_path=="res://scripts/james_cargo_workshop.gd","Normal renderer selection")
	return {"player":player,"view":view}
''' +s[z:]
a=s.index('\tnpc=preload("res://character/james-floor-case-west-v1/checkpoint_floor_actor_v2.gd").new()')
z=s.index('\tvar stations:Array=',a)
s=s[:a]+'''\tvar installed_normal:Dictionary=install_candidate()
	player=installed_normal.player;npc.preview_player=player
''' +s[z:]
a=s.index('\tvar view=preload("res://character/james-floor-case-west-v1/checkpoint_workshop_v2.gd").new()')
z=s.index('\tvar original_rooms:',a)
s=s[:a]+'''\tvar view=installed_normal.view
''' +s[z:]
s=s.replace('npc=preload("res://character/james-floor-case-west-v1/checkpoint_floor_actor_v2.gd").new()','npc=game.BranforthNPC.new()')
s=s.replace('"james-floor-case-study"','"james-floor-case"')
s=s.replace('check(not SAVE.problem(packet).is_empty(),"Ordinary loader rejects unadmitted candidate marker")','check(SAVE.problem(packet).is_empty(),"Normal loader admits production extension")')
s=s.replace('bad.crew.branforth.stage=""','bad.crew.branforth.stage="unadmitted_james_cargo_return"')
s=s.replace('"Reject missing admission marker"','"Reject unadmitted staged marker"')
s=s.replace('checkpoint-v2','normal-checkpoint-v1').replace('checkpoint_probe_v2','normal_checkpoint_probe')
a=s.index('\tfor name in [');z=s.index('\tvar f:=',a)
s=s[:a]+'''\tfor name in ["normal_checkpoint_facade.gd","normal_checkpoint_probe.gd"]:
		if not FileAccess.file_exists(OUT+name+".uid"):
			var uid:=FileAccess.open(OUT+name+".uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	for name in ["james_cargo_actor.gd","james_cargo_player.gd","james_cargo_workshop.gd"]:
		var path:String="res://scripts/"+name+".uid"
		if not FileAccess.file_exists(path):
			var uid:=FileAccess.open(path,FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
''' +s[z:]
scope='Ten prescribed actual carry returns with normal factory/player/renderer selection and normal RunSave capture/write/read/restore_staged; no custom actor/player/view injection or post-restore replacement. Both gears/before/after/midpoint/terminal/idle. Native source/world captures and exact paused source/clock/contact/plan/room ownership, finite completion. Not title/new-process Continue, natural scheduling, ordinary unload, hazard regression or full visual/master acceptance.'
a=s.index('"scope":"');z=s.index('"},"  "))',a)
s=s[:a]+'"scope":'+json.dumps(scope)+s[z+1:]
(p/'normal_checkpoint_probe.gd').write_text(s)
old=json.loads((p/'checkpoint_probe_v2-inputs.json').read_bytes())
paths=[r/k for k in old]+[r/'scripts/main.gd',r/'scripts/grid_canvas.gd',r/'scripts/run_save.gd',r/'scripts/james_cargo_checkpoint.gd',r/'scripts/james_cargo_actor.gd',r/'scripts/james_cargo_player.gd',r/'scripts/james_cargo_workshop.gd',p/'normal_checkpoint_probe.gd',p/'normal_checkpoint_facade.gd']
(p/'normal_checkpoint_probe-inputs.json').write_text(json.dumps({str(f.relative_to(r)):hashlib.sha256(f.read_bytes()).hexdigest() for f in paths},indent=2)+'\n')
print('Normal factories/renderer/RunSave ten-phase fixture prepared;56targeted inputs frozen.')
