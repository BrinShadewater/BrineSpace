from pathlib import Path
P=Path(__file__).resolve().parent
s=(P.parent/'bill-drink-north-coherent-v1/build_cross_review.py').read_text(encoding='utf-8').replace('north','west')
s=s.replace('Rear-held bowl and cup stay in front of torso.','West-facing bowl, spoon and cup use independent authored poses.')
s=s.replace(".write_text(html)",".write_text(html,encoding='utf-8')")
(P/'build_cross_review.py').write_text(s,encoding='utf-8')
