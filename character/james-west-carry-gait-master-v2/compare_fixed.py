from pathlib import Path
p=Path(__file__).resolve().parent
source=(p/'compare_pair.py').read_text().replace("names=['contact-near','base','contact-far']","names=['near-feet2','base','contact-far-feet']").replace("'pair-review.json'","'fixed-pair-review.json'").replace("'paired-contact-study.png'","'paired-fixed-contact-study.png'").replace("'opposed-contact-detail.png'","'opposed-fixed-contact-detail.png'")
exec(compile(source,str(p/'compare_pair.py'),'exec'))
