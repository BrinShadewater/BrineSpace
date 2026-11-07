"""Retain five complete own-East figures; repeated support remains unselected."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'tools/build_marsh_south_carry01.py').read_text().replace('south','east').replace('South','East').replace('exec-93058684-6a69-4380-ad91-8a7f50de23b5','exec-3a8c9230-d3ae-4fe6-b221-ab3ee9bcec81')
source=source.replace("req['orderedReferences']+req['sourceFrames']","req['orderedReferences']+req['sourceFrames']+req.get('guideToolDependencies',[])")
source=source.replace('Retained unselected complete four-pose cargo cycle plus neutral','Retained unselected: all four poses repeat near-leading/support halves')
source=source.replace("'left-contact','left-support-passing','right-contact','right-support-passing'","'near-contact','near-support-passing','requested-far-contact-wrong-near','requested-far-passing-wrong-near'")
source=source.replace('Raw opposite support poses and two-hand crate support inspected','Raw consistent crate support/material inspected; requested far-contact/passing repeat near support')
exec(compile(source,str(ROOT/'tools/build_marsh_east_carry01.py'),'exec'),{'__file__':str(ROOT/'tools/build_marsh_east_carry01.py'),'__name__':'__main__'})
