"""Normal selected family + full saves and visible Continue source comparisons."""
from pathlib import Path
import hashlib,json,shutil
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-west-injury-material-v1'
RUN=ROOT/'output/marsh-animation-audit/west-damage-normal-native-v1-2026-10-02'
OUT=BASE/'normal-review-v1'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def resolve(manifest,path):return ROOT/path.removeprefix('res://') if path.startswith('res://') else manifest.parent/path

def main():
    report=read(RUN/'report.json')
    assert report['failures']==0 and len(report['checkpoints'])==20 and len(report['captures'])==40
    assert (RUN/'native-exit.txt').read_text().strip()=='0' and 'ERROR:' not in (RUN/'native.log').read_text()
    inputs=read(RUN/'inputs-before.json');assert inputs==read(RUN/'inputs-after.json')
    for path,digest in inputs.items():assert sha(ROOT/path)==digest,'post-run input drift '+path
    owner=read(RUN/'owner-before.json');assert owner==read(RUN/'owner-after.json')
    catalog=ROOT/'character/marsh-v2/catalog.json';selected={}
    body=read(catalog)['body']
    assert body[-2:]==['../marsh-west-collapse-material-v1/candidate-02/manifest.json','../marsh-west-injury-material-v1/candidate-01/manifest.json']
    for name in body:
        manifest=resolve(catalog,name);data=read(manifest)
        for state in data['states']:
            selected[state['id']]={'paths':[resolve(manifest,p) for p in state['frameFiles']],'standingHeight':data.get('standingHeight'),'pivot':data.get('pivot'),'manifest':manifest}
    OUT.mkdir(exist_ok=True);grouped={};records=[]
    for row in report['captures']:
        source=Image.open(RUN/row['sourceFile']).convert('RGBA');entry=selected[row['key']]
        matches=[i for i,path in enumerate(entry['paths']) if source.tobytes()==Image.open(path).convert('RGBA').tobytes()]
        assert matches,'native source does not match normal selected manifest'
        native=Image.open(RUN/row['file']).convert('RGB');width,height=row['designSize']
        assert width>0 and height>0
        x=round(row['canvasPosition'][0]*native.width/width);y=round(row['canvasPosition'][1]*native.height/height)
        cropbox=(x-100,y-110,x+110,y+30)
        assert 0<=cropbox[0]<cropbox[2]<=native.width and 0<=cropbox[1]<cropbox[3]<=native.height
        crop=native.crop(cropbox);record=dict(row,matchedSlot=matches[0],sourceSha256=sha(RUN/row['sourceFile']),nativeSha256=sha(RUN/row['file']),crop=list(cropbox))
        records.append(record);grouped.setdefault(row['case'],{})[row['moment']]=(record,source,crop)
        for key in ['file','sourceFile']:shutil.copy2(RUN/row[key],OUT/row[key])
    pairs=[]
    for group in range(4):
        board=Image.new('RGB',(650,5*230),'#293b40');draw=ImageDraw.Draw(board)
        for row,(label,entries) in enumerate(list(grouped.items())[group*5:group*5+5]):
            before,a,acrop=entries['before'];continued,b,bcrop=entries['continued']
            assert a.tobytes()==b.tobytes() and before['foot']==continued['foot'] and before['key']==continued['key']
            board.paste(a,(0,row*230+35),a);board.paste(acrop,(205,row*230+65));board.paste(bcrop,(430,row*230+65))
            draw.text((4,row*230+5),label+' / '+before['key']+' slot'+str(before['matchedSlot']),fill='white')
            draw.text((4,row*230+22),'Source H148 / original native / visible Continued native',fill='#b1d5c6')
            pairs.append({'case':label,'sourceRGBAExact':True,'key':before['key'],'slot':before['matchedSlot'],'footExact':True,'sourceSha256s':[before['sourceSha256'],continued['sourceSha256']]})
        board.save(OUT/f'paired-{group}.png')
    family_records=[]
    for action in ['death-ground','injury-ground','injury-rise']:
        board=Image.new('RGB',(7*256,4*296),'#293b40');draw=ImageDraw.Draw(board)
        for row,direction in enumerate(['east','west','north','south']):
            idle=selected['idle-'+direction];entry=selected[action+'-'+direction]
            assert len(entry['paths'])==6 and idle['standingHeight']==148 and entry['standingHeight']==148
            bounds=[]
            for col,(path,metadata) in enumerate([(idle['paths'][0],idle)]+[(p,entry) for p in entry['paths']]):
                image=Image.open(path).convert('RGBA');pivot=metadata['pivot']
                registered=Image.new('RGBA',(256,256));registered.alpha_composite(image,(128-int(pivot[0]),224-int(pivot[1])))
                assert sum(registered.getchannel('A').histogram()[1:])==sum(image.getchannel('A').histogram()[1:]),'whole family figure clipped'
                board.paste(registered,(col*256,row*296+35),registered)
                draw.text((col*256+3,row*296+3),direction+(' idle' if col==0 else ' '+action+str(col-1)),fill='white')
                b=image.getbbox();bounds.append(b)
                draw.text((col*256+3,row*296+18),'occupied%dx%d'%(b[2]-b[0],b[3]-b[1]),fill='#c3d8d3')
            family_records.append({'action':action,'direction':direction,'manifest':entry['manifest'].relative_to(ROOT).as_posix(),'bounds':bounds,'sourceSha256s':[sha(p) for p in entry['paths']]})
        board.save(OUT/f'family-{action}.png')
    evidence={'checks':report['checks'],'failures':0,'exitCode':0,'engineErrors':0,'fullCheckpoints':20,'freshVisibleTitleContinues':20,'nativeSourceCaptures':40,'exactOriginalContinuedPairs':20,'stableBoundedInputs':len(inputs),'unchangedOwnerNonLogFiles':len(owner),'normalAdmission':True,'artStatus':'Provisional improved West whole-body material. Other-facing master/material joins and full moving/master family polish open.','normalCatalog':{'bodyManifests':len(body),'selectedStates':len(selected),'selectedSlots':sum(len(e['paths']) for e in selected.values())},'scope':report['scope'],'pairs':pairs,'records':records,'familyReview':family_records,'nativeVisualReview':False,'familyVisualReview':False,'limits':'Not natural traffic, realtime/browser moving review, articulated limb contact or whole-family acceptance. Bounded input freeze excludes unrelated loaded catalog art and tests/index.json metadata added after launch.'}
    assessment=OUT/'visual-assessment.json'
    if assessment.exists():
        assessed=read(assessment);evidence['nativeVisualReview']=assessed['allTwentyPairsInspected'];evidence['familyVisualReview']=assessed['allThreeFacingFamilyBoardsInspected']
    (OUT/'verification.json').write_text(json.dumps(evidence,indent=2)+'\n')
    (OUT/'index.html').write_text('''<!doctype html><meta charset="utf-8"><title>Marsh West normal damage family Continue</title><style>body{background:#182b30;color:#dae8e2;font:16px system-ui;max-width:1500px;margin:25px auto}img{max-width:100%;image-rendering:pixelated}</style><h1>Marsh West normal damage material and full Continue</h1><p>Provisional normal selection: improved dry shutdown, white-fluid injury and complete recovery. Twenty full checkpoints/fresh visible Title Continues; forty native/source views. Whole actor/playback/source/root parity, pause, settled death and fresh idle completion. Full-family motion/material acceptance remains open.</p><p><a href="verification.json">Detailed scoped evidence</a></p>'''+''.join(f'<img src="paired-{i}.png">' for i in range(4))+''.join(f'<h2>{action} — selected four facings, common148 density</h2><img src="family-{action}.png">' for action in ['death-ground','injury-ground','injury-rise']),encoding='utf-8')
    print(json.dumps({k:evidence[k] for k in ['checks','fullCheckpoints','freshVisibleTitleContinues','nativeSourceCaptures','exactOriginalContinuedPairs','stableBoundedInputs','unchangedOwnerNonLogFiles','normalCatalog','normalAdmission']}))
if __name__=='__main__':main()
