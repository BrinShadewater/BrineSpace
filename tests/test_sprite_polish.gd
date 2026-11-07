extends SceneTree
## Native same-scale review using the production raw-PNG player. No player saves.
const Player=preload("res://scripts/crew_sprite_player.gd")
const Companion=preload("res://scripts/companion_npc.gd")
var out="res://output/sprite-polish"
var requested_states := PackedStringArray()
var failures:=0
var board: Node2D
var players: Array=[]
var phase:=0.0
var action:="idle"
const NAMES=["Bill","Veld","Branforth","Marsh","River","Josh","Margot"]
const DIRS=["south","north","east","west"]
func _init():call_deferred("run")
func check(ok: bool,message: String):
	if not ok:failures+=1;push_error(message)
func draw_board():
	board.draw_rect(Rect2(0,0,1400,900),Color("18242a"))
	for col in range(players.size()):
		board.draw_string(ThemeDB.fallback_font,Vector2(col*190+20,30),NAMES[col],HORIZONTAL_ALIGNMENT_LEFT,-1,20)
		for row in range(4):
			var key: String=action+"-"+DIRS[row]
			var at:=Vector2(col*190+8,row*205+45)
			if col==0:board.draw_string(ThemeDB.fallback_font,Vector2(8,row*205+48),action+" / "+DIRS[row],HORIZONTAL_ALIGNMENT_LEFT,-1,11)
			if not players[col].frames.has(key):
				board.draw_string(ThemeDB.fallback_font,at+Vector2(20,90),"Not authored",HORIZONTAL_ALIGNMENT_LEFT,-1,14)
				continue
			var cursor: float=fmod(phase,players[col].cycle_seconds(key)) if players[col].timing[key].loop else phase
			var texture: Texture2D=players[col].frame_at_elapsed(key,cursor)
			var height: float=texture.get_meta("crew_standing_height",74.0)
			var pivot: Vector2=texture.get_meta("crew_pivot",Vector2(46,86))
			for pair in [[148.0,Vector2(92,172)],[65.28,Vector2(156,172)]]:
				var scale: float=float(pair[0])/height
				board.draw_texture_rect(texture,Rect2(at+pair[1]-pivot*scale,texture.get_size()*scale),false)
func run():
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--states="):requested_states=arg.trim_prefix("--states=").split(",")
		if arg.begins_with("--output="):out=arg.trim_prefix("--output=")
	DirAccess.make_dir_recursive_absolute(out)
	root.size=Vector2i(1400,900)
	root.content_scale_size=Vector2i(1400,900)
	for actor in ["bill","veld","branforth","marsh","river","josh","margot"]:
		var player=Player.new()
		if Player.REVISION_ROOTS.has(actor):
			var base: String=Player.REVISION_ROOTS[actor]
			var catalog=JSON.parse_string(FileAccess.get_file_as_string(base+"catalog.json"))
			for path in catalog.body:player.load_manifest(base+str(path),true)
		else:
			player.load_manifest("res://character/animation-expansion-v5/"+actor+"/manifest.json")
			player.load_manifest("res://character/animation-expansion-v5/"+actor+"-actions/manifest.json",true)
		players.append(player)
		for d in DIRS:
			for state in ["idle","walk"]:
				check(player.frames.has(state+"-"+d),actor+" coverage "+state+"-"+d)
	check(players[3].frames["idle-south"].size()==2,"Marsh dedicated two-frame idle")
	for id in ["river","josh"]:
		var actor=Companion.new(id)
		for behavior in actor.ACTIONS[id]:
			for d in DIRS:
				var idle=actor.player.frames["idle-"+d][0].get_image().get_data()
				if behavior!="boot":check(actor.poses.frames[behavior+"-enter-"+d][0].get_image().get_data()==idle,"Action starts on idle: "+id+behavior+d)
				check(actor.poses.frames[behavior+"-exit-"+d][-1].get_image().get_data()==idle,"Action ends on idle: "+id+behavior+d)
	board=Node2D.new();board.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;board.draw.connect(draw_board);root.add_child(board)
	var review_states=OS.get_cmdline_user_args()
	if review_states.is_empty():review_states=PackedStringArray(["idle","walk","sit-idle","read-seated","sleep","pickup","carry","swim","tread","sit","groom","nap","stretch","yawn","boot","powerdown","move-start","move-stop","turn-south","torch"])
	if not requested_states.is_empty():review_states=requested_states
	for state in review_states:
		action=state
		for step in range(12):
			phase=step*.1;board.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
			root.get_texture().get_image().save_png(out.path_join("native-%s-%02d.png"%[state,step]))
	print("SPRITE REVIEW: coverage/join failures=",failures,"; visual acceptance required")
	quit(failures)
