"""Build source/native review sheets and a local gallery. Source PNGs are never edited."""
from pathlib import Path
import html
import json
from PIL import Image,ImageDraw,ImageFont

PACK=Path(__file__).resolve().parent
briefs=json.loads((PACK/'briefs.json').read_text())
ids=list(briefs)
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',19)
# Diagnostic contact sheets only: assembled previews do not replace source assets.
for page in range(4):
    chosen=ids[page*7:(page+1)*7]
    sheet=Image.new('RGB',(1200,len(chosen)*240),(25,34,40))
    draw=ImageDraw.Draw(sheet)
    for n,key in enumerate(chosen):
        path=PACK/'masters'/f'{key}.png'
        draw.text((16,n*240+6),key.replace('_',' ').title(),font=font,fill=(228,226,216))
        if path.exists():
            im=Image.open(path)
            im.thumbnail((1168,204),Image.Resampling.LANCZOS)
            sheet.paste(im,((1200-im.width)//2,n*240+34),im)
    sheet.save(PACK/'review'/f'source-sheet-{page+1}.png')
native=[key for key in ids if (PACK/'review'/f'{key}-q0.png').exists()]
if native:
    for page in range(4):
        chosen=native[page*7:(page+1)*7]
        sheet=Image.new('RGB',(2048,len(chosen)*536),(25,34,40))
        draw=ImageDraw.Draw(sheet)
        for n,key in enumerate(chosen):
            draw.text((12,n*536+2),key.replace('_',' ').title()+' / four native orientations',font=font,fill=(228,226,216))
            for q in range(4):
                im=Image.open(PACK/'review'/f'{key}-q{q}.png').convert('RGB')
                sheet.paste(im,(q*512,n*536+24))
        sheet.save(PACK/'review'/f'native-sheet-{page+1}.png')
cards=[]
for key,b in briefs.items():
    cards.append(f'''<article data-name="{key.replace('_',' ')}" data-department="{b['department']}"><h2>{key.replace('_',' ').title()}</h2><p class="meta">{b['department']} · {html.escape(b['function'])}</p><a href="masters/{key}.png"><img class="master" loading="lazy" src="masters/{key}.png" alt="{key.replace('_',' ')} wall master"></a><details><summary>Room views and production brief</summary><p>{html.escape(b['details'])}</p><p><a href="prompts/{key}.txt">Exact prompt</a></p><div class="views">{''.join(f'<a href="review/{key}-q{q}.png"><img loading="lazy" src="review/{key}-q{q}.png" alt="{key}, orientation {q}"></a>' for q in range(4)) if key in native else '<p>Native capture pending.</p>'}</div></details></article>''')
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BrineSpace · 28 bespoke riser walls</title><style>
:root{color-scheme:dark}*{box-sizing:border-box}body{margin:0;background:#131e24;color:#e4e2d8;font:16px/1.55 system-ui}header,nav,main{max-width:1320px;margin:auto;padding:24px}header{padding-top:48px}h1{font-size:36px;line-height:1.15;margin:10px 0}h2{font-size:20px;margin:0}p{color:#aebcbf}small{letter-spacing:.16em;color:#adbfbe}nav{position:sticky;top:0;z-index:1;background:#131e24f5;display:flex;gap:12px;align-items:center}input,select{font:inherit;padding:10px;background:#25343b;border:1px solid #4f6269;border-radius:5px;color:#eee}input{flex:1}main{display:grid;grid-template-columns:1fr 1fr;gap:18px;padding-top:0}article{border:1px solid #384a52;border-radius:8px;padding:20px;background:#1b2a31}article[hidden]{display:none}.meta{font-size:14px;margin:5px 0 12px}.master{width:100%;display:block;background:repeating-conic-gradient(#28353c 0% 25%,#223038 0% 50%) 50%/20px 20px;border-radius:4px}.views{display:grid;grid-template-columns:1fr 1fr;gap:5px}.views img{width:100%;image-rendering:pixelated}a{color:#d8b778}summary{cursor:pointer;color:#c7d1ce;margin-top:14px}details p{font-size:14px}@media(max-width:800px){main{grid-template-columns:1fr}nav{flex-wrap:wrap}h1{font-size:28px}}
</style><header><small>BRINESPACE / RISER EXPANSION</small><h1>28 rooms. Their own walls.</h1><p>Purpose-specific service fittings, restrained department materials and clear reserves for the existing windows and doors.</p><p>Original generated PNGs are preserved. Native room views show the production renderer; visual owner acceptance is pending.</p></header><nav><input id="search" aria-label="Search rooms" placeholder="Find a room…"><select id="department" aria-label="Department"><option value="">All departments</option>'''+''.join(f'<option>{d}</option>' for d in sorted({v['department'] for v in briefs.values()}))+'''</select><span id="count"></span></nav><main>'''+''.join(cards)+'''</main><script>
const search=document.querySelector('#search'),department=document.querySelector('#department'),cards=[...document.querySelectorAll('article')];function filter(){let n=0;for(const card of cards){card.hidden=!card.dataset.name.includes(search.value.toLowerCase())||(department.value&&card.dataset.department!==department.value);if(!card.hidden)n++}document.querySelector('#count').textContent=n+' / 28'}search.addEventListener('input',filter);department.addEventListener('change',filter);filter();</script></html>'''
(PACK/'index.html').write_text(page,encoding='utf-8')
print(f'Gallery: {len(ids)} rooms, {len(native)*4} native orientation images; review sheets built.')
