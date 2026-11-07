"""Retain original generated East whole-source execution and request hash."""
from pathlib import Path
import hashlib,json,shutil
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-east-collapse-material-v1/sources'
original=Path('C:/Users/Alex/.codex/generated_images/01a0fbf5-ac74-7c72-98e7-34736a220c96/exec-a2764187-5722-4f22-9b24-cb9493e2cc87.png')
target=BASE/'collapse-01.raw.png';shutil.copy2(original,target)
request_path=BASE/'collapse-01.request.json';request=json.loads(request_path.read_text())
request.update(status='generated whole East source; unselected, packaging/review pending',generationId='exec-a2764187-5722-4f22-9b24-cb9493e2cc87',originalGeneratedPath=str(original),rawSha256=hashlib.sha256(target.read_bytes()).hexdigest())
request_path.write_text(json.dumps(request,indent=2)+'\n')
print('Retained East raw source, executionID and SHA; original preserved.')
