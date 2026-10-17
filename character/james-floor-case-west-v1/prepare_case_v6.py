from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1]
s=(p/'package_case_v5.gd').read_text().replace('v5','v6').replace('V5','V6')
s=s.replace('Vector2i(1632,964)','Vector2i(1630,965)').replace('Rect2i(527,316,577,343)','Rect2i(498,314,634,357)')
s=s.replace('43.0/569.0','43.0/626.0').replace('[1632,964]','[1630,965]').replace('[531,320,569,335]','[502,318,626,349]').replace('[527,316,577,343]','[498,314,634,357]')
s=s.replace('# Lanczos coverage reaches the crop margin; shared43/569 yields the desired\n\t# actual alpha footprint44x26, rather than a wider45x27 rounding result.','# Shared scale fits width without changing source aspect or case grade.')
(p/'package_case_v6.gd').write_text(s)
print('V6 authored hardware variant native packaging prepared.')
