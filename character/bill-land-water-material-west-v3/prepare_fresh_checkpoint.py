from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parent.parent;E=P.parent/'bill-land-water-material-east-v4'
codec=(P.parent/'bill-land-water-material-east-v3/checkpoint.gd').read_text(encoding='utf-8').replace('east','west')
(P/'checkpoint.gd').write_text(codec,encoding='utf-8');(P/'checkpoint.gd.uid').write_text('uid://cbillwestwetcodec03\n')
main=(R/'scripts/main.gd').read_text(encoding='utf-8');needle='const GridCanvasScript := preload("res://scripts/grid_canvas.gd")';assert main.count(needle)==1
(P/'fresh_fixture_main.gd').write_text(main.replace(needle,'const GridCanvasScript := preload("res://character/bill-land-water-material-west-v3/grid.gd")'),encoding='utf-8');(P/'fresh_fixture_main.gd.uid').write_text('uid://cbillwestwetfreshmain03\n')
scene=(P/'fixture.tscn').read_text(encoding='utf-8').replace('fixture_main.gd','fresh_fixture_main.gd');assert 'west-v3/fresh_fixture_main.gd' in scene
(P/'fresh_fixture.tscn').write_text(scene,encoding='utf-8')
t=(R/'tests/test_bill_land_water_fresh_checkpoint_east_v2.gd').read_text(encoding='utf-8')
t=t.replace('bill-land-water-material-east-v4','bill-land-water-material-west-v3').replace('bill-land-water-material-east-v3/checkpoint.gd','bill-land-water-material-west-v3/checkpoint.gd').replace('bill-land-water-fresh-checkpoint-east-v2','bill-land-water-fresh-checkpoint-west-v1').replace('FRESH CHECKPOINT EAST V2:','FRESH CHECKPOINT WEST V1:')
t=t.replace('[[false,81],[false,425],[true,81],[true,425]]','[[false,81],[false,432],[true,81],[true,432]]')
t=t.replace('actor.foot=pair[0];actor.direction="east"','actor.foot=pair[1];actor.direction="west"').replace('PackedVector2Array([pair[1],pair[0],pair[1],pair[0]])','PackedVector2Array([pair[0],pair[1],pair[0],pair[1]])')
needle=' game.set_process(false);game.tick_timer.stop();'
start=t.index('func fresh():');end=t.index('func capture(',start);block=t[start:end]
assert block.count(needle)==1
loaded=(R/'tests/test_bill_land_water_material_west_v3.gd').read_text(encoding='utf-8');a=loaded.index(' check(game.get_script().resource_path==');b=loaded.index(' game.set_process(false)',a)
checks=loaded[a:b].replace('west-v3/fixture_main.gd','west-v3/fresh_fixture_main.gd')
block=block.replace(needle,checks+needle);t=t[:start]+block+t[end:]
needle='  await record_capture(game,view,name+"-after-candidate",restored)'
assert t.count(needle)==1
t=t.replace(needle,'''  var guarded:Dictionary=WET_SAVE.capture(game.grid_view)
  for kind in ["version","clock","gear","phase","bank","extent","source","previous"]:
   var bad:Dictionary=guarded.duplicate(true)
   if kind=="version":bad.version=99
   elif kind=="clock":bad.clock+=.01
   elif kind=="gear":bad.gear="diving-helmet" if bad.gear=="" else ""
   elif kind=="phase":bad.target_phase.key="swim-east"
   elif kind=="bank":bad.bank.sources[3].rgba="modified-artwork"
   elif kind=="extent":bad.extent[0]-=1
   elif kind=="source":bad.incoming.signature.rgba="modified-artwork"
   else:bad.previous.direction="east"
   check(not WET_SAVE.restore(game.grid_view,bad),"Reject malformed "+kind+" bridge snapshot")
   check(WET_SAVE.capture(game.grid_view)==guarded,"Rejected "+kind+" preserves admitted bridge and playback")
  check(restored.get_image().get_data()==pixels,"Rejected sidecars preserve exact loaded presentation")
'''+needle)
test=R/'tests/test_bill_land_water_fresh_checkpoint_west_v1.gd';test.write_text(t,encoding='utf-8');test.with_suffix('.gd.uid').write_text('uid://cbillwestwetfreshtest01\n')
runner=(R/'tools/run_bill_land_water_fresh_checkpoint_east_v2_validation.py').read_text(encoding='utf-8').replace('bill-land-water-fresh-checkpoint-east-v2','bill-land-water-fresh-checkpoint-west-v1').replace('bill_land_water_fresh_checkpoint_east_v2','bill_land_water_fresh_checkpoint_west_v1').replace('FRESH CHECKPOINT EAST V2:','FRESH CHECKPOINT WEST V1:').replace('helmet-425-future-after','helmet-432-future-after')
(R/'tools/run_bill_land_water_fresh_checkpoint_west_v1_validation.py').write_text(runner,encoding='utf-8')
publisher=(E/'build_fresh_checkpoint_review.py').read_text(encoding='utf-8').replace('bill-land-water-fresh-checkpoint-east-v2','bill-land-water-fresh-checkpoint-west-v1').replace('Bill East','Bill West')
start=publisher.index("for gear in ['bare','helmet']:");end=publisher.index("board.save(",start)
publisher=publisher[:start]+'''for gear in ['bare','helmet']:
 for tick,bank,index in [(81,'bill-land-water-west-v4',3),(432,'bill-water-exit-west-v1',4)]:
  a=Image.open(O/f'{gear}-{tick}-before-candidate-source.png').convert('RGBA')
  state='land-swim-west' if tick==81 else 'swim-land-west'
  b=Image.open(P.parent/bank/gear/f'frames/{state}/{index:03}.png').convert('RGBA')
  assert a.size==b.size and a.tobytes()==b.tobytes(), 'Save must exercise current authored West pose'
assert not changes,changes
'''+publisher[end:]
publisher=publisher.replace("'targetedInputChanges':changes,", "'targetedInputChanges':changes,'frozenInputCount':len(inputs),")
(P/'build_fresh_checkpoint_review.py').write_text(publisher,encoding='utf-8')
files=list(json.loads((P/'targeted-inputs.json').read_text(encoding='utf-8')))
files+=['scripts/run_save.gd','character/bill-land-water-material-west-v3/checkpoint.gd','character/bill-land-water-material-west-v3/fresh_fixture_main.gd','character/bill-land-water-material-west-v3/fresh_fixture.tscn','tests/test_bill_land_water_fresh_checkpoint_west_v1.gd']
(P/'fresh-targeted-inputs.json').write_text(json.dumps({f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in sorted(set(files))},indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(frozenInputs=len(set(files)),cases=4,entryTick=81,entryPose=3,exitTick=432,exitPose=4,malformedKinds=8,scope='Normal disk/fresh scene world restore then staged resource-free West sidecar; title Continue and normal admission separate.')))
