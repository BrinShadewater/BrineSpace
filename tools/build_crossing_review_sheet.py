"""Arrange unscaled native doorway crops for human review; never certify art."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw

def build(index, output, crop):
    rows = json.loads(index.read_text(encoding="utf-8"))
    if not rows or output.exists():
        raise ValueError("Require populated index and new output directory")
    left, top, right, bottom = crop
    if min(left, top) < 0 or right <= left or bottom <= top:
        raise ValueError("Invalid crop bounds")
    width, height = right-left, bottom-top
    frames = []
    root = index.parent.resolve()
    for row in rows:
        source = (root / row["file"]).resolve()
        if not source.is_relative_to(root):
            raise ValueError("Frame path escapes capture directory")
        with Image.open(source) as frame:
            if right > frame.width or bottom > frame.height:
                raise ValueError("Crop exceeds native frame")
            frames.append(frame.crop(crop).convert("RGB"))
    output.mkdir(parents=True)
    sheets = []
    for start in range(0, len(rows), 42):
        subset = rows[start:start+42]
        sheet = Image.new("RGB", (width*7, (height+24)*((len(subset)+6)//7)), "#142027")
        draw = ImageDraw.Draw(sheet)
        for offset, row in enumerate(subset):
            x, y = offset%7*width, offset//7*(height+24)
            sheet.paste(frames[start+offset], (x,y))
            label = "p%s q%s %s" % (row.get("canonical_port","?"),row["rotation"],row["requested_fraction"])
            draw.text((x+2,y+height+2),label,fill="white")
        path = output / ("page-%d.png" % (len(sheets)+1))
        sheet.save(path)
        sheets.append({"file":path.name,"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),"first_frame":start,"frames":len(subset)})
    (output / "index.json").write_text(json.dumps({"source_index":str(index.resolve()),"source_index_sha256":hashlib.sha256(index.read_bytes()).hexdigest(),"crop_xyxy":crop,"resized":False,"reviewed":False,"frames":len(rows),"sheets":sheets},indent=2)+"\n",encoding="utf-8")
    print("%d frames arranged in %d sheets; visual review required." % (len(rows),len(sheets)))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("index",type=Path)
    parser.add_argument("output",type=Path)
    parser.add_argument("--crop",type=int,nargs=4,required=True,metavar=("LEFT","TOP","RIGHT","BOTTOM"))
    args = parser.parse_args()
    build(args.index,args.output,args.crop)
