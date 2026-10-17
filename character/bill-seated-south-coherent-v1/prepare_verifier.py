from pathlib import Path
P=Path(__file__).resolve().parent
s=(P.parent/'bill-seated-north-coherent-v1/verify.py').read_text(encoding='utf-8').replace('north','south')
s=s.replace("for source,digest in r['sources'].items():check(hashlib.sha256((P/source).read_bytes()).hexdigest()==digest,'authored source')","check(hashlib.sha256((P/r['source']).read_bytes()).hexdigest()==r['sourceSha256'],'authored source')")
s=s.replace("check(all([f['scaleX'],f['scaleY']]==(r['primaryRuler'] if f['source'].endswith('sit-v1.png') else r['interiorRuler']) for f in r['frames']),'fixed rulers by source')","check(all([f['scaleX'],f['scaleY']]==[r['scaleX'],r['scaleY']] for f in r['frames']),'fixed atlas ruler')")
s=s.replace("heads=[76]+[f['headAxis'][1] for f in r['frames']];check(all(a<=b for a,b in zip(heads,heads[1:])),'crown lowers monotonically')","heads=[76]+[f['headAxis'][1] for f in r['frames']];check(all(a<=b for a,b in zip(heads[:5],heads[1:5])) and heads[-1]<heads[-2] and heads[-1]>=heads[1],'crown lowers then straightens into seated rest')")
(P/'verify.py').write_text(s,encoding='utf-8')
s=(P.parent/'bill-seated-north-coherent-v1/build_review.py').read_text(encoding='utf-8').replace('north','south').replace('Seated idle loop and real furniture contact still pending.','South sofa base: upright seated endpoint after the forward lowering poses. Seated breathing, reading and real sofa contact still pending.')
(P/'build_review.py').write_text(s,encoding='utf-8')
