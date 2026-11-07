"""Export the selected, independently authored Bill east/west walk recipes."""
from pathlib import Path
import argparse
import json
from rebuild_bill_art import ROOT, HelmetRebaker, read, image, tilted
from build_bill_alternating_west_walk import build as build_west
from build_bill_alternating_east_walk import build as build_east


def build(output):
    output = Path(output).resolve()
    output.relative_to((ROOT / 'output').resolve())
    output.mkdir(parents=True, exist_ok=True)
    helmets = HelmetRebaker(None,max_height=48)
    recipes = {'east': build_east(ROOT, read, image, helmets, tilted,verify_equipment=False),
               'west': build_west(ROOT, read, image, helmets, tilted,verify_equipment=False)}
    for variant in ('bare', 'helmet'):
        manifest = {'name': 'bill-connected-walk-' + variant,
                    'frameWidth': 184, 'frameHeight': 184, 'pivot': [92, 172],
                    'standingHeight': 148, 'precomposed': True,
                    'strideDistanceCells': {'walk': 92 * .17 / 148}, 'states': []}
        for direction in ('east', 'west'):
            files = []
            for phase in range(6):
                frame = recipes[direction][0 if variant == 'bare' else 1]['walk-' + direction][phase].copy()
                suffix = 'candidate' if variant == 'bare' else 'helmet'
                name = f'{direction}-{suffix}-{phase:02}.png'
                frame.save(output / name)
                files.append(name)
            manifest['states'].append({'id': 'walk-' + direction, 'frameFiles': files,
                                      'frameDurationsMs': [170,130,150,170,130,150], 'loop': True})
        (output / f'{variant}-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print('24 selected walk review frames exported; production files untouched')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'output/bill-connected-walk')
    build(parser.parse_args().output)
