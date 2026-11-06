"""Exercise quality fallbacks, low-power pixel caps, and timer disjoint recovery."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json
OUT=Path(__file__).parent;BASE='http://127.0.0.1:8017';report=[];errors=[]
with sync_playwright() as p:
 b=p.chromium.launch(channel='chromium')
 for name,setup,expected in [
  ('mobile','',2),
  ('low-memory',"Object.defineProperty(navigator,'deviceMemory',{configurable:true,value:2})",1.25),
  ('data-saving',"Object.defineProperty(navigator,'connection',{configurable:true,value:{saveData:true}})",1.25),
  ('no-GPU-timer',"const original=WebGL2RenderingContext.prototype.getExtension;WebGL2RenderingContext.prototype.getExtension=function(name){return name==='EXT_disjoint_timer_query_webgl2'?null:original.call(this,name)}",2)]:
  page=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2.75,reduced_motion='reduce');page.on('pageerror',lambda e:errors.append(str(e)));page.add_init_script(setup)
  page.goto(BASE);page.wait_for_function('window.__cosmos?.frames>0');state=page.evaluate('({...__cosmos})')
  assert state['pixelRatio']==expected and state['particles']==4000,(name,state)
  if name=='no-GPU-timer':assert state['gpuMs'] is None
  t=state['diskTime'];page.wait_for_timeout(250);assert page.evaluate('__cosmos.diskTime')==t
  page.set_viewport_size({'width':844,'height':390});page.wait_for_timeout(250)
  assert page.evaluate('__cosmos.diskTime')==t
  assert page.evaluate('document.querySelector("canvas").getContext("webgl2").getError()')==0
  report.append({'case':name,'pixelRatio':state['pixelRatio'],'reducedMotionAndResize':'passed'});page.close()
 page=b.new_page(viewport={'width':390,'height':844});page.on('pageerror',lambda e:errors.append(str(e)))
 page.add_init_script('''window.forceDisjoint=false;window.forceSlow=false;const gp=WebGL2RenderingContext.prototype.getParameter,gq=WebGL2RenderingContext.prototype.getQueryParameter;WebGL2RenderingContext.prototype.getParameter=function(p){return p===36795&&forceDisjoint?true:gp.call(this,p)};WebGL2RenderingContext.prototype.getQueryParameter=function(q,p){return p===34918&&forceSlow?100e6:gq.call(this,q,p)};''')
 page.goto(BASE);page.wait_for_function('window.__cosmos?.gpuMs>0');page.evaluate('forceDisjoint=true');page.wait_for_function('__cosmos.gpuMs===null')
 page.evaluate('forceDisjoint=false');page.wait_for_function('__cosmos.gpuMs>0');a=page.evaluate('({...__cosmos})');page.evaluate('forceSlow=true');page.wait_for_timeout(6500);z=page.evaluate('({...__cosmos})')
 assert z['resolution']['scale']<a['resolution']['scale'] and z['diskTime']>a['diskTime'],(a,z)
 assert page.evaluate('document.querySelector("canvas").getContext("webgl2").getError()')==0
 report.append({'case':'disjoint recovery / forced 100-ms GPU overload','beforeScale':a['resolution']['scale'],'afterScale':z['resolution']['scale'],'gpuMs':z['gpuMs'],'clockContinues':True});page.close();b.close()
assert not errors,errors
(OUT/'policy-results.json').write_text(json.dumps({'cases':report,'errors':errors},indent=2));print(json.dumps({'cases':report,'errors':errors},indent=2))
