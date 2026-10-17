from pathlib import Path

root=Path(__file__).resolve().parents[2]
source=(root/'tests/test_veld_bunk_body_continue.gd').read_text()
source=source.replace('body_continue','body_resume').replace('body-continue-v1','body-resume-v1').replace('bunk-continue','bunk-resume').replace('BUNK CONTINUE','BUNK RESUME').replace('BODY CONTINUE','BODY RESUME')
source=source.replace('game.visual_time_seconds=400.3','game.visual_time_seconds=400.1')
source=source.replace('func run():', '''func pixels_hash(texture:Texture2D)->String:
	var ctx=HashingContext.new();ctx.start(HashingContext.HASH_SHA256);ctx.update(texture.get_image().get_data())
	return ctx.finish().hex_encode()
func motion_sample(game)->Dictionary:
	var actor=game.veld_npc;var player=game.grid_view.veld_player
	var texture:Texture2D=game.grid_view._get_veld_frame_source(game)
	var offset:Vector2=actor.observation_visual_offset()+LIFE.head_alignment(actor,player)+preload("res://scripts/veld_death_motion.gd").visual_offset(game,actor)
	var at:Vector2=actor.foot-(Vector2(CELL)+Vector2.ONE*.5)*384+offset
	return {"pixels":pixels_hash(texture),"foot":actor.foot,"stage":actor.stage,"state":actor.state,"timer":actor.timer,"gear":actor.helmet_equipped,"dead":actor.dead,"clock":game.visual_time_seconds,"offset":offset,"depth":preload("res://scripts/veld_death_motion.gd").draw_depth(game,actor,texture,at),"needs":actor.needs.duplicate(true)}
func future_trace(game,name:String)->Array:
	var result:Array=[];var previous:String=""
	for tick in 64:
		game.veld_npc.update(game,.02);game.visual_time_seconds+=.02
		var sample:Dictionary=motion_sample(game);sample.tick=tick
		check(game.veld_npc.valid_veld_snapshot(game.veld_npc.snapshot()),"Future actor snapshot valid: "+name)
		if sample.pixels!=previous or tick==63:
			var texture:Texture2D=game.grid_view._get_veld_frame_source(game)
			sample.rendered=await capture_bunk(game,CELL,name+"-tick-%02d"%tick,texture)
		previous=sample.pixels;result.append(sample)
	return result
func compare_future(expected:Array,actual:Array,name:String):
	check(expected.size()==64 and actual.size()==64,"64 future 20ms steps: "+name)
	for tick in mini(expected.size(),actual.size()):
		var a:Dictionary=expected[tick];var b:Dictionary=actual[tick]
		for key in ["pixels","foot","stage","state","gear","dead","offset","needs"]:
			check(a[key]==b[key],"Future "+key+" matches uninterrupted trace: "+name+" tick "+str(tick))
		for key in ["timer","clock","depth"]:
			check(is_equal_approx(float(a[key]),float(b[key])),"Future "+key+" matches uninterrupted trace: "+name+" tick "+str(tick))
		if a.has("rendered"):
			check(b.has("rendered"),"Corresponding native source change: "+name)
			if b.has("rendered"):
				check(a.rendered.position==b.rendered.position and is_equal_approx(a.rendered.depth,b.rendered.depth),"Future native room position/depth: "+name)
func run():''')
needle='\t\t\tcheck(game.running and not game.testing_free_build'
insert='''			var playback:Dictionary=game.grid_view.crew_playback_snapshot()
			var expected:Array=await future_trace(game,name+"-reference")
			# Restore the exact saved starting point before writing the real checkpoint.
			await actor.restore_snapshot(game,snapshot,true)
			game.grid_view.restore_crew_playback(playback);game.visual_time_seconds=clock
			check(actor.snapshot()==snapshot,"Reference trace rewound to exact actor snapshot")
			check(game.grid_view._get_veld_frame_source(game).get_image().get_data()==pixels,"Reference trace rewound to exact source")
'''
source=source.replace(needle,insert+needle)
needle='\t\t\trecords.append('
source=source.replace(needle,'\t\t\tvar actual:Array=await future_trace(game,name+"-resumed")\n\t\t\tcompare_future(expected,actual,name)\n'+needle)
source=source.replace('"before":before,"after":after}', '"before":before,"after":after,"reference":expected,"resumed":actual}')
(root/'tests/test_veld_bunk_body_resume.gd').write_text(source)
runner=(root/'tools/run_veld_bunk_body_continue.py').read_text().replace('body_continue','body_resume').replace('body-continue-v1','body-resume-v1').replace('BUNK CONTINUE','BUNK RESUME').replace('BODY CONTINUE','BODY RESUME')
runner=runner.replace('timeout=600','timeout=750')
# Bind targeted inputs before launch, without claiming every engine dependency.
runner=runner.replace('before=fingerprint();', '''inputs=[ROOT/'scripts/veld_npc.gd',ROOT/'scripts/veld_death_motion.gd',ROOT/'scripts/crew_life.gd',ROOT/'scripts/run_save.gd',ROOT/'tests/test_veld_bunk_body_resume.gd']
    inputs+=list((ROOT/'character/veld-bunk-body-master-v1/frames').rglob('*.png'))
    inputs+=[ROOT/'character/veld-bunk-body-master-v1/bare-manifest.json',ROOT/'character/veld-bunk-body-master-v1/helmet-manifest.json']
    bindings={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
    (OUT/'inputs-before.json').write_text(json.dumps(bindings,indent=2)+'\\n')
    before=fingerprint();''')
runner=runner.replace("changes=sorted(k", "after_bindings={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}\n    (OUT/'inputs-after.json').write_text(json.dumps(after_bindings,indent=2)+'\\n')\n    changes=sorted(k")
runner=runner.replace("'passed':runtime and not changes", "'passed':runtime and not changes and bindings==after_bindings,'targetedInputsUnchanged':bindings==after_bindings,'targetedInputCount':len(bindings)")
(root/'tools/run_veld_bunk_body_resume.py').write_text(runner)
