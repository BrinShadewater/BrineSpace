"""Bind staged South interruption captures, keeping lifecycle and visual scopes explicit."""
from pathlib import Path
import hashlib,json,collections
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'output/marsh-animation-audit/south-start-interruptions-v1-2026-10-02'
DEST=ROOT/'character/marsh-south-walk-material-v1/interruption-review-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    r=json.loads((RUN/'report.json').read_text());assert r['failures']==0 and r['cases']==64 and len(r['captures'])==128
    inputs=json.loads((RUN/'inputs-before.json').read_text());assert inputs==json.loads((RUN/'inputs-after.json').read_text())
    for p,d in inputs.items():assert sha(ROOT/p)==d,p
    owner=json.loads((RUN/'owner-before.json').read_text());assert owner==json.loads((RUN/'owner-after.json').read_text())
    assert 'ERROR:' not in (RUN/'native.log').read_text(encoding='utf-8-sig')
    contract=json.loads((ROOT/'character/marsh-consistency-review-v1/runtime-contract.json').read_text())['states']
    groups=collections.defaultdict(list);records=[];crop=(400,200,550,400)
    DEST.mkdir(exist_ok=True)
    for cap in r['captures']:
        key=cap['key'];slot=cap['slot']
        if key=='walk-start-south':expected_path=ROOT/'character/marsh-south-walk-material-v1/candidate-02/south-start'/('%03d.png'%slot)
        elif key=='walk-south':expected_path=ROOT/'character/marsh-south-walk-material-v1/candidate-02'/('%03d.png'%slot)
        else:
            expected_path=ROOT/contract[key]['files'][slot];assert sha(expected_path)==contract[key]['hashes'][slot]
        actual=Image.open(RUN/cap['sourceFile']).convert('RGBA');expected=Image.open(expected_path).convert('RGBA')
        assert actual.size==expected.size and actual.tobytes()==expected.tobytes(),(key,slot)
        pivot=[92,172] if key in ['walk-start-south','walk-south'] else contract[key]['pivot']
        presentation=Image.new('RGBA',(184,184));presentation.alpha_composite(actual,(round(92-pivot[0]),round(172-pivot[1])))
        assert sum(a>0 for a in presentation.getchannel('A').tobytes())==sum(a>0 for a in actual.getchannel('A').tobytes()),'review presentation clipped '+key
        im=Image.open(RUN/cap['file']).convert('RGB').crop(crop)
        group=cap['work'] if cap['kind'] in ['power','suspension'] else 'hazard-'+str(cap['phase'])
        groups[group].append((cap,im,presentation));records.append({**cap,'nativeSha256':sha(RUN/cap['file']),'sourceSha256':sha(RUN/cap['sourceFile']),'sourcePath':expected_path.relative_to(ROOT).as_posix(),'sourceFileSha256':sha(expected_path),'crop':crop,'sourcePivot':pivot,'reviewPresentation':'Whole source translated to common184canvas/p92,172; no resampling or clipped alpha. Raw submitted source retained separately.'})
    previews=[]
    for index,(name,entries) in enumerate(groups.items()):
        rows=(len(entries)+7)//8;board=Image.new('RGB',(1200,rows*236),'#293b40');d=ImageDraw.Draw(board)
        sb=Image.new('RGB',(1472,rows*220),'#293b40');sd=ImageDraw.Draw(sb)
        for i,(cap,im,source) in enumerate(entries):
            x=i%8*150;y=i//8*236;board.paste(im,(x,y+36));d.text((x+2,y+2),cap['kind']+' '+cap['moment'],fill='white');d.text((x+2,y+18),f"{cap['phase']:.2f}s #{cap['slot']} {cap['goal']}",fill='white')
            x=i%8*184;y=i//8*220;sb.paste(source,(x,y+36),source);sd.text((x+2,y+2),cap['kind']+' '+cap['moment'],fill='white');sd.text((x+2,y+18),cap['key']+f' #{cap["slot"]}',fill='white')
        file=f'group-{index}-native.png';sf=f'group-{index}-source.png';board.save(DEST/file);sb.save(DEST/sf);previews.append({'name':name,'file':file,'sourceFile':sf,'captures':len(entries)})
    evidence={**r,'captures':records,'targetedInputs':inputs,'ownerNonLogFiles':len(owner),'ownerUnchanged':True,'targetedInputsUnchanged':True,'sourcePairsVerified':128,'previews':previews,'normalAdmission':False,'nativeLogSha256':sha(RUN/'native.log'),'inputFreezeScope':'39 targeted controller/preferred-bank/runtime/grade inputs. Additional normal takeover source files checked against runtime contract and exact captured RGBA at publication; not included in prelaunch39-file freeze. Not recursive world dependency inventory.'}
    evidence['visualReview']='All eight native boards and pivot-normalized source boards inspected. Source availability and dry material coherence remain; mid-step/gait4 immediate takeover to idle or fresh-facing start has no authored settling, so smooth cancellation remains open. Actual high-water rendering obscures Marsh; source selection alone cannot prove wet visibility/material acceptance. Injury/death captures show takeover entry only, not full fall/death clips.'
    (DEST/'verification.json').write_text(json.dumps(evidence,indent=2)+'\n')
    html='<!doctype html><meta charset="utf-8"><title>Marsh South start interruption study</title><style>body{background:#17282c;color:#e4e7dd;font:17px system-ui;margin:30px auto;max-width:1500px}img{max-width:100%;image-rendering:pixelated}</style><h1>South start: actual interruption boundaries</h1><p>'+str(r['checks'])+' native checks,64cases/128source-native pairs,0failures. Four clocks across32actual ordinary service power/suspension losses and32fire/flood/charge/impact/death/padded-peer/floor removals. Old goal/path cleared before actual fresh goal choice; harmless wandering in the same room and genuinely fresh zero-clock routes remain legal. No callback or old route advancement.</p><p>'+r['scope']+'</p><p>39targeted inputs stable,2931owner non-log files unchanged/scratch APPDATA. Normal takeover source files are verified against runtime contract/capturedRGBA at publication, outside prelaunch39-file freeze. This checks takeover behavior/source availability; it does not prove smooth cancellation settling, actual save/title Continue or natural traffic.</p>'
    for p in previews:html+='<h2>'+p['name']+'</h2><img src="'+p['file']+'"><img src="'+p['sourceFile']+'">'
    html+='<p>'+evidence['visualReview']+'</p><p>Whole source boards use declared pivots to translate into common184/p92,172 presentation, no resampling/clipped alpha; original submitted PNGs separately retained.</p><p><a href="verification.json">Bound evidence</a> · <a href="../motion-review-v1/index.html">Separate full gait/start study</a></p>'
    (DEST/'index.html').write_text(html);print(r['checks'],'checks;',128,'exact source/native pairs;',len(previews),'paired native/source boards;',len(owner),'owner files unchanged')
if __name__=='__main__':main()
