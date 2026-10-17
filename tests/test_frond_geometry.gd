extends SceneTree
const Settings=preload("res://scripts/title_settings.gd")
var checks:=0
var failures:=0
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func reference(rect:Rect2,clock:float,seed:float)->Dictionary:
	var points:=PackedVector2Array();var uv:=PackedVector2Array();var indices:=PackedInt32Array()
	for row in range(6):
		var a:=float(row)/6.0;var b:=float(row+1)/6.0
		var x:=0.0 if Settings.reduced_motion or Settings.effects_quality==0 else pow(1.0-a,2)*(.024*sin(clock*.72+seed)+.008*sin(clock*1.13+seed*1.7))
		var y:=0.0 if Settings.reduced_motion or Settings.effects_quality==0 else pow(1.0-b,2)*(.024*sin(clock*.72+seed)+.008*sin(clock*1.13+seed*1.7))
		var top:=rect.position+Vector2(x*rect.size.x,a*rect.size.y)
		var bottom:=rect.position+Vector2(y*rect.size.x,b*rect.size.y)
		var base:=points.size()
		points.append_array(PackedVector2Array([top,top+Vector2(rect.size.x,0),bottom+Vector2(rect.size.x,0),bottom]))
		uv.append_array(PackedVector2Array([Vector2(0,a),Vector2(1,a),Vector2(1,b),Vector2(0,b)]))
		indices.append_array(PackedInt32Array([base+3,base,base+1,base+1,base+2,base+3]))
	return {"points":points,"uv":uv,"indices":indices}
func _init():call_deferred("run")
func run():
	if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=OS.get_user_data_dir().replace(char(92),"/"):quit(2);return
	var candidate:Script=load("res://scripts/ambient_fronds.gd")
	check(candidate.has_method("strip_geometry"),"Shared-edge frond geometry is available")
	if failures:quit(1);return
	var saved_reduced:bool=Settings.reduced_motion;var saved_quality:int=Settings.effects_quality
	var cases:=0
	for reduced in [false,true]:
		Settings.reduced_motion=reduced
		for quality in [0,1,2]:
			Settings.effects_quality=quality
			for rect in [Rect2(170.375,50.125,35.5,280.5),Rect2(-500.25,700.125,77.25,180.75),Rect2(1920.33,-1080.77,-120.0,360.0)]:
				for clock in [-8.0,0.0,1.375,7.99,8.0,8.01,17000.125]:
					for seed in [-.75,0.0,2.31,88.123]:
						var expected:=reference(rect,clock,seed)
						var actual:Dictionary=candidate.strip_geometry(rect,clock,seed)
						cases+=1
						for key in ["points","uv","indices"]:check(actual[key].to_byte_array()==expected[key].to_byte_array(),"Exact original buffer "+key+str([reduced,quality,rect,clock,seed]))
	Settings.reduced_motion=false;Settings.effects_quality=1
	var first:Dictionary=candidate.strip_geometry(Rect2(0,0,80,240),1.375,2.31)
	var saved:Dictionary=first.duplicate(true)
	var next:Dictionary=candidate.strip_geometry(Rect2(-900.3,500.7,35.5,150),7.99,-.75)
	check(first==saved,"Later plant does not mutate prior geometry")
	check(first.points!=next.points,"Positions belong to each plant")
	first.points[0]=Vector2.INF;first.uv[0]=Vector2.INF;first.indices[0]=10000
	var again:Dictionary=candidate.strip_geometry(Rect2(0,0,80,240),1.375,2.31)
	check(again==saved,"Caller mutations do not alter fixed topology or later plants")
	check(again.uv.size()*8+again.indices.size()*4==336,"Fixed topology stays 336 packed bytes")
	Settings.reduced_motion=saved_reduced;Settings.effects_quality=saved_quality
	FileAccess.open("user://frond-geometry-result.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"cases":cases,"failures":failures}))
	print("FROND_GEOMETRY ",checks," checks ",cases," cases ",failures," failures");quit(1 if failures else 0)
