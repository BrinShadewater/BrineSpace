"""Local source and matched60Hz native review of the east-run registration fix."""
from pathlib import Path
import json
import subprocess
import imageio_ffmpeg
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'character/marsh-east-run-smooth-v1'
EVIDENCE = ROOT / 'output/marsh-east-run-smooth-2026-10-14'


def publish():
    review = BASE / 'review'
    review.mkdir(exist_ok=True)
    before = json.loads((EVIDENCE / 'before-native/report.json').read_text())
    after = json.loads((EVIDENCE / 'after-native/report.json').read_text())
    assert before['failures'] == after['failures'] == 0
    assert len(before['samples']) == len(after['samples'])
    frames = []
    for a, b in zip(before['samples'], after['samples']):
        panel = Image.new('RGB', (800, 424), '#26333c')
        panel.paste(Image.open(EVIDENCE / 'before-native' / a['file']), (0, 24))
        panel.paste(Image.open(EVIDENCE / 'after-native' / b['file']), (400, 24))
        draw = ImageDraw.Draw(panel)
        draw.text((8, 7), 'Before', fill='white')
        draw.text((408, 7), 'After / ' + b['key'] + ' / ' + str(b['slot']), fill='white')
        frames.append(panel)
    video = review / 'native-before-after.mp4'
    with (review / 'encode.log').open('w') as log:
        process = subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '800x424', '-r', '60', '-i', '-', '-an', '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(video)], stdin=subprocess.PIPE, stdout=log, stderr=subprocess.STDOUT)
        for panel in frames: process.stdin.write(panel.tobytes())
        process.stdin.close()
        assert process.wait() == 0
    frames[0].save(review / 'native-poster.png')
    source = []
    contact = Image.new('RGB', (1104, 840), '#26333c')
    for i in range(6):
        old = Image.open(ROOT / f'character/marsh-east-run-material-v1/candidate-03/{i:03}.png').convert('RGBA')
        new = Image.open(BASE / 'run-east-002-registered.png').convert('RGBA') if i == 2 else old
        panel = Image.new('RGB', (736, 400), '#26333c')
        for col, image in enumerate([old, new]):
            figure = image.resize((368, 368), Image.Resampling.NEAREST)
            panel.paste(figure, (col * 368, 28), figure)
            ImageDraw.Draw(panel).text((col * 368 + 8, 8), ('Before' if col == 0 else 'After') + ' / pose ' + str(i), fill='white')
            x, y = i % 3 * 368, (i // 3 * 2 + col) * 210
            contact.paste(image, (x + 92, y + 20), image)
            ImageDraw.Draw(contact).text((x + 8, y + 5), ('Before' if col == 0 else 'After') + ' / ' + str(i), fill='white')
        source.append(panel)
    source[0].save(review / 'source-before-after.webp', save_all=True, append_images=source[1:], duration=[100] * 6, loop=0, lossless=True)
    source[2].save(review / 'airborne-before-after.png')
    contact.save(review / 'all-poses.png')
    # The changed airborne pose in actual room context, one sample from each cycle.
    pairs = [(a, b) for a, b in zip(before['samples'], after['samples']) if b['key'] == 'run-east' and b['slot'] == 2]
    rows = [pairs[0], pairs[len(pairs) // 2], pairs[-1]]
    board = Image.new('RGB', (800, len(rows) * 424), '#26333c')
    for i, (a, b) in enumerate(rows):
        board.paste(frames[b['index']], (0, i * 424))
    board.save(review / 'native-airborne-pairs.png')
    (review / 'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Marsh east run correction</title><style>body{background:#17232b;color:#eeeadd;font:18px system-ui;max-width:1100px;margin:30px auto;padding:0 20px}video,img{max-width:100%;image-rendering:pixelated}section{background:#26333c;padding:16px;margin:20px 0}</style><h1>Marsh east run correction</h1><p>The first airborne drawing lurched forward, then snapped back. Its complete body now registers ten pixels left; planted poses and timing stay unchanged.</p><section><h2>Native before / after</h2><p>Both sides use the same60Hz simulation capture and identical movement. Play or scrub the run and slowing transition.</p><video controls loop muted preload="metadata" poster="native-poster.png" src="native-before-after.mp4"></video></section><section><h2>Exact source comparison</h2><p>Six existing drawings, same cadence. Only pose2 changes registration; no generated replacement artwork is selected.</p><img src="source-before-after.webp"></section><details><summary>Changed airborne drawing</summary><img src="airborne-before-after.png"><img src="native-airborne-pairs.png"></details>', encoding='utf-8')
    print('Published paired60fps native video, exact source loop and airborne comparison')


if __name__ == '__main__': publish()
