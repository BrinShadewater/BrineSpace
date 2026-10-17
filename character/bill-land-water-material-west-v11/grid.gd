extends "res://character/bill-land-water-material-west-v10/grid.gd"
func bridge_bank(gear:String,enter:bool)->Array:
 var id:String=gear+("-enter" if enter else "-exit")
 if not bridge_banks.has(id):
  var files:Dictionary={
   "-enter":"res://character/bill-west-active-gait-water-audit-v2/staged-entry/bare/manifest.json",
   "diving-helmet-enter":"res://character/bill-west-active-gait-water-audit-v2/staged-entry/helmet/manifest.json",
   "-exit":"res://character/bill-west-active-gait-water-audit-v2/staged-exit/bare/manifest.json",
   "diving-helmet-exit":"res://character/bill-west-active-gait-water-audit-v2/staged-exit/helmet/manifest.json"}
  var loader=preload("res://scripts/crew_sprite_player.gd").new();loader.load_manifest(files[id],true)
  var key:String="land-swim-west" if enter else "swim-land-west"
  bridge_banks[id]=[loader.frames[key],loader.timing[key].durations]
 var bank:Array=bridge_banks[id];var label:String=("entry-" if enter else "exit-")+("bare" if gear.is_empty() else "helmet");var centers:Array=head_data()[label]
 for i in range(centers.size()):
  source_head_centers[bank[0][i+1]]=Vector2(centers[i][0],centers[i][1]);source_head_sizes[bank[0][i+1]]=Vector2(21,23) if gear.is_empty() else Vector2(40,40)
 return bank
