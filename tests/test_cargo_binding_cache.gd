extends SceneTree
const Cargo=preload("res://scripts/james_cargo_checkpoint.gd")
class CountingFrame extends "res://scripts/crew_storage/frame.gd":
	var reads:=0
	func _get_image()->Image:
		reads+=1
		return source
class MutableFrame extends Texture2D:
	var image:Image
	var reads:=0
	func _get_image()->Image:
		reads+=1
		return image
class Player extends RefCounted:
	var frames:Dictionary={}
	var equipment_frames:Dictionary={"diving-helmet":{}}
	var timing:Dictionary={}
	var equipment_timing:Dictionary={"diving-helmet":{}}
	var return_plan:Dictionary={}
	var floor_art:Texture2D
	func bank_for(gear:String)->Dictionary:return frames if gear.is_empty() else equipment_frames[gear]
	func floor_texture()->Texture2D:return floor_art
var failures:=0
var checks:=0
var sources:Array=[]
func _init()->void:call_deferred("run")
func expect(ok:bool,label:String)->void:
	checks+=1
	if not ok:failures+=1;push_error(label)
func image(color:Color)->Image:
	var result:=Image.create(16,16,false,Image.FORMAT_RGBA8)
	result.fill(color)
	return result
func wrapper(color:Color)->Texture2D:
	var cpu:=CountingFrame.new();cpu.source=image(color);sources.append(cpu)
	var display:=CanvasTexture.new();display.diffuse_texture=cpu
	display.set_meta("crew_pivot",Vector2(128,224));display.set_meta("crew_standing_height",148)
	return display
func reads()->int:
	var count:=0
	for source in sources:count+=source.reads
	return count
func run()->void:
	var player:=Player.new()
	for gear in ["","diving-helmet"]:
		var bank:Dictionary=player.bank_for(gear)
		var clocks:Dictionary=player.timing if gear.is_empty() else player.equipment_timing[gear]
		for key in ["unload-west","carry-settle-west"]:
			bank[key]=[];clocks[key]={"durations":[]}
			for index in range(7 if key=="unload-west" else 6):
				bank[key].append(wrapper(Color(.1+index*.01,.2,.3,1)))
				clocks[key].durations.append(100.0)
	player.floor_art=CountingFrame.new();player.floor_art.source=image(Color(.4,.5,.6,1))
	var first:Dictionary=Cargo.bank_bindings(player)
	expect(Cargo.valid_bank_bindings(first),"Complete original cargo identity remains valid")
	expect(first[""]["unload-west"][0].rgba==image(Color(.1,.2,.3,1)).get_data().hex_encode().sha256_text(),"Legacy RGBA-hex fingerprint is unchanged")
	var cold_reads:=reads()
	var again:Dictionary=Cargo.bank_bindings(player)
	expect(again==first,"Repeated binding is identical")
	expect(reads()==cold_reads,"Unchanged compressed cargo frames must not be decoded on another Save")
	var frame:CanvasTexture=player.frames["unload-west"][0]
	var cpu=frame.diffuse_texture
	frame.set_meta("crew_pivot",Vector2(127,224))
	player.timing["unload-west"].durations[0]=110.0
	var altered:Dictionary=Cargo.bank_bindings(player)
	expect(altered[""]["unload-west"][0].pivot==Vector2(127,224) and altered[""]["unload-west"][0].seconds==.11,"Metadata and timing are captured fresh")
	expect(reads()==cold_reads,"Metadata/timing changes do not decode unchanged pixels")
	frame.set_meta("crew_pivot",Vector2(128,224))
	var before_mutation:int=cpu.reads
	var replacement:Image=image(Color(.7,.2,.3,1))
	cpu.packed=replacement.get_data().compress(FileAccess.COMPRESSION_ZSTD)
	var changed:Dictionary=Cargo.bank_bindings(player)
	expect(changed[""]["unload-west"][0].rgba==replacement.get_data().hex_encode().sha256_text(),"Changed packed bytes invalidate the cached identity")
	expect(cpu.reads==before_mutation+1,"Changed compressed source decodes once")
	Cargo.bank_bindings(player)
	expect(cpu.reads==before_mutation+1,"Changed source is reusable after refreshing identity")
	var edited:Image=image(Color(.3,.8,.5,1))
	var edit_bytes:PackedByteArray=edited.get_data().compress(FileAccess.COMPRESSION_ZSTD)
	cpu.packed.resize(edit_bytes.size())
	for index in edit_bytes.size():cpu.packed[index]=edit_bytes[index]
	changed=Cargo.bank_bindings(player)
	expect(changed[""]["unload-west"][0].rgba==edited.get_data().hex_encode().sha256_text(),"In-place compressed-byte edits cannot poison the cached key")
	var old_image:Image=cpu.get_image();old_image.fill(Color.BLACK)
	expect(Cargo.bank_bindings(player)==changed,"Mutating a returned decoded copy does not alter source identity")
	var other:=CountingFrame.new();other.source=image(Color(.2,.8,.1,1));sources.append(other)
	frame.diffuse_texture=other
	var swapped:Dictionary=Cargo.bank_bindings(player)
	expect(swapped[""]["unload-west"][0].rgba!=changed[""]["unload-west"][0].rgba,"Replacing diffuse source inside the same wrapper changes identity")
	var la:=CountingFrame.new();var la_image:Image=image(Color(.3,.4,.5,.6));la_image.convert(Image.FORMAT_LA8)
	la.source=la_image;frame.diffuse_texture=la
	expect(Cargo.bank_bindings(player)[""]["unload-west"][0].rgba==la_image.get_data().hex_encode().sha256_text(),"Legacy fingerprints preserve LA8 bytes without RGBA conversion")
	var mutable:=MutableFrame.new();mutable.image=image(Color(.1,.9,.2,1));frame.diffuse_texture=mutable
	var m1:Dictionary=Cargo.bank_bindings(player)
	mutable.image.fill(Color(.9,.1,.2,1))
	var m2:Dictionary=Cargo.bank_bindings(player)
	expect(m1[""]["unload-west"][0].rgba!=m2[""]["unload-west"][0].rgba and mutable.reads==2,"Mutable texture fallback is always fingerprinted afresh")
	frame.diffuse_texture=other
	player.return_plan={"gear":"","rows":[{"key":"unload-west","index":0},{"key":"unload-west","index":1}],"started":1.0}
	var base:Dictionary={"crew":{"branforth":{"stage":"old"}}}
	var a:Dictionary=Cargo.capture(base,player,"new-stage")
	player.return_plan.rows.reverse();player.return_plan.started=2.0
	var b:Dictionary=Cargo.capture(base,player,"next-stage")
	expect(a.james_cargo_return.plan.started==1.0 and b.james_cargo_return.plan.started==2.0,"Current plan clocks are fresh; earlier capture stays detached")
	expect(a.james_cargo_return.sourceBindings[0]==b.james_cargo_return.sourceBindings[1],"Current plan row order selects the current source bindings")
	expect(base.crew.branforth.stage=="old" and b.crew.branforth.stage=="next-stage","Actor stage remains fresh without mutating caller data")
	b.james_cargo_return.bankBindings[""]["unload-west"][0].rgba="bad"
	expect(Cargo.bank_bindings(player)==swapped,"Returned binding dictionaries cannot poison future captures")
	print("CARGO_BINDING_CACHE ",checks," checks / ",failures," failures")
	quit(1 if failures else 0)
