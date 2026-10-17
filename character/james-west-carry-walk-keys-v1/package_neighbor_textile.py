from pathlib import Path
import sys
p=Path(__file__).resolve().parent
phase=int(sys.argv[1]);sourceversion=int(sys.argv[2]);version=int(sys.argv[3]);baseversion={1:66,3:70}[phase]
s=(p/'package_interior_detail_v77.py').read_text()
s=s.replace('interior-detail-phase2-v77',f'textile-detail-phase{phase}-v{version}').replace('master-material-phase2-v69',f'master-material-phase{phase}-v{baseversion}').replace('detail-phase2-v75',f'detail-phase{phase}-v{sourceversion}')
s=s.replace('boxes=[(134,115,148,132),(117,118,130,130),(120,151,136,163),(136,153,143,166),(123,187,136,198),(139,184,148,197)]','boxes=[(134,115,148,130),(117,118,130,130),(120,151,136,161),(136,153,143,165)]')
s=s.replace("report=dict(sourceSha256=","assert np.array_equal(candidate[165:],base[165:])\nreport=dict(kneesStrapsCalvesBootsBelow165Exact=True,sourceSha256=")
s=s.replace('{mode}-002.png',f'{{mode}}-{phase:03d}.png').replace('original stride2',f'original stride{phase}').replace('before V69',f'before V{baseversion}').replace('whole detail V75',f'whole detail V{sourceversion}').replace('interior admission V77',f'textile admission V{version}')
exec(compile(s,str(__file__),'exec'))
