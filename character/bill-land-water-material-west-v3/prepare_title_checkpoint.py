from pathlib import Path
import hashlib, json

P = Path(__file__).resolve().parent
R = P.parent.parent
E = P.parent / 'bill-land-water-material-east-v3'
def west(text):
    return text.replace('east', 'west').replace('EAST', 'WEST').replace('bare-72', 'bare-81').replace('helmet-72', 'helmet-81').replace('425', '432')
for name in ['title_fixture.gd','title_fixture_main.gd','title_bridge_envelope.gd','seal_title_checkpoints.gd']:
    (P/name).write_text(west((E/name).read_text(encoding='utf-8')),encoding='utf-8')
    (P/(name+'.uid')).write_text('uid://cbillwesttitle'+name.split('.')[0].replace('_','')+'03\n')
title=(R/'scripts/title_screen.gd').read_text(encoding='utf-8')
needle='const GAME_SCENE := "res://scenes/main.tscn"'
assert title.count(needle)==1
(P/'title_fixture_base.gd').write_text(title.replace(needle,'const GAME_SCENE := "res://character/bill-land-water-material-west-v3/title_game.tscn"'),encoding='utf-8')
main=(R/'scripts/main.gd').read_text(encoding='utf-8')
needle='const GridCanvasScript := preload("res://scripts/grid_canvas.gd")'
assert main.count(needle)==1
(P/'title_fixture_base_main.gd').write_text(main.replace(needle,'const GridCanvasScript := preload("res://character/bill-land-water-material-west-v3/grid.gd")'),encoding='utf-8')
for name in ['title_fixture_base','title_fixture_base_main']:
    (P/(name+'.gd.uid')).write_text('uid://cbillwest'+name.replace('_','')+'03\n')
(P/'title_game.tscn').write_text((P/'fixture.tscn').read_text().replace('fixture_main.gd','title_fixture_main.gd'),encoding='utf-8')
(P/'title_screen.tscn').write_text((R/'scenes/title_screen.tscn').read_text().replace('res://scripts/title_screen.gd','res://character/bill-land-water-material-west-v3/title_fixture.gd'),encoding='utf-8')
fresh=(R/'tests/test_bill_land_water_fresh_checkpoint_west_v1.gd').read_text(encoding='utf-8')
header=fresh.split('func water_at(')[0].replace('bill-land-water-fresh-checkpoint-west-v1/','bill-land-water-title-checkpoint-west-v1/')
tail=west((R/'tests/test_bill_land_water_title_checkpoint_east_v1.gd').read_text(encoding='utf-8').split('func water_at(')[1])
test=header+'func water_at('+tail
start=fresh.index(' check(game.get_script().resource_path==')
end=fresh.index(' game.set_process(false)',start)
loaded=fresh[start:end].replace('fresh_fixture_main.gd','title_fixture_main.gd')
loaded=loaded.replace('var path:String=manifest_path', 'var raw_path:String=manifest_path').replace('image.load(path)', 'image.load(raw_path)')
needle=' var actor=game.bill_npc;var grid=game.grid_view;var view=grid.rare_room_views["salvage_workshop"]'
assert test.count(needle)==1
test=test.replace(needle,loaded+needle)
(R/'tests/test_bill_land_water_title_checkpoint_west_v1.gd').write_text(test,encoding='utf-8')
(R/'tests/test_bill_land_water_title_checkpoint_west_v1.gd.uid').write_text('uid://cbillwesttitleprobe03\n')
runner=west((R/'tools/run_bill_land_water_title_checkpoint_east_v1_validation.py').read_text(encoding='utf-8'))
(R/'tools/run_bill_land_water_title_checkpoint_west_v1_validation.py').write_text(runner,encoding='utf-8')
publisher=west((E/'build_title_checkpoint_review.py').read_text(encoding='utf-8'))
publisher=publisher.replace("assert v['passed'] and len(v['intervals'])==5", "assert v['passed'] and len(v['intervals'])==5;D.mkdir(exist_ok=True)")
publisher=publisher.replace("board.save(D/'title-comparison.png')", "assert not changes,changes\nboard.save(D/'title-comparison.png')")
(P/'build_title_checkpoint_review.py').write_text(publisher,encoding='utf-8')
inputs=json.loads((P/'fresh-targeted-inputs.json').read_text())
paths=set(inputs)
paths.update(['scripts/title_screen.gd','scripts/loading_transition.gd','tests/test_bill_land_water_title_checkpoint_west_v1.gd','tools/run_bill_land_water_title_checkpoint_west_v1_validation.py'])
for name in ['title_fixture.gd','title_fixture_main.gd','title_fixture_base.gd','title_fixture_base_main.gd','title_bridge_envelope.gd','seal_title_checkpoints.gd','title_screen.tscn','title_game.tscn']:
    paths.add((P/name).relative_to(R).as_posix())
for name in ['bare-81','bare-432','helmet-81','helmet-432']:
    for leaf in ['bill-water-'+name+'.loop',name+'-bridge.bin',name+'-before-candidate-source.png',name+'-future-before-candidate-source.png']:
        paths.add((P/'fresh-checkpoint-review'/leaf).relative_to(R).as_posix())
(P/'title-targeted-inputs.json').write_text(json.dumps({f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in sorted(paths)},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'preparedCases':4,'frozenInputs':len(paths),'entryTick':81,'exitTick':432,'currentLoadedFrameChecks':28}))
