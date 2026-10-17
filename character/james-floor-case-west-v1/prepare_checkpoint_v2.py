from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1]
s=(p/'rise_floor_state.gd').read_text().replace('const SOURCE="james-west-case3"','const SOURCE="james-west-case7"\nconst ART_PATH="res://character/james-floor-case-west-v1/floor-case-west-v7.png"')
(p/'checkpoint_floor_state_v2.gd').write_text(s)
for name in ['floor_actor','floor_player']:
    s=(p/('rise_'+name+'.gd')).read_text().replace('rise_floor_state.gd','checkpoint_floor_state_v2.gd')
    (p/('checkpoint_'+name+'_v2.gd')).write_text(s)
s=(p/'shared_case_workshop.gd').read_text()
s=s.replace('extends "res://character/james-floor-case-west-v1/body_release_workshop.gd"','extends "res://character/james-floor-case-west-v1/workshop_preview.gd"\nconst FLOOR=preload("res://character/james-floor-case-west-v1/checkpoint_floor_state_v2.gd")\nvar bound_room:Dictionary={}\nvar embedded_case:=false\nfunc bind_room(room:Dictionary)->void:\n\tbound_room=room;sync_case()\nfunc sync_case()->void:\n\tvar data:Dictionary=FLOOR.payload(bound_room)\n\tcase_anchor=Vector2(data.anchor) if not data.is_empty() else Vector2.ZERO\n\tcase_enabled=not data.is_empty() and not embedded_case\nfunc configure_embedded(q:int,open_sides:Array,running:bool,time_seconds:float,omitted_sides:Array=[])->void:\n\tsuper.configure_embedded(q,open_sides,running,time_seconds,omitted_sides)\n\tsync_case()')
(p/'checkpoint_workshop_v2.gd').write_text(s)
s=(p/'checkpoint.gd').read_text().replace('floor_state.gd','checkpoint_floor_state_v2.gd').replace('floor_actor.gd','checkpoint_floor_actor_v2.gd').replace('floor_player.gd','checkpoint_floor_player_v2.gd').replace('james-west-return9-floor3','james-west-return9-rise6-floor7')
helpers='''static func floor_binding(player)->Dictionary:
	if player.preview_view==null or player.preview_view.case_texture==null:return {}
	return {"source":FLOOR.SOURCE,"png":FileAccess.get_sha256(FLOOR.ART_PATH),"rgba":player.preview_view.case_texture.get_image().get_data().hex_encode().sha256_text(),"pivot":Vector2(128,224),"height":148}
static func bank_bindings(player)->Dictionary:
	var result:Dictionary={}
	for gear in ["","diving-helmet"]:
		var bank:Dictionary=player.bank_for(gear)
		var clocks:Dictionary=player.timing if gear=="" else player.equipment_timing.get(gear,{})
		var bound:Dictionary={}
		for key in ["unload-west","carry-settle-west"]:
			if not bank.has(key) or not clocks.has(key):return {}
			var rows:Array=[]
			for index in range(bank[key].size()):
				var texture:Texture2D=bank[key][index]
				rows.append({"rgba":texture.get_image().get_data().hex_encode().sha256_text(),"pivot":texture.get_meta("crew_pivot"),"height":texture.get_meta("crew_standing_height"),"seconds":float(clocks[key].durations[index])/1000.0})
			bound[key]=rows
		result[gear]=bound
	return result
static func valid_floor_binding(value:Variant)->bool:
	if not value is Dictionary or value.size()!=5:return false
	if value.get("source")!=FLOOR.SOURCE or value.get("pivot")!=Vector2(128,224) or value.get("height")!=148:return false
	for key in ["png","rgba"]:
		if not value.get(key) is String or value[key].length()!=64:return false
	return true
static func valid_bank_bindings(value:Variant)->bool:
	if not value is Dictionary or value.size()!=2:return false
	for gear in ["","diving-helmet"]:
		if not value.get(gear) is Dictionary or value[gear].size()!=2:return false
		for key in ["unload-west","carry-settle-west"]:
			var rows:Variant=value[gear].get(key)
			if not rows is Array or rows.size()!=(7 if key=="unload-west" else 6):return false
			for row in rows:
				if not row is Dictionary or row.size()!=4 or not row.get("rgba") is String or row.rgba.length()!=64:return false
				if not row.get("pivot") is Vector2 or row.pivot!=Vector2(128,224) or row.get("height")!=148:return false
				if not row.get("seconds") is float or not is_finite(row.seconds) or row.seconds<=0 or row.seconds>.5:return false
	return true
'''
s=s.replace('static func capture(game)',helpers+'static func capture(game)')
s=s.replace('{"version":1,"binding":BINDING,"actorStage":stage,"plan":plan,"sourceBindings":source_bindings(player,plan)}','{"version":2,"binding":BINDING,"actorStage":stage,"plan":plan,"sourceBindings":source_bindings(player,plan),"floorBinding":floor_binding(player),"bankBindings":bank_bindings(player)}')
s=s.replace('extra.size()!=5 or extra.get("version")!=1','extra.size()!=7 or extra.get("version")!=2')
s=s.replace('\tvar plan:Dictionary=extra.plan','\tif not valid_floor_binding(extra.get("floorBinding")) or not valid_bank_bindings(extra.get("bankBindings")):return false\n\tvar plan:Dictionary=extra.plan')
s=s.replace('\tif not valid_shape(data):return false\n\tvar plan:', '\tif not valid_shape(data):return false\n\tif data[FIELD].floorBinding!=floor_binding(player) or data[FIELD].bankBindings!=bank_bindings(player):return false\n\tvar plan:')
(p/'checkpoint_v2.gd').write_text(s)
s=(p/'checkpoint_probe.gd').read_text().replace('checkpoint.gd','checkpoint_v2.gd').replace('floor_state.gd','checkpoint_floor_state_v2.gd').replace('floor_actor.gd','checkpoint_floor_actor_v2.gd').replace('floor_player.gd','checkpoint_floor_player_v2.gd').replace('release_workshop.gd','checkpoint_workshop_v2.gd')
for variable in ['candidate','player']:
    needle='\tgame.grid_view.branforth_player='+variable
    insertion=f'\t{variable}.load_manifest("res://character/james-floor-case-west-v1/bare-rise-v6-manifest.json",true)\n\tcheck({variable}.load_equipment_manifest("diving-helmet","res://character/james-floor-case-west-v1/helmet-rise-v6-manifest.json"),"New paired seven-frame rise bank")\n'
    s=s.replace(needle,insertion+needle)
