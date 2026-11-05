"""Optional hardware profile with full Chromium's native graphics backend.
The standard headless-shell suite uses SwiftShader; this separate report records
actual renderer identity. It never certifies physical-phone performance.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,sys,platform
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'tests/visual-evidence'
BASE=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8000'
reports=[]
with sync_playwright() as p:
 browser=p.chromium.launch(channel='chromium')
 for width,height,dpr in [(1440,900,1),(1920,1080,1.25)]:
  page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=dpr)
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  page.goto(BASE,wait_until='networkidle');page.wait_for_function('window.__cosmos.frames>3');page.wait_for_timeout(10000)
  before=page.evaluate('({wall:performance.now(),...window.__cosmos})');page.wait_for_timeout(8000)
  after=page.evaluate('({wall:performance.now(),...window.__cosmos})')
  gpu=page.evaluate('''()=>{let gl=document.querySelector('canvas').getContext('webgl2'),ext=gl.getExtension('WEBGL_debug_renderer_info');return ext?gl.getParameter(ext.UNMASKED_RENDERER_WEBGL):gl.getParameter(gl.RENDERER)}''')
  result={'viewport':[width,height],'devicePixelRatio':dpr,'renderer':gpu,'browser':browser.version,'platform':platform.platform(),'measuredFPS':(after['frames']-before['frames'])*1000/(after['wall']-before['wall']),'clockRatio':(after['diskTime']-before['diskTime'])*1000/(after['wall']-before['wall']),'before':before,'after':after,'errors':errors}
  assert not errors,errors
  page.screenshot(path=str(OUT/f'hardware-{width}.png'))
  reports.append(result);page.close()
 context=browser.new_context(viewport={'width':1440,'height':900},record_video_dir=str(OUT),record_video_size={'width':1440,'height':900})
 page=context.new_page();page.goto(BASE,wait_until='networkidle');page.wait_for_function('window.__cosmos.frames>3')
 page.wait_for_timeout(3000);page.screenshot(path=str(OUT/'hardware-idle-a.png'))
 page.wait_for_timeout(3500);page.screenshot(path=str(OUT/'hardware-idle-b.png'))
 for y in [450,900,1350,1900,1350,900,450,0]:
  page.evaluate('(y)=>scrollTo({top:y,behavior:"smooth"})',y);page.wait_for_timeout(1600)
 video=page.video;context.close();video.save_as(str(OUT/'hardware-idle-and-flight.webm'));video.path().unlink(missing_ok=True)
 browser.close()
(OUT/'hardware-performance.json').write_text(json.dumps(reports,indent=2)+'\n')
print(json.dumps([{key:record[key] for key in ['viewport','devicePixelRatio','renderer','measuredFPS','clockRatio']} for record in reports],indent=2))
