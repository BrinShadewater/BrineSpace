"""Prepare finite timing, restored player holds and native whole-source evidence."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1];mode,side,revision=sys.argv[1:4]
stem=f'{mode}-{side}-{revision}';B=ROOT/'character/marsh-water-transition-material-v1'
r=json.loads((B/f'sources/{stem}.request.json').read_text());key=r['selectedTransitionState']['id'];action=key.removesuffix('-'+side)
source='''extends SceneTree
const Player=preload("res://scripts/crew_sprite_player.gd")
const OUTPUT="res://output/marsh-animation-audit/water-STEM-native-2026-10-03/"
const MANIFEST="res://character/marsh-water-transition-material-v1/STEM-unselected/manifest.json"
const KEY="KEYTOKEN"
class Review extends Node2D:
	var textures:Array=[]
	func _draw():
		draw_rect(Rect2(0,0,1344,490),Color("293b40"))
		for col in range(textures.size()):
			var t:Texture2D=textures[col]
			var pivot:Vector2=Vector2(92,172) if col==5 else Vector2(112,172)
			for row in range(2):
				var s:float=1.0 if row==0 else 65.28/148.0
				var anchor=Vector2(112+224*col,275 if row==0 else 440)
				draw_texture_rect(t,Rect2(anchor-pivot*s,t.get_size()*s),false)
			draw_string(ThemeDB.fallback_font,Vector2(4+224*col,25),["OLD motion", "Whole staged", "Exact origin", "Exact destination", "Own neutral", "Own master"][col],HORIZONTAL_ALIGNMENT_LEFT,-1,12)
var checks:=0
var failures:=0
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func image_file(path:String) -> Image:
	var result:=Image.new();result.load_png_from_buffer(FileAccess.get_file_as_bytes(path));return result
func same(a:Texture2D,b:Texture2D) -> bool:return a!=null and b!=null and a.get_image().get_data()==b.get_image().get_data()
func make_player():
	var player=Player.new();player.load_manifest(MANIFEST);return player
func _init():call_deferred("run")
func run():
	if DisplayServer.get_name()=="headless":quit(2);return
	root.size=Vector2i(1344,490);root.content_scale_size=Vector2i.ZERO;root.content_scale_factor=1.0
	DirAccess.make_dir_recursive_absolute(OUTPUT)
	var view=Review.new();view.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(view)
	var player=make_player();var durations:Array=DURATIONSTOKEN;var total:float=0
	for duration in durations:total+=float(duration)/1000.0
	check(is_equal_approx(player.cycle_seconds(KEY),total),"normal finite duration retained")
	check(not player.timing[KEY].loop,"normal nonlooping contract")
	var origin=ImageTexture.create_from_image(image_file("res://character/marsh-water-transition-material-v1/STEM-unselected/endpoint-origin.png"))
	var destination=ImageTexture.create_from_image(image_file("res://character/marsh-water-transition-material-v1/STEM-unselected/endpoint-destination.png"))
	check(same(player.frames[KEY][0],origin),"exact normalized origin")
	check(same(player.frames[KEY][5],destination),"exact normalized destination")
	var neutral=ImageTexture.create_from_image(image_file("res://character/marsh-water-transition-material-v1/STEM-unselected/ruler.png"))
	var master=ImageTexture.create_from_image(image_file("MASTERTOKEN"))
	var oldpaths:Array=OLDPATHSTOKEN;var captures:Array=[];var samples:Array=[];var seen:Dictionary={};var restores:=0
	for step in range(int(ceil(total/.02))+2):
		var elapsed:float=0 if step==0 else step*.02+.001
		var cursor:float=elapsed;var slot:int=5
		for i in range(6):
			if cursor<float(durations[i])/1000.0:slot=i;break
			cursor-=float(durations[i])/1000.0
		var texture:Texture2D=player.frame("ACTIONTOKEN","SIDETOKEN",100+elapsed,Vector2.ZERO,"",false)
		check(same(texture,player.frames[KEY][slot]),"actual stateful finite player source "+str(step))
		check(same(player.frame_at_elapsed(KEY,elapsed),texture),"grid finite elapsed API source "+str(step))
		check(texture.get_meta("crew_pivot")==Vector2(112,172) and texture.get_meta("crew_standing_height")==148,"native metadata")
		samples.append({"elapsed":elapsed,"slot":slot})
		if seen.has(slot):continue
		seen[slot]=true;var snap:Dictionary=player.snapshot();var clone=make_player()
		check(Player.valid_snapshot(snap),"player snapshot valid");clone.restore_snapshot(snap)
		check(clone.snapshot()==snap,"whole restore parity")
		check(same(clone.frame("ACTIONTOKEN","SIDETOKEN",100+elapsed,Vector2.ZERO,"",false),texture) and clone.snapshot()==snap,"same clock finite restored hold");restores+=1
		view.textures=[ImageTexture.create_from_image(image_file(oldpaths[slot])),texture,origin,destination,neutral,master]
		view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
		var file:String="native-%02d.png"%slot;check(root.get_texture().get_image().save_png(OUTPUT+file)==OK,"native capture")
		captures.append({"file":file,"slot":slot})
	check(seen.size()==6 and restores==6 and captures.size()==6,"all six poses restored and captured")
	check(same(player.frame_at_elapsed(KEY,10),player.frames[KEY][5]),"finite final clamp")
	var report=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE)
	report.store_string(JSON.stringify({"checks":checks,"failures":failures,"samples":samples,"captures":captures,"playerRestores":restores,"durationSeconds":total,"scope":"Actual stateful CrewSpritePlayer and grid frame_at_elapsed API finite normal timing,20ms(+1ms after initial) samples,6restores/same-clock holds,all6native source-size/world-height pairs,normalized exact endpoint pixels. Not exact internal boundary testing or actual actor/controller/grid .52pickup/drain interlock/contact/fullSave/helmet/art/admission/fullset acceptance."},"\\t"));report.close()
	print("MARSH WATER STEM: ",checks,"checks,",failures,"failures");quit(1 if failures else 0)
'''
for a,b in [('STEM',stem),('KEYTOKEN',key),('ACTIONTOKEN',action),('SIDETOKEN',side),('DURATIONSTOKEN',json.dumps(r['selectedTransitionState']['frameDurationsMs'])),('OLDPATHSTOKEN',json.dumps(['res://'+q['path'] for q in r['sourceFrames'][-6:]])),('MASTERTOKEN','res://'+r['selectedIdleMaster']['path'])]:source=source.replace(a,b)
p=ROOT/f'tools/review_marsh_water_{mode}_{side}{revision}.gd';p.write_text(source)
uid={'pickup-east-02':'uid://bf9rp4vh6kn3','drain-north-01':'uid://dk8m2nq5pv7s','pickup-west-01':'uid://ct6pn4mh8kv2','pickup-west-02':'uid://bp7m5nv2qh8k','pickup-west-03':'uid://cv4p8nq6mh2r','drain-south-01':'uid://bn3vq7k5mp9r','drain-south-04':'uid://dp4v8nm6qh3k','drain-south-05':'uid://bw5m9pq3nv6r','drain-south-06':'uid://dj7v2nm4pq8h','pickup-north-01':'uid://bm4pv8nh2q7r','pickup-north-02':'uid://df2p7nm9qv6h','pickup-south-01':'uid://ck6n9pm4vh2s','pickup-south-02':'uid://ds7m4pq9nv2h','drain-east-01':'uid://dq8m5ph7nv3k','drain-west-01':'uid://bc3v6qn9mp4h'}[stem];p.with_suffix('.gd.uid').write_text(uid+'\n')
print(stem,'finite native fixture prepared')
