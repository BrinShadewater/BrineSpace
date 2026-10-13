"""Publish actual seat-controller captures beside current registered source/idle."""
from pathlib import Path
import hashlib, html, json
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
CAP = ROOT / 'output/marsh-animation-audit/seat-lifecycle-2026-10-02-reviewed'
OUT = ROOT / 'character/marsh-seat-lifecycle-review-v1'

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    report = json.loads((CAP/'report.json').read_text())
    assert report['failures'] == 0
    contract_path = ROOT/'character/marsh-consistency-review-v1/runtime-contract.json'
    contract = json.loads(contract_path.read_text())['states']
    groups = {}
    for record in report['captures']:
        groups.setdefault((record['room'], record['rotation']), []).append(record)
    assert len(groups) == 8
    sections = []
    refs = []
    for direction in ('south','north','east','west'):
        path = f'character/marsh-motion-polish-v1/sources/{direction}-standing-identity-01.png'
        refs.append({'direction':direction,'path':path,'sha256':hashlib.sha256((ROOT/path).read_bytes()).hexdigest()})
    for (room, rotation), rows in groups.items():
        tiles = []
        for record in rows:
            spec = contract[record['key']]
            source = spec['files'][record['slot']]
            assert hashlib.sha256((ROOT/source).read_bytes()).hexdigest() == spec['hashes'][record['slot']]
            record['source'] = source
            record['sourceSha256'] = spec['hashes'][record['slot']]
            record['captureSha256'] = hashlib.sha256((CAP/record['file']).read_bytes()).hexdigest()
            native = Image.open(CAP/record['file']).convert('RGB')
            # Fixed room viewport mapping from the observed native 1600x900 capture.
            # Crop wide enough for every authored seating offset; retain full originals.
            x = 566 + (record['foot'][0]-7872)*1.2
            y = 498 + (record['foot'][1]-7872)*1.2
            crop = native.crop((round(x-120),round(y-150),round(x+120),round(y+90)))
            tile = Image.new('RGB',(700,290),'#293b40')
            tile.paste(crop,(0,40))
            draw = ImageDraw.Draw(tile)
            draw.text((4,4),f"{record['stage'] or 'standing'} / {record['key']} #{record['slot']} / {record['elapsed']:.2f}s",fill='white')
            draw.text((4,24),'Native chair context',fill='white')
            for left, key, file in [(240,'idle-'+record['key'].rsplit('-',1)[1],None),(460,record['key'],source)]:
                anchor = contract[key]
                image = Image.open(ROOT/(file or anchor['files'][0])).convert('RGBA')
                tile.paste(image,(left+112-round(anchor['pivot'][0]),265-round(anchor['pivot'][1])),image)
                draw.text((left+4,24),'Registered idle' if file is None else 'Selected whole source',fill='white')
                draw.line((left+4,265,left+220,265),fill='#839597')
            tiles.append(tile)
        stem = f'{room}-q{rotation}'
        durations = [max(20,round((b['elapsed']-a['elapsed'])*1000)) for a,b in zip(rows,rows[1:])] + [1000]
        tiles[0].save(OUT/(stem+'.gif'),save_all=True,append_images=tiles[1:],duration=durations,loop=0)
        board = Image.new('RGB',(1400,290*((len(tiles)+1)//2)),'#293b40')
        for i,tile in enumerate(tiles): board.paste(tile,((i%2)*700,(i//2)*290))
        board.save(OUT/(stem+'-all.png'))
        seen = set()
        unique = []
        for i,record in enumerate(rows):
            identity = (record['stage'],record['key'],record['slot'])
            if identity not in seen:
                seen.add(identity); unique.append(i)
        first = Image.new('RGB',(1400,290*((len(unique)+1)//2)),'#293b40')
        for i,index in enumerate(unique): first.paste(tiles[index],((i%2)*700,(i//2)*290))
        first.save(OUT/(stem+'-distinct.png'))
        # Compact milestone board for visual review, with full chronological board linked.
        selected = []
        stages = list(dict.fromkeys(r['stage'] for r in rows))
        for stage in stages:
            indices = [i for i,r in enumerate(rows) if r['stage']==stage]
            selected.extend([indices[0],indices[len(indices)//2],indices[-1]] if len(indices)>2 else indices)
        selected = list(dict.fromkeys(selected))
        summary = Image.new('RGB',(1400,290*((len(selected)+1)//2)),'#293b40')
        for i,index in enumerate(selected): summary.paste(tiles[index],((i%2)*700,(i//2)*290))
        summary.save(OUT/(stem+'-summary.png'))
        sections.append(f'<h2>{html.escape(stem)}</h2><img src="{stem}.gif"><details><summary>Every captured pose change ({len(rows)})</summary><a href="{stem}-all.png"><img src="{stem}-all.png" loading="lazy"></a></details>')
    report['masters'] = refs
    report['runtimeContractSha256'] = hashlib.sha256(contract_path.read_bytes()).hexdigest()
    report['limits'] = 'GIF holds each pose-change capture for its measured actor-clock interval. Captures are not continuous native video. Fixed viewport crops retain full originals in output. No natural chooser/approach, other-actor traffic, owner layout, checkpoint or all-family acceptance.'
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    masters = ''.join(f'<figure><img height="220" src="../../{r["path"]}"><figcaption>{r["direction"]} original identity master</figcaption></figure>' for r in refs)
    page = '<!doctype html><meta charset="utf-8"><title>Marsh live chair lifecycle</title><style>body{background:#17212a;color:#eee;font:16px sans-serif;margin:24px}img{max-width:100%}.masters{display:flex}figure{margin:8px}a{color:#8bd}</style><h1>Marsh live chair lifecycle</h1><p>Default lounge and observation furniture, all four rotations. Prescribed reachable arrival; actual 20ms Marsh updates through sit, seated/read and rise. World and peers paused. Whole source beside pivot-registered idle; original masters below.</p><p>'+html.escape(report['limits'])+'</p><div class="masters">'+masters+'</div>'+''.join(sections)+'<p><a href="report.json">Exact sources, capture hashes and clocks</a> · <a href="../marsh-master-repair-v1/index.html">Full master repair</a></p>'
    (OUT/'index.html').write_text(page,encoding='utf-8')
    print(f"Published {len(groups)} contexts / {len(report['captures'])} captures; all current source hashes verified")

if __name__ == '__main__': main()
