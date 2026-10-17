from pathlib import Path
R=Path(__file__).resolve().parents[2]
s=(R/'tests/test_veld_lounge_early_fall_north_native.gd').read_text()
s=s.replace('veld-lounge-early-fall-north-native-v1','veld-north-chair-falls-selected-native-v1').replace('test_veld_lounge_early_fall_north_native','test_veld_north_chair_falls_selected_native').replace('EARLY LOUNGE NORTH FALL','NORTH CHAIR FALLS SELECTED').replace('capture_bunk','capture_room')
a=s.index('\tgame.grid_view.veld_player.load_manifest',s.index('func fresh'))
b=s.index('\treturn game',a)
s=s[:a]+'''	# Only the normal production loader may admit the chair fall families.
	for gear in ["","diving-helmet"]:
		var pool:Dictionary=game.grid_view.veld_player.frames if gear.is_empty() else game.grid_view.veld_player.equipment_frames[gear]
		for clip in ["death-lounge-early0-north","death-lounge-early1-north","death-lounge-partial-north","death-lounge-late3-north","death-lounge-late4-north","death-lounge-seated-north"]:
			check(pool.has(clip) and pool[clip].size()==6,"Normal loader admits complete North chair fall: "+clip+" "+gear)
'''+s[b:]
a=s.index('\t\tfor phase in [[');b=s.index(':\n',a)+1
phases=[]
times=[.76,.67,.55,.40,.24,.08]
for pose,timer in enumerate(times):phases.append(f'["lower{pose}","life_sit",{timer:.2f},{pose}]')
for pose,timer in enumerate(times):phases.append(f'["rise{pose}","life_rise",{.8-timer:.2f},{pose}]')
phases+=['["held0","life_seated",7.4,5]','["held3","life_seated",7.4,5]']
s=s[:a]+'\t\tfor phase in ['+','.join(phases)+']:'+s[b:]
s=s.replace('var early_clip:String="death-lounge-early%d-north"%int(phase[3])','''var early_clip:String=["death-lounge-early0-north","death-lounge-early1-north","death-lounge-partial-north","death-lounge-late3-north","death-lounge-late4-north","death-lounge-seated-north"][int(phase[3])]
			var marker:String=["crew_lounge_early_floor_fall","crew_lounge_early_floor_fall","crew_lounge_partial_floor_fall","crew_lounge_late_floor_fall","crew_lounge_late_floor_fall","crew_lounge_floor_fall"][int(phase[3])]''')
s=s.replace('"crew_lounge_early_floor_fall"','marker')
# Restore the marker-name literals replaced in the array above.
s=s.replace('[marker,marker,"crew_lounge_partial_floor_fall"','["crew_lounge_early_floor_fall","crew_lounge_early_floor_fall","crew_lounge_partial_floor_fall"')
anchor='\t\t\tgame.grid_view._get_veld_frame_source(game)\n\t\t\tvar live:Texture2D='
s=s.replace(anchor,'\t\t\tgame.grid_view._get_veld_frame_source(game)\n\t\t\tif phase[0]=="held3":game.visual_time_seconds+=1.9;game.grid_view._get_veld_frame_source(game)\n\t\t\tvar live:Texture2D=')
s=s.replace('recipe.entry_index=2','recipe.entry_index=99').replace('recipe.lounge_motion.amount=.8','recipe.lounge_motion.amount=2.0')
# Whole-seated fall captures live breathing rather than binding to one exact entry.
a=s.index('\t\t\tvar candidate:Texture2D=pool[early_clip][0]');b=s.index('\t\t\tif true:',a)
block=s[a:b]
block='\t\t\tif int(phase[3])<5:\n'+''.join('\t'+line+'\n' for line in block.rstrip().splitlines())
s=s[:a]+block+s[b:]
s=s.replace('var root_amount:float=1.0-clampf((elapsed-.18)/.16,0.0,1.0)','''var hold:float=.18 if recipe.clip in ["death-lounge-early0-north","death-lounge-early1-north"] else (.34 if recipe.clip=="death-lounge-partial-north" else .36)
		var fade:float=.16 if recipe.clip in ["death-lounge-early0-north","death-lounge-early1-north"] else (.18 if recipe.clip=="death-lounge-partial-north" else .36)
		var root_amount:float=1.0-clampf((elapsed-hold)/fade,0.0,1.0)''')
s=s.replace('records.size()==8','records.size()==28').replace('8 fresh disk restores','28 fresh disk restores').replace('Both gears/early poses0and1 lowering/rising','Both gears/all6lowering/all6rising/two held breathing phases')
s=s.replace('\tvar f=FileAccess.open(OUT+"records.json",FileAccess.WRITE)', '''	for gear in ["bare","helmet"]:
		var entrances:Dictionary={}
		for record in records:
			if record.name in [gear+"-held0",gear+"-held3"]:entrances[record.name]=record.reference[0].pixels
		check(entrances.size()==2 and entrances.get(gear+"-held0","")!=entrances.get(gear+"-held3",""),"Distinct normally loaded held breathing entrances: "+gear)
	var f=FileAccess.open(OUT+"records.json",FileAccess.WRITE)''')
(R/'tests/test_veld_north_chair_falls_selected_native.gd').write_text(s)
(R/'tests/test_veld_north_chair_falls_selected_native.gd.uid').write_text('uid://cdsp2aqf9xt4h\n')
t=(R/'tools/run_veld_lounge_early_fall_north_native.py').read_text().replace('veld-lounge-early-fall-north-native-v1','veld-north-chair-falls-selected-native-v1').replace('test_veld_lounge_early_fall_north_native','test_veld_north_chair_falls_selected_native').replace('helmet-rise1-after-room','helmet-held3-after-room').replace('EARLY LOUNGE NORTH FALL','NORTH CHAIR FALLS SELECTED').replace('8 fresh disk restores','28 fresh disk restores').replace('timeout=750','timeout=1600')
anchor="    inputs+=list((ROOT/'character/veld-seated-north-coherent-v1/frames').rglob('*.png'))"
t=t.replace(anchor,"    inputs+=[ROOT/'scripts/grid_canvas.gd',ROOT/'character/veld-seated-north-selected-v1/bare-manifest.json',ROOT/'character/veld-seated-north-selected-v1/helmet-manifest.json']\n"+anchor)
(R/'tools/run_veld_north_chair_falls_selected_native.py').write_text(t)
print('28 normal-loader mortality/disk/future cases saved; no test-only source loading')
