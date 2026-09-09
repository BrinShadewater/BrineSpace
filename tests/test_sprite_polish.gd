extends SceneTree
## Native same-scale review using the production raw-PNG player. No player saves.
const Player=preload("res://scripts/crew_sprite_player.gd")
const Companion=preload("res://scripts/companion_npc.gd")
const OUT="res://output/sprite-polish"
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
			if not players[col].frames.has(key):key="idle-"+DIRS[row]
			var texture: Texture2D=players[col].frame_at_elapsed(key,phase)
			var at:=Vector2(col*190+8,row*205+45)
			board.draw_texture_rect(texture,Rect2(at,Vector2(184,184)),false)
			# Small copy uses the actual canonical room scale (384*.17/74).
			board.draw_texture_rect(texture,Rect2(at+Vector2(105,103),Vector2(92,92)*.8821621622),false)
func run():
	DirAccess.make_dir_recursive_absolute(OUT)
	root.size=Vector2i(1400,900)
	root.content_scale_size=Vector2i(1400,900)
	for path in ["major-bill-v2/final","dr-veld-v1/final","chief-engineer-branforth-v1/final","animation-expansion-v5/marsh","animation-expansion-v5/river","animation-expansion-v5/josh","animation-expansion-v5/margot"]:
		var player=Player.new();player.load_manifest("res://character/"+path+"/manifest.json");players.append(player)
		if path.begins_with("animation-expansion-v5/") and not path.ends_with("marsh"):player.load_manifest("res://character/"+path+"-actions/manifest.json",true)
		for d in DIRS:
			for state in ["idle","walk"]:
				check(player.frames.has(state+"-"+d),path+" coverage "+state+"-"+d)
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
	for state in review_states:
		action=state
		for step in range(12):
			phase=step*.1;board.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
			root.get_texture().get_image().save_png(OUT.path_join("native-%s-%02d.png"%[state,step]))
	print("SPRITE POLISH ","PASS" if failures==0 else "FAIL"," failures=",failures)
	quit(failures)
