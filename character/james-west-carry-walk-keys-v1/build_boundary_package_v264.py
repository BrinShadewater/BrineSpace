from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'package_joint_thigh_v262.py').read_text(encoding='utf-8').replace('thigh-coordinated-v262','thigh-boundaries-v264')
s=s.replace('bb=b.copy();hh=h.copy();',"if not source['edit']:mask[:]=False\n bb=b.copy();hh=h.copy();")
s=s.replace("float(np.median(luma(b[mask])))", "float(np.median(luma(b[mask]))) if mask.any() else None").replace("float(np.median(luma(bb[mask])))", "float(np.median(luma(bb[mask]))) if mask.any() else None").replace("float(np.percentile(luma(b[mask]),95))", "float(np.percentile(luma(b[mask]),95)) if mask.any() else None").replace("float(np.percentile(luma(bb[mask]),95))", "float(np.percentile(luma(bb[mask]),95)) if mask.any() else None")
(p/'package_thigh_boundaries_v264.py').write_text(s,encoding='utf-8')
