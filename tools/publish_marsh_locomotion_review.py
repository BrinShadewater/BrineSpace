"""Publish the bounded October14 source and native locomotion review locally."""
from pathlib import Path
import hashlib
import json
import subprocess
import imageio_ffmpeg
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'character/marsh-locomotion-review-2026-10-14'
EVIDENCE = ROOT / 'output/marsh-locomotion-2026-10-14'


def registered(path, pivot):
    source = Image.open(path).convert('RGBA')
    image = Image.new('RGBA', (184, 184))
    image.paste(source, (92 - round(pivot[0]), 172 - round(pivot[1])))
    return image


def publish():
    review = OUT / 'review'
    review.mkdir(exist_ok=True)
    before = json.loads((EVIDENCE / 'before-native/report.json').read_text())
    after = json.loads((EVIDENCE / 'after-native/report.json').read_text())
    assert before['failures'] == after['failures'] == 0
    catalog_path = ROOT / 'character/marsh-v2/catalog.json'
    selected = {}
    for relative in json.loads(catalog_path.read_text())['body']:
        p = (catalog_path.parent / relative).resolve()
        manifest = json.loads(p.read_text())
        for state in manifest['states']:
            selected[state['id']] = (p, manifest, state)
    prior = json.loads((OUT / 'selected-before.json').read_text())
    native_cards = []
    join_cards = []
    source_cards = []
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    receipts = []
    for case in after['cases']:
        label = case['direction']
        samples = [s for s in after['samples'] if s['direction'] == label]
        original = [s for s in before['samples'] if s['direction'] == label]
        width = 800 if original else 400
        frames = []
        for i, sample in enumerate(samples):
            image = Image.new('RGB', (width, 424), '#26333c')
            draw = ImageDraw.Draw(image)
            if original:
                image.paste(Image.open(EVIDENCE / 'before-native' / original[i]['file']), (0, 24))
                draw.text((8, 7), 'Before', fill='white')
            image.paste(Image.open(EVIDENCE / 'after-native' / sample['file']), (width - 400, 24))
            draw.text((width - 392, 7), 'Installed / ' + sample['key'] + ' / ' + str(sample['slot']), fill='white')
            frames.append(image)
        video = review / (label + '.mp4')
        with (review / (label + '-encode.log')).open('w') as log:
            process = subprocess.Popen([ffmpeg, '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{width}x424', '-r', '25', '-i', '-', '-an', '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(video)], stdin=subprocess.PIPE, stdout=log, stderr=subprocess.STDOUT)
            for frame in frames:
                process.stdin.write(frame.tobytes())
            process.stdin.close()
            assert process.wait() == 0
        frames[0].save(review / (label + '-poster.png'))
        native_cards.append('<article><h3>' + label + '</h3><video controls loop muted preload="metadata" poster="' + label + '-poster.png" src="' + label + '.mp4"></video></article>')
        # One frame at each observed pose change for chronological inspection.
        chosen = []
        last = None
        for sample in samples:
            key = (sample['key'], sample['slot'])
            if key != last:
                chosen.append(sample)
                last = key
        cols = 6
        board = Image.new('RGB', (cols * 200, ((len(chosen) + cols - 1) // cols) * 224), '#26333c')
        for n, sample in enumerate(chosen):
            cell = Image.open(EVIDENCE / 'after-native' / sample['file']).convert('RGB')
            # Follow the recorded actor in its real crop; retain room pixels around it.
            x = round(sample['canvasPosition'][0] - sample['region'][0])
            y = round(sample['canvasPosition'][1] - sample['region'][1])
            center_x = max(100, min(300, x))
            region = (center_x - 100, y - 130, center_x + 100, y + 30)
            assert region[0] >= 0 and region[1] >= 0 and region[2] <= 400 and region[3] <= 400
            col, row = n % cols, n // cols
            board.paste(cell.crop(region), (col * 200, row * 224 + 24))
            ImageDraw.Draw(board).text((col * 200 + 4, row * 224 + 5), sample['key'] + '/' + str(sample['slot']), fill='white')
        board.save(review / (label + '-chronology.png'))
        receipts.append(dict(case=label, samples=len(samples), nativeDurationMs=len(samples) * 40, sourceSlots=sorted({s['key'] + '/' + str(s['slot']) for s in samples}), video=video.name))
    # Focus on the corrected boundaries at a readable source scale.
    edits = json.loads((ROOT / 'character/marsh-locomotion-joins-v1/provenance.json').read_text())['changedSlots']
    for edit in edits:
        key, slot = edit['state'], edit['slot']
        direction = key.split('-')[-1]
        authority = 'walk-north' if key == 'walk-start-north' else 'idle-' + direction
        authority_slot = 1 if authority == 'walk-north' else 0
        p, m, s = selected[key]
        q, n, target = selected[authority]
        def resolve(parent, f): return ROOT / f[6:] if f.startswith('res://') else (parent / f).resolve()
        old = registered(ROOT / prior[key]['files'][slot]['path'], prior[key]['metadata']['pivot'])
        new = registered(resolve(p.parent, s['frameFiles'][slot]), m['pivot'])
        anchor = registered(resolve(q.parent, target['frameFiles'][authority_slot]), n['pivot'])
        assert new.tobytes() == anchor.tobytes()
        images = []
        for left, right in [(old, new), (anchor, anchor)]:
            panel = Image.new('RGB', (736, 400), '#26333c')
            for x, figure in [(0, left), (368, right)]:
                big = figure.resize((368, 368), Image.Resampling.NEAREST)
                panel.paste(big, (x, 28), big)
            draw = ImageDraw.Draw(panel)
            draw.text((8, 8), 'Before / ' + key + ' / ' + str(slot), fill='white')
            draw.text((376, 8), 'After / shared complete pose', fill='white')
            images.append(panel)
        filename = key + '-' + str(slot) + '-boundary.webp'
        images[0].save(review / filename, save_all=True, append_images=images[1:], duration=[400, 400], loop=0, lossless=True)
        join_cards.append('<article><h3>' + key + ' / ' + str(slot) + '</h3><img src="' + filename + '"></article>')
    for key in prior:
        p, m, s = selected[key]
        images = []
        for f in s['frameFiles']:
            source = ROOT / f[6:] if f.startswith('res://') else (p.parent / f).resolve()
            figure = registered(source, m['pivot'])
            image = Image.new('RGB', (276, 312), '#26333c')
            big = figure.resize((276, 276), Image.Resampling.NEAREST)
            image.paste(big, (0, 30), big)
            images.append(image)
        filename = 'current-' + key + '.webp'
        images[0].save(review / filename, save_all=True, append_images=images[1:], duration=s['frameDurationsMs'], loop=0, lossless=True)
        source_cards.append('<article><h3>' + key + '</h3><img src="' + filename + '"></article>')
    html = '<!doctype html><meta charset="utf-8"><title>Marsh locomotion polish</title><style>body{background:#17232b;color:#eeeadd;font:18px system-ui;max-width:1550px;margin:30px auto;padding:0 20px}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(620px,1fr));gap:20px}article{background:#26333c;padding:12px}h3{font-size:18px}video,img{width:100%;image-rendering:pixelated}a{color:#a2d9cc}</style><h1>Marsh locomotion polish</h1><p>Walking, running and short steps in all four directions. Nine start/stop/step boundary holds now share the selected standing or gait drawing. Walk/run cycles and movement timing are retained.</p><h2>Native route playback</h2><p>Use the video controls to play or scrub. Walking/running show before and after on the same prescribed routes; short steps show the installed version. Captured every40ms of simulation, played at25fps. This is sampled native motion, not real-time performance footage.</p><main>' + ''.join(native_cards) + '</main><h2>Boundary corrections, enlarged</h2><p>Each comparison alternates a transition boundary with its adjoining idle or gait pose. Left shows the earlier change of drawing; right shares the same complete pose.</p><main>' + ''.join(join_cards) + '</main><details><summary>All34 selected source clips</summary><p>Isolated clips replay from the beginning; a finite clip replay is a viewer reset.</p><main>' + ''.join(source_cards) + '</main></details>'
    (review / 'index.html').write_text(html, encoding='utf-8')
    (review / 'receipt.json').write_text(json.dumps(dict(cases=receipts, scopeAudit=json.loads((EVIDENCE / 'scope-audit.json').read_text())), indent=2) + '\n')
    print('Published12 native videos,9 boundary comparisons and34 current source previews')


if __name__ == '__main__':
    publish()
