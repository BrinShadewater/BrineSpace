"""Package actual staged world captures; no fabricated root interpolation."""
from pathlib import Path
import hashlib, json, html
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'character/marsh-north-ground-production-v1'
CAP = ROOT / 'output/marsh-animation-audit/north-production-native-2026-10-02'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    BASE.mkdir(parents=True, exist_ok=True)
    report = json.loads((CAP / 'report.json').read_text())
    assert report['failures'] == 0 and report['checkpoints'] == 3
    before = json.loads((CAP / 'owner-before.json').read_text())
    assert before == json.loads((CAP / 'owner-after.json').read_text())
    states = json.loads((ROOT / 'character/marsh-consistency-review-v1/runtime-contract.json').read_text())['states']
    images = []
    board = Image.new('RGB', (800, ((len(report['captures']) + 3) // 4) * 250), '#293b40')
    draw = ImageDraw.Draw(board)
    for i, record in enumerate(report['captures']):
        source = (ROOT / 'character/marsh-north-walk-material-v1/candidate-01/north-start' / f"{record['slot']:03d}.png"
                  if record['key'] == 'walk-start-north' else ROOT / states[record['key']]['files'][record['slot']])
        record['source'] = source.relative_to(ROOT).as_posix()
        record['sourceSha256'] = sha(source)
        record['captureSha256'] = sha(CAP / record['file'])
        native = Image.open(CAP / record['file']).convert('RGB')
        images.append(native)
        # Fixed room crop from the full native camera, same for every sample.
        crop = native.crop((440, 260, 680, 530)).resize((200, 225))
        board.paste(crop, ((i % 4) * 200, (i // 4) * 250 + 25))
        draw.text(((i % 4) * 200 + 3, (i // 4) * 250 + 3),
                  f"{record['time']:.2f}s {record['key']} {record['slot']}", fill='white')
    board.save(BASE / 'native-contact.png')
    durations = [round((b['time'] - a['time']) * 1000) for a, b in zip(report['captures'], report['captures'][1:])] + [200]
    images[0].save(BASE / 'native-pose-changes.gif', save_all=True, append_images=images[1:], duration=durations, loop=0)
    report['ownerProfileFilesUnchanged'] = len(before)
    report['mediaScope'] = 'Full native viewport samples at pose changes, reconstructed holds; not continuous native video. Fixed crops contain actual room captures, no source/root compositing.'
    (BASE / 'native-report.json').write_text(json.dumps(report, indent=2) + '\n')
    (BASE / 'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Marsh production North start</title>'
        '<style>body{background:#17212a;color:#eee;font:16px sans-serif;margin:24px}img{max-width:100%}a{color:#8bd}</style>'
        '<h1>Marsh North start — production world root</h1><p>' + html.escape(report['scope']) + '</p><p>'
        + html.escape(report['mediaScope']) + '</p><img src="native-pose-changes.gif"><h2>Fixed native room crops</h2>'
        '<img src="native-contact.png"><p><a href="native-report.json">Checks, source and capture hashes</a> · '
        '<a href="../../scripts/marsh_npc.gd">Production controller</a></p>', encoding='utf-8')
    print(f"Published {report['checks']} checks, {len(images)} actual world samples, three standard disk restorations; {len(before)} owner files unchanged")

if __name__ == '__main__':
    main()
