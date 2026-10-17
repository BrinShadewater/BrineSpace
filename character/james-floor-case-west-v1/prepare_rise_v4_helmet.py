from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'package_rise_v4.gd').read_text()
for a,b in [('rise-generated-v4-bare.png','rise-generated-v4-helmet.png'),('rise-v4/bare','rise-v4/helmet'),('rise-v4-package-evidence.json','rise-v4-helmet-package-evidence.json'),('package_rise_v4.gd.uid','package_rise_v4_helmet.gd.uid'),('"gear":"bare"','"gear":"helmet"'),('bare midpoint','helmet midpoint')]:s=s.replace(a,b)
(p/'package_rise_v4_helmet.gd').write_text(s)
s=(p/'review_rise_v4.py').read_text().replace("c['gear']=='bare'","c['gear']=='helmet'").replace('rise-v4/bare','rise-v4/helmet').replace('bare-rise-v4-review.png','helmet-rise-v4-review.png').replace('rise-v4-review-evidence.json','rise-v4-helmet-review-evidence.json').replace('No helmet or native world motion acceptance.','Paired helmet source comparison; no native world motion acceptance.')
(p/'review_rise_v4_helmet.py').write_text(s)
