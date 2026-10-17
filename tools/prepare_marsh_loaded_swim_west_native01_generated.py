"""Stage the four authored poses with existing six-slot aliases and timing."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-loaded-swim-material-v1'
r=json.loads((B/'sources/west-loop-01.request.json').read_text());state=r['selectedMotionState'].copy()
assert len(state['frameFiles'])==6 and state['frameDurationsMs']==[180]*6 and state['loop']
order=[0,1,2,3,2,1];O=B/'west-loop-01-unselected'
state['frameFiles']=['res://'+(O/f'{i:03}.png').relative_to(ROOT).as_posix() for i in order]
(O/'manifest.json').write_text(json.dumps({'revision':'marsh-loaded-swim-east-material02-unselected','frameWidth':224,'frameHeight':208,'pivot':[112,172],'standingHeight':148,'textureFilter':'nearest','states':[state]},indent=2)+'\n')
oldfiles=[q['path'] for q in r['sourceFrames'][:6]]
source='''extends SceneTree
const Player=preload("res://scripts/crew_sprite_player.gd")
const OUTPUT="res://output/marsh-animation-audit/loaded-swim-west-native-01-2026-10-02/"
class Review extends Node2D:
	var textures:Array=[]
	var labels:Array=[]
	func _draw():
		draw_rect(Rect2(0,0,960,490),Color("293b40"))
		for col in range(textures.size()):
			var t:Texture2D=textures[col]
			var pivot:Vector2=Vector2(112,172) if col<3 else Vector2(92,172)
			for row in range(2):
				var s:float=1.0 if row==0 else 65.28/148.0
				var anchor=Vector2(120+240*col,280 if row==0 else 440)
				draw_texture_rect(t,Rect2(anchor-pivot*s,t.get_size()*s),false)
			draw_string(ThemeDB.fallback_font,Vector2(8+240*col,30),labels[col],HORIZONTAL_ALIGNMENT_LEFT,-1,13)
var checks:=0
var failures:=0
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func image_file(path:String) -> Image:
	var result:=Image.new();result.load_png_from_buffer(FileAccess.get_file_as_bytes(path));return result
func _init():call_deferred("run")
func run():
	if DisplayServer.get_name()=="headless":quit(2);return
	root.size=Vector2i(960,490);root.content_scale_size=Vector2i.ZERO;root.content_scale_factor=1.0
	DirAccess.make_dir_recursive_absolute(OUTPUT)
	var player=Player.new();player.load_manifest("res://character/marsh-loaded-swim-material-v1/west-loop-01-unselected/manifest.json")
	var oldpaths:Array=OLDPATHS
	var view=Review.new();view.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(view)
	var neutral=ImageTexture.create_from_image(image_file("res://character/marsh-loaded-swim-material-v1/west-loop-01-unselected/ruler.png"))
	var master=ImageTexture.create_from_image(image_file("res://character/marsh-v2/frames/bare/idle-west/000.png"))
	var captures:Array=[];var samples:Array=[];var seen:Dictionary={}
	check(is_equal_approx(player.cycle_seconds("swim-carry-west"),1.08),"existing 1080ms loop retained")
	for step in range(109):
		var elapsed:float=step*.02+(.000001 if step>0 else 0.0)
		var slot:int=mini(5,int(floor(fmod(elapsed,1.08)/.18+.000001)))
		var texture:Texture2D=player.frame("swim-carry","west",100+elapsed,Vector2(elapsed*.1,0),"",true)
		check(texture.get_image().get_data()==player.frames["swim-carry-west"][slot].get_image().get_data(),"actual advancing player source "+str(step))
		check(texture.get_meta("crew_pivot")==Vector2(112,172) and texture.get_meta("crew_standing_height")==148,"native declared pivot/scale")
		samples.append({"elapsed":elapsed,"slot":slot})
		if seen.has(slot):continue
		seen[slot]=true
		var snap:Dictionary=player.snapshot();var clone=Player.new();clone.load_manifest("res://character/marsh-loaded-swim-material-v1/west-loop-01-unselected/manifest.json")
		check(Player.valid_snapshot(snap),"player snapshot valid")
		clone.restore_snapshot(snap)
		check(clone.snapshot()==snap,"whole player restore parity")
		var restored:Texture2D=clone.frame("swim-carry","west",100+elapsed,Vector2(elapsed*.1,0),"",true)
		check(restored.get_image().get_data()==texture.get_image().get_data() and clone.snapshot()==snap,"same clock pause/restored source")
		view.textures=[ImageTexture.create_from_image(image_file(oldpaths[slot])),texture,neutral,master]
		view.labels=["Current selected / slot "+str(slot),"WholeWest01 staged / slot "+str(slot),"WholeWest01 neutral ruler","Selected West master"]
		view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
		var file:String="native-%02d.png"%slot
		check(root.get_texture().get_image().save_png(OUTPUT+file)==OK,"native review capture")
		captures.append({"file":file,"slot":slot})
	check(seen.size()==6 and samples.size()==109,"all six holds, two loop wraps sampled")
	var report=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE)
	report.store_string(JSON.stringify({"checks":checks,"failures":failures,"samples":samples,"captures":captures,"authoredFigures":4,"slots":6,"scope":"Actual CrewSpritePlayer advancing 20ms through two 1080ms loops; six authored timing slots alias four whole02 figures, six player restore/same-clock pause checks. Native source-size and 65.28-world-height comparison to selected old loop/own neutral/master. NOT normal actor/controller/world/paid expedition/fullSave/helmet/contact/seam/admission/full-set acceptance."},"\\t"));report.close()
	print("MARSH LOADED SWIM WEST01: ",checks,"checks,",failures,"failures")
	quit(1 if failures else 0)
'''
source=source.replace('OLDPATHS',json.dumps(['res://'+p for p in oldfiles]))
p=ROOT/'tools/review_marsh_loaded_swim_west01.gd';p.write_text(source);p.with_suffix('.gd.uid').write_text('uid://cnwq2txp6ge\n')
print('Private six-slot/four-figure loop staged; native player comparison fixture prepared.')
