from pathlib import Path
R=Path(__file__).resolve().parents[2]
s=(R/'tests/test_veld_lounge_fall_north_native.gd').read_text()
for a,b in [('veld-lounge-fall-north','veld-lounge-partial-fall-north'),('test_veld_lounge_fall_north_native','test_veld_lounge_partial_fall_north_native'),('death-lounge-seated-north','death-lounge-partial-north'),('crew_lounge_floor_fall','crew_lounge_partial_floor_fall'),('LOUNGE NORTH FALL','PARTIAL LOUNGE NORTH FALL'),('(elapsed-.36)/.36','(elapsed-.34)/.18'),('recipe.lounge_motion.amount=.7','recipe.lounge_motion.amount=.8'),('Both gears/held two breathing phases and seated lower-rise','Both gears/two fractional offsets for matching partial lower-rise source')]:s=s.replace(a,b)
s=s.replace('[["held-0","life_seated",7.4],["held-3","life_seated",7.4],["lower-seated","life_sit",.08],["rise-seated","life_rise",.72]]','[["lower-early","life_sit",.60],["lower-late","life_sit",.50],["rise-early","life_rise",.20],["rise-late","life_rise",.30]]')
s=s.replace('\t\t\tif phase[0]=="held-3":game.visual_time_seconds+=1.9;game.grid_view._get_veld_frame_source(game)\n','')
anchor='\t\t\tpool["death-lounge-partial-north"][0].set_meta("crew_lounge_partial_floor_fall",true)'
s=s.replace(anchor,anchor+'''
			var candidate:Texture2D=pool["death-lounge-partial-north"][0]
			pool["death-lounge-partial-north"][0]=pool["death-lounge-partial-north"][1]
			check(preload("res://scripts/veld_death_motion.gd").capture(game,actor).get("clip","")!="death-lounge-partial-north","Different marked source cannot bind partial entrance")
			pool["death-lounge-partial-north"][0]=candidate''')
(R/'tests/test_veld_lounge_partial_fall_north_native.gd').write_text(s)
(R/'tests/test_veld_lounge_partial_fall_north_native.gd.uid').write_text('uid://dos8ljnhyp3c7\n')
t=(R/'tools/run_veld_lounge_fall_north_native.py').read_text()
for a,b in [('veld-lounge-fall-north','veld-lounge-partial-fall-north'),('test_veld_lounge_fall_north_native','test_veld_lounge_partial_fall_north_native'),('helmet-rise-seated-after-room','helmet-rise-late-after-room'),('LOUNGE NORTH FALL','PARTIAL LOUNGE NORTH FALL')]:t=t.replace(a,b)
(R/'tools/run_veld_lounge_partial_fall_north_native.py').write_text(t)
print('Paired eight-case actual mortality/disk/future fixture saved')
