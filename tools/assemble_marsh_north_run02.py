"""Assemble complete unselected North phases without changing their pixels."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
source = (ROOT/'tools/assemble_marsh_west_run02.py').read_text()
source = source.replace('west','north').replace('West','North')
source = source.replace("names=['near-half-01-unselected/near-contact.png','near-half-01-unselected/near-passing.png','far-half-02-unselected/far-flight.png','far-half-02-unselected/far-contact.png','far-half-02-unselected/far-passing.png','near-half-01-unselected/near-flight.png']", "names=['contacts-02-unselected/left-contact.png','candidate-01/001.png','candidate-01/002.png','contacts-02-unselected/right-contact.png','passing-03-unselected/right-passing.png','candidate-01/005.png']")
source = source.replace("phases=['near-contact','near-support-passing','far-knee-flight','far-contact','far-support-passing','near-knee-flight']", "phases=['left-contact','left-support-passing','right-leading-flight','right-contact','right-support-passing','left-leading-flight']")
source = source.replace('Held-source clearer alternation/material/body; stance/contact/camera/proportions/motion and native joins pending.', 'Rear support alternates in complete source poses. Passing arms, knee/sole lift, contact projection, flight/body joins and native motion remain provisional. Bounding-box bottom is not anatomical contact proof.')
exec(compile(source,str(ROOT/'tools/assemble_marsh_north_run02.py'),'exec'), {'__file__':str(ROOT/'tools/assemble_marsh_north_run02.py'),'__name__':'__main__'})
