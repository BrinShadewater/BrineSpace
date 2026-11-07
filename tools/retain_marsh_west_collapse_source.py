"""Retain generated original West whole source and frozen request provenance."""
from pathlib import Path
import hashlib,json,shutil
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-west-collapse-material-v1/sources'
original=Path('C:/Users/Alex/.codex/generated_images/01a0fbf5-ac74-7c72-98e7-34736a220c96/exec-0911fb3e-1f30-4630-894e-88a1915ee5e1.png')
target=BASE/'collapse-01.raw.png';shutil.copy2(original,target)
request_path=BASE/'collapse-01.request.json';request=json.loads(request_path.read_text())
request.update(status='generated whole West source; unselected, packaging/review pending',generationId='exec-0911fb3e-1f30-4630-894e-88a1915ee5e1',originalGeneratedPath=str(original),rawSha256=hashlib.sha256(target.read_bytes()).hexdigest())
request_path.write_text(json.dumps(request,indent=2)+'\n')
print('Retained West raw source, executionID and SHA; original preserved.')
