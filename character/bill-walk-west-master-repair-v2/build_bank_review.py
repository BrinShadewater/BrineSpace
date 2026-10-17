from pathlib import Path
import hashlib
import json
import re
from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
BANK = ROOT / 'character/bill-walk-west-material-v1'

freeze = json.loads((OUT/'selected-gait-freeze.json').read_text(encoding='utf-8'))
assert len(freeze) == 98
for path, sha in freeze.items():
    assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == sha, path
state = json.loads((BANK/'manifest.json').read_text(encoding='utf-8'))['states'][0]
assert state['frameCount'] == 48 and sum(state['frameDurationsMs']) == 2000

records = {}
for file in sorted(OUT.glob('generation-provenance*v2.json')):
    job = json.loads(file.read_text(encoding='utf-8'))
    if job['status'] != 'completed':
        continue
    match = re.fullmatch(r'walk-(\d{3})-material-edit-v2.png', Path(job['savedPath']).name)
    if not match:
        continue
    n = int(match.group(1))
    study = OUT/('canvas-normalized-study.png' if n == 28 else f'canvas-normalized-study-{n:03}.png')
    if not study.exists():
        continue
    assert hashlib.sha256(Path(job['savedPath']).read_bytes()).hexdigest() == job['sha256']
    assert hashlib.sha256(Path(job['originalPath']).read_bytes()).hexdigest() == job['sha256']
    assert hashlib.sha256((ROOT/job['promptFile']).read_bytes()).hexdigest() == job['promptSha256'] == job['submittedPromptSha256']
    for ref in job['references']:
        assert hashlib.sha256(Path(ref['path']).read_bytes()).hexdigest() == ref['sha256']
    review = json.loads((OUT/('review.json' if n == 28 else f'review-{n:03}.json')).read_text(encoding='utf-8'))
    records[n] = {
        'frame': n, 'study': study.name, 'generationId': job['generationId'],
        'source': str(Path(job['savedPath']).relative_to(OUT)),
        'prompt': str(Path(job['promptFile']).resolve().relative_to(OUT)),
        'sourceSha256': job['sha256'], 'studySha256': hashlib.sha256(study.read_bytes()).hexdigest(),
        'silhouetteIoU': review['silhouetteIoU'],
        'selectedBounds': review['selectedBounds'], 'editedBounds': review['editedBounds'],
        'status': 'authored_source_study_unselected'
    }
assert records
numbers = sorted(records)
cols = 6
groups = (len(numbers)+cols-1)//cols
board = Image.new('RGB', (cols*256, groups*600), (23,42,51))
draw = ImageDraw.Draw(board)
for i, n in enumerate(numbers):
    col, group = i % cols, i // cols
    old = Image.open(BANK/f'frames/bare/walk-west/{n:03}.png').convert('RGBA')
    edited = Image.open(OUT/records[n]['study']).convert('RGBA')
    assert old.size == edited.size == (256,256)
    for row, (title, im) in enumerate([('Selected',old),('Material study',edited)]):
        x, y = col*256, group*600+row*300
        draw.text((x+8,y+6), f'{title} {n:03}', fill='white')
        board.paste(im,(x,y+25),im)
board.save(OUT/'bank-overview.png')

windows = {'wrap':[47,0,1], 'early':[1,2,3], 'stride':[3,4,5,6,7], 'passing':[7,8,9,10,11], 'crossing':[11,12,13,14,15], 'firstthird':list(range(16)), 'opening':[15,16,17,18,19], 'first20':list(range(20)), 'extended':[19,20,21,22,23], 'firsthalf':list(range(24)), 'middle':list(range(23,30)), 'returning':list(range(28,33)), 'first33':list(range(33)), 'first39':list(range(39)), 'latepassing':list(range(32,39)), 'closing':list(range(38,48)), 'full48':list(range(48)), 'adjacent':[34,35]}
windows = {k:v for k,v in windows.items() if all(n in records for n in v)}
segments = {key:{'frames':nums,'holds':[state['frameDurationsMs'][n] for n in nums]} for key,nums in windows.items()}
paths = {str(n):{'old':f'/character/bill-walk-west-material-v1/frames/bare/walk-west/{n:03}.png','new':records[n]['study']} for n in numbers}
html = (OUT/'sources/context-template.html').read_text(encoding='utf-8')
html = re.sub(r'const segments=.*?;const paths=.*?;', lambda m:'const segments='+json.dumps(segments)+';const paths='+json.dumps(paths)+';',html,count=1)
labels = {'wrap':'Loop boundary','early':'Early stride','stride':'Stride','passing':'Passing step','crossing':'Crossing step','firstthird':'First 16 frames','opening':'Opening stride','first20':'First 20 frames','extended':'Extended stride','firsthalf':'First half','middle':'Middle stride','returning':'Returning step','first33':'First 33 frames','first39':'First 39 frames','latepassing':'Late passing step','closing':'Closing stride','full48':'Complete bare source sequence','adjacent':'Later passing step'}
ranges = {key: ('47 to 0 to 1' if key=='wrap' else str(nums[0])+' to '+str(nums[-1])) for key,nums in windows.items()}
options = ''.join(f'<option value="{key}">{labels[key]}: {ranges[key]}</option>' for key in windows)
html = re.sub(r'<select id="segment">.*?</select>', '<select id="segment">'+options+'</select>',html,count=1,flags=re.S)
html = html.replace('Six authored source studies',f'{len(records)} authored source studies')
html = html.replace('six-pose-context-review.png','bank-overview.png')
html = html.replace('Selected and edited frames47,0,1,28,34,35 with head closeups','Whole selected and material-study walking bank')
html = html.replace('6 of48bare phases authored',f'{len(records)} of48bare phases authored')
html = html.replace('Bill West walking continuity','Bill West walking bank review')
html = html.replace('Small head-outline changes remain at the loop boundary; this is not ready to replace the complete gait.', 'Head, collar, glove and boot continuity still need correction; source coverage does not establish a finished gait.')
(OUT/'bank.html').write_text(html,encoding='utf-8')
helmet_report=ROOT/'character/bill-walk-west-helmet-master-repair-v1/bank-assessment.json'
helmet_count=json.loads(helmet_report.read_text(encoding='utf-8'))['authoredHelmetStudies'] if helmet_report.exists() else 0
report = {
    'status':('full_bare_source_bank_continuity_and_helmet_pending_unselected' if len(records)==48 else 'authored_bank_incomplete_unselected'), 'authoredBareStudies':len(records),
    'remainingBare':48-len(records),'remainingHelmet':48-helmet_count,'helmetAuthoredSourceStudies':helmet_count,'helmetSourceBank':'character/bill-walk-west-helmet-master-repair-v1/bank-assessment.json','poses':[records[n] for n in numbers],
    'previewWindows':segments,'selectedGaitFilesUnchanged':98,
    'headMotionCorrected':False,'normalAdmission':False,'nativeAcceptance':False,
    'scope':'Own source studies only. Bounded browser windows do not prove complete gait, physical root/contact or controller handoffs.'
}
(OUT/'bank-assessment.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'sourceStudies':len(records),'remainingBare':48-len(records),'frames':numbers,'previewWindows':segments,'selectedGaitUnchanged':98}))
