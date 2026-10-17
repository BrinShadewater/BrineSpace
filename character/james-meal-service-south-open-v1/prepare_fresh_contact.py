"""Fresh whole source projection with two native depth-order diagnostics."""
from pathlib import Path
P=Path(__file__).resolve().parent
source=(P/'prepare_deep_contact.py').read_text()
source=source.replace("deep-contact-source-v2.png","deep-contact-source-v4.png").replace('scale=.15','scale=.13').replace('anchor=(628,1082)','anchor=(614,995)')
source=source.replace('deep-contact','fresh-contact').replace('native-deep-contact','native-fresh-contact').replace('deep-captures','fresh-captures')
# The raw generation retains its original version filename.
source=source.replace('fresh-contact-source-v4.png','deep-contact-source-v4.png')
source=source.replace('skull ~140px -> 21px; shoulders ~340px -> 51px','fresh skull ~160px -> 21px; shoulders ~350px -> 46px')
source=source.replace('Whole source registered at .15','Whole fresh source registered at .13')
exec(compile(source,str(P/'prepare_fresh_contact.py'),'exec'))
fixture=(P/'native-fresh-contact.gd').read_text()
needle='last=texture'
fixture=fixture.replace(needle,'if index==3 and not texture.has_meta("contact_layer_sampled"):\n\t\t\t\ttexture.set_meta("contact_layer_sampled",true);texture.set_meta("crew_depth_offset",64.0)\n\t\t\t\tsamples.append({"index":3,"depthOffset":64,"capture":await capture("source-03-foreground",npc)})\n\t\t\t\ttexture.set_meta("crew_depth_offset",0.0)\n\t\t\t'+needle)
fixture=fixture.replace('JAMES SOUTH DEEP CONTACT DIAGNOSTIC','JAMES SOUTH FRESH CONTACT DIAGNOSTIC')
(P/'native-fresh-contact.gd').write_text(fixture)
print('Fresh source .13 at actual boot anchor; compare normal and +64 world depth.')
