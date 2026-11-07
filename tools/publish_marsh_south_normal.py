"""Bind normal South full checkpoint/Title Continue evidence and visual pairs."""
from pathlib import Path
import collections
import hashlib
import json
import re
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'output/marsh-animation-audit/south-normal-native-v1-2026-10-02'
VISIBLE=ROOT/'output/marsh-animation-audit/south-visible-continue-v1-2026-10-02'
UNIT=ROOT/'output/marsh-animation-audit/south-normal-regressions-v1-2026-10-02'
DEST=ROOT/'character/marsh-south-stop-v1/normal-review-v1'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    report=json.loads((RUN/'report.json').read_text())
    assert report['failures']==0 and len(report['checkpoints'])==12 and len(report['captures'])==24
    inputs=json.loads((RUN/'inputs-before.json').read_text())
    after=json.loads((RUN/'inputs-after.json').read_text())
    drift={p for p in inputs if inputs[p]!=after.get(p)}
    assert drift=={'tests/index.json'}
    # Standalone -s fixture never reads the runner index. Preserve both hashes
    # and disclose its registration/lane edit rather than claim full stability.
    stable={p:d for p,d in inputs.items() if p not in drift}
    for path,digest in inputs.items():
        if path not in drift:assert sha(ROOT/path)==after[path],path
    assert sha(RUN/'frozen-grid-source.txt')==sha(RUN/'loaded-grid-source.txt')==inputs['scripts/grid_canvas.gd']
    owner=json.loads((RUN/'owner-before.json').read_text())
    assert owner==json.loads((RUN/'owner-after.json').read_text())
    assert 'ERROR:' not in (RUN/'native.log').read_text(encoding='utf-8-sig')
    assert json.loads((UNIT/'inputs-before.json').read_text())==json.loads((UNIT/'inputs-after.json').read_text())
    assert json.loads((UNIT/'owner-before.json').read_text())==json.loads((UNIT/'owner-after.json').read_text())
    counts={}
    for name in ['test_marsh_south_start_controller','test_marsh_south_stop_controller','test_marsh_north_start_runtime','test_marsh_north_stop_controller','test_marsh_north_step_controller']:
        log=(UNIT/(name+'.log')).read_text(encoding='utf-8-sig')
        result=re.search(r'(\d+) checks,\s*0 failures',log)
        assert result and 'ERROR:' not in log,name
        counts[name]=int(result.group(1))
    repaired=json.loads((UNIT/'snapshot-repaired-inputs-before.json').read_text())
    assert repaired==json.loads((UNIT/'snapshot-repaired-inputs-after.json').read_text())
    assert {p:d for p,d in repaired.items() if p not in drift}==stable
    assert json.loads((UNIT/'snapshot-repaired-owner-before.json').read_text())==json.loads((UNIT/'snapshot-repaired-owner-after.json').read_text())
    log=(UNIT/'snapshot-repaired.log').read_text(encoding='utf-8-sig')
    assert '387 checks,0 failures' in log and 'ERROR:' not in log
    counts['test_marsh_south_snapshots']=387
    north_inputs=json.loads((UNIT/'north-production-inputs-before.json').read_text())
    assert north_inputs==json.loads((UNIT/'north-production-inputs-after.json').read_text())
    assert {p:d for p,d in north_inputs.items() if p not in drift}==stable
    assert json.loads((UNIT/'north-production-owner-before.json').read_text())==json.loads((UNIT/'north-production-owner-after.json').read_text())
    north_log=(UNIT/'north-production.log').read_text(encoding='utf-8-sig')
    assert '72 checks,0 failures' in north_log and 'ERROR:' not in north_log
    counts['test_marsh_north_production']=72
    pairs=collections.defaultdict(list)
    for cap in report['captures']:pairs[cap['case']].append(cap)
    expected={f'start-{t:.2f}' for t in [.18,.4,.7]}|{f'stop-{p}' for p in range(6)}|{'cancel-4','idle-pending-4','idle-drawn-4'}
    assert set(pairs)==expected
    for caps in pairs.values():
        assert Image.open(RUN/caps[0]['sourceFile']).convert('RGBA').tobytes()==Image.open(RUN/caps[1]['sourceFile']).convert('RGBA').tobytes()
    visible_report=json.loads((VISIBLE/'report.json').read_text())
    assert visible_report['failures']==0 and len(visible_report['captures'])==12
    visible_inputs=json.loads((VISIBLE/'inputs-before.json').read_text())
    assert visible_inputs==json.loads((VISIBLE/'inputs-after.json').read_text())
    assert json.loads((VISIBLE/'owner-before.json').read_text())==json.loads((VISIBLE/'owner-after.json').read_text())
    assert 'ERROR:' not in (VISIBLE/'native.log').read_text(encoding='utf-8-sig')
    for path,digest in visible_inputs.items():
        if path!='tools/publish_marsh_south_normal.py':assert sha(ROOT/path)==digest,path
    visible_caps={c['case']:c for c in visible_report['captures']}
    assert set(visible_caps)==expected and all(c['loadingAcknowledged'] for c in visible_caps.values())
    DEST.mkdir(exist_ok=True)
    boards=[]; enriched=[]
    for group,names in [('starts',[f'start-{t:.2f}' for t in [.18,.4,.7]]),('stops',[f'stop-{p}' for p in range(6)]),('handoffs',['cancel-4','idle-pending-4','idle-drawn-4'])]:
        native=Image.new('RGB',(300,len(names)*238),'#293b40')
        source=Image.new('RGB',(368,len(names)*220),'#293b40')
        nd,sd=ImageDraw.Draw(native),ImageDraw.Draw(source)
        for row,name in enumerate(names):
            caps=[pairs[name][0],visible_caps[name]]
            assert caps[0]['foot']==caps[1]['foot']
            a,b=[Image.open(base/c['sourceFile']).convert('RGBA') for base,c in zip([RUN,VISIBLE],caps)]
            assert a.size==b.size and a.tobytes()==b.tobytes()
            for col,(cap,pose) in enumerate(zip(caps,[a,b])):
                capture_run=RUN if col==0 else VISIBLE
                if cap['key'].startswith('walk-stop-phase'):
                    phase=int(cap['key'].split('phase')[1].split('-')[0])
                    folder=ROOT/f'character/marsh-south-stop-v1/candidate-{["06","06","06","01","07","01"][phase]}/phase-{phase}'
                else:
                    folder=ROOT/{'walk-start-south':'character/marsh-south-idle-material-v1/candidate-01/south-start','walk-south':'character/marsh-south-walk-material-v1/candidate-02','idle-south':'character/marsh-south-idle-material-v1/candidate-01'}[cap['key']]
                matching=[p for p in folder.glob('*.png') if Image.open(p).convert('RGBA').tobytes()==pose.tobytes()]
                assert matching,cap
                canonical=matching[0];canonical_key=canonical.relative_to(ROOT).as_posix()
                assert canonical_key in inputs and sha(canonical)==inputs[canonical_key]
                shot=Image.open(capture_run/cap['file']).convert('RGB').crop((400,200,550,400))
                native.paste(shot,(col*150,row*238+36));source.paste(pose,(col*184,row*220+36),pose)
                nd.text((col*150+2,row*238+2),name,fill='white');nd.text((col*150+2,row*238+18),cap['moment'],fill='white')
                sd.text((col*184+2,row*220+2),name+' '+cap['moment'],fill='white')
                enriched.append({**cap,'captureRun':capture_run.relative_to(ROOT).as_posix(),'nativeSha256':sha(capture_run/cap['file']),'sourceSha256':sha(capture_run/cap['sourceFile']),'canonicalSource':canonical_key,'canonicalSourceSha256':sha(canonical)})
        nf,sf=group+'-native.png',group+'-source.png';native.save(DEST/nf);source.save(DEST/sf);boards.append({'name':group,'native':nf,'source':sf})
    for item in report['checkpoints']:
        disk=RUN/'scratch-profile/Godot/app_userdata/BrineSpace'/item['disk'][7:]
        assert disk.is_file();item['sha256']=sha(disk);item['scratchPath']=disk.relative_to(ROOT).as_posix()
        copied=VISIBLE/'scratch-profile/Godot/app_userdata/BrineSpace'/('visible-'+item['case']+'.loop')
        assert sha(copied)==sha(disk)
    failed=[]
    for suffix,reason in [('first-freeze-failure','Stopped after prelaunch inventory failed on mistyped test name. No native acceptance.'),('first-startup-boundary','188checks/12full checkpoints/24captures/6fixture failures; pending gait/idle seeds consumed during prewarm before startup_complete. Exact source pairs passed; corrected first-observable draw assertions and retained probes.')]:
        prior=RUN.with_name(RUN.name+'-'+suffix)
        assert json.loads((prior/'owner-before.json').read_text())==json.loads((prior/'owner-after.json').read_text())
        failed.append({'path':prior.relative_to(ROOT).as_posix(),'disposition':reason,'ownerUnchanged':True,'logSha256':sha(prior/'native.log')})
    evidence={**report,'captures':enriched,'targetedInputs':inputs,'targetedInputsAfter':after,'targetedInputsStable':len(stable),'inventoryFiles':len(inputs),'inventoryMetadataChange':{'path':'tests/index.json','beforeSha256':inputs['tests/index.json'],'afterSha256':after['tests/index.json'],'reason':'Added fixture to companion tests and explicit native lane during standalone -s run; index does not drive that run.'},'loadedRendererMatchesFrozen':True,'ownerUnchanged':True,'ownerNonLogFiles':len(owner),'regressionCounts':counts,'regressionChecks':sum(counts.values()),'repairedSnapshotInputs':repaired,'nativeLogSha256':sha(RUN/'native.log'),'publisherSha256':sha(Path(__file__)),'failedIntervals':failed,'normalAdmission':True,'fullRunSaveCheckpoints':12,'freshTitleContinues':12,'exactSourcePairs':12,'boards':boards,'visualReview':'Pending three native/source board pairs. Normal integration remains provisional; known seams, support-depth settling, phase4extra lift and injury/death grade boundaries need polish.'}
    evidence.update({'nativeChecksTotal':report['checks']+visible_report['checks'],'visibleContinueChecks':visible_report['checks'],'visibleContinueInputs':visible_inputs,'visibleContinueInputsStable':len(visible_inputs),'visibleContinueScope':visible_report['scope'],'visibleContinueOwnerUnchanged':True,'visibleContinueLogSha256':sha(VISIBLE/'native.log'),'visibleContinuePublisherPreCaptureSha256':visible_inputs['tools/publish_marsh_south_normal.py'],'publisherUpdatedAfterVisibleCapture':True,'primaryCoveredNativeCapturesRetained':12,'usableNativeSourcePairs':24,'freshTitleContinuesAcrossTwoLanes':24})
    evidence['inventoryMetadataChange']['latestPostRunIndexSha256']=sha(ROOT/'tests/index.json')
    evidence['visualReview']='Pending three unoccluded native/source board pairs. Twelve loading-covered screenshots retained as rejected visual evidence; source/clock checks remain valid. Normal integration provisional: contact, recovery lift, width/detail/grade and injury/death boundaries remain.'
    (DEST/'verification.json').write_text(json.dumps(evidence,indent=2)+'\n')
    html='<meta charset="utf-8"><title>Marsh South normal Continue</title><style>body{background:#17282c;color:#e4e7dd;font:18px system-ui;max-width:1200px;margin:30px auto}img{image-rendering:pixelated;max-width:100%;vertical-align:top}</style><h1>Normal South checkpoint and Title Continue</h1><p>'+report['scope']+'</p><p>'+str(report['checks'])+' native checks;12full checkpoints;12fresh Title Continues;12exact source pairs;'+str(sum(counts.values()))+' related unit checks;'+str(len(stable))+' stable targeted inputs;'+str(len(owner))+' owner files unchanged. One inventoried test-index metadata edit is recorded separately.</p>'
    for board in boards:html+='<h2>'+board['name']+'</h2><img src="'+board['native']+'"><img src="'+board['source']+'">'
    html+='<p>'+evidence['visualReview']+'</p><a href="verification.json">Bound evidence</a>'
    html+='<p>Supplemental visible Continue: '+str(visible_report['checks'])+'checks/12fresh starts,0failures; actual loading Continue acknowledged;'+str(len(visible_inputs))+'inputs stable. Publisher revised after this capture interval. The earlier12covered screenshots are excluded from visual acceptance.</p>'
    (DEST/'index.html').write_text(html)
    print(report['checks'],'native checks;12full checkpoints/TitleContinues;24captures;',sum(counts.values()),'related unit checks;',len(stable),'stable inputs;1test-index metadata change;',len(owner),'owner files unchanged')
if __name__=='__main__':main()
