"""Native staged meal/drink chain and controlled return-cut dispatch review."""
from pathlib import Path
P=Path(__file__).resolve().parent
s=(P/'native-reach-candidate.gd').read_text()
start=s.index('class CandidateJames');end=s.index('\nvar game',start)
s=s[:start]+'''class CandidateJames extends "res://scripts/branforth_npc.gd":
	var preview_key:String=""
	var preview_elapsed:float=0.0
	var cycle_lengths:Dictionary={"eat":1.5,"drink":3.0}
	func animation_state()->String:
		if not preview_key.is_empty():return preview_key.trim_suffix("-south")
		if active and not dead and not helmet_equipped and movement_medium=="dry" and direction=="south":
			if stage=="life_eat":
				if timer>5.1:return "meal-acquire"
				return "meal-deposit" if timer<=.9 else "eat"
			if stage=="life_drink":
				if timer>2.1:return "cup-acquire"
				return "cup-deposit" if timer<=.9 else "drink"
		return super.animation_state()
	func action_elapsed()->float:
		if not preview_key.is_empty():return preview_elapsed
		var pose=animation_state()
		if pose=="meal-acquire":return 6.0-timer
		if pose=="cup-acquire":return 3.0-timer
		if pose in ["meal-deposit","cup-deposit"]:return .9-timer
		if pose=="eat" and stage=="life_eat":return fposmod(6.0-timer-.9,1.4)/1.4*float(cycle_lengths.eat)
		if pose=="drink" and stage=="life_drink":return (3.0-timer-.9)/1.2*float(cycle_lengths.drink)
		return super.action_elapsed()
''' +s[end:]
s=s.replace('reach-manifest.json','handoffs-manifest.json').replace('reach-captures','handoff-captures')
start=s.index('\tvar foot:Vector2=npc.foot;');end=s.index('\n\tvar file:=',start)
s=s[:start]+'''	var foot:Vector2=npc.foot;var frames:Dictionary={};var samples:Array=[];var last:Texture2D;var previous:String=""
	var manifest_states:Dictionary={}
	var pack:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/james-meal-service-south-open-v1/handoffs-manifest.json"))
	for entry in pack.states:
		manifest_states[entry.id]=entry
		if entry.id in ["eat-south","drink-south"]:
			var duration:=0.0
			for ms in entry.frameDurationsMs:duration+=float(ms)*.001
			npc.cycle_lengths[entry.id.trim_suffix("-south")]=duration
	var normal_states:Array=["meal-acquire","eat","meal-deposit","cup-acquire","drink","cup-deposit"]
	var completed:=false
	for tick in range(1200):
		var pose:String=npc.animation_state();var texture:Texture2D=game.grid_view._get_branforth_frame_source(game)
		if pose not in normal_states:
			check(last!=null and last.get_image().get_region(Rect2i(36,52,184,192)).get_data()==texture.get_image().get_data(),"Final deposit joins actual selected empty idle after common-pivot crop")
			completed=true;break
		var key:String=pose+"-south";var index:int=player.frames[key].find(texture)
		check(index>=0,"Actual drawer selects staged handoff/loop source")
		if previous!=pose and last!=null:check(last.get_image().get_data()==texture.get_image().get_data(),"Exact source join "+previous+" to "+pose)
		if not frames.has(key):frames[key]={}
		if not frames[key].has(index):
			check(npc.foot==foot and npc.direction=="south","Whole meal/drink source remains at supported contact")
			frames[key][index]=true;samples.append({"key":key,"index":index,"elapsed":npc.action_elapsed(),"capture":await capture("%s-%02d"%[pose,index],npc)})
		last=texture;previous=pose;game._update_test_walker(1.0/120);game.visual_time_seconds+=1.0/120
	check(completed,"Actual Life.next progresses meal6s through drink3s to empty idle")
	for pose in normal_states:
		var key:String=pose+"-south";check(frames.has(key) and frames[key].size()==manifest_states[key].frameCount,"All candidate sources drawn "+key)
	var controlled_cuts:Array=[]
	npc.stage="";npc.goal="";npc.path.clear();npc.state="idle";npc.direction="south";npc.foot=foot
	for entry in pack.states:
		if not String(entry.id).begins_with("meal-return-"):continue
		var source_key:String=entry.provenance.sourceState;var source_index:int=entry.provenance.sourceIndex
		var source_time:=.00001
		for index in range(source_index):source_time+=float(manifest_states[source_key].frameDurationsMs[index])*.001
		npc.preview_key=source_key;npc.preview_elapsed=source_time
		var before:Texture2D=game.grid_view._get_branforth_frame_source(game)
		check(before.get_image().get_data()==player.frames[source_key][source_index].get_image().get_data(),"Controlled source clock selects exact interruption pose "+entry.id)
		npc.preview_key=entry.id;npc.preview_elapsed=0.0
		var first:Texture2D=game.grid_view._get_branforth_frame_source(game)
		check(first.get_image().get_data()==before.get_image().get_data(),"Actual return drawer begins with exact current pixels "+entry.id)
		check(first.get_meta("crew_depth_offset",0)==before.get_meta("crew_depth_offset",0),"Return cut retains exact depth "+entry.id)
		var duration:=0.0
		for ms in entry.frameDurationsMs:duration+=float(ms)*.001
		npc.preview_elapsed=duration+.00001
		var terminal:Texture2D=game.grid_view._get_branforth_frame_source(game)
		check(terminal.get_image().get_data()==player.frames["meal-acquire-south"][0].get_image().get_data(),"Return clamps to exact empty standing "+entry.id)
		controlled_cuts.append({"key":entry.id,"sourceIndex":source_index,"duration":duration,"firstExact":true,"lastExact":true})
	check(controlled_cuts.size()==44,"All44 source-index return variants dispatched")
	npc.preview_key=""
''' +s[end:]
s=s.replace('native-reach-candidate','native-handoffs-candidate')
s=s.replace('var completed:=false','var completed:=false;var normal_completion:Dictionary={}')
s=s.replace('if pose not in normal_states:\n', 'if pose not in normal_states:\n\t\t\tnormal_completion={"snapshot":npc.snapshot(),"pose":pose,"playerKey":player.current_key,"textureSize":texture.get_size(),"lastSize":last.get_size() if last!=null else Vector2.ZERO,"capture":await capture("normal-completion",npc)}\n\t\t\tprint("ACTUAL NORMAL COMPLETION ",normal_completion)\n')
s=s.replace('check(last!=null and last.get_image().get_region(Rect2i(36,52,184,192)).get_data()==texture.get_image().get_data(),"Final deposit joins actual selected empty idle after common-pivot crop")','var registered_idle:=Image.create(256,256,false,Image.FORMAT_RGBA8)\n\t\t\tregistered_idle.fill(Color(0,0,0,0))\n\t\t\tvar pivot_delta:Vector2=last.get_meta("crew_pivot")-texture.get_meta("crew_pivot")\n\t\t\tregistered_idle.blit_rect(texture.get_image(),Rect2i(Vector2i.ZERO,texture.get_image().get_size()),Vector2i(pivot_delta))\n\t\t\tcheck(last!=null and last.get_image().get_data()==registered_idle.get_data(),"Final deposit joins complete live idle image after metadata-pivot registration")')
s=s.replace('"samples":samples,','"samples":samples,"controlledCuts":controlled_cuts,"frameCoverage":frames,"normalCompletion":normal_completion,')
s=s.replace('Eight-pose reach candidate from independent whole authored sources, exact registered endpoints; staged only, not installed or visually accepted.','Staged complete9second South meal/drink presentation via temporary CandidateJames subclass. Normal actual Life.next and supported chooser/route; all6phase textures and exact joins. Return variants are controlled drawer/source-index dispatch, NOT actual hazard/clearance decision, snapshot/Continue or normal-loader proof. Cup contact/body projection remains visual review pending.')
s=s.replace('JAMES SOUTH REACH CANDIDATE','JAMES SOUTH HANDOFFS CANDIDATE')
(P/'native-handoffs-candidate.gd').write_text(s)
print('Actual normal meal/drink stage flow with candidate visuals;44controlled return dispatches.')
