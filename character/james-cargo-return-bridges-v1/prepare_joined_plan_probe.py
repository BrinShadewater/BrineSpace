from pathlib import Path
p=Path(__file__).resolve().parent;r=p.parents[1]
text=(r/'character/james-east-cargo-heads-v3/return-plan-probe.gd').read_text()
text=text.replace('const OUT := "res://character/james-east-cargo-heads-v3/"','const OUT := "res://character/james-cargo-return-bridges-v1/"')
old='var plans:Array=[];var join_gaps:=0;var idle_gaps:=0'
new='''player.load_manifest(OUT+"bare-joined-manifest-v4.json",true)
	check(player.load_equipment_manifest("diving-helmet",OUT+"helmet-joined-manifest-v4.json"),"Paired joined bridge loads")
	var plans:Array=[];var join_gaps:=0;var idle_gaps:=0;var bridge_plans:=0'''
assert text.count(old)==1;text=text.replace(old,new)
needle='for key in bank:\n'
assert text.count(needle)==1;text=text.replace(needle,needle+'\t\t\tif key=="carry-settle-west":continue\n')
needle='plans.append(plan)'
assert text.count(needle)==1;text=text.replace(needle,'if plan.rows.any(func(row):return row.key=="carry-settle-west"):bridge_plans+=1\n\t\t\t\tplans.append(plan)')
needle='check(planner.build(player,"idle-east",0,gear).is_empty(),"Reject noncargo")'
new='''check(planner.build(player,"carry-settle-west",0,gear).is_empty(),"Reject bridge as outgoing ordinary cargo")
		var key:String="carry-turn-east-west"
		var index:int=bank[key].size()-1
		var good:Dictionary=planner.build(player,key,index,gear)
		check(good.rows.any(func(row):return row.key=="carry-settle-west"),"Exact endpoints admit staged bridge")
		var retained:Texture2D=bank["carry-settle-west"][-1]
		bank["carry-settle-west"][-1]=bank["carry-settle-west"][1]
		var bad:Dictionary=planner.build(player,key,index,gear)
		check(not bad.rows.any(func(row):return row.key=="carry-settle-west") and bad.gaps.any(func(gap):return gap.to=="unload-west"),"Wrong endpoint rejects bridge without forced seam")
		bank["carry-settle-west"][-1]=retained
		check(planner.build(player,"idle-east",0,gear).is_empty(),"Reject noncargo")'''
assert text.count(needle)==1;text=text.replace(needle,new)
text=text.replace('return-plan-probe-evidence.json','joined-plan-v4-evidence.json').replace('"idleJoinGaps":idle_gaps','"idleJoinGaps":idle_gaps,"bridgePlans":bridge_plans')
text=text.replace('for name in ["return_plan.gd","return-plan-probe.gd"]:','for name in ["joined-plan-v4.gd"]:')
text=text.replace('JAMES RETURN PLANS: ','JAMES JOINED RETURN V4: ').replace('"idle joins pending")','"idle joins pending; ",bridge_plans,"bridge plans")')
text=text.replace('Staged unselected finite whole-source plans through normal loaded James bank;','Staged v4 joined candidate injection into normal loaded James bank;')
(p/'joined-plan-v4.gd').write_text(text)
print('Prepared all-slot joined-source probe and invalid endpoint rejection.')
