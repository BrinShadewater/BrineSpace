"""Preview explicitly measured travel against a fixed floor; never selects assets."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]


def main(study_path, output):
    study_path = Path(study_path).resolve()
    study = json.loads(study_path.read_text())
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    sign = {'west': -1, 'east': 1}[study['direction']]
    records = []
    for action, spec in study['transitions'].items():
        recipe_path = ROOT / spec['recipe']
        recipe = json.loads(recipe_path.read_text())
        distances = spec['travelPixels']
        durations = spec['durationMs']
        assert len(distances) == len(durations) == len(recipe['sourceFrames'])
        assert distances[0] == 0 and all(b >= a for a, b in zip(distances, distances[1:]))
        frames, hashes = [], []
        for index, distance in enumerate(distances):
            source = ROOT / recipe['output'] / f"{recipe['state']}-{index:03}.png"
            hashes.append(hashlib.sha256(source.read_bytes()).hexdigest())
            pose = Image.open(source).convert('RGBA')
            frame = Image.new('RGB', (384, 280), '#293b40')
            draw = ImageDraw.Draw(frame)
            for x in range(0, 384, 16):
                draw.line((x, 224, x, 279), fill='#42585e')
            draw.line((0, 224, 383, 224), fill='#799596')
            frame.paste(pose, (64 + sign * round(distance), 0), pose)
            draw.text((8, 254), f'{action} {index}: travel {distance}px; uncertainty +/-{spec["uncertaintyPixels"]}px', fill='white')
            frames.append(frame)
        sheet = Image.new('RGB', (384 * len(frames), 280))
        for index, frame in enumerate(frames):
            sheet.paste(frame, (384 * index, 0))
        sheet.save(output / f'{action}-contact.png')
        frames[0].save(output / f'{action}-travel.gif', save_all=True,
                       append_images=frames[1:], duration=durations, loop=0)
        records.append({'action': action, 'frameSha256': hashes,
                        'recipeSha256': hashlib.sha256(recipe_path.read_bytes()).hexdigest(),
                        'travelWorldUnits': distances[-1] * study['worldStandingHeight'] / study['standingHeight']})
    report = {'status': 'review-media-only', 'studySha256': hashlib.sha256(study_path.read_bytes()).hexdigest(),
              'records': records, 'limits': study['limits']}
    (output / 'contact-review.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('study')
    parser.add_argument('output')
    args = parser.parse_args()
    main(args.study, args.output)
