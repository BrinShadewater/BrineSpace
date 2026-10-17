from pathlib import Path
R=Path(__file__).resolve().parents[2]
s=(R/'tests/test_veld_lounge_fall_north_native.gd').read_text()
for a,b in [('veld-lounge-fall-north','veld-lounge-late-fall-north'),('test_veld_lounge_fall_north_native','test_veld_lounge_late_fall_north_native'),('LOUNGE NORTH FALL','LATE LOUNGE NORTH FALL'),('crew_lounge_floor_fall','crew_lounge_late_floor_fall'),('recipe.lounge_motion.amount=.7','recipe.lounge_motion.amount=.2'),('Both gears/held two breathing phases and seated lower-rise','Both gears/late poses3and4 lowering/rising')]:s=s.replace(a,b)
s=s.replace('[["held-0","life_seated",7.4],["held-3","life_seated",7.4],["lower-seated","life_sit",.08],["rise-seated","life_rise",.72]]','[["lower3","life_sit",.40,3],["lower4","life_sit",.24,4],["rise3","life_rise",.40,3],["rise4","life_rise",.56,4]]')
s=s.replace('\t\t\tif phase[0]=="held-3":game.visual_time_seconds+=1.9;game.grid_view._get_veld_frame_source(game)\n','')
s=s.replace('pool["death-lounge-seated-north"]','pool[late_clip]')
s=s.replace('var pool:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]','var pool:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]\n\t\t\tvar late_clip:String="death-lounge-late%d-north"%int(phase[3])')
s=s.replace('.get("clip","")!="death-lounge-seated-north"','.get("clip","")!=late_clip')
s=s.replace('var expected_clip:String="death-lounge-seated-north"','var expected_clip:String=late_clip')
s=s.replace('recipe.entry_index=4 if recipe.entry_key=="sit-down-north" else 6','recipe.entry_index=0')
anchor='\t\t\tpool[late_clip][0].set_meta("crew_lounge_late_floor_fall",true)'
s=s.replace(anchor,anchor+'''
			var candidate:Texture2D=pool[late_clip][0]
			pool[late_clip][0]=pool[late_clip][1]
			check(preload("res://scripts/veld_death_motion.gd").capture(game,actor).get("clip","")!=late_clip,"Different marked source cannot bind late entrance")
			pool[late_clip][0]=candidate''')
anchor='\tgame.grid_view.veld_player.load_manifest("res://character/veld-lounge-late-fall-north-v1/bare-manifest.json",true)'
s=s.replace(anchor,'''\tgame.grid_view.veld_player.load_manifest("res://character/veld-lounge-fall-north-v1/bare-manifest.json",true)
	check(game.grid_view.veld_player.load_equipment_manifest("diving-helmet","res://character/veld-lounge-fall-north-v1/helmet-manifest.json"),"Existing fully seated regression candidate")
	game.grid_view.veld_player.load_manifest("res://character/veld-lounge-partial-fall-north-v1/bare-manifest.json",true)
	check(game.grid_view.veld_player.load_equipment_manifest("diving-helmet","res://character/veld-lounge-partial-fall-north-v1/helmet-manifest.json"),"Existing partial regression candidate")
'''+anchor)
anchor='\t\tfor phase in [['
i=s.index(anchor)
s=s[:i]+'''		for regression in [["life_sit",.55,"death-lounge-partial-north"],["life_seated",7.4,"death-lounge-seated-north"],["life_sit",.08,"death-lounge-seated-north"]]:
			prepare(game.veld_npc,station,equipped);game.veld_npc.stage=regression[0];game.veld_npc.timer=regression[1]
			game.visual_time_seconds=400;game.grid_view.veld_player.current_key="";game.grid_view.veld_player.last_time=-1
			game.veld_npc.water_death_last_frame=null;game.grid_view._get_veld_frame_source(game)
			check(preload("res://scripts/veld_death_motion.gd").capture(game,game.veld_npc).get("clip","")==regression[2],"Existing partial/held/final seated selector preserved with all candidates loaded")
'''+s[i:]
(R/'tests/test_veld_lounge_late_fall_north_native.gd').write_text(s)
(R/'tests/test_veld_lounge_late_fall_north_native.gd.uid').write_text('uid://bqx1n2vm70wdh\n')
t=(R/'tools/run_veld_lounge_fall_north_native.py').read_text()
for a,b in [('veld-lounge-fall-north','veld-lounge-late-fall-north'),('test_veld_lounge_fall_north_native','test_veld_lounge_late_fall_north_native'),('helmet-rise-seated-after-room','helmet-rise4-after-room'),('LOUNGE NORTH FALL','LATE LOUNGE NORTH FALL')]:t=t.replace(a,b)
anchor="    bindings={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}"
t=t.replace(anchor,"""    for folder in ['veld-lounge-fall-north-v1','veld-lounge-partial-fall-north-v1']:
        inputs+=list((ROOT/'character'/folder/'frames').rglob('*.png'))
        inputs+=[ROOT/'character'/folder/'bare-manifest.json',ROOT/'character'/folder/'helmet-manifest.json']
"""+anchor)
(R/'tools/run_veld_lounge_late_fall_north_native.py').write_text(t)
print('Eight paired actual mortality/disk/future cases plus existing selector guards')