s=s.replace('["before","after","idle"]','["before","after","midpoint","terminal","idle"]')
s=s.replace('\t\t\tif phase=="idle":','\t\t\tif phase in ["midpoint","terminal"]:\n\t\t\t\tgame.visual_time_seconds=release+(.081 if phase=="midpoint" else .161);npc.update(game,.02);game.grid_view._get_branforth_frame(game)\n\t\t\tif phase=="idle":')
s=s.replace('bad[CHECKPOINT.FIELD].version=1.0','bad[CHECKPOINT.FIELD].version=2.0')
needle='\t\t\tcheck(SAVE.problem(CHECKPOINT.base_packet(packet)).is_empty(),"Base station/legacy schema retained")'
rejects='''			bad=packet.duplicate(true);bad[CHECKPOINT.FIELD].floorBinding.png="0".repeat(64)
			check(not CHECKPOINT.admits_loaded(bad,player),"Reject altered case PNG binding even at idle")
			bad=packet.duplicate(true);bad[CHECKPOINT.FIELD].floorBinding.rgba="0".repeat(64)
			check(not CHECKPOINT.admits_loaded(bad,player),"Reject altered case submitted pixels")
			bad=packet.duplicate(true);bad[CHECKPOINT.FIELD].bankBindings[""].get("unload-west")[5].rgba="0".repeat(64)
			check(not CHECKPOINT.admits_loaded(bad,player),"Reject changed midpoint binding even at idle")
			var actual_case:Texture2D=view.case_texture
			view.case_texture=ImageTexture.create_from_image(Image.create(256,256,false,Image.FORMAT_RGBA8))
			check(not CHECKPOINT.admits_loaded(packet,player),"Reject actually loaded wrong case texture")
			view.case_texture=actual_case
			var actual_mid:Texture2D=player.frames["unload-west"][5]
			player.frames["unload-west"][5]=player.frames["unload-west"][4]
			check(not CHECKPOINT.admits_loaded(packet,player),"Reject actually loaded wrong midpoint")
			player.frames["unload-west"][5]=actual_mid
			check(CHECKPOINT.admits_loaded(packet,player),"Exact case/bank re-admitted after negative trials")
'''
s=s.replace(needle,rejects+needle)
s=s.replace('"-checkpoint-"','"-checkpoint-v2-"').replace('checkpoint_probe.gd','checkpoint_probe_v2.gd').replace('checkpoint_probe-evidence.json','checkpoint_probe_v2-evidence.json')
s=s.replace('for name in ["checkpoint_v2.gd","checkpoint_probe_v2.gd"]:', 'for name in ["checkpoint_v2.gd","checkpoint_probe_v2.gd","checkpoint_floor_state_v2.gd","checkpoint_floor_actor_v2.gd","checkpoint_floor_player_v2.gd","checkpoint_workshop_v2.gd"]:')
s=s.replace('Six actual carry returns/both gears/before release, after release, idle.','Ten actual carry returns/both gears/before release, after release, midpoint, terminal, idle. New full paired7-frame unload/6-frame bridge RGBA/clock/pivot bindings and actual case PNG/submitted RGBA binding including idle.').replace('18native source/room pairs','30native source/room pairs').replace(';6cases;18presentations',';10cases;30presentations')
(p/'checkpoint_probe_v2.gd').write_text(s)
s=(p/'review_checkpoint.py').read_text().replace('checkpoint_probe-evidence.json','checkpoint_probe_v2-evidence.json').replace('checkpoint_probe-inputs.json','checkpoint_probe_v2-inputs.json').replace('len(records)==18','len(records)==30').replace('floor-case-west.png','floor-case-west-v7.png').replace("['before','after','idle']","['before','after','midpoint','terminal','idle']").replace("'-checkpoint-'","'-checkpoint-v2-'").replace('-checkpoint-review.png','-checkpoint-v2-review.png').replace('checkpoint-review.json','checkpoint-v2-review.json').replace('18native','30native').replace('Pairs\':18','Pairs\':30').replace('Six staged','Ten staged')
(p/'review_checkpoint_v2.py').write_text(s)
prior=json.loads((p/'motion_rise_v6-inputs.json').read_bytes());paths=[r/k for k in prior]+[p/f for f in ['checkpoint_v2.gd','checkpoint_probe_v2.gd','checkpoint_floor_state_v2.gd','checkpoint_floor_actor_v2.gd','checkpoint_floor_player_v2.gd','checkpoint_workshop_v2.gd']]+[r/'scripts/run_save.gd',r/'scripts/bill_npc.gd']
(p/'checkpoint_probe_v2-inputs.json').write_text(json.dumps({str(path.relative_to(r)):hashlib.sha256(path.read_bytes()).hexdigest() for path in paths},indent=2)+'\n')
print('Ten paired staged disk/fresh-main phases; strict full bank + actual case bindings;'+str(len(set(paths)))+'targeted inputs frozen.')
