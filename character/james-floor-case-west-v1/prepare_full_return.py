from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1]
s=(p/'motion_rise_v6.gd').read_text();start=s.index('\t\tcapture_foot=fixed_foot');end=s.index('\tif not FileAccess.file_exists(OUT+"motion_rise_v6.gd.uid")')
tail='''		capture_foot=fixed_foot
		var expected:Dictionary={}
		for row in plan.rows:expected[str(row.key)+":"+str(row.index)]=true
		var seen:Dictionary={};var ticks:Array=[];var previous_signature:="";var captures:=0
		var total_ticks:int=ceili((until+.6-game.visual_time_seconds)/.02)
		for tick in range(total_ticks+1):
			if tick>0:npc.update(game,.02);game.visual_time_seconds+=.02
			var current:Texture2D=game.grid_view._get_branforth_frame(game)
			var row_id:="departure";var row_index:=-1
			if player.return_active(game.visual_time_seconds):
				var cursor:float=game.visual_time_seconds-plan.started
				for i in range(plan.rows.size()):
					cursor-=float(plan.rows[i].seconds)
					if cursor<0:row_id=str(plan.rows[i].key)+":"+str(plan.rows[i].index);row_index=i;seen[row_id]=true;break
			var owned:Dictionary=FLOOR.payload(game.occupied[ORIGIN])
			if game.visual_time_seconds<release:check(owned.is_empty(),"Full sequence no early case ownership")
			else:check(not owned.is_empty() and owned.anchor==fixed_foot-center,"Full sequence fixed released anchor")
			if row_index>=0:check(npc.foot==fixed_foot,"Full return fixed actual root")
			check(not(view.case_enabled and view.embedded_case),"Full return no duplicated case")
			var signature:String=row_id+":"+str(current.get_instance_id())
			var captured:=false
			if signature!=previous_signature or tick==total_ticks:
				await record_case(view,npc,mode+"-full-return-v6-%03d"%captures)
				results[-1]["rowId"]=row_id;results[-1]["rowIndex"]=row_index
				captures+=1;captured=true;previous_signature=signature
			ticks.append({"time":game.visual_time_seconds,"rowId":row_id,"rowIndex":row_index,"captured":captured,"foot":[npc.foot.x,npc.foot.y],"owned":not owned.is_empty(),"embedded":view.embedded_case,"enabled":view.case_enabled})
		for key in expected:check(seen.has(key),"Every admitted source row visible: "+key)
		check(player.return_plan.is_empty() and npc.foot.distance_to(fixed_foot)>1,"Full return completes and actual departure starts")
		results.append({"fullReturn":true,"mode":mode,"plan":plan,"ticks":ticks,"expectedRows":expected.keys(),"seenRows":seen.keys(),"captures":captures,"release":release,"until":until,"fixedFoot":[fixed_foot.x,fixed_foot.y],"departure":npc.foot.distance_to(fixed_foot)})
		print("JAMES FULL RETURN ",mode," ticks=",ticks.size()," captured=",captures," rows=",seen.size()," failures=",failures)
		if failures:quit(1);return
'''
s=s[:start]+tail+s[end:];s=s.replace('motion_rise_v6.gd.uid','full_return_v6.gd.uid').replace('motion_rise_v6-evidence.json','full_return_v6-evidence.json')
s=s.replace('Two actual prescribed carry power-loss returns/both gears.45native20ms samples each around release/finite completion and first ordinary departure; fixed camera anchored at unload contact.90source/room pairs.','Two actual prescribed carry power-loss returns/both gears. Full finite program with20ms actor updates, native source/world capture on every source row/texture change plus last departure sample. Per-tick room/contact assertions and exact row coverage. Fixed camera; all admitted carry/turn/bridge/unload rows exercised.').replace('failures;90presentations','failures;full source-change presentations')
(p/'full_return_v6.gd').write_text(s)
prior=json.loads((p/'motion_rise_v6-inputs.json').read_bytes());paths=[r/k for k in prior]+[p/'full_return_v6.gd']
(p/'full_return_v6-inputs.json').write_text(json.dumps({str(path.relative_to(r)):hashlib.sha256(path.read_bytes()).hexdigest() for path in paths},indent=2)+'\n')
print('Full finite return20ms updates/source-change native captures prepared;40targeted inputs frozen.')
