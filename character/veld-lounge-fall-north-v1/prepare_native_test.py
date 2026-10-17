"""Derive the established full disk/future fixture, retaining real mortality/save APIs."""
from pathlib import Path
R=Path(__file__).resolve().parents[2]
s=(R/'tests/test_veld_bunk_early_fall_native.gd').read_text(encoding='utf-8')
s=s.replace('bunk-early-fall','lounge-fall-north').replace('test_veld_bunk_early_fall_native','test_veld_lounge_fall_north_native')
a=s.index('\tgame.grid_view.veld_player.load_manifest',s.index('func fresh'))
b=s.index('\treturn game',a)
s=s[:a]+'''\tgame.grid_view.veld_player.load_manifest("res://character/veld-lounge-fall-north-v1/bare-manifest.json",true)
\tcheck(game.grid_view.veld_player.load_equipment_manifest("diving-helmet","res://character/veld-lounge-fall-north-v1/helmet-manifest.json"),"Fixture-only paired North lounge fall; normal selected North seating")
'''+s[b:]
s=s.replace('actor.direction="east"','actor.direction="north"').replace('"Actual specialised bunk dispatch"','"Actual lounge dispatch"')
s=s.replace('game._place_room("crew_hab",CELL,true)','game._place_room("crew_lounge",CELL,true)')
s=s.replace('candidate.get("veld_bunk",false)','candidate.get("mode","")=="sit" and candidate.facing=="north"')
s=s.replace('"Clear specialised East bunk station"','"Clear actual North lounge station"')
s=s.replace('[["lower-standing","life_lie",1.78],["lower-crouch","life_lie",1.60],["rise-standing","life_get_up",.06],["rise-crouch","life_get_up",.24]]','[["held-0","life_seated",7.4],["held-3","life_seated",7.4],["lower-seated","life_sit",.08],["rise-seated","life_rise",.72]]')
s=s.replace('''\t\t\tgame.grid_view._get_veld_frame_source(game)
\t\t\tif true:''','''\t\t\tgame.grid_view._get_veld_frame_source(game)
\t\t\tif phase[0]=="held-3":game.visual_time_seconds+=1.9;game.grid_view._get_veld_frame_source(game)
\t\t\tvar live:Texture2D=game.grid_view._get_veld_frame_source(game)
\t\t\tvar expected_entry:PackedByteArray=live.get_image().get_data()
\t\t\tvar entry_offset:Vector2=actor.observation_visual_offset()+LIFE.head_alignment(actor,player)
\t\t\tvar entry_at:Vector2=actor.foot-(Vector2(CELL)+Vector2.ONE*.5)*384+entry_offset
\t\t\tvar entry_depth:float=LIFE.seated_draw_depth(actor,live,entry_at)
\t\t\tvar gear:String="diving-helmet" if equipped else ""
\t\t\tvar pool:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
\t\t\tpool["death-lounge-seated-north"][0].remove_meta("crew_lounge_floor_fall")
\t\t\tcheck(preload("res://scripts/veld_death_motion.gd").capture(game,actor).get("clip","")!="death-lounge-seated-north","Unmarked source cannot opt into lounge fall")
\t\t\tpool["death-lounge-seated-north"][0].set_meta("crew_lounge_floor_fall",true)
\t\t\tif true:''')
s=s.replace('FLOOD.kill(game,actor,"veld","bunk Continue fixture");game.visual_time_seconds=400.1','FLOOD.kill(game,actor,"veld","North lounge Continue fixture");game.visual_time_seconds+=.1')
s=s.replace('var expected_clip:String="death-bunk-standing-east" if str(phase[0]).ends_with("standing") else "death-bunk-crouch-east"','var expected_clip:String="death-lounge-seated-north"')
a=s.index('\t\t\t\tfor bad in [');b=s.index('\t\t\tvar shown:Texture2D',a)
s=s[:a]+'''\t\t\t\tcheck(game.grid_view._get_veld_frame_source(game).get_image().get_data()==expected_entry,"Death starts with exact displayed seated/breathing source")
\t\t\t\tcheck(preload("res://scripts/veld_death_motion.gd").visual_offset(game,actor)==entry_offset,"Exact displayed chair position retained")
\t\t\t\tcheck(is_equal_approx(preload("res://scripts/veld_death_motion.gd").draw_depth(game,actor,live,entry_at),entry_depth),"Exact displayed chair ordering retained")
\t\t\t\tfor bad in ["first","entry_index","entry_position_offset","entry_equipment","amount","local_foot","clip","seat_depth"]:
\t\t\t\t\tvar malformed:Dictionary=actor.snapshot();var recipe:Dictionary=malformed.veld_water_death
\t\t\t\t\tif bad=="first":recipe.first=2
\t\t\t\t\telif bad=="entry_index":recipe.entry_index=4 if recipe.entry_key=="sit-down-north" else 6
\t\t\t\t\telif bad=="entry_position_offset":recipe.entry_position_offset+=Vector2(0,16)
\t\t\t\t\telif bad=="entry_equipment":recipe.entry_equipment="" if equipped else "diving-helmet"
\t\t\t\t\telif bad=="amount":recipe.lounge_motion.amount=.7
\t\t\t\t\telif bad=="local_foot":recipe.lounge_motion.local_foot+=Vector2(1,0)
\t\t\t\t\telif bad=="clip":recipe.clip="death-ground-north"
\t\t\t\t\telse:recipe.lounge_motion.seat_depth=NAN
\t\t\t\t\tcheck(not actor.valid_veld_snapshot(malformed),"Invalid lounge source/root/gear rejected: "+bad)
'''+s[b:]
s=s.replace('check(sample.offset==Vector2.ZERO,"Unsupported early pose stays registered to floor")','''var root_amount:float=1.0-clampf((elapsed-.36)/.36,0.0,1.0)
\t\tvar expected_offset:Vector2=Vector2(recipe.entry_position_offset)*root_amount
\t\tcheck(sample.offset.distance_to(expected_offset)<.0001,"Independent saved seat-to-floor root progression")
\t\tvar local:Vector2=game.veld_npc.foot-(Vector2(CELL)+Vector2.ONE*.5)*384
\t\tcheck(is_equal_approx(sample.depth,maxf(local.y+expected_offset.y,float(recipe.lounge_motion.seat_depth))),"Independent registered chair/floor depth")''')
s=s.replace('BUNK EARLY FLOOR','LOUNGE NORTH FALL').replace('VELD BUNK EARLY FLOOR','VELD LOUNGE NORTH FALL')
s=s.replace('"Both gears/four early lower-rise phases"','"Both gears/held two breathing phases and seated lower-rise"')
(R/'tests/test_veld_lounge_fall_north_native.gd').write_text(s,encoding='utf-8')
(R/'tests/test_veld_lounge_fall_north_native.gd.uid').write_text('uid://dwm4jkpxac93n\n',encoding='utf-8')
t=(R/'tools/run_veld_bunk_early_fall_native.py').read_text(encoding='utf-8')
t=t.replace('bunk-early-fall','lounge-fall-north').replace('test_veld_bunk_early_fall_native','test_veld_lounge_fall_north_native').replace('BUNK EARLY FLOOR','LOUNGE NORTH FALL').replace('helmet-rise-crouch-after-room','helmet-rise-seated-after-room')
t=t.replace('veld-bunk-body-master-v1','veld-seated-north-coherent-v1')
(R/'tools/run_veld_lounge_fall_north_native.py').write_text(t,encoding='utf-8')
print('Paired real mortality/full disk/future fixture saved; normal North seat sources retained')
