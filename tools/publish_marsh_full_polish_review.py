"""Publish full-set audit findings and current source comparisons."""
from pathlib import Path
import json,re
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-full-polish-v1';OUT=ROOT/'character/marsh-consistency-review-v1'

def main():
    states=json.loads((BASE/'baseline-contract.json').read_text())['states'];selection=json.loads((BASE/'selection.json').read_text());grading=json.loads((BASE/'grading.json').read_text());review=BASE/'review';review.mkdir(exist_ok=True)
    actions=['run','sit-idle','swim','swim-carry','death-ground','eat','swim-distress','recover-air']
    for page in range(2):
        board=Image.new('RGB',(2208,4*220),'#293b40');draw=ImageDraw.Draw(board)
        for row,action in enumerate(actions[page*4:page*4+4]):
            for col,d in enumerate(('south','north','east','west')):
                key=action+'-'+d;slot=5 if action=='death-ground' else len(states[key]['files'])//2
                paths=[BASE/'original'/states['idle-'+d]['files'][0],BASE/'original'/states[key]['files'][slot],ROOT/selection['states'][key][slot]]
                for j,p in enumerate(paths):
                    im=Image.open(p).convert('RGBA');pivot=states[key]['pivot'] if j else states['idle-'+d]['pivot'];anchor=(col*552+j*184+92,row*220+196)
                    board.paste(im,(anchor[0]-round(pivot[0]),anchor[1]-round(pivot[1])),im);draw.text((col*552+j*184+4,row*220+4),action+' '+d+' '+('idle','before','graded')[j],fill='white')
        board.save(review/f'grading-{page:02}.png')
    board=Image.new('RGB',(736,230),'#293b40');draw=ImageDraw.Draw(board)
    paths=[ROOT/'character/marsh-shutdown-injury-match-v1/north-revision-01-backup/death-ground.png',ROOT/selection['states']['death-ground-north'][-1],ROOT/'character/marsh-shutdown-injury-match-v1/north-revision-01-backup/injury-ground.png',ROOT/selection['stagedFrames']['injury-ground-north'][-1]]
    for col,p in enumerate(paths):
        im=Image.open(p).convert('RGBA');board.paste(im,(col*184,24),im);draw.text((col*184+4,4),('Dry before','Dry corrected','Injury before','Injury corrected')[col],fill='white')
    board.save(review/'north-death-before-after.png')
    for action in ('death-ground','injury-ground'):
        for d in ('south','north','east','west'):
            files=selection['states'][action+'-'+d] if action=='death-ground' else selection['stagedFrames'][action+'-'+d];frames=[]
            for f in files:
                im=Image.open(ROOT/f).convert('RGBA');bg=Image.new('RGB',(240,244),'#17212a');bg.paste(im,(28,24),im);frames.append(bg)
            frames[0].save(review/(action+'-'+d+'.gif'),save_all=True,append_images=frames[1:],duration=states['death-ground-'+d]['durations'],loop=0)
    findings={
        'scope':{'runtimeStates':len(states),'frameSlots':sum(len(s['files']) for s in states.values()),'chains':25,'stagedWhiteFluidFrames':24},
        'artStyle':'Preserve fitted ivory/slate suit, muted sage shoulders, graphite gloves/boots and the existing shaded sprite finish. No global tint, outline erosion, blur, palette reduction or replacement of accepted idle/walk.',
        'colourGrading':{'changedPaths':grading['changedPaths'],'method':'Fixed family/direction ivory material gains; preserve face/hair and all pixels outside material masks. Padded copies of the same artwork receive identical grading.','fits':grading['fits']},
        'animationConsistency':'Retain authored durations, loop flags, facing/depth metadata, exact shared artwork and reversed/composed turns. Verify every loaded slot through native elapsed-time playback.',
        'perspective':'North final ground death revised to close trailing legs behind hips, with rear-view foreshortening. South/east/west final extraction now retains complete bodies crossing source grid divisions. Independent cardinal views retain right-side implant orientation.',
        'size':'Keep each original canvas, pivot and 148px standing calibration. Pose height remains anatomical; kneeling, sitting and swimming are not normalized to standing bounding boxes. Review source and 65.28px station sizes.',
        'detail':'Preserve existing spatial detail, alpha silhouettes and protected identity pixels. Keep higher-resolution raw sources and rejected anatomy for provenance. Material mapping uses the existing locked palette.',
        'limits':'Native samples verify sprite playback and scale. Existing furniture-contact evidence remains applicable because graded alpha/geometry is unchanged. Browser controls remain unverified after local navigation was rejected. Full-set owner visual acceptance remains open. Live containment injury and running are reviewed separately in marsh-gameplay-review-v1.'
    }
    (BASE/'audit.json').write_text(json.dumps(findings,indent=2)+'\n')
    page=OUT/'index.html';html=page.read_text(encoding='utf8');section='<h2>Full-set polish / September 29</h2><p>All 192 loaded states and 978 frame slots were audited across style, material colour, motion joins, perspective, scale and detail. '+str(grading['changedPaths'])+' paths received fixed material grading. North ground death now has two close trailing legs; long ground-death poses retain complete arms and boots. Timing and scale stay unchanged.</p><img style="max-width:100%" src="../marsh-full-polish-v1/review/north-death-before-after.png" alt="North ground death before and corrected"><details><summary>Material grading beside idle</summary>'
    for i in range(2):section+=f'<img style="max-width:100%" src="../marsh-full-polish-v1/review/grading-{i:02}.png" alt="Material grading comparisons">'
    section+='</details><h3>Corrected north collapse</h3><p>Dry shutdown is installed. White synthetic fluid is now used by the live nonfatal containment reaction; its recovery is shown in the gameplay review.</p><img src="../marsh-full-polish-v1/review/death-ground-north.gif" alt="Dry north shutdown"><img src="../marsh-full-polish-v1/review/injury-ground-north.gif" alt="North white-fluid injury">'
    if '<h2>Full-set polish / September 29</h2>' not in html:html=html.replace('<script>',section+'<script>',1)
    page.write_text(html,encoding='utf8')
    old=ROOT/'character/marsh-run-carry-review-v1/index.html';data=old.read_bytes()
    for action in ('death-ground','injury-ground'):
        for d in ('south','north','east','west'):
            data=data.replace(f'../marsh-shutdown-injury-match-v1/review/{action}-{d}/motion.gif'.encode(),f'../marsh-full-polish-v1/review/{action}-{d}.gif'.encode())
    old.write_bytes(data)
    for p in (page,old):
        links=re.findall(r'<(?:img|a)[^>]+(?:src|href)="([^"]+)"',p.read_bytes().decode('utf8',errors='replace'))
        assert all((p.parent/x).exists() for x in links if not x.startswith(('http','#')))
    script=re.search(r'<script>(.*?)</script>',html,re.S).group(1);(ROOT/'output/marsh-animation-audit/consistency-review-script.js').write_text(script,encoding='utf8')
    print('Full-set audit, two grading boards, north before/after and eight current shutdown/injury previews published')

if __name__=='__main__':main()
