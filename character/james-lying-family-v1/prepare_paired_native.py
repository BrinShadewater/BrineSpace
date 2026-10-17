from pathlib import Path
P=Path(__file__).resolve().parent
s=(P/'native-loader.gd').read_text()
s=s.replace('var manifest: Dictionary=', 'check(player.load_equipment_manifest("diving-helmet","res://character/james-lying-family-v1/helmet-manifest.json"),"Paired helmet contract")\n\tvar eq: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/james-lying-family-v1/helmet-manifest.json"))\n\tvar manifest: Dictionary=')
needle='\t\t\telapsed+=float(state.frameDurationsMs[slot])/1000.0'
proof='''
			var es: Dictionary=eq.states.filter(func(v):return v.id==key)[0]
			var et: Texture2D=player.equipment_frames["diving-helmet"][key][slot]
			var ei:=Image.load_from_file("res://character/james-lying-family-v1/"+es.frameFiles[slot])
			check(et.get_image().get_data()==ei.get_data(),"Exact helmet pixels "+key)
			check(et.get_meta("crew_pivot")==tex.get_meta("crew_pivot"),"Paired pivot "+key)
			check(et.get_meta("crew_standing_height")==tex.get_meta("crew_standing_height"),"Paired anatomy "+key)
			check(et.get_meta("crew_depth_offset")==tex.get_meta("crew_depth_offset"),"Paired furniture depth "+key)
			check(player.frame_at_elapsed(key,elapsed+float(state.frameDurationsMs[slot])/2000.0,"diving-helmet")==et,"Helmet clock "+key)
			if key.begins_with("sleep-"):check(et.get_meta("crew_rest_head_offset")==tex.get_meta("crew_rest_head_offset"),"Paired pillow anchor "+key)
'''
s=s.replace(needle,proof+needle,1).replace('JAMES LYING: ', 'JAMES PAIRED LYING: ')
(P/'native-paired.gd').write_text(s)
s=(P/'retained-berth.gd').read_text()
s=s.replace('var frame: Texture2D=player.frames[', 'npc.helmet_equipped=true\n\tcheck(player.load_equipment_manifest("diving-helmet","res://character/james-lying-family-v1/helmet-manifest.json"),"Shared lying helmet paired")\n\tvar frame: Texture2D=player.equipment_frames["diving-helmet"][',1)
s=s.replace('james-lying-family-v1/retained-berth/', 'james-lying-family-v1/retained-berth-helmet/').replace('JAMES RETAINED BERTH: ', 'JAMES RETAINED HELMET BERTH: ')
(P/'retained-berth-helmet.gd').write_text(s);(P/'retained-berth-helmet').mkdir(exist_ok=True)
