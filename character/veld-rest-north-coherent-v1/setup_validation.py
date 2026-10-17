from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1];E=P.with_name('veld-rest-east-coherent-v1')
s=(E/'verify_paired.py').read_text(encoding='utf-8').replace('east','north').replace('148/517','148/468').replace('(39,35,4)','(35,33,4)')
a=s.index('original=np.array');b=s.index('for m in [bare,helm]:',a)
s=s[:a]+'''original=np.array(Image.open(P/'sources/canonical-head.png'))
check(original.shape==(35,33,4));check(sha(R/reg['nativeComponent'])==reg['nativeComponentSha256']);check(np.array_equal(original,np.array(Image.open(R/reg['nativeComponent']))))
pitch=json.loads((P/'pitch-registration.json').read_text());check(abs(pitch['fixedRuler']-33/500)<1e-12);check(sha(P/pitch['source'])==pitch['sourceSha256'])
for head in pitch['heads']:
    check(sha(P/head['file'])==head['sha256']);check(list(Image.open(P/head['file']).size)==head['size'])
    check(head['size'][0] in [32,33] and head['size'][1] in [33,34])
check([f['forwardPitchDegrees'] for f in reg['frames']]==[15,0,-35,-80,-80]);check(all(f['tiltCounterclockwise']==0 for f in reg['frames']))
'''+s[b:]
s=s.replace("'material-grade.json']","'material-grade.json','pitch-registration.json']+[h['file'] for h in pitch['heads']]")
s=s.replace("'nativeHelmet':[35,39],'closedEyeRGBPixels':15","'nativeHelmet':[33,35],'depthPitchRuler':33/500")
(P/'verify_paired.py').write_text(s,encoding='utf-8')
s=(R/'tests/test_veld_rest_west_candidate.gd').read_text(encoding='utf-8').replace('west','north').replace('WEST','NORTH')
(R/'tests/test_veld_rest_north_candidate.gd').write_text(s,encoding='utf-8')
s=(R/'tools/run_veld_rest_west_candidate.py').read_text(encoding='utf-8').replace('west','north').replace('WEST','NORTH')
(R/'tools/run_veld_rest_north_candidate.py').write_text(s,encoding='utf-8');print('North authored pitch/source and native player checks prepared.')
