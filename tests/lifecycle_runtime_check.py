"""Native GPU timing and browser visibility/suspension checks; no video overhead."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,sys
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'tests/lifecycle-audit'
BASE=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8000'
report={'performance':[]};errors=[];baseline='--baseline' in sys.argv
with sync_playwright() as p:
 browser=p.chromium.launch(channel='chromium')
 for width,height,dpr in [(1440,900,1),(1920,1080,1.25)]:
  page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=dpr)
  page.on('pageerror',lambda e:errors.append(str(e)))
  if baseline:page.route('**/visuals/shaders.js',lambda route:route.fulfill(body=(OUT/'baseline-shaders.js').read_text(),content_type='text/javascript'))
  page.goto(BASE);page.wait_for_function('window.__cosmos?.frames>3');page.wait_for_timeout(10000)
  a=page.evaluate('({wall:performance.now(),...__cosmos})');page.wait_for_timeout(8000);b=page.evaluate('({wall:performance.now(),...__cosmos})')
  fps=(b['frames']-a['frames'])*1000/(b['wall']-a['wall']);clock=(b['diskTime']-a['diskTime'])*1000/(b['wall']-a['wall'])
  gpu=page.evaluate('''()=>{const gl=document.querySelector('canvas').getContext('webgl2'),ext=gl.getExtension('WEBGL_debug_renderer_info');return gl.getParameter(ext.UNMASKED_RENDERER_WEBGL)}''')
  assert fps>30 and .9<clock<1.1,(fps,clock,b['resolution'],b['samples'])
  report['performance'].append(dict(viewport=[width,height],dpr=dpr,renderer=gpu,fps=fps,clockRatio=clock,scale=b['resolution']['scale']))
  if width==1440:
   page.evaluate('window.visibilityLog=[];document.addEventListener("visibilitychange",()=>visibilityLog.push({hidden:document.hidden,time:__cosmos.diskTime}))')
   cdp=page.context.new_cdp_session(page)
   try:
    window=cdp.send('Browser.getWindowForTarget');cdp.send('Browser.setWindowBounds',{'windowId':window['windowId'],'bounds':{'windowState':'minimized'}});page.wait_for_timeout(400)
    hidden=page.evaluate('document.hidden')
    if hidden:
     a=page.evaluate('__cosmos.diskTime');page.wait_for_timeout(700);b=page.evaluate('__cosmos.diskTime');assert a==b
    cdp.send('Browser.setWindowBounds',{'windowId':window['windowId'],'bounds':{'windowState':'normal'}});page.wait_for_timeout(400)
    report['nativeHiddenTab']=hidden
   except Exception as error:report['nativeHiddenTab']=str(error)
   # If headless minimization cannot hide the document, exercise the visibility
   # handler explicitly and label that emulation instead of claiming native coverage.
   if report['nativeHiddenTab'] is not True:
    page.evaluate('Object.defineProperty(document,"hidden",{configurable:true,value:true});document.dispatchEvent(new Event("visibilitychange"))')
    page.wait_for_timeout(100);a=page.evaluate('__cosmos.diskTime');page.wait_for_timeout(700);assert page.evaluate('__cosmos.diskTime')==a
    page.evaluate('delete document.hidden;document.dispatchEvent(new Event("visibilitychange"))');report['emulatedVisibilityPause']='passed'
   a=page.evaluate('__cosmos.diskTime');page.wait_for_timeout(700);assert page.evaluate('__cosmos.diskTime')>a
   report['visibilityLog']=page.evaluate('visibilityLog');report['visibilityResume']='passed'
  page.close()
 browser.close()
assert not errors,errors
report.update(status='passed',errors=errors,browser='Chromium/Metal; not physical mobile hardware')
(OUT/('runtime-baseline.json' if baseline else 'runtime-results.json')).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
