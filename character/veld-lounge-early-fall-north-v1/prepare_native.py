from pathlib import Path
R=Path(__file__).resolve().parents[2]
s=(R/'tests/test_veld_lounge_late_fall_north_native.gd').read_text()
for a,b in [('veld-lounge-late-fall-north','veld-lounge-early-fall-north'),('test_veld_lounge_late_fall_north_native','test_veld_lounge_early_fall_north_native'),('LATE LOUNGE NORTH FALL','EARLY LOUNGE NORTH FALL'),('crew_lounge_late_floor_fall','crew_lounge_early_floor_fall'),('death-lounge-late%d-north','death-lounge-early%d-north'),('late_clip','early_clip'),('(elapsed-.36)/.36','(elapsed-.18)/.16'),('recipe.lounge_motion.amount=.2','recipe.lounge_motion.amount=.8'),('recipe.entry_index=0','recipe.entry_index=2'),('Both gears/late poses3and4 lowering/rising','Both gears/early poses0and1 lowering/rising')]:s=s.replace(a,b)
s=s.replace('[["lower3","life_sit",.40,3],["lower4","life_sit",.24,4],["rise3","life_rise",.40,3],["rise4","life_rise",.56,4]]','[["lower0","life_sit",.76,0],["lower1","life_sit",.67,1],["rise0","life_rise",.04,0],["rise1","life_rise",.13,1]]')
anchor='\tgame.grid_view.veld_player.load_manifest("res://character/veld-lounge-early-fall-north-v1/bare-manifest.json",true)'
s=s.replace(anchor,'''\tgame.grid_view.veld_player.load_manifest("res://character/veld-lounge-late-fall-north-v1/bare-manifest.json",true)
	check(game.grid_view.veld_player.load_equipment_manifest("diving-helmet","res://character/veld-lounge-late-fall-north-v1/helmet-manifest.json"),"Existing late regression candidates")
'''+anchor)
s=s.replace('[["life_sit",.55,"death-lounge-partial-north"],["life_seated",7.4,"death-lounge-seated-north"],["life_sit",.08,"death-lounge-seated-north"]]','[["life_sit",.55,"death-lounge-partial-north"],["life_seated",7.4,"death-lounge-seated-north"],["life_sit",.08,"death-lounge-seated-north"],["life_sit",.4,"death-lounge-late3-north"],["life_sit",.24,"death-lounge-late4-north"],["life_rise",.55,"death-lounge-late4-north"],["life_sit",.8,"death-lounge-early0-north"],["life_rise",0,"death-lounge-early0-north"]]')
(R/'tests/test_veld_lounge_early_fall_north_native.gd').write_text(s)
(R/'tests/test_veld_lounge_early_fall_north_native.gd.uid').write_text('uid://b6mi0kpxqnhjc\n')
t=(R/'tools/run_veld_lounge_late_fall_north_native.py').read_text()
for a,b in [('veld-lounge-late-fall-north','veld-lounge-early-fall-north'),('test_veld_lounge_late_fall_north_native','test_veld_lounge_early_fall_north_native'),('helmet-rise4-after-room','helmet-rise1-after-room'),('LATE LOUNGE NORTH FALL','EARLY LOUNGE NORTH FALL')]:t=t.replace(a,b)
t=t.replace("['veld-lounge-fall-north-v1','veld-lounge-partial-fall-north-v1']","['veld-lounge-fall-north-v1','veld-lounge-partial-fall-north-v1','veld-lounge-late-fall-north-v1']")
(R/'tools/run_veld_lounge_early_fall_north_native.py').write_text(t)
print('Eight early mortality/disk/future cases and16existing/boundary selector guards')
