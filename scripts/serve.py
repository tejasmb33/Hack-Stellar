"""Serve the local site. Use --open to launch the default browser."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit
import argparse, threading, webbrowser
ROOT=Path(__file__).resolve().parents[1]
class Handler(SimpleHTTPRequestHandler):
 def do_GET(self):
  if any(part.startswith('.') for part in Path(unquote(urlsplit(self.path).path)).parts if part not in ('/', '')):
   self.send_error(404);return
  super().do_GET()
parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=8000);parser.add_argument('--open',action='store_true');args=parser.parse_args()
url=f'http://127.0.0.1:{args.port}'
try:server=ThreadingHTTPServer(('127.0.0.1',args.port),partial(Handler,directory=str(ROOT)))
except OSError as error:raise SystemExit(f'Cannot start preview: {error}. Try --port 8001.')
print(f'Ace Hackathon: {url}\nProblem Statements: {url}/problem-statements/\nPress Ctrl+C to stop.',flush=True)
if args.open:threading.Timer(.5,lambda:webbrowser.open(url)).start()
try:server.serve_forever()
except KeyboardInterrupt:print('\nPreview stopped.')
finally:server.server_close()
