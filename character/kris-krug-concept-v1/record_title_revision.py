from pathlib import Path
import hashlib
import json
from PIL import Image

root = Path(__file__).resolve().parent
source = root / 'concept-02-no-hat-unique-suit.png'
result = root / 'concept-03-concordance-specialist.png'
im = Image.open(result)
im.load()
identity = json.loads((root / 'identity.json').read_text(encoding='utf-8'))
assert identity['title'] == 'Cognitive Concordance Specialist'
assert identity['speciality'] == 'Intent Harmonisation'
assert (root / identity['current_sheet']).is_file()
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
record = {
    'tool': 'built-in image_gen',
    'generated_source': 'C:/Users/Alex/.codex/generated_images/01a10108-0cea-7ee1-8d89-586acd3a735c/exec-25cfa00c-a457-4108-ac4a-f52a1f1e4384.png',
    'reference': {'path': str(source), 'sha256': sha(source)},
    'concept_sha256': sha(result),
    'prompt_file': 'revision-03-title-prompt.txt',
    'dimensions': list(im.size),
    'mode': im.mode,
    'review': 'Agent visually reviewed full sheet: exact selected name, title and speciality rendered; no hat, wrap suit and five complete views retained. Generated edit does not certify byte-exact body preservation.',
    'owner_role_acceptance': '2026-10-03',
    'owner_visual_acceptance': 'pending',
}
(root / 'provenance-v3.json').write_text(json.dumps(record, indent=2), encoding='utf-8')
print('Revision PNG decoded; accepted title/speciality and current-sheet reference verified; provenance saved.')
