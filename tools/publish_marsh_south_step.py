"""Bind unselected source audition and retain explicit contact/identity defects."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw
import numpy as np
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-south-step-v1'
RUN=ROOT/'output/marsh-animation-audit/south-step-source-native-v1-2026-10-02'
DEST=BASE/'source-review-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    report=json.loads((RUN/'report.json').read_text());assert report['checks']==171 and report['failures']==0 and len(report['captures'])==7
    inputs=json.loads((RUN/'inputs-before.json').read_text());assert inputs==json.loads((RUN/'inputs-after.json').read_text())
    for p,digest in inputs.items():assert sha(ROOT/p)==digest,p
    owner=json.loads((RUN/'owner-before.json').read_text());assert owner==json.loads((RUN/'owner-after.json').read_text())
    log=(RUN/'native.log').read_text(encoding='utf-8-sig');assert '171 checks,7 captures,0 failures' in log and 'ERROR:' not in log
    DEST.mkdir(exist_ok=True)
    boards=[];enriched=[]
    for group,caps in [('early',report['captures'][:4]),('late',report['captures'][4:])]:
        board=Image.new('RGB',(940,len(caps)*338),'#293b40');draw=ImageDraw.Draw(board)
        for i,cap in enumerate(caps):
            canonical=BASE/f'candidate-03/{cap["slot"]:03d}.png'
            actual=Image.open(RUN/cap['sourceFile']).convert('RGBA');expected=Image.open(canonical).convert('RGBA')
            assert actual.size==expected.size and actual.tobytes()==expected.tobytes()
            shot=Image.open(RUN/cap['file']).convert('RGB');assert shot.size==(1200,600)
            pixels=np.array(shot);background=pixels[180,120]
            baseline_mask=np.any(pixels[188:360,128:312]!=background,axis=2)
            yy,xx=np.where(baseline_mask);baseline_height=int(yy.max()-yy.min()+1)
            assert baseline_height==148,baseline_height
            if cap['slot'] in [0,6]:
                mask=np.any(pixels[284:360,839:921]!=background,axis=2);ny,nx=np.where(mask)
                native_height=int(ny.max()-ny.min()+1);assert native_height in [65,66],native_height
            else:native_height=None
            board.paste(Image.open(RUN/cap['file']).convert('RGB').crop((100,145,1040,448)),(0,i*338+30))
            draw.text((5,i*338+4),f'slot{cap["slot"]} / {cap["elapsed"]:.2f}s / fixed anchor source playback',fill='white')
            enriched.append({**cap,'nativeSha256':sha(RUN/cap['file']),'capturedSourceSha256':sha(RUN/cap['sourceFile']),'canonicalSource':canonical.relative_to(ROOT).as_posix(),'canonicalSourceSha256':sha(canonical),'measuredBaselineNativeHeight':baseline_height,'measuredStepNeutralNativeHeight':native_height})
        path=group+'-native.png';board.save(DEST/path);boards.append(path)
    recipes={v:json.loads((BASE/f'candidate-{v}/recipe.json').read_text()) for v in ['01','02','03']}
    idle=Image.open(ROOT/'character/marsh-south-idle-material-v1/candidate-01/000.png').convert('RGBA');bbox=idle.getbbox();idle_width=bbox[2]-bbox[0]
    selection={'status':'unselected South short-step source03 is best basis; reach/closure/identity joins incomplete','normalAdmission':False,'manifest':'character/marsh-south-step-v1/candidate-03/manifest.json','authoredInteriors':4,'declaredSlots':7,'durationMs':840,'preparation':'exact selected idle1; idle0 exact endpoints','rejectedDrafts':{'01':'Wrong support-side swap at plant;63–65pixel width against58idle.','02':'Wrong lift side; recover boot rises farther rather than closing;63–64pixel width.'},'basis03':'Consistent lead/support;59–61pixel moving widths,60neutral ruler; right recovery lowers3dense pixels instead of rising.','selectedIdleWidth':idle_width,'openDefects':['Reach left sole moves only166→167dense with2dense inward drift; insufficient projected reach toward new front plane.','Plant-to-recovery left anchor79→78dense (one-pixel centroid quantization around78.5idle).','Trailing boot155→158dense closes forward3 but remains12dense behind final root-projected idle sole170; x97→95 moves inward, then jumps10.5dense to105.5idle.','Generated neutral sole spacing21dense versus27selected; moving widths1–3dense above selected; face/arm/detail/grade boundary still requires review.'],'rootPlanDense':[0,0,0,0,13,13,13],'rootPlanImplemented':False,'evidence':'character/marsh-south-step-v1/source-review-v1/verification.json','next':'Whole-figure corrections for reaching pose and final right-foot closing pose, preserving left support and selected stance/material. Then physical root/controller/native/safety/Continue; do not install current source as finished short step.'}
    (BASE/'selection.json').write_text(json.dumps(selection,indent=2)+'\n')
    prior=RUN.with_name(RUN.name+'-first-window-scale')
    assert json.loads((prior/'owner-before.json').read_text())==json.loads((prior/'owner-after.json').read_text())
    evidence={**report,'captures':enriched,'selection':selection,'recipes':recipes,'targetedInputs':inputs,'targetedInputsStable':len(inputs),'ownerNonLogFiles':len(owner),'ownerUnchanged':True,'normalAdmission':False,'nativeLogSha256':sha(RUN/'native.log'),'publisherSha256':sha(Path(__file__)),'nativeBoards':boards,'retainedInitialInterval':{'path':prior.relative_to(ROOT).as_posix(),'checks':170,'captures':7,'reason':'Project1920→1600 window scale made actual pixel rulers smaller than labels. Rejected pixel-scale evidence, retained; source-phase checks remained green. New fixture zero content_scale_size/factor1 and actual raster height measurements.','ownerUnchanged':True},'visualReview':'Pending two native chronological plates and three complete source boards. No physical movement or global art acceptance.'}
    (DEST/'verification.json').write_text(json.dumps(evidence,indent=2)+'\n')
    html='<meta charset="utf-8"><title>Marsh South short-step source study</title><style>body{background:#17282c;color:#e4e7dd;font:18px system-ui;margin:30px auto;max-width:1500px}img{max-width:100%;image-rendering:pixelated}</style><h1>South short-step source study — unselected</h1><p>'+report['scope']+'</p><p>171checks/7source-native pairs,0failures;55targeted inputs stable;2931owner files unchanged. Four complete generated interiors plus exact idle0/idle1 aliases; one neutral-ruler scale, no anatomy/grade edits. Actual148pixel baseline and65–66pixel neutral native raster measured. First downscaled interval retained.</p>'
    for v in ['01','02','03']:html+='<h2>Source'+v+'</h2><img src="../candidate-'+v+'/comparison.png">'
    for board in boards:html+='<h2>Chronological native source plate</h2><img src="'+board+'">'
    html+='<h2>Open geometry</h2><ul>'+''.join('<li>'+s+'</li>' for s in selection['openDefects'])+'</ul><p>'+evidence['visualReview']+'</p><a href="verification.json">Bound evidence</a>'
    (DEST/'index.html').write_text(html,encoding='utf-8')
    print('171native checks/7exact source-native pairs;actual148/65pixel rulers;55inputs stable;',len(owner),'owner files unchanged;source03unselected with reach/closure defects retained')
if __name__=='__main__':main()
