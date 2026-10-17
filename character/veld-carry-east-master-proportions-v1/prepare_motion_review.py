from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1]
script=(R/'character/veld-carry-west-master-proportions-v1/review_motion.py').read_text().replace('west','east').replace('West','East')
script=script.replace("P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-carry-east-master-proportions-v1'","BASE=Path(__file__).resolve().parent;R=BASE.parents[1];P=BASE/'paired-package-v1';O=R/'output/veld-carry-east-master-proportions-native-v2'")
start=script.index("html='''")
script=script[:start]+'''html="""<!doctype html><meta charset="utf-8"><title>Veld East paired master carry</title><style>body{background:#202a30;color:#e1e7eb;font:16px system-ui;margin:24px}img{max-width:100%}p{max-width:75ch}</style><h1>Veld East carry — master helmet pairing</h1><p>Staged correction. Actual sprite-player captures compare selected art above and candidate below at 47, 93 and 148px standing rulers. Two cycles sampled using the distance clock. Recorded captures support source and alignment review; full world motion and adoption remain pending.</p><h2>Paired sources and helmet fit</h2><img src="paired-master-contact.png"><h2>Bare engine comparison</h2><img src="bare-native-motion.apng"><h2>Helmet engine comparison</h2><img src="helmet-native-motion.apng">"""
(P/'index.html').write_text(html,encoding='utf-8')
print('4 chronological boards / 104 source-native pairs; 104 lossless decoded native frames verified')
'''
(P/'review_motion.py').write_text(script,encoding='utf-8')
