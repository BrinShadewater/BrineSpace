"""Audit the selected ocean assets from this continuation without rewriting hashes."""
import argparse
import json
from pathlib import Path
from audit_environment_pack import inspect_pack
from build_release_manifest import collect

ROOT = Path(__file__).resolve().parents[1]
PACKS = (
    ('ocean-floor-expansion-v1', 'assets/environment/ocean-floor-expansion-v1/ocean_floor_view.gd'),
    ('alien-fungi-biomes-v1', 'assets/environment/alien-fungi-biomes-v1/fungi_biome_view.gd'),
    ('seep-geology-v1', 'assets/environment/sub-biomes-v1/sub_biome_view.gd'),
    ('habitat-sediments-v1', 'assets/environment/sub-biomes-v1/sub_biome_view.gd'),
    ('tall-sea-plants-v1', 'assets/environment/tall-sea-plants-v1/tall_plants_view.gd'),
    ('giant-mushrooms-v1', 'assets/environment/giant-mushrooms-v1/giant_mushroom_view.gd'),
    ('upright-kelp-v1', 'assets/environment/upright-kelp-v1/upright_kelp_view.gd'),
)

def audit():
    packs, selections = [], []
    for name, consumer in PACKS:
        ledger_path = ROOT / 'assets/environment' / name / 'manifest.json'
        report = inspect_pack(ledger_path)
        assert not report['unregistered_candidates'], name
        ledger = json.loads(ledger_path.read_text())
        source = (ROOT / consumer).read_text()
        selected = [a for a in ledger['assets'] if a.get('runtime_selected', True)]
        for asset in selected:
            path = 'res://assets/environment/' + name + '/' + asset['selected_source']
            assert '"' + path + '"' in source, 'Missing whole runtime binding: ' + path
            selections.append({'pack': name, 'id': asset['id'], 'path': path,
                               'consumer': consumer, 'kind': asset['kind']})
        packs.append({'pack': name, 'selected': len(selected),
                      'rasters': report['source_count'], 'identities': report['identity_count']})
    assert len(selections) == 30
    runtime_files, _ = collect(ROOT)
    missing = [a['path'] for a in selections if a['path'][6:] not in runtime_files]
    assert not missing, 'Unreachable release assets: ' + ', '.join(missing)
    return {'selected_count': len(selections), 'raster_count': sum(p['rasters'] for p in packs),
            'packs': packs, 'selected_assets': selections,
            'release_dependency_reachable': len(selections),
            'visual_acceptance': 'Separate native comparison and gameplay review required'}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    result = audit()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x', encoding='utf-8') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print(f"PASS: seven packs, {result['selected_count']} selected assets, "
          f"{result['raster_count']} immutable rasters; all whole paths bound and release-reachable")
