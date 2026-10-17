from pathlib import Path
p=Path(__file__).resolve().parent
s=(p.parent/'james-seated-family-v1/baseline.gd').read_text()
s=s.replace('var failures:=0','var failures:=0\nvar checks:=0').replace('if not ok:failures+=1;push_error(why)','checks+=1\n\tif not ok:failures+=1;push_error(why)')
s=s.replace('var sleeping: bool="sleep" in args','var sleeping: bool=true\n\tcheck("brine-james-native-" in OS.get_environment("APPDATA"),"Scratch APPDATA required")\n\tif failures:quit(2);return')
s=s.replace('game.set_process(false);', 'game.grid_view.branforth_player.load_manifest("res://character/james-lying-family-v1/bare-manifest.json",true)\n\tgame.set_process(false);',1)
s=s.replace('res://character/james-seated-family-v1/baseline/', 'res://character/james-lying-family-v1/native/')
s=s.replace('SEATING ROOM: ', 'JAMES LYING: ')
anchor='\tgame.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw'
proof='''
	var manifest: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/james-lying-family-v1/bare-manifest.json"))
	for state in manifest.states:
		var key: String=state.id
		check(player.frames[key].size()==6,"Six authored slots "+key)
		var elapsed: float=0.0
		for slot in range(6):
			var tex: Texture2D=player.frames[key][slot]
			var disk:=Image.load_from_file("res://character/james-lying-family-v1/"+state.frameFiles[slot])
			check(tex.get_image().get_data()==disk.get_data(),"Exact authored pixels "+key+str(slot))
			check(tex.get_meta("crew_pivot")==Vector2(128,224),"Pivot "+key)
			check(tex.get_meta("crew_standing_height")==148.0,"Scale metadata "+key)
			check(tex.get_meta("crew_depth_offset")==state.depthOffsets[slot],"Furniture depth "+key)
			check(player.frame_at_elapsed(key,elapsed+float(state.frameDurationsMs[slot])/2000.0)==tex,"Simulation clock slot "+key+str(slot))
			elapsed+=float(state.frameDurationsMs[slot])/1000.0
		check(absf(player.cycle_seconds(key)-elapsed)<0.001,"Cycle duration "+key)
'''
s=s.replace(anchor,proof+anchor,1)
# The existing baseline's optional branch remains unreachable; append actual north contacts.
marker='\tvar geometry_file:='
extra='''
	var rest_timer: float=npc.timer
	for action in ["lie-down","sleep","get-up"]:
		var key: String=action+"-north"
		var elapsed: float=0.0
		for slot in range(6):
			npc.stage="life_lie" if action=="lie-down" else ("life_get_up" if action=="get-up" else "life_sleep")
			var midpoint: float=elapsed+float(player.timing[key].durations[slot])/2000.0
			npc.timer=rest_timer if action=="sleep" else 0.8-midpoint
			player.current_key=key;player.phase=midpoint;player.last_time=game.grid_view.crew_animation_time
			game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
			root.get_texture().get_image().save_png(out+"%s-%02d.png"%[action,slot])
			elapsed+=float(player.timing[key].durations[slot])/1000.0
		npc.stage="life_sleep";npc.timer=rest_timer
'''
# Inspect actual renderer clock API before enabling contact clock steering.
extra=extra.replace(';player.last_time=game.grid_view.crew_animation_time','')
s=s.replace(marker,extra+marker,1)
s=s.replace('failures," failures;', 'checks," checks; ",failures," failures;')
(p/'native.gd').write_text(s)
(p/'native').mkdir(exist_ok=True)
