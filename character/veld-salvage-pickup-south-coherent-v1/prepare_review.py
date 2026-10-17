from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[1];E=R/'character/veld-salvage-pickup-east-coherent-v1'
assert not (H/'make_review.py').exists(), 'Do not overwrite reviewed recipe'
s=(E/'make_review.py').read_text(encoding='utf-8').replace('east','south')
s=s.replace('exec-d964c453-e260-41cc-b15d-5ba2af70d1b3.png','exec-ef488ba1-55c9-4637-8566-5fa061ab42df.png')
s=s.replace('exec-3f38cbc7-0081-44f8-ac78-ae97278e3419.png','exec-1d2fa02e-99e5-4bc6-8644-60cc53e3204a.png')
s=s.replace("C/'source-v2.png'", "C/'source-v3.png'")
s=s.replace("[H/'work-source-v1.png',C/'source-v3.png']", "[H/'work-source-v1.png']")
s=s.replace('ctx.drawImage(im,120,87,75,70','ctx.drawImage(im,90,110,75,70')
(H/'make_review.py').write_text(s,encoding='utf-8')
