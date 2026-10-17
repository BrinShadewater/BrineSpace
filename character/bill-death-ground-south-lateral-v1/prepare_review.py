from pathlib import Path
P=Path(__file__).resolve().parent
s=(P.parent/'bill-death-ground-north-lateral-v1/build_review.py').read_text(encoding='utf-8').replace('north','south')
(P/'build_review.py').write_text(s,encoding='utf-8')
print('Prepared paired south finite preview and native crop review')
