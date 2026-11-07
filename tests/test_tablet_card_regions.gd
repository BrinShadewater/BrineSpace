extends SceneTree
var failures:=0
class ObservedCard extends "res://scripts/deferred_card_texture.gd":
 var image_reads:=0
 func _get_image() -> Image:
  image_reads+=1
  return super._get_image()
func check(ok:bool,label:String):
 if not ok:failures+=1;push_error(label)
func _init():call_deferred("run")
func run():
 if DisplayServer.get_name()=="headless" or OS.get_user_data_dir()!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):quit(2);return
 var grid=preload("res://scripts/grid_canvas.gd").new()
 var paths:Dictionary=preload("res://scripts/room_card_art.gd").PATHS
 var cards:Array=[];var references:Array=[];var start:=Time.get_ticks_usec()
 for id in paths:
  var image:Image=preload("res://scripts/safe_image.gd").raw_image(paths[id]);image.generate_mipmaps()
  var card:=ObservedCard.new();card.configure(image);cards.append(card)
  references.append(grid._find_content_region(image))
 start=Time.get_ticks_usec()
 for card in cards:grid._cache_texture_source_region(card)
 var preparation_ms:float=(Time.get_ticks_usec()-start)/1000.0
 var reads:=0
 for card in cards:reads+=card.image_reads
 check(reads==0,"Unused tablet cards must not be decoded for unused fallback crop bounds")
 check(grid.texture_source_regions.is_empty(),"Unused card crop cache remains empty")
 print("CARD_REGION_PREPARE_MS ",preparation_ms," reads=",reads)
 if reads!=0:grid.free();quit(1);return
 for i in cards.size():
  var card=cards[i]
  check(grid._texture_source_region(card)==references[i],"First demanded crop preserves exact source lattice")
  check(card.image_reads==1 and card.uploaded_texture==null,"Crop demand reads CPU pixels once without GPU upload")
  check(grid._texture_source_region(card)==references[i] and card.image_reads==1,"Repeated crop reuses cached bounds")
 var shown=cards[0]
 check(shown.get_rid().is_valid(),"Card UI can upload before grid crop request")
 grid.texture_source_regions.erase(shown.get_instance_id())
 check(grid._texture_source_region(shown)==references[0],"Demand after prior card upload keeps the exact crop")
 var raw:Image=preload("res://scripts/safe_image.gd").raw_image(paths.brine_core)
 var eager:=ImageTexture.create_from_image(raw);grid._cache_texture_source_region(eager,raw)
 check(grid.texture_source_regions[eager.get_instance_id()]==grid._find_content_region(raw),"Eager desktop/raw-image crop behavior preserved")
 print("TABLET CARD REGIONS cards=",cards.size()," failures=",failures)
 grid.free();quit(1 if failures else 0)
