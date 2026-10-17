"""Bound source-owned contact layering against the supported counter."""
from pathlib import Path
P=Path(__file__).resolve().parent
s=(P/'native-reach-candidate.gd').read_text()
s=s.replace('reach-captures','depth-captures').replace('native-reach-candidate','native-contact-depth')
needle='last=texture'
addition='''if index==4 and not texture.has_meta("depth_probe_sampled"):
				texture.set_meta("depth_probe_sampled",true)
				var original_depth:float=texture.get_meta("crew_depth_offset",0.0)
				for depth in [0,8,16,24,32,40,48,56,64]:
					texture.set_meta("crew_depth_offset",float(depth))
					check(npc.foot==foot and npc.direction=="south","Depth-only diagnostic preserves contact and direction")
					samples.append({"index":4,"depthOffset":depth,"capture":await capture("contact-depth-%02d"%depth,npc)})
				texture.set_meta("crew_depth_offset",original_depth)
			last=texture'''
s=s.replace(needle,addition).replace('JAMES SOUTH REACH CANDIDATE','JAMES SOUTH CONTACT DEPTH')
(P/'native-contact-depth.gd').write_text(s)
print('Nine controlled depth samples at one fixed authored contact pose.')
