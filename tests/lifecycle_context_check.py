"""Compare the historical disposal order with recovery, without GPU instrumentation."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,sys,subprocess
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'tests/lifecycle-audit'
BASE=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8000'
old=(OUT/'baseline-experience.js').read_text();report=[]
with sync_playwright() as p:
 browser=p.chromium.launch(channel='chromium')
 for baseline in [True,False]:
  page=browser.new_page(viewport={'width':874,'height':418});messages=[];exceptions=[]
  page.on('pageerror',lambda e:exceptions.append(str(e)))
  page.on('console',lambda m:messages.append(m.text) if 'INVALID_' in m.text else None)
  if baseline:page.route('**/visuals/experience.js',lambda route:route.fulfill(body=old,content_type='text/javascript'))
  page.goto(BASE);page.wait_for_function('window.__cosmos?.frames>5')
  for cycle in range(3):
   before=page.evaluate('({...__cosmos})')
   if cycle==1:page.emulate_media(reduced_motion='reduce');page.wait_for_timeout(200)
   page.evaluate('window.gl=document.querySelector("canvas").getContext("webgl2");window.loss=gl.getExtension("WEBGL_lose_context");loss.loseContext()')
   page.wait_for_function('document.body.classList.contains("scene-unavailable")')
   page.set_viewport_size({'width':900+cycle*20,'height':440+cycle*10});page.wait_for_timeout(150);page.evaluate('loss.restoreContext()');page.wait_for_function('document.body.classList.contains("scene-ready")');page.wait_for_timeout(400)
   error=page.evaluate('gl.getError()');after=page.evaluate('({...__cosmos})')
   if baseline:assert error==1282
   else:
    assert error==0,(cycle,messages)
    assert after['diskTime']>=before['diskTime']
   if cycle==1:
    t=after['diskTime'];page.wait_for_timeout(200);assert page.evaluate('__cosmos.diskTime')==t
    page.emulate_media(reduced_motion='no-preference')
   t=page.evaluate('__cosmos.diskTime');page.wait_for_timeout(500);assert page.evaluate('__cosmos.diskTime')>t
   report.append(dict(baseline=baseline,cycle=cycle,glError=error,before=before,after=after))
  if not baseline:assert not messages and not exceptions,(messages,exceptions)
  report[-1]['invalidMessages']=messages;page.close()
 browser.close()
(OUT/'context-results.json').write_text(json.dumps(dict(status='passed',cycles=report),indent=2)+'\n')
print(json.dumps({'status':'passed','cycles':len(report),'oldErrors':[r['glError'] for r in report if r['baseline']],'currentErrors':[r['glError'] for r in report if not r['baseline']]},indent=2))
