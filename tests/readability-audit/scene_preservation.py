"""Compare actual composited backgrounds at fixed time with content hidden in QA."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageChops
import io,json
OUT=Path(__file__).parent;report=[];errors=[]
with sync_playwright() as p:
 b=p.chromium.launch(channel='chromium')
 for width,height in [(1440,900),(390,844)]:
  for path in ['/','/problem-statements/','/problem-statements/ps-01/']:
   images={};states={}
   for label,base in [('before','http://127.0.0.1:8000'),('after','http://127.0.0.1:8018')]:
    page=b.new_page(viewport={'width':width,'height':height},reduced_motion='reduce');page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto(base+path,wait_until='networkidle');page.evaluate('document.fonts.ready');page.wait_for_function('window.__cosmos?.frames>0')
    page.evaluate("document.querySelectorAll('header,main,footer,.floating-register,.skip-link').forEach(e=>e.style.visibility='hidden')")
    for y in ([0,900,2200,4300] if path=='/' else [0]):
     page.evaluate('(y)=>scrollTo({top:y,behavior:"instant"})',y);page.wait_for_timeout(150)
     # A settled static redraw gives both captures zero scroll velocity; the
     # existing dust shader otherwise retains the one-frame scroll streak.
     page.evaluate('dispatchEvent(new Event("resize"))');page.wait_for_timeout(150)
     images[label,y]=Image.open(io.BytesIO(page.screenshot())).convert('RGB');states[label,y]=page.evaluate('({...__cosmos})')
    page.close()
   for y in ([0,900,2200,4300] if path=='/' else [0]):
    diff=ImageChops.difference(images['before',y],images['after',y]);
    if diff.getbbox() is not None:
     print(json.dumps({'mismatch':[width,path,y],'before':states['before',y],'after':states['after',y],'bounds':diff.getbbox()}),flush=True)
     images['before',y].save(OUT/'scene-mismatch-before.png');images['after',y].save(OUT/'scene-mismatch-after.png')
    assert diff.getbbox() is None,(width,path,y)
    a,z=states['before',y],states['after',y]
    for key in ['camera','center','resolution','raySteps','particles']:
     assert a.get(key)==z.get(key),(width,path,y,key)
    report.append({'width':width,'path':path,'scroll':y,'pixelIdentical':True})
 b.close()
assert not errors,errors
(OUT/'scene-results.json').write_text(json.dumps({'cases':report,'errors':errors},indent=2));print(json.dumps({'cases':len(report),'pixelIdentical':True,'errors':errors}))
