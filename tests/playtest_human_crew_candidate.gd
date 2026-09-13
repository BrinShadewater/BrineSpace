extends SceneTree
## Native render review at a consistent world scale, including every frame slot.
var output: String
var failures := 0
class ToolFixture:
	var marsh_npc=preload("res://scripts/marsh_npc.gd").new()
func check(ok: bool, why: String) -> void:
	if not ok: failures+=1; push_error(why)
func anchored_pixels(source: Image,pivot: Vector2) -> PackedByteArray:
	var canvas:=Image.create(512,512,false,Image.FORMAT_RGBA8)
	canvas.fill(Color(0,0,0,0))
	canvas.blit_rect(source,Rect2i(Vector2i.ZERO,source.get_size()),Vector2i(Vector2(256,384)-pivot))
	return canvas.get_data()
func pixels(texture: Texture2D) -> PackedByteArray:
	return anchored_pixels(texture.get_image(),texture.get_meta("crew_pivot"))
class Sheet extends Node2D:
	var player
	var keys: Array=[]
	var page := 0
	var phase := 0
	func _draw() -> void:
		draw_rect(Rect2(0,0,1440,960),Color("293b40"))
		for slot in range(24):
			var index: int=page*24+slot
			if index>=keys.size():break
			var key: String=keys[index]
			var origin:=Vector2((slot%4)*360,(slot/4)*160)
			draw_string(ThemeDB.fallback_font,origin+Vector2(8,17),key,HORIZONTAL_ALIGNMENT_LEFT,-1,14,Color.WHITE)
			for col in range(2):
				var rows: Dictionary=player.frames if col==0 else player.equipment_frames["diving-helmet"]
				if not rows.has(key):continue
				var texture: Texture2D=rows[key][phase%rows[key].size()]
				var pivot: Vector2=texture.get_meta("crew_pivot")
				var scale: float=65.28/float(texture.get_meta("crew_standing_height"))*1.5
				var anchor:=origin+Vector2(86+col*180,138 if not texture.get_meta("crew_water_pose") else 95)
				draw_texture_rect(texture,Rect2(anchor-pivot*scale,texture.get_size()*scale),false)
