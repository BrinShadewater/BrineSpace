"""Immutable source and runtime binding checks for the ocean-floor expansion."""
import hashlib,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from audit_environment_pack import inspect_pack
ROOT=Path(__file__).resolve().parents[1]
PACK=ROOT/'assets/environment/ocean-floor-expansion-v1'
report=inspect_pack(PACK/'manifest.json')
assert report['identity_count']==10 # Eight installed assets and two rejected study identities.
assert not report['unregistered_candidates'],report['unregistered_candidates']
view=(PACK/'ocean_floor_view.gd').read_text()
for a in json.loads((PACK/'manifest.json').read_text())['assets']:
    if a.get('runtime_selected',False):
        assert 'res://assets/environment/ocean-floor-expansion-v1/'+a['selected_source'] in view
environment=(ROOT/'scripts/environment_art.gd').read_text()
for name in ['fractured-stone','mineral-vein']:
    assert 'res://assets/environment/ocean-floor-expansion-v1/runtime/'+name+'.png' in environment
assert 'ocean_floor.render_into(canvas,cell_size,sub_biomes.regions)' in (ROOT/'assets/environment/seabed-v1/seabed_background.gd').read_text()
assert 'EnvironmentArt.texture("mineral-surface")' in (ROOT/'assets/environment/rock-blockers-v1/rock_view.gd').read_text()
print('PASS:',report['identity_count'],'identities,',report['source_count'],'rasters; immutable sources, alpha and runtime bindings')
