from pathlib import Path
p=Path(__file__).resolve().parent;r=p.parents[1]
text=(r/'character/james-east-cargo-heads-v3/interruption-probe.gd').read_text().replace('const OUT := "res://character/james-east-cargo-heads-v3/"','const OUT := "res://character/james-cargo-return-bridges-v1/"')
needle='npc.movement_medium="dry"\n'
injection='''npc.movement_medium="dry"
	npc=preload("res://character/james-cargo-return-bridges-v1/return_actor.gd").new()
	game.branforth_npc=npc;npc.rebuild(game);npc.active=true;npc.movement_medium="dry"
	var baseline=player
	player=preload("res://character/james-cargo-return-bridges-v1/return_player.gd").new()
	for property in ["frames","timing","strides","gait_phase_groups","equipment_frames","equipment_timing","equipment_strides"]:player.set(property,baseline.get(property).duplicate(true))
	player.load_manifest(OUT+"bare-joined-manifest-v4.json",true)
	check(player.load_equipment_manifest("diving-helmet",OUT+"helmet-joined-manifest-v4.json"),"Paired bridge loads")
	game.grid_view.branforth_player=player;npc.preview_player=player
'''
assert text.count(needle)==1;text=text.replace(needle,injection)
text=text.replace('player.current_key="";player.motion.clear();player.last_time=-1','player.current_key="";player.motion.clear();player.last_time=-1;player.return_plan.clear();player.last_source.clear()')
text=text.replace('interrupt-','candidate-return-')
needle='var capture_after:String=await capture("candidate-return-"+stem+"-after-000",npc)'
new=needle+'''
			var immediate:Dictionary={"afterStage":npc.stage,"afterPose":npc.animation_state(),"afterTimer":npc.timer,"afterMotion":player.motion.duplicate(true)}
			var plan:Dictionary=player.return_plan.duplicate(true)
			check(not plan.is_empty(),"Return admitted for "+stem+": "+npc.return_reason)
			var trace:Array=[];var seen:Dictionary={};var baseline_need:float=npc.needs.curiosity;var stepped:=0.0
			if not plan.is_empty():
				check(before.get_image().get_data()==after.get_image().get_data(),"Exact first displayed pose retained")
				check(not preload("res://scripts/branforth_npc.gd").valid_snapshot(npc.snapshot()),"Unsupported candidate checkpoint explicitly rejected")
				for tick in range(400):
					var clock:float=game.visual_time_seconds
					if clock>=plan.until:break
					var cursor:float=clock-plan.started;var selected:Dictionary={}
					for row in plan.rows:
						cursor-=row.seconds
						if cursor<0:selected=row;break
					check(not selected.is_empty(),"Finite source oracle")
					var texture:Texture2D=game.grid_view._get_branforth_frame(game)
					var bank:Dictionary=player.bank_for(plan.gear)
					check(texture.get_image().get_data()==bank[selected.key][selected.index].get_image().get_data(),"Actual drawn return slot exact")
					check(npc.foot==before_foot and npc.path.is_empty() and npc.goal=="","Physical contact and cancelled work goal retained")
					var tag:String=selected.key+"-"+str(selected.index)
					if not seen.has(tag):
						seen[tag]=true
						var label:String="candidate-return-"+stem+"-pose-%02d-000"%seen.size()
						texture.get_image().save_png(OUT+"arrival-captures/"+label+"-source.png")
						trace.append({"key":selected.key,"index":selected.index,"time":clock,"world":await capture(label,npc),"source":OUT+"arrival-captures/"+label+"-source.png"})
					game.visual_time_seconds+=.02;npc.update(game,.02);stepped+=.02
				check(player.return_plan.is_empty(),"Finite return source segment completes")
				check(absf(npc.needs.curiosity-(baseline_need+stepped*.22))<.0001,"Needs remain live; no cancelled work reward")
				check(npc.foot==before_foot,"Foot planted through completion update")
			results.append({"mode":mode,"target":target,"admitted":not plan.is_empty(),"plan":plan,"trace":trace,"returnReason":npc.return_reason,"geometry":npc.return_geometry.duplicate(true),"curiosityBefore":baseline_need,"curiosityAfter":npc.needs.curiosity,"elapsed":stepped,"sameFoot":before_foot==npc.foot})
'''
assert text.count(needle)==1;text=text.replace(needle,new)
# Preserve initial before/after record separately as a diagnostic, not a second
# lifecycle case count.
text=text.replace('results.append({"mode":mode,"target":target,"beforeStage":','results.append({"diagnostic":true,"mode":mode,"target":target,"beforeStage":')
text=text.replace('"afterStage":npc.stage,"afterPose":npc.animation_state(),"afterTimer":npc.timer,"afterMotion":player.motion.duplicate(true),"sameFoot"','"afterStage":immediate.afterStage,"afterPose":immediate.afterPose,"afterTimer":immediate.afterTimer,"afterMotion":immediate.afterMotion,"sameFoot"')
text=text.replace('interruption-probe-evidence.json','actor-return-evidence.json').replace('interruption-probe.gd.uid','actor-return.gd.uid')
text=text.replace('JAMES WORKSHOP INTERRUPTION PROBE: ','JAMES ACTUAL RETURN CANDIDATE: ')
text=text.replace('No corrective motion or Continue acceptance.','Staged source-bound controller return with footprint admission, live needs, all changing native source/room captures. Floor/idle and safety/ordinary Continue acceptance pending.')
text=text.replace('if not FileAccess.file_exists(OUT+"actor-return.gd.uid"):\n\t\tvar f:=FileAccess.open(OUT+"actor-return.gd.uid",FileAccess.WRITE);f.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))','for name in ["actor-return.gd","return_actor.gd","return_player.gd"]:\n\t\tif not FileAccess.file_exists(OUT+name+".uid"):\n\t\t\tvar uid:=FileAccess.open(OUT+name+".uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))')
(p/'actor-return.gd').write_text(text)
print('Prepared six actual service-loss candidate journeys with native changing-pose captures.')