func _init() -> void:call_deferred("run")
func run() -> void:
	if DisplayServer.get_name()=="headless":quit(2);return
	var args := OS.get_cmdline_user_args()
	var actor: String = args[0] if not args.is_empty() else "veld"
	var revision: String = {"veld":"dr-veld-v2","branforth":"chief-engineer-branforth-v2","marsh":"marsh-v2"}[actor]
	output="res://output/crew-replacement-2026-09-12/"+actor+"/native/"
	if "welding-sides" in args:output="res://output/crew-replacement-2026-09-12/"+actor+"/welding-sides-native/"
	if "welding-all" in args:output="res://output/crew-replacement-2026-09-12/"+actor+"/welding-all-native/"
	if "scanner-study" in args:output="res://output/crew-replacement-2026-09-12/"+actor+"/scanner-study-native/"
	if "scanner-selected" in args:output="res://output/crew-replacement-2026-09-12/"+actor+"/scanner-selected-native/"
	if "cargo-east" in args:output="res://output/crew-replacement-2026-09-12/"+actor+"/cargo-native/"
	if "cargo-west" in args:output="res://output/crew-replacement-2026-09-12/"+actor+"/cargo-west-native/"
	if "cargo-south" in args:output="res://output/crew-replacement-2026-09-12/"+actor+"/cargo-south-native/"
	if "cargo-north" in args:output="res://output/crew-replacement-2026-09-12/"+actor+"/cargo-north-native/"
	var seating_direction: String=""
	for direction in ["east","north","south","west"]:
		if "seating-"+direction in args:seating_direction=direction
	if not seating_direction.is_empty():output="res://output/crew-replacement-2026-09-12/"+actor+"/seating-"+seating_direction+"-native/"
	if "sleeping-north" in args:output="res://output/crew-replacement-2026-09-12/"+actor+"/sleeping-north-native/"
	if "sleeping-east" in args:output="res://output/crew-replacement-2026-09-12/"+actor+"/sleeping-east-native/"
	if "sleeping-west" in args:output="res://output/crew-replacement-2026-09-12/"+actor+"/sleeping-west-native/"
	if "sleeping-south" in args:output="res://output/crew-replacement-2026-09-12/"+actor+"/sleeping-south-native/"
	DirAccess.make_dir_recursive_absolute(output)
	root.size=Vector2i(1440,960)
	root.content_scale_size=Vector2i.ZERO
	root.content_scale_factor=1.0
	var player=load("res://scripts/crew_sprite_player.gd").new()
	var base: String="res://character/"+revision+"/"
	var catalog: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(base+"catalog.json"))
	for path in catalog.body: player.load_manifest(base+str(path),true)
	player.equipment_frames["diving-helmet"]={}
	for path in catalog.equipment: check(player.load_equipment_manifest("diving-helmet",base+str(path)),"Equipment loaded: "+str(path))
	var contract: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://tools/crew-art-source-contracts/"+actor+".json"))
	var supplemental: Dictionary={}
	var supplemental_path: String="res://tools/crew-art-source-contracts/"+actor+"-supplemental.json"
	if FileAccess.file_exists(supplemental_path):supplemental=JSON.parse_string(FileAccess.get_file_as_string(supplemental_path))
	check(player.frames.size()==contract.states.size()+supplemental.size(),"Complete body coverage")
	for key in supplemental:
		check(player.frames.has(key),"Supplemental body coverage "+key)
		if player.frames.has(key):check(player.timing[key].durations==supplemental[key].durations and player.frames[key].size()==supplemental[key].sha256.size(),"Supplemental frame count and timing "+key)
	check(player.equipment_frames["diving-helmet"].size()==(0 if actor=="marsh" else contract.equipment.size()),"Complete gear coverage")
	for entry in contract.states:
		var expected_durations: Array=[130.0,170.0,150.0,200.0,150.0,100.0] if actor=="branforth" and entry.id=="walk-west" else entry.timing.durations
		check(player.timing[entry.id].durations==expected_durations,"Timing "+entry.id)
		var elapsed:=0.0
		for i in range(entry.frames.size()):
			var frame: Texture2D=player.frames[entry.id][i]
			check(frame.get_meta("crew_standing_height")==148.0,"Density "+entry.id)
			check(player.frame_at_elapsed(entry.id,elapsed+float(expected_durations[i])/2000.0)==frame,"Playback "+entry.id)
			elapsed+=float(expected_durations[i])/1000.0
	player.frame("walk","east",1.0,Vector2.ZERO)
	player.frame("walk","east",2.0,Vector2(.04,0))
	var snapshot: Dictionary=player.snapshot()
	player.frame("walk","east",2.0,Vector2(.04,0))
	check(player.snapshot()==snapshot,"Paused sample holds playback")
	player.frame("walk","east",3.0,Vector2(.08,0))
	player.restore_snapshot(snapshot)
	check(player.snapshot()==snapshot,"Playback snapshot restore")
	var sheet:=Sheet.new();sheet.player=player;sheet.keys=player.frames.keys();sheet.keys.sort()
	var idle_direction: String=""
	for direction in ["east","west","north","south"]:
		if "marsh-idle-"+direction in args:idle_direction=direction
	if not idle_direction.is_empty():
		check(actor=="marsh","Marsh idle review actor")
		output="res://output/crew-replacement-2026-09-12/marsh/idle-"+idle_direction+"-selected-native/"
		DirAccess.make_dir_recursive_absolute(output)
		sheet.keys=["idle-"+idle_direction,"walk-"+idle_direction]
		for i in range(2):
			var source:=Image.new()
			source.load_png_from_buffer(FileAccess.get_file_as_bytes("res://character/marsh-motion-polish-v1/review/idle-%s-video-cycle-01/idle-%s-%03d.png"%[idle_direction,idle_direction,i]))
			check(pixels(player.frames["idle-"+idle_direction][i])==anchored_pixels(source,Vector2(128,224)),"Selected whole-body idle pose "+str(i))
	if "seated-identity-study" in args or "seated-identity-selected" in args:
		check(actor=="veld","Seated identity belongs to Veld")
		output="res://output/crew-replacement-2026-09-12/veld/seated-identity-"+("selected" if "seated-identity-selected" in args else "study")+"-native/"
		sheet.keys=["sit-down-east","sit-idle-east","sit-rise-east"]
		for equipped in [false,true]:
			var rows: Dictionary=player.equipment_frames["diving-helmet"] if equipped else player.frames
			for key in sheet.keys:
				var replacements: Array=[]
				for index in range(6):
					var im:=Image.new()
					check(im.load_png_from_buffer(FileAccess.get_file_as_bytes("res://character/veld-identity-correction-v1/review/seated-east-body-01/%s%s-%03d.png"%["helmet-" if equipped else "",key,index]))==OK,"Seated identity source loads")
					var tex:=ImageTexture.create_from_image(im)
					for meta in rows[key][index].get_meta_list():tex.set_meta(meta,rows[key][index].get_meta(meta))
					tex.set_meta("crew_pivot",Vector2(128,224));replacements.append(tex)
					if "seated-identity-selected" in args:check(pixels(rows[key][index])==pixels(tex),"Selected seated identity pixels")
				rows[key]=replacements
				var elapsed:=0.0
				for index in range(6):
					var duration: float=float(player.timing[key].durations[index])/1000.0
					check(player.frame_at_elapsed(key,elapsed+duration*.5,"diving-helmet" if equipped else "")==replacements[index],"Seated original timing")
					elapsed+=duration
			check(pixels(rows["sit-down-east"][0])==pixels(rows["idle-east"][0]),"Seating joins corrected standing")
			check(pixels(rows["sit-down-east"][5])==pixels(rows["sit-idle-east"][0]),"Descent joins seated idle")
			check(pixels(rows["sit-rise-east"][0])==pixels(rows["sit-idle-east"][5]),"Seated idle joins rise")
			check(pixels(rows["sit-rise-east"][5])==pixels(rows["idle-east"][0]),"Rise joins corrected standing")
	if "helmet-transition-study" in args or "helmet-transition-selected" in args:
		check(actor=="veld","Helmet transition study belongs to Veld")
		output="res://output/crew-replacement-2026-09-12/veld/helmet-transition-"+("selected" if "helmet-transition-selected" in args else "study")+"-native/"
		DirAccess.make_dir_recursive_absolute(output)
		sheet.keys=["equip-helmet-east","remove-helmet-east"]
		for key in sheet.keys:
			var replacements: Array=[]
			var elapsed:=0.0
			check(player.frames[key].size()==12,"Original helmet slot count")
			for index in range(12):
				var im:=Image.new()
				check(im.load_png_from_buffer(FileAccess.get_file_as_bytes("res://character/veld-identity-correction-v1/review/helmet-transition-body-01/%s-%03d.png"%[key,index]))==OK,"Helmet transition source loads")
				var tex:=ImageTexture.create_from_image(im)
				for meta in player.frames[key][index].get_meta_list():tex.set_meta(meta,player.frames[key][index].get_meta(meta))
				tex.set_meta("crew_pivot",Vector2(128,224));replacements.append(tex)
				if "helmet-transition-selected" in args:check(pixels(player.frames[key][index])==pixels(tex),"Selected helmet transition pixels")
			player.frames[key]=replacements
			for index in range(12):
				var duration: float=float(player.timing[key].durations[index])/1000.0
				check(player.frame_at_elapsed(key,elapsed+duration*.5)==replacements[index],"Helmet transition original timing")
				elapsed+=duration
		var don: Array=player.frames["equip-helmet-east"]
		var remove: Array=player.frames["remove-helmet-east"]
		check(pixels(don[0])==pixels(player.frames["idle-east"][0]),"Don joins bare idle")
		check(pixels(don[11])==pixels(player.equipment_frames["diving-helmet"]["idle-east"][0]),"Don joins fitted idle")
		check(pixels(remove[0])==pixels(don[11]) and pixels(remove[11])==pixels(don[0]),"Removal has matching equipment endpoints")
	if "identity-chain-study" in args or "identity-chain-selected" in args or "identity-direction-study" in args or "identity-direction-selected" in args:
		check(actor=="veld","Identity chain belongs to Veld")
		var directional_identity: bool="identity-direction-study" in args or "identity-direction-selected" in args
		var identity_reference_root: String="res://character/veld-identity-correction-v1/review/east-chain-01/"
		output="res://output/crew-replacement-2026-09-12/veld/identity-chain-study-native/"
		if "identity-chain-selected" in args:output="res://output/crew-replacement-2026-09-12/veld/identity-chain-selected-native/"
		DirAccess.make_dir_recursive_absolute(output)
		sheet.keys=["idle-east","kneel-east","repair-east","stand-east","interact-east"]
		if directional_identity:
			output="res://output/crew-replacement-2026-09-12/veld/identity-direction-study-native/"
			if "identity-direction-selected" in args:output="res://output/crew-replacement-2026-09-12/veld/identity-direction-selected-native/"
			DirAccess.make_dir_recursive_absolute(output)
			identity_reference_root="res://character/veld-identity-correction-v1/review/directional-movement-01/"
			sheet.keys=["idle-south","walk-south","idle-west","walk-west","idle-north","walk-north"]
		var sample_chain_direction: String="south" if "south-sample-chain" in args else ("west" if "west-sample-chain" in args else ("north" if "north-sample-chain" in args else ""))
		var directional_sample_chain: bool=not sample_chain_direction.is_empty()
		if directional_sample_chain:
			identity_reference_root="res://character/veld-identity-correction-v1/review/"+sample_chain_direction+"-kneel-body-01/"
			output="res://output/crew-replacement-2026-09-12/veld/"+sample_chain_direction+"-sample-chain-"+("selected" if "identity-chain-selected" in args else "study")+"-native/"
			DirAccess.make_dir_recursive_absolute(output)
			sheet.keys=["kneel-"+sample_chain_direction,"repair-"+sample_chain_direction,"stand-"+sample_chain_direction]
		for equipped in [false,true]:
			var rows: Dictionary=player.equipment_frames["diving-helmet"] if equipped else player.frames
			for key in sheet.keys:
				var replacements: Array=[]
				for index in range(6):
					var im:=Image.new()
					var prefix: String="helmet-" if equipped else ""
					check(im.load(identity_reference_root+"%s%s-%03d.png"%[prefix,key,index])==OK,"Identity chain source loads")
					var tex:=ImageTexture.create_from_image(im)
					for meta in rows[key][index].get_meta_list():tex.set_meta(meta,rows[key][index].get_meta(meta))
					tex.set_meta("crew_pivot",Vector2(128,224));replacements.append(tex)
					if "identity-chain-selected" in args or "identity-direction-selected" in args:check(pixels(rows[key][index])==pixels(tex),"Selected identity chain pixels")
					if directional_identity:
						var preserved:=Image.new()
						check(preserved.load_png_from_buffer(FileAccess.get_file_as_bytes("res://character/veld-identity-correction-v1/sources/%s-%s-original-%03d.png"%[key,"equipment" if equipped else "body",index]))==OK,"Original movement reference loads")
						var before:=Image.create_from_data(512,512,false,Image.FORMAT_RGBA8,anchored_pixels(preserved,Vector2(128,224)))
						var after:=Image.create_from_data(512,512,false,Image.FORMAT_RGBA8,pixels(tex))
						before.fill_rect(Rect2i(228,220,60,60),Color(0,0,0,0))
						after.fill_rect(Rect2i(228,220,60,60),Color(0,0,0,0))
						check(before.get_data()==after.get_data(),"Directional identity preserves outside-head pixels")
				rows[key]=replacements
				var elapsed:=0.0
				for index in range(6):
					var duration: float=float(player.timing[key].durations[index])/1000.0
					check(player.frame_at_elapsed(key,elapsed+duration*.5,"diving-helmet" if equipped else "")==replacements[index],"Identity chain preserves timed phase")
					elapsed+=duration
				if directional_identity and key.begins_with("walk-"):
					var direction: String=key.trim_prefix("walk-")
					var source_contract: Array=JSON.parse_string(FileAccess.get_file_as_string("res://character/veld-identity-correction-v1/sources/remaining-direction-movement-contract.json"))
					var stride: float=float(contract.strides.walk)
					for source_entry in source_contract:
						if source_entry.state==key and source_entry.variant=="body" and source_entry.stride!=null:stride=float(source_entry.stride)
					check(is_equal_approx(float(player.strides.get(key,player.strides.walk)),stride),"Directional stride preserved")
					for sample in range(60):
						var distance:=sample*.04*.08
						var position:=Vector2(-distance,0) if direction=="west" else Vector2(0,distance*(-1 if direction=="north" else 1))
						# Vector2 positions have single-precision components; use the supplied
						# position rather than an unrounded scalar at exact phase boundaries.
						var expected=player.frame_at_elapsed(key,fposmod(position.length()/stride*elapsed,elapsed),"diving-helmet" if equipped else "")
						var actual=player.frame("walk",direction,sample*.04,position,"diving-helmet" if equipped else "")
						check(actual==expected,"Directional distance cadence %s gear=%s sample=%d actual=%d expected=%d snapshot=%s"%[key,str(equipped),sample,rows[key].find(actual),rows[key].find(expected),str(player.snapshot())])
			if directional_identity:continue
			var chain_direction: String=sample_chain_direction if directional_sample_chain else "east"
			check(pixels(rows["idle-"+chain_direction][0])==pixels(rows["kneel-"+chain_direction][0]),"Corrected idle joins kneel")
			check(pixels(rows["kneel-"+chain_direction][5])==pixels(rows["repair-"+chain_direction][0]),"Corrected kneel joins sample")
			check(pixels(rows["repair-"+chain_direction][5])==pixels(rows["stand-"+chain_direction][0]),"Corrected sample joins stand")
			check(pixels(rows["stand-"+chain_direction][5])==pixels(rows["idle-"+chain_direction][0]),"Corrected stand joins idle")
			if not directional_sample_chain:check(pixels(rows["interact-"+chain_direction][0])==pixels(rows["idle-"+chain_direction][0]) and pixels(rows["interact-"+chain_direction][5])==pixels(rows["idle-"+chain_direction][0]),"Corrected scanner joins idle")
	if "scanner-study" in args or "scanner-selected" in args or "sample-study" in args or "sample-selected" in args:
		var instrument_direction: String="east"
		for direction in ["south","west","north"]:
			if "instrument-"+direction in args:instrument_direction=direction
		var instrument_key: String="repair-east" if "sample-study" in args or "sample-selected" in args else "interact-"+instrument_direction
		var sample_mode: bool=instrument_key=="repair-east"
		var corrected_east_scanner: bool=actor=="veld" and instrument_key=="interact-east"
		var corrected_south_scanner: bool=actor=="veld" and instrument_key=="interact-south"
		var corrected_west_scanner: bool=actor=="veld" and instrument_key=="interact-west"
		var corrected_north_scanner: bool=actor=="veld" and instrument_key=="interact-north"
		if sample_mode:
			check(actor=="veld","Sample study belongs to Veld")
			output="res://output/crew-replacement-2026-09-12/veld/"+("sample-selected-native/" if "sample-selected" in args else "sample-study-native/")
			if "identity-correction" in args:output="res://output/crew-replacement-2026-09-12/veld/sample-identity-study-native/"
			DirAccess.make_dir_recursive_absolute(output)
		if instrument_direction!="east":
			output=output.trim_suffix("/")+"-"+instrument_direction+"/"
			DirAccess.make_dir_recursive_absolute(output)
		check(actor in ["veld","branforth","marsh"],"Instrument source belongs to supported actor")
		sheet.keys=[instrument_key]
		for equipped in ([false] if actor=="marsh" else [false,true]):
			var rows: Dictionary=player.equipment_frames["diving-helmet"] if equipped else player.frames
			var original: Array=rows[instrument_key]
			var replacements: Array=[]
			var elapsed:=0.0
			for index in range(6):
				var im:=Image.new()
				var prefix: String="helmet-" if equipped else ""
				var reference_path: String="res://character/crew-action-detail-v2/review/veld-east-sample-01/%srepair-east-%03d.png"%[prefix,index] if sample_mode else "res://character/crew-action-detail-v2/review/%s-role-interact-%s-strip-01/%sinteract-%s-%03d.png"%[actor,instrument_direction,prefix,instrument_direction,index]
				if sample_mode or corrected_east_scanner:reference_path="res://character/veld-identity-correction-v1/review/east-chain-01/%s%s-%03d.png"%[prefix,instrument_key,index]
				if corrected_south_scanner:reference_path="res://character/veld-identity-correction-v1/review/south-scanner-body-02/%sinteract-south-%03d.png"%[prefix,index]
				if corrected_west_scanner:reference_path="res://character/veld-identity-correction-v1/review/west-scanner-body-01/%sinteract-west-%03d.png"%[prefix,index]
				if corrected_north_scanner:reference_path="res://character/veld-identity-correction-v1/review/north-scanner-body-01/%sinteract-north-%03d.png"%[prefix,index]
				if sample_mode and "identity-correction" in args:reference_path="res://character/veld-identity-correction-v1/review/east-sample-01/%srepair-east-%03d.png"%[prefix,index]
				check(im.load(reference_path)==OK,"Action study loads")
				var tex:=ImageTexture.create_from_image(im)
				for meta in original[index].get_meta_list():tex.set_meta(meta,original[index].get_meta(meta))
				tex.set_meta("crew_pivot",Vector2(128,224) if sample_mode or corrected_east_scanner or corrected_south_scanner or corrected_west_scanner or corrected_north_scanner else Vector2(92,172))
				replacements.append(tex)
				if "scanner-selected" in args or "sample-selected" in args:check(pixels(original[index])==pixels(tex),"Selected scanner source pixels")
			rows[instrument_key]=replacements
			for index in range(6):
				var duration: float=float(player.timing[instrument_key].durations[index])/1000.0
				check(player.frame_at_elapsed(instrument_key,elapsed+duration*.5,"diving-helmet" if equipped else "")==replacements[index],"Scanner paired timed playback")
				elapsed+=duration
			if corrected_south_scanner or corrected_west_scanner or corrected_north_scanner:
				check(pixels(replacements[0])==pixels(rows["idle-"+instrument_direction][0]) and pixels(replacements[5])==pixels(rows["idle-"+instrument_direction][0]),"Full-body scanner joins corrected idle")
			elif actor=="branforth" and instrument_direction=="west":
				for endpoint_index in range(2):
					var endpoint_name: String="opening" if endpoint_index==0 else "closing"
					var slot_index: int=0 if endpoint_index==0 else 5
					var group: String="equipment" if equipped else "body"
					var revised:=Image.new()
					check(revised.load("res://character/crew-action-detail-v2/review/branforth-west-meter-endpoints-01/%s-%s.png"%[group,endpoint_name])==OK,"Revised endpoint loads")
					check(pixels(replacements[slot_index])==anchored_pixels(revised,Vector2(92,172)),"Revised meter endpoint matches")
					var preserved:=Image.new()
					check(preserved.load("res://character/crew-action-detail-v2/sources/branforth-west-meter-%s-%s-01.png"%[group,endpoint_name])==OK,"Original endpoint reference loads")
					revised.fill_rect(Rect2i(48,61,22,27),Color(0,0,0,0))
					preserved.fill_rect(Rect2i(48,61,22,27),Color(0,0,0,0))
					check(revised.get_data()==preserved.get_data(),"Endpoint preserves pixels outside tool edit")
			elif sample_mode and "identity-correction" in args:
				for index in range(6):
					var before:=Image.create_from_data(512,512,false,Image.FORMAT_RGBA8,pixels(original[index]))
					var after:=Image.create_from_data(512,512,false,Image.FORMAT_RGBA8,pixels(replacements[index]))
					before.fill_rect(Rect2i(228,272,60,43),Color(0,0,0,0))
					after.fill_rect(Rect2i(228,272,60,43),Color(0,0,0,0))
					check(before.get_data()==after.get_data(),"Identity study preserves pixels outside head and collar")
			else:
				check(pixels(replacements[0])==pixels(original[0]) and pixels(replacements[5])==pixels(original[5]),"Scanner preserves selected idle endpoints")
	if "welding-sides" in args or "welding-all" in args:
		check(actor=="marsh","Welding source references belong to Marsh")
		var directions: Array=["east","west","north","south"] if "welding-all" in args else ["east","west"]
		sheet.keys=[]
		for direction in directions:
			var source_group: String="axial-01" if direction in ["north","south"] else "sides-02"
			if direction=="south":source_group="low-south-01"
			for action in ["torch-draw","weld","torch-stow"]:
				sheet.keys.append(action+"-"+direction)
				for index in range(6):
					var reference:=Image.new()
					var reference_path: String="res://character/crew-action-detail-v2/review/marsh-welding-%s/%s-%s-%03d.png"%[source_group,direction,action,index]
					if direction=="south":reference_path="res://character/crew-action-detail-v2/review/marsh-low-reach-sequence-01/south-%s-%03d.png"%[action,index]
					reference.load_png_from_buffer(FileAccess.get_file_as_bytes(reference_path))
					check(pixels(player.frames[action+"-"+direction][index])==anchored_pixels(reference,Vector2(92,172)),"Selected tool source %s %s %d"%[direction,action,index])
			var draw_frames: Array=player.frames["torch-draw-"+direction]
			var stow: Array=player.frames["torch-stow-"+direction]
			var weld: Array=player.frames["weld-"+direction]
			check(pixels(draw_frames[5])==pixels(weld[0]),"Draw joins weld "+direction)
			check(pixels(weld[5])==pixels(stow[0]),"Weld seam joins stow "+direction)
			for index in range(6):
				check(pixels(draw_frames[index])==pixels(stow[5-index]),"Exact reverse stow")
				check(pixels(weld[index])!=pixels(draw_frames[0]),"Working loop keeps tool out")
			check(pixels(player.frames["weld-"+direction][2])!=pixels(player.frames["repair-"+direction][2]),"Welding is distinct from repair "+direction)
		var fixture:=ToolFixture.new()
		fixture.marsh_npc.goal="construction";fixture.marsh_npc.state="weld"
		var renderer=load("res://scripts/grid_canvas.gd").new();renderer.marsh_player=player
		for direction in directions:
			fixture.marsh_npc.direction=direction
			for sample in [[0.0,"torch-draw",0],[.28,"torch-draw",3],[.519,"torch-draw",5],[9.48,"torch-stow",0],[9.76,"torch-stow",3],[9.999,"torch-stow",5]]:
				fixture.marsh_npc.timer=sample[0]
				check(renderer._get_marsh_frame(fixture)==player.frames[sample[1]+"-"+direction][sample[2]],"Full tool clip fits construction window %s %s"%[direction,str(sample)])
		renderer.free()
	if "cargo-east" in args:sheet.keys=["pickup-east","carry-east","unload-east"]
	if "cargo-west" in args:sheet.keys=["pickup-west","carry-west","unload-west"]
	if "cargo-south" in args:sheet.keys=["pickup-south","carry-south","unload-south"]
	if "cargo-north" in args:sheet.keys=["pickup-north","carry-north","unload-north"]
	if not seating_direction.is_empty():sheet.keys=["sit-down-"+seating_direction,"sit-idle-"+seating_direction,"sit-rise-"+seating_direction]
	if "sleeping-north" in args:sheet.keys=["lie-down-north","sleep-north","get-up-north"]
	if "sleeping-east" in args:sheet.keys=["lie-down-east","sleep-east","get-up-east"]
	if "sleeping-west" in args:sheet.keys=["lie-down-west","sleep-west","get-up-west"]
	if "sleeping-south" in args:sheet.keys=["lie-down-south","sleep-south","get-up-south"]
	if "cargo-east" in args or "cargo-west" in args or "cargo-south" in args or "cargo-north" in args:
		var direction: String="west" if "cargo-west" in args else "east"
		if "cargo-south" in args:direction="south"
		if "cargo-north" in args:direction="north"
		var clip: String="carry-"+direction
		var revision_number: String="02" if actor=="veld" and direction=="east" else "01"
		var recipe_path: String="res://character/crew-action-detail-v2/review/%s-carry-%s-local-%s/recipe.json"%[actor,direction,revision_number]
		var recipe: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(recipe_path))
		var stride: float=float(recipe.rig.travel)*2.0*65.28/148.0/384.0
		check(is_equal_approx(player.strides.get(clip,0.0),stride),"Cargo stride matches independent rig")
		for sample in range(60):
			var distance:=sample*.04*.08
			var position:=Vector2(0,distance) if direction=="south" else Vector2(distance*(-1.0 if direction=="west" else 1.0),0)
			if direction=="north":position=Vector2(0,-distance)
			var texture: Texture2D=player.frame("carry",direction,sample*.04,position)
			var phase:=int(floor(fposmod(distance/stride,1.0)*6.0))
			check(texture==player.frames[clip][phase],"Cargo distance cadence sample "+str(sample))
	check(DirAccess.make_dir_recursive_absolute(output)==OK,"Native review output directory ready")
	root.add_child(sheet)
	for page in range(ceili(sheet.keys.size()/24.0)):
		for phase in range(12):
			sheet.page=page;sheet.phase=phase;sheet.queue_redraw()
			await process_frame
			await RenderingServer.frame_post_draw
			check(root.get_texture().get_image().save_png(output+"page-%02d-frame-%02d.png"%[page,phase])==OK,"Native review capture saved")
	print("HUMAN CANDIDATE: %s: %d body states, %d equipped states, %d failures" % [actor,player.frames.size(),player.equipment_frames["diving-helmet"].size(),failures])
	quit(1 if failures else 0)
