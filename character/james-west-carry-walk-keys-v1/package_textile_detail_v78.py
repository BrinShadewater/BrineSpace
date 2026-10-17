from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'package_interior_detail_v77.py').read_text().replace('interior-detail-phase2-v77','textile-detail-phase2-v78').replace('interior admission V77','textile admission V78')
s=s.replace('boxes=[(134,115,148,132),(117,118,130,130),(120,151,136,163),(136,153,143,166),(123,187,136,198),(139,184,148,197)]','boxes=[(134,115,148,130),(117,118,130,130),(120,151,136,161),(136,153,143,165)]')
s=s.replace("report=dict(sourceSha256=","assert np.array_equal(candidate[165:],base[165:])\nreport=dict(kneesStrapsCalvesBootsBelow165Exact=True,sourceSha256=")
exec(compile(s,str(__file__),'exec'))
