from pathlib import Path
P=Path(__file__).resolve().parent
s=(P/'native-routes.gd').read_text().replace('for d in ["east","south","west","north"]:', 'for d in ["north"]:').replace('route-evidence.json','north-probe-evidence.json')
(P/'native-north-probe.gd').write_text(s)
