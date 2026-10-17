"""Build a normal-loader interruption fixture from retained staged evidence."""
from pathlib import Path
R=Path(__file__).resolve().parents[2]
p=R/'tests/test_veld_read_south_interrupt.gd'
s=p.read_text(encoding='utf-8')
s=s.replace('tests/test_veld_read_south_continue.gd','tests/test_veld_seated_south_selected.gd')
s=s.replace('veld-read-south-interrupt-v1','veld-south-read-interrupt-selected-v1')
s=s.replace('test_veld_read_south_interrupt.gd','test_veld_south_read_interrupt_selected.gd')
s=s.replace('func run():', '''func sample(game)->Dictionary:
	var actor=game.veld_npc
	var texture:Texture2D=game.grid_view._get_veld_live_frame_source(game)
	var at:Vector2=actor.foot-(Vector2(CELL)+Vector2.ONE*.5)*384+LIFE.offset(actor)
	return {"pixel":texture.get_image().get_data().hex_encode().sha256_text(),"stage":actor.stage,"timer":actor.timer,"pose":actor.tablet_exit_pose,"foot":[actor.foot.x,actor.foot.y],"offset":[LIFE.offset(actor).x,LIFE.offset(actor).y],"depth":LIFE.seated_draw_depth(actor,texture,at),"gear":actor.helmet_equipped,"goal":actor.goal,"needs":actor.needs.duplicate(true)}
func future(game,name:String,captures:bool)->Array:
	var sequence:Array=[]
	var last_signature=""
	for tick in 180:
		var value=sample(game)
		sequence.append(value)
		var signature:String=value.pixel+value.stage
		if captures and signature!=last_signature:
			await capture_exit(game,name+"-future-"+str(tick),game.grid_view._get_veld_live_frame_source(game))
		last_signature=signature
		if game.veld_npc.stage.is_empty():break
		game.veld_npc.update(game,1.0/120)
		game.visual_time_seconds+=1.0/120
	check(game.veld_npc.stage.is_empty(),"Finite interruption reaches ordinary standing")
	return sequence
func compare_future(expected:Array,actual:Array):
	check(expected.size()==actual.size(),"Fresh Continue finite sequence length")
	for i in mini(expected.size(),actual.size()):
		for key in ["pixel","stage","pose","foot","offset","gear","goal"]:
			check(expected[i][key]==actual[i][key],"Future exact source/contact/state "+key)
		for key in ["timer","depth"]:
			check(is_equal_approx(expected[i][key],actual[i][key]),"Future resumed clock/depth "+key)
		for key in expected[i].needs:
			check(is_equal_approx(expected[i].needs[key],actual[i].needs[key]),"Future resumed needs "+key)
func run():''')
s=s.replace('var records:Array=[]','var records:Array=[]\n\tvar saved_sources:Dictionary={}\n\tvar future_records:Array=[]')
s=s.replace('[.2,3.0,4.4,11.8]','[.05,.10,.25,.40,.60,2.40,4.20,6.10,8.00,10.00,11.55,11.70,11.85,11.95]')
s=s.replace('if loss=="power" and elapsed==3.0:', '''var binding:String=("helmet" if equipped else "bare")+before.get_image().get_data().hex_encode().sha256_text()
				if loss=="power" and not saved_sources.has(binding):
					saved_sources[binding]=true''')
s=s.replace('var disk:Dictionary=SAVE.read(game.run_save_path);check(not disk.is_empty(),"Interrupted exit disk read")','''var disk:Dictionary=SAVE.read(game.run_save_path);check(not disk.is_empty(),"Interrupted exit disk read")
					var reference_future=await future(game,name+"-reference",true)
					if failures:quit(1);return''')
s=s.replace('restores+=1','''var resumed_future=await future(game,name+"-resumed",false)
					compare_future(reference_future,resumed_future)
					future_records.append({"name":name,"reference":reference_future,"resumed":resumed_future})
					restores+=1''')
s=s.replace('"scope":"actual NPC power/suspend guard and timed exit, prescribed sofa entry with staged source overrides"','"futures":future_records,"scope":"normal loader, actual power/suspension guards at all fourteen reading slots; prescribed default South sofa contact, paused world with actor stepped; six unique poses per gear ordinary disk/fresh-main finite future Continue"')
s=s.replace('check(restores==2,"Both gears interrupted exit disk Continue")','check(restores==12 and interruptions==56,"Both gears/all fourteen slots/two losses and twelve distinct-pose disk futures")')
s=s.replace('VELD READ SOUTH INTERRUPT:','VELD SOUTH READ INTERRUPT SELECTED:')
s=s.replace('Actual interrupted contact held")','Actual interrupted contact held")\n\t\t\t\tcheck(is_equal_approx(sample(game).depth,LIFE.seated_draw_depth(actor,before,actor.foot-(Vector2(CELL)+Vector2.ONE*.5)*384+LIFE.offset(actor))),"Interruption retains seat depth")')
(R/'tests/test_veld_south_read_interrupt_selected.gd').write_text(s,encoding='utf-8')
(R/'tests/test_veld_south_read_interrupt_selected.gd.uid').write_text('uid://d0evsrdisel1\n',encoding='utf-8')
w=(R/'tools/run_veld_read_south_interrupt.py').read_text(encoding='utf-8')
w=w.replace('veld-read-south-interrupt-v1','veld-south-read-interrupt-selected-v1').replace('test_veld_read_south_interrupt.gd','test_veld_south_read_interrupt_selected.gd')
w=w.replace('timeout=600','timeout=900').replace('0 failures; 16 interruptions','0 failures; 56 interruptions').replace('VELD READ SOUTH INTERRUPT','VELD SOUTH READ INTERRUPT SELECTED')
w=w.replace("before=fingerprint();", """frozen_paths=[ROOT/p for p in ['scripts/grid_canvas.gd','scripts/veld_npc.gd','scripts/bill_npc.gd','scripts/crew_life.gd','scripts/crew_sprite_player.gd','scripts/run_save.gd','character/ACTIVE_ASSETS.json','tests/test_veld_south_read_interrupt_selected.gd','tests/test_veld_seated_south_selected.gd','tests/test_veld_seated_north_continue.gd']]
    for gear in ['bare','helmet']:
        manifest=ROOT/f'character/veld-seated-south-selected-v1/{gear}-manifest.json'
        frozen_paths.append(manifest)
        data=json.loads(manifest.read_text(encoding='utf-8'))
        for state in data['states']:
            for frame in state['frameFiles']:
                value=frame if isinstance(frame,str) else frame['path']
                frozen_paths.append(ROOT/value.removeprefix('res://'))
    frozen_paths=sorted(set(frozen_paths))
    frozen={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in frozen_paths}
    (OUT/'inputs-before.json').write_text(json.dumps(frozen,indent=2)+'\\n',encoding='utf-8')
    before=fingerprint();""")
w=w.replace('after=fingerprint();',"""inputs_after={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in frozen_paths}
    input_changes=sorted(k for k in frozen if frozen[k]!=inputs_after[k])
    (OUT/'inputs-after.json').write_text(json.dumps(inputs_after,indent=2)+'\\n',encoding='utf-8')
    after=fingerprint();""")
w=w.replace("runtime and not changes", "runtime and not changes and not input_changes")
w=w.replace("'runtimePassed':runtime", "'frozenInputCount':len(frozen),'frozenInputChanges':input_changes,'runtimePassed':runtime")
(R/'tools/run_veld_south_read_interrupt_selected.py').write_text(w,encoding='utf-8')
print('Prepared normal-loader fixture and isolated runner')
