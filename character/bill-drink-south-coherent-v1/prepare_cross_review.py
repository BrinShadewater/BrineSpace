from pathlib import Path
P=Path(__file__).resolve().parent
s=(P.parent/'bill-drink-north-coherent-v1/build_cross_review.py').read_text(encoding='utf-8').replace('north','south').replace('Rear-held bowl and cup stay in front of torso.','Front bowl support and cup grips remain visible. Chest badges use subdued steel.')
(P/'build_cross_review.py').write_text(s,encoding='utf-8')
