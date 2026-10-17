from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parent.parent
OLD=P.parent/'bill-land-water-material-west-v1'
s=(OLD/'prepare.py').read_text(encoding='utf-8').replace('bill-land-water-west-v2','bill-land-water-west-v4').replace('bill-land-water-material-west-v1','bill-land-water-material-west-v2').replace('bill_land_water_material_west_v1','bill_land_water_material_west_v2').replace('BILL LAND WATER MATERIAL WEST V1:','BILL LAND WATER MATERIAL WEST V2:').replace('cbillwestwetentry','cbillwestwetdetail').replace(".replace('material-east-v4','material-west-v1')",".replace('material-east-v4','material-west-v2')")
s=s.replace('Vector2(158,80),Vector2(147,114),Vector2(141,118),Vector2(130,150),Vector2(131,188)','Vector2(157,79),Vector2(148,114),Vector2(140,117),Vector2(130,150),Vector2(131,188)')
# Original preparer was derived from East V4 and replaced its original anchor tuple.
s=s.replace('Vector2(158,80),Vector2(147,114),Vector2(141,118),Vector2(130,150),Vector2(131,188)','Vector2(157,79),Vector2(148,114),Vector2(140,117),Vector2(130,150),Vector2(131,188)')
exec(compile(s,str(P/'prepare-derived.py'),'exec'),{'__file__':str(P/'prepare-derived.py'),'__name__':'__main__'})
# Strengthen generated revision with explicit scene and decoded frame checks.
import json,hashlib
testpath=R/'tests/test_bill_land_water_material_west_v2.gd'
t=testpath.read_text(encoding='utf-8');needle=' game.set_process(false)'
assert t.count(needle)==1
t=t.replace(needle,(P/'loaded-source-guards.txt').read_text(encoding='utf-8')+needle)
testpath.write_text(t,encoding='utf-8')
assert 'material-west-v1/fixture_main' not in (P/'fixture.tscn').read_text()
f=P/'targeted-inputs.json';e=json.loads(f.read_text());e['character/bill-land-water-material-west-v2/fixture.tscn']=''
for relative in e:e[relative]=hashlib.sha256((R/relative).read_bytes()).hexdigest()
f.write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
print('Prepared current V4 fixture with explicit source admission checks and 27-input freeze. Review publishers are maintained separately.')
