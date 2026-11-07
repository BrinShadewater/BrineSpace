extends SceneTree
const View=preload("res://assets/environment/sub-biomes-v1/sub_biome_view.gd")
class FailedVariant extends "res://assets/environment/biome-floor-variants-v1/biome_floor_view.gd":
 func texture_for(_region:Dictionary,fallback:Texture2D)->Texture2D:return fallback
var failures:=0
func check(ok:bool,label:String):
 if not ok:failures+=1;push_error(label)
func _init():call_deferred("run")
func run():
 if OS.get_user_data_dir()!=OS.get_environment("BRINESPACE_TEST_USER_DIR") or DisplayServer.get_name()=="headless":quit(2);return
 var monitor=preload("res://scripts/performance_monitor.gd").new()
 var counts=monitor.runtime_cache_counters()
 check(counts.drone.cached_decoded_bytes==preload("res://scripts/drone_animation.gd").cached_bytes,"Runtime cache counters report existing ownership without loading pixels")
 check(not counts.has("crew"),"Detached monitor does not invent a station")
 monitor.free()
 var region={"biome":"iron","center":Vector2(30,11),"radius":Vector2(4,3.5)}
 check(not preload("res://assets/environment/biome-floor-variants-v1/biome_floor_view.gd").variant_for(region).is_empty(),"Fixture selects an authored variant")
 root.set_meta("tablet_controls",false)
 var desktop=View.new();desktop.regions=[region];desktop.prepare()
 var props=desktop.props.duplicate(true)
 var expected=desktop.ground_variants.texture_for(region,desktop.textures["iron-ground"]).get_image().get_data()
 root.set_meta("tablet_controls",true)
 var tablet=View.new();tablet.regions=[region];tablet.prepare()
 check(not tablet.textures.has("iron-ground"),"Tablet does not upload the replaced ground source")
 check(tablet.textures.size()==2,"Only the active biome props retain uploads")
 check(tablet.props==props,"Deterministic prop generation and RNG consumption stay exact")
 check(tablet.meshes[0].surface_get_arrays(0)==desktop.meshes[0].surface_get_arrays(0),"Habitat geometry stays exact")
 var actual=tablet.ground_variants.texture_for(region,tablet.textures.get("iron-ground"))
 check(actual!=null and actual.get_image().get_data()==expected,"Selected material retains exact authored pixels")
 var rejected=View.new();rejected.regions=[region];rejected.ground_variants=FailedVariant.new();rejected.prepare()
 check(rejected.textures.has("iron-ground"),"Unavailable variant retains the base source")
 var mixed=View.new();var base_region=region.duplicate();base_region.center=Vector2(30,12);mixed.regions=[region,base_region];mixed.prepare()
 check(mixed.textures.has("iron-ground"),"Mixed regions of one biome retain the required base material")
 check(desktop.textures.size()==21,"Desktop eager policy stays intact")
 region.center=Vector2(30,12)
 check(preload("res://assets/environment/biome-floor-variants-v1/biome_floor_view.gd").variant_for(region).is_empty(),"Fallback fixture uses base ground")
 var fallback=View.new();fallback.regions=[region];fallback.prepare()
 check(fallback.textures.has("iron-ground"),"Base ground still loads when required")
 check(preload("res://scripts/safe_image.gd").failures.is_empty(),"No source failures")
 print("TABLET HABITAT MATERIALS failures=",failures);quit(1 if failures else 0)
