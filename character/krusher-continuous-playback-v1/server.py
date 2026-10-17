from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
import os
R=Path(__file__).resolve().parents[2];H=Path(__file__).resolve().parent;O=H/os.environ.get('KRUSHER_REVIEW_RUN','playback-v10');O.mkdir(exist_ok=True);os.chdir(R)
class Handler(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
 def do_POST(self):
  name=self.path.removeprefix('/evidence/')
  if not self.path.startswith('/evidence/') or '/' in name or '..' in name:self.send_error(400);return
  data=self.rfile.read(int(self.headers['Content-Length']));(O/name).write_bytes(data);self.send_response(200);self.end_headers()
ThreadingHTTPServer(('127.0.0.1',8794),Handler).serve_forever()
