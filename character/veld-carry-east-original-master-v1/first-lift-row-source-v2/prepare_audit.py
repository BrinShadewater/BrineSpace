from pathlib import Path
P=Path(__file__).resolve().parent
for name in ['register_source.py','audit_transition.py']:
 s=(P.parent/'first-lift-row-source-v1'/name).read_text(encoding='utf-8').replace('raw-first-lift-v1.png','raw-first-lift-v2.png')
 (P/name).write_text(s,encoding='utf-8')
print('Same whole-atlas148density/registration and independent master/foot diagnostics prepared.')
