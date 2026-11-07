"""Direct Hailuo I2V: explicit single submission, resumable polling and download.

Key comes only from MINIMAX_API_KEY. Never retry a paid POST automatically.
Docs: https://platform.minimax.io/docs/api-reference/video-generation-i2v
"""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import sys
from datetime import datetime, timezone

import requests
from PIL import Image

API = "https://api.minimax.io/v1/"


def api(path, payload=None, params=None):
    key = os.environ.get("MINIMAX_API_KEY", "").strip()
    if not key:
        raise RuntimeError("MINIMAX_API_KEY is missing")
    try:
        r = requests.request("POST" if payload is not None else "GET", API + path,
                             headers={"Authorization": "Bearer " + key},
                             json=payload, params=params, timeout=90,
                             allow_redirects=False)
        data = r.json()
    except (requests.RequestException, ValueError):
        raise RuntimeError("API transport/JSON error; submission may have reached server. Do not blindly resubmit.") from None
    status = data.get("base_resp", {})
    if r.status_code != 200 or status.get("status_code") != 0:
        msg = str(status.get("status_msg", "Unrecognized response")).replace(key, "[REDACTED]")
        raise RuntimeError(f"HTTP {r.status_code}; API {status.get('status_code')}: {msg}")
    return data


def save(path, data):
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def submit(args):
    raw = args.image.read_bytes()
    if len(raw) >= 20 * 1024 * 1024:
        raise RuntimeError("Image must be smaller than 20 MB")
    with Image.open(args.image) as im:
        w, h = im.size
        mime = Image.MIME.get(im.format)
    if min(w, h) <= 300 or not .4 <= w / h <= 2.5 or mime not in ("image/png", "image/jpeg", "image/webp"):
        raise RuntimeError("Unsupported image format or dimensions")
    last_image = getattr(args, "last_image", None)
    last_raw = None
    if last_image is not None:
        last_raw = last_image.read_bytes()
        if len(last_raw) >= 20 * 1024 * 1024:
            raise RuntimeError("End image must be smaller than 20 MB")
        with Image.open(last_image) as im:
            last_mime = Image.MIME.get(im.format)
            if im.size != (w, h) or last_mime not in ("image/png", "image/jpeg", "image/webp"):
                raise RuntimeError("End image must match first image dimensions and supported format")
    prompt = args.prompt_file.read_text(encoding="utf-8-sig").strip()
    if not 1 <= len(prompt) <= 2000:
        raise RuntimeError("Prompt must be 1-2000 characters")
    args.output.mkdir(parents=True, exist_ok=True)
    state = args.output / "generation.json"
    model = "MiniMax-Hailuo-02" if last_raw is not None else "MiniMax-Hailuo-2.3-Fast"
    estimate = .28 if last_raw is not None else .19
    payload = dict(model=model, duration=6,
                   resolution="768P", prompt_optimizer=False, prompt=prompt)
    record = dict(provider="MiniMax direct", createdAt=datetime.now(timezone.utc).isoformat(),
                  params=payload.copy(), image=str(args.image.resolve()),
                  imageSha256=hashlib.sha256(raw).hexdigest(),
                  estimatedUSD=estimate, status="submission_started")
    if last_raw is not None:
        record.update(lastImage=str(last_image.resolve()),
                      lastImageSha256=hashlib.sha256(last_raw).hexdigest())
    # Exclusive ledger prevents duplicate charges, including ambiguous transport failures.
    with state.open("x", encoding="utf-8") as f:
        json.dump(record, f, indent=2)
    payload["first_frame_image"] = "data:" + mime + ";base64," + base64.b64encode(raw).decode()
    if last_raw is not None:
        payload["last_frame_image"] = "data:" + last_mime + ";base64," + base64.b64encode(last_raw).decode()
    try:
        response = api("video_generation", payload)
    except RuntimeError as exc:
        record.update(status="submission_error", error=str(exc))
        save(state, record)
        raise
    record.update(task_id=response["task_id"], status="submitted")
    save(state, record)
    print(json.dumps({"task_id": record["task_id"], "estimatedUSD": estimate}))


def poll(args):
    state = args.output / "generation.json"
    record = json.loads(state.read_text(encoding="utf-8"))
    if "task_id" not in record:
        raise RuntimeError("No task ID; inspect submission error before proceeding")
    result = api("query/video_generation", params={"task_id": record["task_id"]})
    record["status"] = result["status"]
    record["file_id"] = result.get("file_id")
    save(state, record)
    print("Task status:", record["status"])
    if record["status"].lower() == "success" and not (args.output / "source.mp4").exists():
        info = api("files/retrieve", params={"file_id": record["file_id"]})
        url = info["file"]["download_url"]
        if not url.startswith("https://"):
            raise RuntimeError("Download URL must use HTTPS")
        # CDN receives no API authorization header. Signed URL never persisted/logged.
        with requests.get(url, stream=True, timeout=90) as r:
            r.raise_for_status()
            partial = args.output / "source.mp4.part"
            with partial.open("wb") as f:
                for chunk in r.iter_content(1024 * 1024):
                    f.write(chunk)
        partial.replace(args.output / "source.mp4")
        print("Saved source.mp4")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("check", help="Read-only authentication check; no generation")
    s = sub.add_parser("submit", help="Submit ONE paid 6s/768p generation; optional end image uses Hailuo02")
    s.add_argument("--image", type=Path, required=True)
    s.add_argument("--last-image", type=Path, help="Exact end pose; Hailuo02, estimated USD0.28")
    s.add_argument("--prompt-file", type=Path, required=True)
    s.add_argument("--output", type=Path, required=True)
    q = sub.add_parser("poll", help="Query once and download if finished; never submits")
    q.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    if args.command == "check":
        api("files/list", params={"purpose": "video_generation_input"})
        print("Authentication succeeded (read-only check).")
    elif args.command == "submit":
        submit(args)
    else:
        poll(args)


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, OSError, requests.RequestException) as exc:
        # Never print HTTP objects, headers, signed URLs or key-bearing tracebacks.
        print(str(exc) if isinstance(exc, RuntimeError) else type(exc).__name__, file=sys.stderr)
        sys.exit(1)
