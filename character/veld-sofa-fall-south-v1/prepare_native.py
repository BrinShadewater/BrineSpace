from pathlib import Path
R=Path(__file__).resolve().parents[2]
s=(R/'tests/test_veld_south_sofa_fall_diagnostic.gd').read_text(encoding='utf-8')
s=s.replace('veld-south-sofa-fall-diagnostic-v1','veld-sofa-fall-south-staged-v1')
s=s.replace('func shot(','''func fresh():
	var game=await super.fresh()
	game.grid_view.veld_player.load_manifest("res://character/veld-sofa-fall-south-v1/bare-manifest.json",true)
	check(game.grid_view.veld_player.load_equipment_manifest("diving-helmet","res://character/veld-sofa-fall-south-v1/helmet-manifest.json"),"Staged paired sofa fall candidate only")
	return game
func shot(''')
start=s.index('\t\tvar actor=game.veld_npc')
end=s.index('\t\tgame.queue_free();await process_frame',start)
block=s[start:end]
block=block.replace('actor.bunk_motion.clear();','actor.bunk_motion.clear();actor.water_death_motion.clear();actor.water_death_last_frame=null;')
block=block.replace('12-actor.timer>=3','12-actor.timer>=reading_sample')
block=block.replace('var gear:String="helmet" if equipped else "bare"','var gear:String=("helmet" if equipped else "bare")+"-"+str(reading_sample)')
block=block.replace('actor.prepare_death_motion(game);actor.die()', '''game.grid_view._get_veld_frame_source(game)
		actor.prepare_death_motion(game);actor.die()
		check(actor.water_death_motion.get("clip","")=="death-sofa-read-south","Actual staged supported reader recipe selected")
		check(actor.valid_veld_snapshot(actor.snapshot()),"Sofa recipe admitted by actual actor snapshot validator")
		if failures:quit(1);return''')
block=block.replace('[0.0,.179,.181,.34,.54,.76,1.4]','[0.0,.179,.181,.361,.561,.781,1.021,1.52]')
block=block.replace('check(shown!=null,"Actual selected death source available")', '''check(shown!=null,"Actual selected death source available")
			var key:String="diving-helmet" if equipped else ""
			var frames:Array=game.grid_view.veld_player.frames["death-sofa-read-south"] if key.is_empty() else game.grid_view.veld_player.equipment_frames[key]["death-sofa-read-south"]
			var index:int=0 if elapsed<.18 else (1 if elapsed<.36 else (2 if elapsed<.56 else (3 if elapsed<.78 else (4 if elapsed<1.02 else 5))))
			var expected:Texture2D=before if index==0 else frames[index]
			check(shown.get_image().get_data()==expected.get_image().get_data(),"Independent six-pose source-clock oracle")''')
block=block.replace('await shot(game,gear+"-"+str(elapsed),shown)', '''await shot(game,gear+"-"+str(elapsed),shown)
			check(actor.foot==Vector2(actor.water_death_motion.sofa_motion.local_foot)+(Vector2(CELL)+Vector2.ONE*.5)*384,"Physical navigation foot unchanged through supported fall")
			if elapsed<.36:check(offset==actor.water_death_motion.entry_position_offset,"Sofa supports entrance and slump")
			if elapsed>=.78:check(offset==Vector2.ZERO and is_equal_approx(DEATH.draw_depth(game,actor,shown,at),at.y),"Floor contact/depth releases fully by floor pose")
			if elapsed in [.179,.361,.781,1.52]:
				var file=FileAccess.open("user://sofa-actor.snapshot",FileAccess.WRITE);file.store_var(actor.snapshot());file.close()
				file=FileAccess.open("user://sofa-actor.snapshot",FileAccess.READ);var disk:Dictionary=file.get_var();file.close()
				var restored=actor.get_script().new();await restored.restore_snapshot(game,disk,true);game.veld_npc=restored
				check(restored.dead and restored.geometry.is_empty(),"Fresh dead actor-file restore")
				check(game.grid_view._get_veld_frame_source(game).get_image().get_data()==shown.get_image().get_data() and DEATH.visual_offset(game,restored)==offset,"Actor-file source/contact exact at saved clock")
				check(is_equal_approx(DEATH.draw_depth(game,restored,shown,at),DEATH.draw_depth(game,actor,shown,at)),"Actor-file sofa/floor depth exact")
				game.veld_npc=actor;restores+=1
		for invalid in ["first","seat","equipment","slot"]:
			var bad:Dictionary=actor.snapshot().duplicate(true)
			match invalid:
				"first":bad.veld_water_death.first=2
				"seat":bad.veld_water_death.sofa_motion.seat+=Vector2(0,10)
				"equipment":bad.veld_water_death.entry_equipment="" if equipped else "diving-helmet"
				"slot":bad.veld_water_death.entry_index=14
			check(not actor.valid_veld_snapshot(bad),"Malformed sofa death recipe rejected: "+invalid)
		interruptions+=1''')
block='\t\tfor reading_sample in [.05,.10,.25,.40,2.40,4.20]:\n'+''.join('\t'+line if line.strip() else line for line in block.splitlines(True))
s=s[:start]+block+s[end:]
s=s.replace('VELD SOUTH SOFA FALL DIAGNOSTIC:','VELD SOUTH SOFA FALL STAGED:').replace('two prescribed actor mortality contexts; visual result pending','12 prescribed actor deaths/48 actor-file restores; visual result pending')
s=s.replace('print("VELD SOUTH SOFA FALL STAGED:', 'check(interruptions==12 and restores==48,"Twelve distinct incoming poses and48actor restores")\n\tprint("VELD SOUTH SOFA FALL STAGED:')
(R/'tests/test_veld_sofa_fall_south_staged.gd').write_text(s,encoding='utf-8')
(R/'tests/test_veld_sofa_fall_south_staged.gd.uid').write_text('uid://d0evssfstag1\n',encoding='utf-8')
w=(R/'tools/run_veld_south_sofa_fall_diagnostic.py').read_text(encoding='utf-8')
w=w.replace('veld-south-sofa-fall-diagnostic-v1','veld-sofa-fall-south-staged-v1').replace('test_veld_south_sofa_fall_diagnostic.gd','test_veld_sofa_fall_south_staged.gd')
w=w.replace('VELD SOUTH SOFA FALL DIAGNOSTIC','VELD SOUTH SOFA FALL STAGED').replace('0 failures; two prescribed actor mortality contexts','0 failures; 12 prescribed actor deaths/48 actor-file restores')
w=w.replace("photo=OUT/'helmet-1.4-room.png'","photo=OUT/'helmet-4.2-1.52-room.png'")
w=w.replace("'scripts/veld_death_motion.gd',", "'scripts/veld_death_motion.gd','character/veld-sofa-fall-south-v1/build.py',")
w=w.replace('frozen_paths=sorted(set(frozen_paths))', '''for gear in ['bare','helmet']:
        manifest=ROOT/f'character/veld-sofa-fall-south-v1/{gear}-manifest.json'
        frozen_paths.append(manifest)
        for state in json.loads(manifest.read_text(encoding='utf-8'))['states']:
            frozen_paths.extend(ROOT/f.removeprefix('res://') for f in state['frameFiles'])
    frozen_paths=sorted(set(frozen_paths))''')
(R/'tools/run_veld_sofa_fall_south_staged.py').write_text(w,encoding='utf-8')
print('Prepared isolated paired staged sofa fall and actor-file fixture')
