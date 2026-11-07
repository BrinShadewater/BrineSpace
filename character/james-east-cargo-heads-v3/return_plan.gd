extends RefCounted
## Staged source planner only. A missing artwork join stops the plan rather than
## silently switching to idle. Controller, cargo disposition and saves are pending.

static func same(a:Texture2D,b:Texture2D)->bool:
	return a.get_size()==b.get_size() and a.get_image().get_data()==b.get_image().get_data()

static func build(player,key:String,index:int,gear:String)->Dictionary:
	var bank:Dictionary=player.frames if gear.is_empty() else player.equipment_frames.get(gear,{})
	var clocks:Dictionary=player.timing if gear.is_empty() else player.equipment_timing.get(gear,{})
	if not bank.has(key) or not clocks.has(key) or index<0 or index>=bank[key].size():return {}
	if not key.begins_with("pickup-") and not key.begins_with("unload-") and not key.begins_with("carry-"):return {}
	var facing:String=key.get_slice("-",key.get_slice_count("-")-1)
	if facing not in ["east","west","north","south"]:return {}
	if key.begins_with("carry-") and key!="carry-"+facing and not key.begins_with("carry-turn-"):return {}
	var rows:Array=[{"key":key,"index":index,"seconds":.08}]
	var gaps:Array=[]
	if key.begins_with("pickup-"):
		for i in range(index-1,-1,-1):rows.append({"key":key,"index":i,"seconds":float(clocks[key].durations[i])/1000.0})
	elif key.begins_with("unload-"):
		for i in range(index+1,bank[key].size()):rows.append({"key":key,"index":i,"seconds":float(clocks[key].durations[i])/1000.0})
	else:
		# Complete the actual visible turn or gait remainder before unloading.
		for i in range(index+1,bank[key].size()):rows.append({"key":key,"index":i,"seconds":float(clocks[key].durations[i])/1000.0})
		var unload:String="unload-"+facing
		var final:Dictionary=rows[-1]
		var bridge:String="carry-settle-"+facing
		if bank.has(unload) and bank.has(bridge) and clocks.has(bridge) and same(bank[final.key][final.index],bank[bridge][0]) and same(bank[bridge][-1],bank[unload][0]):
			# A candidate bridge is usable only when both whole-source endpoints
			# bind exactly to the loaded source bank. Never infer joins by labels.
			for i in range(1,bank[bridge].size()):rows.append({"key":bridge,"index":i,"seconds":float(clocks[bridge].durations[i])/1000.0})
			for i in range(1,bank[unload].size()):rows.append({"key":unload,"index":i,"seconds":float(clocks[unload].durations[i])/1000.0})
		elif not bank.has(unload) or not same(bank[final.key][final.index],bank[unload][0]):
			gaps.append({"from":final,"to":unload,"reason":"Missing exact held-cargo join; authored bridge required"})
		else:
			for i in range(1,bank[unload].size()):rows.append({"key":unload,"index":i,"seconds":float(clocks[unload].durations[i])/1000.0})
	var final:Dictionary=rows[-1]
	# Source images have different canvases/pivots. Idle comparison is deliberately
	# left to registered native drawing; full RGBA identity is only a sufficient join.
	var idle:String="idle-"+facing
	if not bank.has(idle) or not same(bank[final.key][final.index],bank[idle][0]):
		gaps.append({"from":final,"to":idle,"reason":"Registered standing settlement and floor-crate handoff required"})
	return {"gear":gear,"source":key,"sourceIndex":index,"facing":facing,"rows":rows,"gaps":gaps,"selected":false}
