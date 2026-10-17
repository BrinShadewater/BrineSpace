import json
from pathlib import Path

from PIL import Image, ImageDraw

root = Path.cwd()
review = root / 'character/james-west-carry-walk-keys-v1/release-resume-playtest-v357'
captures = root / 'output/james-resume-playtest-v357/captures'
data = json.loads((captures / 'review.json').read_text())
assert data['failures'] == 0 and len(data['cases']) == 4 and len(data['resumes']) == 8
(review / 'lifecycle-review.json').write_text(json.dumps(data, indent=2) + '\n')
for case in data['cases']:
    label = case['case']
    rows = [x for x in data['captures'] if x['case'] == label]
    resumes = [x for x in data['resumes'] if x['case'] == label]
    selected = []
    for resume in resumes:
        for suffix, key in [('before', 'beforeFrame'), ('after', 'afterFrame')]:
            index = resume[key] + (1 if suffix == 'after' else 0)
            row = rows[index]
            delay = round((row['time'] - rows[resume['beforeFrame']]['time']) * 1000)
            selected.append((resume['phase'] + ' ' + suffix + (f' +{delay}ms' if suffix == 'after' else ''), row))
    selected.append(('unload', next(x for x in rows if x['tripPhase'] == 'unload')))
    selected.append(('complete', rows[-1]))
    first = Image.open(captures / rows[0]['file'])
    width, height = first.size
    board = Image.new('RGB', (width * 3, (height + 24) * 2), (47, 58, 63))
    draw = ImageDraw.Draw(board)
    for i, (caption, row) in enumerate(selected):
        x, y = i % 3, i // 3
        board.paste(Image.open(captures / row['file']).convert('RGB'), (x * width, y * (height + 24) + 24))
        draw.text((x * width + 4, y * (height + 24) + 5), caption, fill='white')
    board.save(review / (label + '-resume.png'))
(review / 'index.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8">
<title>James — save and continue</title><style>
body{margin:24px auto;padding:0 24px;max-width:1250px;background:#2f3a3f;color:#f3f0e6;font:17px system-ui}
h1{font-size:26px}h2{font-size:20px}p{line-height:1.5;max-width:900px}
img{display:block;max-width:100%;height:auto;border:1px solid #5b686d;margin-bottom:36px}
a{color:#e6c568}small{color:#c7ced0}</style>
<h1>James — save and continue</h1>
<p>Each journey was saved during the loaded return swim and again while the airlock
drained. Both saves resumed in a fresh scene; James returned safely and delivered
the salvage once.</p><p>These are native before-and-after captures from the tested
Windows build. After views use the following simulation frame, once the Continue
camera refocus has settled. They show sampled handoffs rather than continuous motion.</p>
<p><a href="../release-motion-review-v356/index.html">Animation playback</a></p>
''' + ''.join('<h2>Airlock orientation '+str(c['rotation']+1)+'</h2><img alt="Loaded return and drain before and after continuing, followed by unload and completion" src="'+c['case']+'-resume.png">' for c in data['cases']) + '</html>')
print(json.dumps({'checks': data['checks'], 'failures': 0, 'cases': 4, 'freshSceneDiskResumes': 8, 'captures': len(data['captures'])}))
