"""Q0 dispatched return uses West, with both privately staged side loops loaded."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'tools/prepare_marsh_loaded_swim_world02.py').read_text()
s=s.replace('loaded-swim-east-world-05','loaded-swim-west-world-01')
s=s.replace('var home:=Vector2i(20,21);var target:=Vector2i(19,24)','var home:=Vector2i(20,19);var target:=Vector2i(21,16)')
s=s.replace('for y in range(21,25):','for y in range(16,20):').replace('for x in [19,20]:','for x in [20,21]:').replace('game.occupied[home].rotation=2','game.occupied[home].rotation=0')
s=s.replace('player.load_manifest("res://character/marsh-loaded-swim-material-v1/east-loop-02-unselected/manifest.json",true)','player.load_manifest("res://character/marsh-loaded-swim-material-v1/east-loop-02-unselected/manifest.json",true)\n\tplayer.load_manifest("res://character/marsh-loaded-swim-material-v1/west-loop-01-unselected/manifest.json",true)')
s=s.replace('key=="swim-carry-east"','key=="swim-carry-west"').replace('all six East timing slots','all six West timing slots')
s=s.replace('"eastSlots":east.keys()','"westSlots":east.keys()')
s=s.replace('One actual normal dispatched q2','One actual normal dispatched q0').replace('Only private East loaded-swim02 source override','Private East02 and West01 loaded-swim source overrides').replace('return/East staged loop','return/West staged loop')
s=s.replace('review_marsh_loaded_swim_world02.gd','review_marsh_loaded_swim_west_world01.gd').replace('uid://dw0swimeastw14','uid://bmzw4hg3cnj')
s=s.replace('prepare_marsh_loaded_swim_world02.py','prepare_marsh_loaded_swim_west_world01.py').replace('fingerprint_marsh_loaded_swim_world02.py','fingerprint_marsh_loaded_swim_west_world01.py')
(ROOT/'tools/prepare_marsh_loaded_swim_west_world01_generated.py').write_text(s)
exec(compile(s,str(ROOT/'tools/prepare_marsh_loaded_swim_west_world01_generated.py'),'exec'))
