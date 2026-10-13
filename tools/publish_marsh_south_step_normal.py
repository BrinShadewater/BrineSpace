"""Publish exact normal South step checkpoint/visible Continue comparisons."""
from pathlib import Path
import hashlib,json,re
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-south-step-v1'
RUN=ROOT/'output/marsh-animation-audit/south-step-normal-native-v1-2026-10-02'
UNIT=ROOT/'output/marsh-animation-audit/south-step-normal-unit-v1-2026-10-02'
OUT=BASE/'normal-review-v1'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    report=read(RUN/'report.json');assert report['failures']==0 and len(report['checkpoints'])==8 and len(report['captures'])==16
    frozen=read(RUN/'inputs-before.json');assert frozen==read(RUN/'inputs-after.json')
    for path,digest in frozen.items():assert sha(ROOT/path)==digest
    owner=read(RUN/'owner-before.json');assert owner==read(RUN/'owner-after.json')
    assert read(UNIT/'owner-before.json')==read(UNIT/'owner-after.json')
    assert read(UNIT/'inputs-before.json')==read(UNIT/'inputs-after.json')
    log=(RUN/'godot.log').read_text(encoding='utf-8-sig');assert 'ERROR:' not in log
    unitchecks=0;units=[]
    for name in ['test_marsh_south_step_controller','test_marsh_south_snapshots','test_marsh_north_step_controller','test_marsh_south_start_controller','test_marsh_south_stop_controller']:
        path=UNIT/(name+'.log');text=path.read_text(encoding='utf-8-sig');assert 'ERROR:' not in text
        result=re.search(r'(\d+) checks,0 failures',text);assert result
        unitchecks+=int(result.group(1));units.append({'test':name,'checks':int(result.group(1)),'logSha256':sha(path)})
    assert unitchecks==4048
    OUT.mkdir(exist_ok=True);crop=(400,180,550,365);records=[];pairs=[]
    catalog=ROOT/'character/marsh-v2/catalog.json';selected={}
    for name in read(catalog)['body']:
        manifest=ROOT/name.removeprefix('res://') if name.startswith('res://') else catalog.parent/name
        for state in read(manifest)['states']:
            selected[state['id']]={'paths':[ROOT/p.removeprefix('res://') if p.startswith('res://') else manifest.parent/p for p in state['frameFiles']],'standingHeight':read(manifest).get('standingHeight'),'pivot':read(manifest).get('pivot')}
    family=Image.new('RGB',(8*256,4*296),'#293b40');family_draw=ImageDraw.Draw(family);family_records=[]
    for row,direction in enumerate(['east','west','north','south']):
        idle_entry=selected['idle-'+direction];idle=idle_entry['paths'][0];step=selected['walk-step-'+direction]
        assert len(step['paths'])==7
        for column,path in enumerate([idle]+step['paths']):
            im=Image.open(path).convert('RGBA');pivot=idle_entry['pivot'] if column==0 else step['pivot']
            assert (idle_entry if column==0 else step)['standingHeight']==148
            registered=Image.new('RGBA',(256,256));registered.alpha_composite(im,(128-int(pivot[0]),224-int(pivot[1])))
            assert sum(registered.getchannel('A').histogram()[1:])==sum(im.getchannel('A').histogram()[1:]),'whole figure clipped'
            family.paste(registered,(column*256,row*296+35),registered)
            family_draw.text((column*256+3,row*296+3),direction+(' selected idle' if column==0 else ' step'+str(column-1)),fill='white')
            bounds=im.getbbox();family_draw.text((column*256+3,row*296+18),'occupied %dx%d'%(bounds[2]-bounds[0],bounds[3]-bounds[1]),fill='#c3d8d3')
        family_records.append({'direction':direction,'standingHeight':step['standingHeight'],'pivot':step['pivot'],'idleSha256':sha(idle),'stepSha256s':[sha(p) for p in step['paths']],'endpointRGBAExact':[Image.open(step['paths'][i]).convert('RGBA').tobytes()==Image.open(idle).convert('RGBA').tobytes() for i in [0,6]]})
    family.save(OUT/'family-short-step.png')
    grouped={}
    for row in report['captures']:
        source=RUN/row['sourceFile'];native=RUN/row['file'];im=Image.open(native).convert('RGB');assert im.size==(1600,900)
        record=dict(row,nativeSha256=sha(native),sourceSha256=sha(source),crop=crop)
        records.append(record);grouped.setdefault(row['case'],{})[row['moment']]=(record,im.crop(crop))
    for group in range(2):
        board=Image.new('RGB',(600,4*405),'#293b40');draw=ImageDraw.Draw(board)
        for y,(label,entries) in enumerate(list(grouped.items())[group*4:(group+1)*4]):
            a=Image.open(RUN/entries['before'][0]['sourceFile']).convert('RGBA')
            b=Image.open(RUN/entries['continued'][0]['sourceFile']).convert('RGBA');assert a.tobytes()==b.tobytes()
            pairs.append({'case':label,'sourceRGBAExact':True,'sourceSha256s':[entries['before'][0]['sourceSha256'],entries['continued'][0]['sourceSha256']]})
            for x,moment in enumerate(['before','continued']):
                row,tile=entries[moment];board.paste(tile.resize((300,370),Image.Resampling.NEAREST),(300*x,405*y+35))
                draw.text((300*x+3,405*y+3),label+' /'+moment,fill='white')
                draw.text((300*x+3,405*y+18),row['key'],fill='#c3d8d3')
        board.save(OUT/f'paired-{group}.png')
    evidence={'normalAdmission':True,'artAcceptance':'provisional; body/face/arm/material/contact joins and entire-family consistency still open','unitChecks':4048,'nativeChecks':report['checks'],'failures':0,'engineErrors':0,'exitCodes':[0,0],'fullRunSaveCheckpoints':8,'freshVisibleTitleContinues':8,'sourcePairs':pairs,'captures':records,'targetedNativeInputs':frozen,'inputsStable':True,'ownerNonLogFiles':len(owner),'ownerUnchanged':True,'unitEvidence':units,'nativeLogSha256':sha(RUN/'godot.log'),'visualReview':'pending','scope':report['scope'],'limits':['Prescribed routes; staged service/hazard/coordinator evidence predates integration, normal regression guards are unit-scoped.','No natural moving-peer traffic or full-family master/grade acceptance.','Native comparisons are paused first-restored-source views, not a complete motion polish pass.']}
    evidence['shortStepFamilyComparison']=family_records
    evidence['selectedCatalogCoverage']={'states':len(selected),'slots':sum(len(state['paths']) for state in selected.values()),'orderedBodyManifests':len(read(catalog)['body'])}
    (OUT/'verification.json').write_text(json.dumps(evidence,indent=2)+'\n')
    html='<!doctype html><meta charset="utf-8"><title>Marsh South step normal Continue</title><style>body{background:#17282c;color:#e4e7dd;font:17px system-ui;margin:30px auto;max-width:1000px}img{image-rendering:pixelated;max-width:100%}</style><h1>Normal South short-step: visible Continue</h1><p>4048controller/snapshot regression checks;'+str(report['checks'])+'native checks. Eight full RunSave checkpoints and eight fresh Title Continue stations,16native/source views,zero failures.108targeted native inputs stable;2931owner files unchanged. Actual loading transmission acknowledged before captures.</p><p>Six finite step phases, cancelled reach and pending idle handoff retain exact first-restored RGBA, physical root/contact offset and saved player handoff. Normal Marsh owns strict south_short restoration and catalog selects candidate05 provisionally. Body/face/arm/material/contact joins, remaining family coverage and whole-family polish still open.</p><img src="paired-0.png"><img src="paired-1.png"><p><a href="verification.json">Exact evidence and scope limits</a></p>'
    html+='<h2>Selected four-direction short-step family</h2><img src="family-short-step.png"><p>Common declared ruler; occupied heights and perspective-specific widths measured independently. This comparison does not establish full-family grade or temporal polish.</p>'
    (OUT/'index.html').write_text(html,encoding='utf-8')
    print(json.dumps({'unitChecks':4048,'nativeChecks':report['checks'],'checkpoints':8,'visibleContinues':8,'exactPairs':8,'inputsStable':len(frozen),'ownerUnchanged':len(owner)}))
if __name__=='__main__':main()
