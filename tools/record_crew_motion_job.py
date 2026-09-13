"""Record one exact-prompt video job from a saved provider listing; never submit jobs."""
from pathlib import Path
import argparse
import hashlib
import json


def contains_prompt(value, prompt):
    if isinstance(value, str):
        return value.strip() == prompt
    if isinstance(value, dict):
        return any(contains_prompt(item, prompt) for item in value.values())
    if isinstance(value, list):
        return any(contains_prompt(item, prompt) for item in value)
    return False


def main(listing, prompt_path, reference_path, record_path):
    listing, prompt_path, reference_path, record_path = map(Path,
        [listing, prompt_path, reference_path, record_path])
    data = listing.read_bytes()
    jobs = json.loads(data.decode('utf-16' if data[:2] in [b'\xff\xfe', b'\xfe\xff'] else 'utf-8-sig'))
    prompt = prompt_path.read_text().strip()
    prior = json.loads(record_path.read_text()) if record_path.exists() else {}
    matches = [job for job in jobs if contains_prompt(job.get('params', {}), prompt)]
    if prior.get('jobId'):
        matches = [job for job in matches if job['id'] == prior['jobId']]
    if len(matches) != 1:
        raise ValueError(f'Expected one exact-prompt job, found {len(matches)}; inspect existing jobs before proceeding')
    job = matches[0]
    hashes = {'promptSha256': hashlib.sha256(prompt_path.read_bytes()).hexdigest(),
              'referenceSha256': hashlib.sha256(reference_path.read_bytes()).hexdigest()}
    for key, value in hashes.items():
        if prior.get(key) and prior[key] != value:
            raise ValueError(f'Preserved {key} differs from current source')
    prior.update(status=job['status'], model=job.get('job_type'), jobId=job['id'],
                 prompt=prompt_path.name, reference=reference_path.name,
                 resume='Inspect this existing job; never resubmit solely after an observation timeout.', **hashes)
    prior.setdefault('selection', 'unselected')
    if job.get('result_url'):
        prior['resultUrl'] = job['result_url']
    record_path.write_text(json.dumps(prior, indent=2)+'\n')
    print('Exact-prompt job and source hashes recorded; status:', job['status'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['listing', 'prompt', 'reference', 'record']:
        parser.add_argument(name)
    args = parser.parse_args()
    main(args.listing, args.prompt, args.reference, args.record)
