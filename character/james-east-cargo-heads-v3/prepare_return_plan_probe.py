from pathlib import Path
p=Path(__file__).resolve().parent
prefix=(p/'native-workshop.gd').read_text().split('\n\tfor room in game.placed_rooms:room.water_level=0.0')[0]
body='''
	var planner=preload("res://character/james-east-cargo-heads-v3/return_plan.gd")
	var plans:Array=[];var join_gaps:=0;var idle_gaps:=0
	for gear in ["","diving-helmet"]:
		var bank:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
		var clocks:Dictionary=player.timing if gear.is_empty() else player.equipment_timing[gear]
		for key in bank:
			if not key.begins_with("pickup-") and not key.begins_with("unload-") and not key.begins_with("carry-"):continue
			for index in bank[key].size():
				var plan:Dictionary=planner.build(player,key,index,gear)
				check(not plan.is_empty(),"Admit loaded cargo slot "+key)
				if plan.is_empty():continue
				check(plan.rows[0].key==key and plan.rows[0].index==index and plan.rows[0].seconds==.08,"Exact displayed first slot retained")
				check(planner.same(bank[key][index],bank[plan.rows[0].key][plan.rows[0].index]),"First RGBA exact")
				var seconds:=0.0
				for j in plan.rows.size():
					var row:Dictionary=plan.rows[j];check(bank.has(row.key) and row.index>=0 and row.index<bank[row.key].size(),"Loaded row exists")
					check(row.seconds>0 and is_finite(row.seconds),"Finite positive source hold")
					if j>0:check(absf(row.seconds-float(clocks[row.key].durations[row.index])/1000)<.000001,"Original authored hold preserved")
					seconds+=row.seconds
				plan.seconds=seconds
				for gap in plan.gaps:
					if str(gap.to).begins_with("unload-"):join_gaps+=1
					else:idle_gaps+=1
				plans.append(plan)
		check(planner.build(player,"idle-east",0,gear).is_empty(),"Reject noncargo")
		check(planner.build(player,"pickup-east",-1,gear).is_empty(),"Reject invalid source index")
		check(planner.build(player,"pickup-east",999,gear).is_empty(),"Reject absent source index")
	var f:=FileAccess.open(OUT+"return-plan-probe-evidence.json",FileAccess.WRITE)
	f.store_string(JSON.stringify({"checks":checks,"failures":failures,"plans":plans,"heldJoinGaps":join_gaps,"idleJoinGaps":idle_gaps,"scope":"Staged unselected finite whole-source plans through normal loaded James bank; every dry cargo source slot and both gears. No controller execution, safety, room clearance, floor crate, saves or continuous motion acceptance."},"  "))
	for name in ["return_plan.gd","return-plan-probe.gd"]:
		if not FileAccess.file_exists(OUT+name+".uid"):
			var uid:=FileAccess.open(OUT+name+".uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("JAMES RETURN PLANS: ",plans.size(),"plans; ",checks,"checks; ",failures,"failures; ",join_gaps,"held join gaps; ",idle_gaps,"idle joins pending")
	quit(1 if failures else 0)
'''
(p/'return-plan-probe.gd').write_text(prefix+body)
print('Prepared normal-loader source planner probe.')
