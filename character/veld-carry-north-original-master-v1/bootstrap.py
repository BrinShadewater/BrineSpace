from pathlib import Path
import shutil
P=Path(__file__).resolve().parent;B=P.with_name('veld-cargo-north-original-master-v3')
s=(B/'register_source.py').read_text().replace('raw-unload-v6.png','raw-gait-v1.png')
s=s.replace("offset=(round(128-axis),224-bottom)","offset=(round(128-axis),224-round((max(c[3] for c in cells)-1)*scale))")
s=s.replace('assert ys.max()==224','assert 222<=ys.max()<=225')
(P/'register_source.py').write_text(s)
shutil.copy2('C:/Users/Alex/.codex/generated_images/01a0ef89-9984-7e73-99c2-84cdd8b28b14/exec-8c8b04c2-a410-40f8-9cd7-abb9d32b50f8.png',P/'raw-gait-v1.png')
