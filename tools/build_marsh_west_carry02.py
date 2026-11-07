"""Retain repeated near-support sheet without accepting an opposite cycle."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'tools/build_marsh_south_carry01.py').read_text().replace('south','west').replace('South','West').replace('carry-01','carry-02').replace('candidate-01','candidate-02').replace('exec-93058684-6a69-4380-ad91-8a7f50de23b5','exec-745a5620-51b5-4ff9-b043-1d8e78887897')
s=s.replace('Retained unselected complete four-pose cargo cycle plus neutral','Retained unselected: all four foreground near thighs lead LEFT; requested opposite half not achieved')
s=s.replace("'left-contact','left-support-passing','right-contact','right-support-passing'","'near-contact','near-passing-provisional','requested-far-contact-wrong-near','requested-far-passing-wrong-near'")
s=s.replace('Raw opposite support poses and two-hand crate support inspected','Raw all four repeat near-support geometry; crate and body concept consistent but opposite half absent')
s=s.replace("req['orderedReferences']+req['sourceFrames']","req['orderedReferences']+req['sourceFrames']+req.get('guideToolDependencies',[])")
exec(compile(s,str(Path(__file__).resolve()),'exec'),{'__file__':str(Path(__file__).resolve()),'__name__':'__main__'})
