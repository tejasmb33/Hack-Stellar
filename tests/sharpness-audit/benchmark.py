"""Paired native GPU timings at equal render sizes, then live adaptive FPS.
GPU time is render duration, not device-wide utilization. No mobile hardware claim.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,statistics,sys
OUT=Path(__file__).parent;BASE='http://127.0.0.1:8017';report={'fixedResolution':[],'live':[]};errors=[]
with sync_playwright() as p:
 b=p.chromium.launch(channel='chromium')
 def before(page):
  for module in ['shaders','pipeline','environment','experience']:
   page.route('**/visuals/'+module+'.js',lambda r,request,m=module:r.fulfill(body=(OUT/f'baseline-{m}.js').read_text(),content_type='text/javascript'))
 for width,height in [(1440,900),(390,844)]:
  for mode in ['before','after']:
   page=b.new_page(viewport={'width':width,'height':height});page.on('pageerror',lambda e:errors.append(str(e)))
   if mode=='before':before(page)
   page.goto(BASE+'/tests/sharpness-audit/harness.html');page.wait_for_function('window.audit')
   # Isolate shader/timer overhead at equal pixel counts; avoid async query overlap.
   result=page.evaluate('''async()=>{const gl=document.querySelector('canvas').getContext('webgl2'),ext=gl.getExtension('EXT_disjoint_timer_query_webgl2');if(!ext)return null;const samples=[];audit.render({time:12,scale:.85});for(let i=0;i<32;i++){await new Promise(requestAnimationFrame);const q=gl.createQuery();gl.beginQuery(ext.TIME_ELAPSED_EXT,q);audit.render({time:12+i*.016,scale:.85});gl.endQuery(ext.TIME_ELAPSED_EXT);while(!gl.getQueryParameter(q,gl.QUERY_RESULT_AVAILABLE))await new Promise(requestAnimationFrame);if(i>5&&!gl.getParameter(ext.GPU_DISJOINT_EXT))samples.push(gl.getQueryParameter(q,gl.QUERY_RESULT)/1e6);gl.deleteQuery(q);}const info=gl.getExtension('WEBGL_debug_renderer_info');return {samples,renderer:info?gl.getParameter(info.UNMASKED_RENDERER_WEBGL):null,error:gl.getError()};}''')
   if result:
    assert result['error']==0,result
    result['medianMs']=statistics.median(result['samples']);result['meanMs']=statistics.mean(result['samples'])
   report['fixedResolution'].append({'viewport':[width,height],'mode':mode,'scale':.85,'result':result});page.close()
 for width,height,dpr in ([] if '--fixed-only' in sys.argv else [(1440,900,1),(1920,1080,1.25),(390,844,2.75)]):
  # Alternate A/B order between profiles to expose some thermal/cadence variation.
  for mode in (['before','after'] if width!=1920 else ['after','before']):
   page=b.new_page(viewport={'width':width,'height':height},device_scale_factor=dpr);page.on('pageerror',lambda e:errors.append(str(e)))
   if mode=='before':before(page)
   page.goto(BASE);page.wait_for_function('window.__cosmos?.frames>3');page.wait_for_timeout(10000)
   a=page.evaluate('({wall:performance.now(),...__cosmos})');page.wait_for_timeout(6000);z=page.evaluate('({wall:performance.now(),...__cosmos})')
   fps=(z['frames']-a['frames'])*1000/(z['wall']-a['wall']);clock=(z['diskTime']-a['diskTime'])*1000/(z['wall']-a['wall'])
   assert fps>26 and .9<clock<1.1,(mode,width,fps,clock)
   assert page.evaluate('document.querySelector("canvas").getContext("webgl2").getError()')==0
   report['live'].append({'viewport':[width,height],'dpr':dpr,'mode':mode,'fps':fps,'clockRatio':clock,'gpuMs':z.get('gpuMs'),'resolution':z['resolution']});page.close()
 b.close()
assert not errors,errors
report.update(errors=errors,note='Native Chromium/Apple Metal; mobile viewport emulation. FPS varies with browser cadence and system load. Equal-resolution GPU timing isolates render cost; live timing includes adaptive quality.')
(OUT/('gpu-fixed-results.json' if '--fixed-only' in sys.argv else 'benchmark-results.json')).write_text(json.dumps(report,indent=2));print(json.dumps({**report,'fixedResolution':[{**r,'result':{k:v for k,v in (r['result'] or {}).items() if k!='samples'}} for r in report['fixedResolution']]},indent=2))
