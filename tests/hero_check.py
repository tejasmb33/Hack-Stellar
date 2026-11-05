"""Live idle/scroll recording and wall-clock regression, with measured renderer identity.
Usage: python tests/hero_check.py [base-url]. Requires Playwright and Pillow.
Visual captures require human inspection; pixel change alone cannot prove visual quality.
"""
from playwright.sync_api import sync_playwright
from pathlib import Path
import json,time
ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'tests/visual-evidence'
out.mkdir(exist_ok=True)
import sys
BASE=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8000'
with sync_playwright() as p:
 browser=p.chromium.launch(args=['--enable-unsafe-swiftshader'])
 context=browser.new_context(viewport={'width':1280,'height':800},record_video_dir=str(out),record_video_size={'width':1280,'height':800})
 page=context.new_page();errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
 page.goto(BASE,wait_until='networkidle');page.wait_for_function('window.__cosmos.frames>3')
 page.wait_for_timeout(9000)
 before=page.evaluate('({wall:performance.now(),...window.__cosmos})')
 page.screenshot(path=str(out/'idle-a.png'))
 page.wait_for_timeout(3500)
 page.screenshot(path=str(out/'idle-b.png'))
 after=page.evaluate('({wall:performance.now(),...window.__cosmos})')
 for y in [500,1000,1500,1000,500,0]:
  page.evaluate('(y)=>scrollTo({top:y,behavior:"smooth"})',y);page.wait_for_timeout(2000)
  if y in [500,1500]:page.screenshot(path=str(out/f'journey-{y}.png'))
 state=page.evaluate('({...window.__cosmos})')
 gpu=page.evaluate('''()=>{const gl=document.querySelector('canvas').getContext('webgl2');const ext=gl.getExtension('WEBGL_debug_renderer_info');return {renderer:gl.getParameter(ext.UNMASKED_RENDERER_WEBGL),vendor:gl.getParameter(ext.UNMASKED_VENDOR_WEBGL)}}''')
 report={'environment':gpu,'viewport':[1280,800],'before':before,'after':after,'measuredFPS':(after['frames']-before['frames'])/((after['wall']-before['wall'])/1000),'clockRatio':(after['diskTime']-before['diskTime'])/((after['wall']-before['wall'])/1000),'errors':errors,'lastState':state}
 video=page.video
 context.close();video.save_as(str(out/'idle-and-flight.webm'))
 video.path().unlink(missing_ok=True)
 browser.close()
 assert not errors,errors
 assert .88<report['clockRatio']<1.12,report['clockRatio']
 from PIL import Image,ImageChops,ImageStat
 a=Image.open(out/'idle-a.png').convert('RGB').crop((650,180,1240,740))
 b=Image.open(out/'idle-b.png').convert('RGB').crop((650,180,1240,740))
 report['diskRegionMeanPixelChange']=sum(ImageStat.Stat(ImageChops.difference(a,b)).mean)/3
 assert report['diskRegionMeanPixelChange']>1,report['diskRegionMeanPixelChange']
 (out/'desktop-performance.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
