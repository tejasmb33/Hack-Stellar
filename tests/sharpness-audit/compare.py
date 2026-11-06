"""Native GPU A/B captures, supersampled reference, capped-cadence regression.
Run against the isolated preview before synchronizing the local review branch.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageChops,ImageStat
import json,io,statistics
OUT=Path(__file__).parent;BASE='http://127.0.0.1:8017';errors=[];report={'fidelity':[],'quality':[],'cadence':[]}
with sync_playwright() as p:
 browser=p.chromium.launch(channel='chromium')
 def route_before(page):
  for module in ['shaders','pipeline','environment','experience']:
   page.route('**/visuals/'+module+'.js',lambda route,request,m=module:route.fulfill(body=(OUT/f'baseline-{m}.js').read_text(),content_type='text/javascript'))
 def observe(page):
  page.on('pageerror',lambda error:errors.append(str(error)))
  page.on('console',lambda m:errors.append(m.text) if m.type=='error' or 'INVALID_' in m.text else None)
 for width,height in [(1440,900),(390,844)]:
  images={}
  for mode in ['before','after','reference']:
   page=browser.new_page(viewport={'width':width,'height':height});observe(page)
   if mode!='after':route_before(page)
   # Reference uses the approved original shader at 3x the linear pixel density.
   page.goto(BASE+'/tests/sharpness-audit/harness.html');page.wait_for_function('window.audit')
   if mode=='reference':page.evaluate('audit.setDpr(3)')
   page.evaluate('audit.render({time:12,progress:0,scale:1})')
   images[mode]=Image.open(io.BytesIO(page.screenshot())).convert('RGB')
   images[mode].save(OUT/f'{mode}-native-{width}.png');page.close()
  reference=images['reference'].resize((width,height),Image.Resampling.LANCZOS)
  # Crops cover the concentrated upper and lower arcs marked by the organizer.
  crops={'upper':(950,100,1250,330),'lower':(1050,730,1350,900)} if width==1440 else {'upper':(100,230,330,350),'lower':(130,710,360,810)}
  for name,box in crops.items():
   values={}
   strip=Image.new('RGB',((box[2]-box[0])*3,box[3]-box[1]))
   for i,mode in enumerate(['before','after','reference']):
    crop=(reference if mode=='reference' else images[mode]).crop(box)
    strip.paste(crop,(i*crop.width,0))
    if mode!='reference':
     diff=ImageChops.difference(crop,reference.crop(box));values[mode]=sum(ImageStat.Stat(diff).rms)/3
   strip.save(OUT/f'crop-{width}-{name}.png')
   report['fidelity'].append({'width':width,'region':name,'RMSETo3xOriginal':values,'improvementPercent':100*(1-values['after']/values['before'])})
 for mode in ['before','after']:
  page=browser.new_page(viewport={'width':1280,'height':800});observe(page)
  if mode=='before':route_before(page)
  # Emulate a browser delivering at most 30 animation callbacks/s while retaining
  # native GPU cost. Respect cancelAnimationFrame through the returned RAF handle.
  page.add_init_script('''(()=>{const request=window.requestAnimationFrame.bind(window),cancel=window.cancelAnimationFrame.bind(window);let id=0;const pending=new Map();window.requestAnimationFrame=callback=>{const key=++id;const start=performance.now();function tick(t){if(t-start>=30){pending.delete(key);callback(t);}else pending.set(key,request(tick));}pending.set(key,request(tick));return key;};window.cancelAnimationFrame=key=>{const handle=pending.get(key);if(handle!==undefined){cancel(handle);pending.delete(key);}};})();''')
  page.goto(BASE);page.wait_for_function('window.__cosmos?.frames>3');page.wait_for_timeout(14000)
  state=page.evaluate('({...__cosmos})');report['cadence'].append({'mode':mode,'fps':state['fps'],'resolution':state['resolution'],'gpuMs':state.get('gpuMs')})
  assert page.evaluate('document.querySelector("canvas").getContext("webgl2").getError()')==0
  page.close()
 # Compare the complete quality policy at the same camera/time/output density.
 for label,width,height,dpr,oldScale,newScale in [('capped-desktop',1280,800,1,report['cadence'][0]['resolution']['scale'],report['cadence'][1]['resolution']['scale']),('mobile',390,844,2,.72,.72)]:
  rendered={}
  for mode in ['before','after','reference']:
   page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=dpr);observe(page)
   if mode!='after':route_before(page)
   page.goto(BASE+'/tests/sharpness-audit/harness.html');page.wait_for_function('window.audit')
   density=3 if mode=='reference' else (1 if width>760 else (1.25 if mode=='before' else 2))
   scale=1 if mode=='reference' else oldScale if mode=='before' else newScale
   page.evaluate('(d)=>audit.setDpr(d)',density);page.evaluate('(s)=>audit.render({time:12,progress:0,scale:s})',scale)
   rendered[mode]=Image.open(io.BytesIO(page.screenshot())).convert('RGB');page.close()
  rendered['before'].save(OUT/f'policy-before-{label}.png');rendered['after'].save(OUT/f'policy-after-{label}.png')
  boxes={'upper':(844,89,1111,293),'lower':(933,649,1200,800)} if width>760 else {'upper':(100,230,330,350),'lower':(130,710,360,810)}
  for name,box in boxes.items():
   box=tuple(round(c*dpr) for c in box);values={};strip=Image.new('RGB',((box[2]-box[0])*3,box[3]-box[1]))
   for i,mode in enumerate(['before','after','reference']):
    crop=rendered[mode].crop(box);strip.paste(crop,(i*crop.width,0))
    if mode!='reference':values[mode]=sum(ImageStat.Stat(ImageChops.difference(crop,rendered['reference'].crop(box))).rms)/3
   strip.save(OUT/f'policy-{label}-{name}.png')
   improvement=100*(1-values['after']/values['before'])
   report['quality'].append({'profile':label,'oldScale':oldScale,'newScale':newScale,'region':name,'RMSETo3xOriginal':values,'improvementPercent':improvement})
   assert improvement>0,(label,name,improvement)
 # Actual website captures at fixed scene time, including original DOM overlays.
 for width,height,dpr in [(1440,900,1.25),(390,844,2.75)]:
  for mode in ['before','after']:
   page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=dpr,reduced_motion='reduce');observe(page)
   if mode=='before':route_before(page)
   page.goto(BASE);page.wait_for_function('window.__cosmos?.frames>0');page.wait_for_timeout(200)
   for pose in [0,.25,.6,1]:
    page.evaluate('(p)=>scrollTo({top:p*(document.querySelector("#hero").offsetTop+document.querySelector("#hero").offsetHeight)*4.8,behavior:"instant"})',pose);page.wait_for_timeout(200)
    page.screenshot(path=str(OUT/f'website-{mode}-{width}-{pose}.png'))
   page.close()
 browser.close()
assert not errors,errors
report['errors']=errors;(OUT/'comparison-results.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
