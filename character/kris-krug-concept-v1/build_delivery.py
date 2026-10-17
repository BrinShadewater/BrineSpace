"""Package the requested concept sheet without changing its source artwork."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from PIL import Image, ImageDraw
import hashlib
import json

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent.parent
sheet = ROOT/'concept-03-concordance-specialist.png'
identity = json.loads((ROOT/'identity.json').read_text(encoding='utf-8'))
provenance = json.loads((ROOT/'provenance-v3.json').read_text(encoding='utf-8'))
assert hashlib.sha256(sheet.read_bytes()).hexdigest() == provenance['concept_sha256']
assert identity['title'] == 'Cognitive Concordance Specialist'
assert identity['speciality'] == 'Intent Harmonisation'
assert identity['current_sheet'] == sheet.name
board = Image.new('RGB', (800, 290), '#25292c')
draw = ImageDraw.Draw(board)
draw.text((20,16), 'KRIS KRUG - FINAL CONCEPT SCALE COMPARISON', fill='white')
draw.text((20,38), '148px standing ruler; opaque concept crops, not runtime frames.', fill='#b9c3c9')
kris = Image.open(sheet).crop((545,266,803,831)).resize((68,148), Image.Resampling.NEAREST)
krusher = Image.open(REPO/'character/krusher-concept-v1/concept-04-krusher-dom.png').crop((548,274,803,824)).resize((69,148), Image.Resampling.NEAREST)
bill_manifest = REPO/'character/crew-runtime-matte-v1/bill/manifest.json'
bill_data = json.loads(bill_manifest.read_text())
bill_state = next(s for s in bill_data['states'] if s['id']=='idle-south')
bill_source = bill_manifest.parent/bill_state['frameFiles'][0]
bill = Image.open(bill_source).convert('RGBA')
bill = bill.crop(bill.getbbox())
bill_scale = 148/float(bill_data['standingHeight'])
bill = bill.resize((round(bill.width*bill_scale),round(bill.height*bill_scale)),Image.Resampling.NEAREST)
for x,label,art in [(85,'Bill: current matte idle',bill),(340,'Krusher: concept',krusher),(600,'Kris: current sheet',kris)]:
    board.paste(art,(x,78),art if art.mode=='RGBA' else None)
    draw.text((x-40,250),label,fill='white')
draw.line((20,226,780,226),fill='#627780')
board.save(ROOT/'scale-review-v4.png')
html = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kris Krüg — character sheet</title><style>body{margin:0;background:#24282b;color:#eee;font:18px system-ui}main{max-width:1200px;margin:auto;padding:24px}img{display:block;width:100%;height:auto}p{max-width:850px;line-height:1.6;color:#c8d2d7}h1{margin-bottom:6px}a{color:#a6dbe2}blockquote{border-left:3px solid #78a4ac;padding-left:18px;color:#c8d2d7}</style><main><h1>Kris Krüg</h1><p><strong>Cognitive Concordance Specialist</strong><br>AI &amp; Robotics · Speciality: <strong>Intent Harmonisation</strong></p><img src="concept-03-concordance-specialist.png" alt="Kris Krüg character sheet: a large full-body portrait and four turnaround views, glasses, long beard, tied-back hair without a hat, charcoal asymmetric wrap pressure suit and muted cyan shoulder"><p>Kris reconciles conflicting machine directives with crew needs. He helps BRINE and the station’s autonomous systems agree on what they are trying to accomplish—and whether those objectives still serve the people living there.</p><p>His signature equipment is a link tablet and harness recorder. The asymmetric charcoal wrap suit, pale collar and muted cyan shoulder place him in AI &amp; Robotics while keeping his silhouette distinct.</p><blockquote>“He was assigned to align my objectives. We are still discussing whose.” — proposed BRINE introduction</blockquote><p><a href="concept-03-concordance-specialist.png" download>Download character sheet</a> · <a href="Kris-Krug-character-sheet.zip" download>Download review package</a></p><details><summary>Crew scale comparison</summary><img src="scale-review-v3.png" alt="Bill, Krusher and Kris compared at 148px standing height"><p>Static concept comparison. This sheet defines the character; sprite animation studies remain separate candidates. No gameplay perk is specified.</p></details></main></html>'''
(ROOT/'index.html').write_text(html,encoding='utf-8')
audit = {
    'scope':'Requested character concept sheet, like Krusher; no requested animation pack or integration',
    'requirements':{
        'name':'Kris Krüg: sheet header and identity.json',
        'reference_likeness':'Agent visual review: glasses, brown-grey beard, gold septum ring and tied-back hair retained from supplied references',
        'remove_hat':'Agent visual review: all five displayed views show uncovered hair',
        'unique_suit':'Agent visual review: asymmetric wrap, split utility skirt, diagonal recorder harness and pale collar',
        'future_sounding_alignment_role':'Exact accepted Cognitive Concordance Specialist and Intent Harmonisation header, identity and page',
        'krusher_style':'Agent visual review of current sheet and 148px comparison against Krusher concept and Bill sprite'
    },
    'sheet_sha256':hashlib.sha256(sheet.read_bytes()).hexdigest(),
    'sheet_dimensions':list(Image.open(sheet).size),
    'visual_review':'Agent reviewed current full sheet and comparison; concept delivery completed, owner visual selection remains unclaimed',
    'limitations':'Minor concept equipment differences between views; not an animation reference contract. Animation studies remain unselected and are outside this sheet delivery.',
    'source_unchanged':True,
    'bill_comparison_reference':{'manifest':bill_manifest.relative_to(REPO).as_posix(),'frame':bill_source.relative_to(REPO).as_posix(),'sha256':hashlib.sha256(bill_source.read_bytes()).hexdigest(),'standingHeight':bill_data['standingHeight'],'selection_evidence':'grid_canvas.gd loads matte pack after major-bill-v3; October 1 selected-source audit identifies the same idle-south source','supersedes':'scale-review-v3.png used old major-bill-v3/rotations/south.png'},
}
(ROOT/'delivery-audit.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False),encoding='utf-8')
html = html.replace('scale-review-v3.png','scale-review-v4.png')
(ROOT/'index.html').write_text(html,encoding='utf-8')
names=['index.html',sheet.name,'scale-review-v4.png','identity.json','README.md','provenance-v3.json','delivery-audit.json']
with ZipFile(ROOT/'Kris-Krug-character-sheet.zip','w',ZIP_DEFLATED) as bundle:
    for name in names: bundle.write(ROOT/name,name)
with ZipFile(ROOT/'Kris-Krug-character-sheet.zip') as bundle:
    assert bundle.testzip() is None and len(bundle.namelist())==len(names)
print(json.dumps({'sheet_hash_verified':True,'source_unchanged':True,'package_files':len(names),'zip_verified':True}))
