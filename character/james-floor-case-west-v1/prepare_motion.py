from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1]
s=(p/'release_v6.gd').read_text();prefix=s[:s.index('\tfor bad in [')]
prefix=prefix.replace('var game','var capture_foot:=Vector2.INF\nvar game',1)
prefix=prefix.replace('var center: Vector2=npc.foot/384.0*game.get_cell_size()','var center: Vector2=(capture_foot if capture_foot.is_finite() else npc.foot)/384.0*game.get_cell_size()')
prefix=prefix.replace('Rect2(npc.foot/384.0*cell_size-','Rect2((capture_foot if capture_foot.is_finite() else npc.foot)/384.0*cell_size-')
prefix=prefix.replace('"sortY":slot.item.sort_y if slot!=null else 0,','"time":game.visual_time_seconds,"pivot":[texture.get_meta("crew_pivot").x,texture.get_meta("crew_pivot").y],"height":texture.get_meta("crew_standing_height"),"sortY":slot.item.sort_y if slot!=null else 0,')
setup=s[s.index('\tfor mode in ["bare","helmet"]:'):s.index('\t\tvar gear:String=')]
tail='''		capture_foot=fixed_foot
		while game.visual_time_seconds<release-.10:
			npc.update(game,.02);game.visual_time_seconds+=.02;game.grid_view._get_branforth_frame(game)
		var first_time:float=game.visual_time_seconds
		var owned:=false;var separate:=false;var embedded:=false
		for sample in range(45):
			if sample>0:
				npc.update(game,.02);game.visual_time_seconds+=.02
			game.grid_view._get_branforth_frame(game)
			var data:Dictionary=FLOOR.payload(game.occupied[ORIGIN])
			if game.visual_time_seconds<release:check(data.is_empty(),"No early ownership")
			else:check(not data.is_empty() and data.anchor==fixed_foot-center,"Owned anchor fixed across all samples")
			if game.visual_time_seconds<until:check(npc.foot==fixed_foot,"Finite return keeps physical contact")
			check(not(view.case_enabled and view.embedded_case),"Never duplicate separate and embedded case")
			owned=owned or not data.is_empty();separate=separate or view.case_enabled;embedded=embedded or view.embedded_case
			await record_case(view,npc,mode+"-motion-v6-%03d"%sample)
		check(owned and embedded and separate and player.return_plan.is_empty(),"Capture crosses source-release and separate-prop handoff")
		results.append({"motion":true,"mode":mode,"first":first_time,"last":game.visual_time_seconds,"release":release,"until":until,"fixedFoot":[fixed_foot.x,fixed_foot.y],"samples":45,"sampleSeconds":.02,"departure":npc.foot.distance_to(fixed_foot)})
		print("JAMES FLOOR MOTION ",mode," samples45 departure=",npc.foot.distance_to(fixed_foot)," failures=",failures)
		if failures:quit(1);return
	if not FileAccess.file_exists(OUT+"motion_v6.gd.uid"):
		var uid:=FileAccess.open(OUT+"motion_v6.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	var f:=FileAccess.open(OUT+"motion_v6-evidence.json",FileAccess.WRITE)
	f.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"Two actual prescribed carry power-loss returns/both gears.45native20ms samples each around release/finite completion and first ordinary departure; fixed camera anchored at unload contact.90source/room pairs. V6 separate prop, original embedded unload frames. No full V9 return/normal selection/Continue/natural scheduling or full master acceptance."},"  "))
	print("JAMES FLOOR MOTION: ",checks,"checks; ",failures,"failures;90presentations")
	quit(1 if failures else 0)
'''
(p/'motion_v6.gd').write_text(prefix+setup+tail)
prior=json.loads((p/'release_v6-inputs.json').read_bytes())
paths=[r/k for k in prior if Path(k).name!='release_v6.gd']+[p/'motion_v6.gd']
(p/'motion_v6-inputs.json').write_text(json.dumps({str(path.relative_to(r)):hashlib.sha256(path.read_bytes()).hexdigest() for path in paths},indent=2)+'\n')
print('Two45sample20ms fixed-camera source/room motion captures prepared;14targeted inputs frozen.')
