"""Publish the current native containment and travel review."""
from pathlib import Path
import json, re
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'character/marsh-gameplay-review-v1'
NATIVE = ROOT / 'output/marsh-animation-audit/gameplay-native'

def main():
    OUT.mkdir(exist_ok=True)
    assert len(list(NATIVE.glob('*.png'))) == 54
    log = (NATIVE.parent / 'gameplay-native.log').read_text()
    assert '54 native captures, 0 failures' in log
    directions = ('north', 'south', 'east', 'west')
    for direction in directions:
        frames = [Image.open(NATIVE / f'{action}-{direction}-{i:02}.png').convert('RGB').crop((290, 115, 890, 570)) for action in ('injury', 'recovery') for i in range(6)]
        frames[0].save(OUT / f'containment-{direction}.gif', save_all=True, append_images=frames[1:], duration=180, loop=0)
        source = []
        for action in ('injury-ground', 'injury-rise'):
            for i in range(6):
                sprite = Image.open(ROOT / f'character/marsh-injury-runtime-v1/frames/{action}-{direction}/{i:03}.png').convert('RGBA')
                background = Image.new('RGB', (184, 184), '#243238')
                background.paste(sprite, (0, 0), sprite)
                source.append(background.resize((368, 368), Image.Resampling.NEAREST))
        source[0].save(OUT / f'source-{direction}.gif', save_all=True, append_images=source[1:], duration=180, loop=0)
    board = Image.new('RGB', (1200, 954), '#243238')
    draw = ImageDraw.Draw(board)
    for i, name in enumerate(('travel-001', 'travel-004', 'travel-008', 'travel-016', 'travel-032', 'critical-return')):
        im = Image.open(NATIVE / (name + '.png')).convert('RGB').crop((290, 115, 890, 570)).resize((600, 295))
        x, y = i % 2 * 600, i // 2 * 318
        board.paste(im, (x, y + 23)); draw.text((x + 5, y + 5), name, fill='white')
    board.save(OUT / 'travel.png')
    html = '''<!doctype html><meta charset="utf-8"><title>Marsh: live damage and running</title>
<style>body{background:#17212a;color:#e4ebe9;font:17px system-ui;max-width:1250px;margin:30px auto;padding:0 24px}a{color:#b0dbc9}img{max-width:100%;image-rendering:pixelated}.pair{display:flex;gap:16px;align-items:center;flex-wrap:wrap}.pair img:first-child{width:600px}.pair img:last-child{width:368px}p{max-width:1000px}</style>
<h1>Marsh: live damage and running</h1>
<p>Containment faults in Marsh's occupied room now cause a nonfatal knockdown, white synthetic-fluid leak and recovery. A busy furniture or cargo action finishes before the reaction starts. The leak is a temporary part of the reaction, fading as he returns to standing. There is no new health meter or lethal damage rule; ordinary shutdown stays dry.</p>
<p>Long, unloaded dry trips run at 1.5 times walking speed, starting beyond 128 world units and slowing within 64. A return to his pod runs at 15% charge or less while charge remains. Short steps, cargo travel, swimming, ordinary low-charge returns and depleted-battery movement keep their existing rules. Traffic and arrival checks use the real elapsed time.</p>
<p>The actual station fixture checks the fault event, movement through the lab/corridor/core route, peer blocking, pause, old checkpoints and Continue during falls, recovery and running: 54 native captures, zero failures. The complete player audit checks 200 states, 1,026 frame slots and 416 captures; the separate furniture fixture checks 84 captures. These captures establish the reviewed fixture scenes, rather than every possible station layout.</p>
<p><a href="../marsh-consistency-review-v1/index.html">Complete current animation review</a></p>
<h2>Containment fall and recovery</h2><p>Native station context beside enlarged current source poses. North retains the corrected close trailing legs.</p>'''
    for direction in directions:
        html += f'<h3>{direction.title()}</h3><div class="pair"><img src="containment-{direction}.gif" alt="{direction} native reaction"><img src="source-{direction}.gif" alt="{direction} source reaction"></div>'
    html += '<h2>Travel and critical return</h2><p>Native route samples through the Xeno Lab and its doorway, ending with a critical-battery return sample.</p><img src="travel.png" alt="Native travel and return samples">'
    (OUT / 'index.html').write_text(html, encoding='utf8')
    marker = b'<h2>Live containment injury and running</h2>'
    section = marker + b'<p>Current gameplay now selects white-fluid injury and recovery from containment faults, and running for long dry trips and critical pod returns. Earlier staged previews below record historical work.</p><p><a href="../marsh-gameplay-review-v1/index.html">Open the current gameplay review</a></p>'
    for path in (ROOT / 'character/marsh-run-carry-review-v1/index.html', ROOT / 'character/marsh-consistency-review-v1/index.html'):
        data = path.read_bytes()
        if marker not in data:
            anchor = b'<script>' if b'<script>' in data else b'</body>'
            data = data.replace(anchor, section + anchor, 1)
            path.write_bytes(data)
    for path in (OUT / 'index.html', ROOT / 'character/marsh-consistency-review-v1/index.html', ROOT / 'character/marsh-run-carry-review-v1/index.html'):
        links = re.findall(r'<(?:img|a)[^>]+(?:src|href)="([^"]+)"', path.read_bytes().decode('utf8', errors='replace'))
        assert all((path.parent / link).exists() for link in links if not link.startswith(('http', '#')))
    (OUT / 'verification.json').write_text(json.dumps({'runtimeStates':200,'frameSlots':1026,'nativeConsistencyCaptures':416,'nativeFurnitureCaptures':84,'nativeGameplayCaptures':54,'failures':0}, indent=2)+'\n')
    print('Gameplay review: four native/source reactions, six travel samples; local links resolve')

if __name__ == '__main__':
    main()
