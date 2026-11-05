"""Real, unaccelerated navigation/scroll lifecycle and composited frame checks.
Controlled layer-specific motion is covered independently by lifecycle_layers_check.
Usage: python tests/lifecycle_navigation_check.py [base-url].
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageChops,ImageStat
import io,json,sys
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'tests/lifecycle-audit'
BASE=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8000'
errors=[];report={'profiles':[]};record='--no-video' not in sys.argv
with sync_playwright() as p:
 browser=p.chromium.launch(channel='chromium',ignore_default_args=['--disable-back-forward-cache'])
 for profile,width,height in [('desktop',1280,800),('mobile',390,844)]:
  context=browser.new_context(viewport={'width':width,'height':height},is_mobile=profile=='mobile',has_touch=profile=='mobile',**({'record_video_dir':str(OUT),'record_video_size':{'width':width,'height':height}} if record else {}))
  context.add_init_script(path=str(ROOT/'tests/ring-audit/gpu-instrument.js'))
  context.add_init_script("""(()=>{const original=requestAnimationFrame;let last=-1;window.__loopAudit={callbacks:0,duplicates:0};window.requestAnimationFrame=function(callback){if(!callback.toString().includes('pipeline.render'))return original(callback);return original(t=>{__loopAudit.callbacks++;if(t===last)__loopAudit.duplicates++;last=t;callback(t);});};})();""")
  page=context.new_page();data={'profile':profile,'observations':[],'scrollCycles':0,'freshLoads':0};report['profiles'].append(data)
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('console',lambda m:errors.append(m.text) if m.type=='error' or (m.type=='warning' and 'INVALID_' in m.text) else None)
  def ready():page.wait_for_function('window.__cosmos?.frames>3&&!window.__cosmos.paused')
  def state():
   result=page.evaluate('({wall:performance.now(),scroll:scrollY,hidden:document.hidden,...window.__cosmos,gpu:readAnimationUniforms(),loop:window.__loopAudit,glError:document.querySelector("canvas").getContext("webgl2").getError()})')
   assert not result['glError'],result
   assert not result['loop']['duplicates'],result
   disk=[g for g in result['gpu'] if g['role']=='disk'];dust=[g for g in result['gpu'] if g['role']=='dust']
   assert disk and dust and abs(disk[-1]['gpu']-dust[-1]['gpu'])<.002,result
   assert result['sceneOpacity']==1 and result['holeVisible'],result
   return result
  def observe(label,ms=1300,save=False):
   a=state();shot_a=page.screenshot();page.wait_for_timeout(ms);shot_b=page.screenshot();b=state()
   clock=(b['diskTime']-a['diskTime'])*1000/(b['wall']-a['wall'])
   difference=sum(ImageStat.Stat(ImageChops.difference(Image.open(io.BytesIO(shot_a)).convert('RGB'),Image.open(io.BytesIO(shot_b)).convert('RGB'))).mean)/3
   assert .7<clock<1.3,(label,clock)
   assert difference>.015,(label,difference)
   data['observations'].append(dict(label=label,before=a,after=b,clockRatio=clock,visibleFrameChange=difference))
   if save:
    (OUT/f'{profile}-{label}-a.png').write_bytes(shot_a);(OUT/f'{profile}-{label}-b.png').write_bytes(shot_b)
  def scroll(y,wait=300):
   page.evaluate('(y)=>scrollTo({top:y,behavior:"instant"})',y);page.wait_for_timeout(wait)
  for run in range(3):
   page.goto(BASE+'/',wait_until='networkidle');ready();data['freshLoads']+=1
   observe('fresh-'+str(run+1),15000 if run==0 else 1400,run==0)
   journey=page.evaluate('(document.querySelector("#hero").offsetTop+document.querySelector("#hero").offsetHeight)*4.8')
   bottom=page.evaluate('document.documentElement.scrollHeight-innerHeight')
   if run==0:
    for y in range(0,int(bottom),180):scroll(y,35)
    scroll(bottom);observe('bottom',save=True)
    for progress in [1,.875,.75,.625,.5,.375,.25,.125,0]:
     scroll(min(bottom,journey*progress),700);observe('rest-'+str(progress),save=progress in [1,.5,0])
    data['scrollCycles']+=1
    for y in [bottom,0,bottom*.7,180,journey*.4,bottom,journey*.9,0,bottom,0]:scroll(y,80)
    observe('irregular-return');data['scrollCycles']+=2
    for size in ([{'width':1440,'height':900},{'width':874,'height':418}] if profile=='desktop' else [{'width':844,'height':390},{'width':390,'height':844}]):
     page.set_viewport_size(size);scroll(journey*.5,800);observe('resize-'+str(size['width']))
    # Actual BFCache where supported: marker distinguishes restore from reload.
    page.evaluate('window.__restoreMarker="home-retained"')
    page.goto(BASE+'/problem-statements/',wait_until='networkidle');ready();observe('directory-top',save=True)
    directory_bottom=page.evaluate('document.documentElement.scrollHeight-innerHeight')
    for y in [directory_bottom*.3,directory_bottom,directory_bottom*.6,0]:scroll(y,250)
    observe('directory-return');page.evaluate('window.__restoreMarker="directory-retained"')
    for action,path,marker in [('back','/','home-retained'),('forward','/problem-statements/','directory-retained'),('back','/','home-retained')]:
     page.evaluate('history.'+action+'()');page.wait_for_url(BASE+path,wait_until='commit');ready();observe(action+'-'+marker)
     data[action+'-'+marker+'-bfcache']=page.evaluate('(m)=>window.__restoreMarker===m',marker)
    page.emulate_media(reduced_motion='reduce');page.wait_for_timeout(250);t=page.evaluate('__cosmos.diskTime');scroll(0);page.wait_for_timeout(250)
    assert page.evaluate('__cosmos.diskTime')==t
    page.emulate_media(reduced_motion='no-preference');observe('reduced-resume')
    # Browser lifecycle suspension; record whether native visibility changed.
    cdp=context.new_cdp_session(page);before=state();cdp.send('Page.setWebLifecycleState',{'state':'frozen'});page.wait_for_timeout(700);cdp.send('Page.setWebLifecycleState',{'state':'active'});ready()
    data['suspension']={'before':before,'after':state()};observe('lifecycle-resume')
    scroll(journey*.5,700)
    page.evaluate('window.__loss=document.querySelector("canvas").getContext("webgl2").getExtension("WEBGL_lose_context");__loss.loseContext()')
    page.wait_for_function('document.body.classList.contains("scene-unavailable")');page.evaluate('__loss.restoreContext()')
    page.wait_for_function('document.body.classList.contains("scene-ready")');ready();page.wait_for_timeout(1100);observe('context-restored',save=True)
   else:
    for y in [bottom,0,journey*.5,bottom*.8,0]:scroll(y,120)
    observe('repeat-return-'+str(run));data['scrollCycles']+=1
  data['final']=state()
  video=page.video;context.close()
  if video:video.save_as(str(OUT/f'{profile}-lifecycle.webm'));video.path().unlink(missing_ok=True)
 browser.close()
assert not errors,errors
report.update(status='passed',errors=errors,note='Native Chromium/Metal; mobile viewport emulation, not physical phone/Safari. Layer isolation is in the separate controlled test.')
(OUT/'navigation-results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':report['status'],'profiles':[{'profile':d['profile'],'freshLoads':d['freshLoads'],'scrollCycles':d['scrollCycles'],'observations':len(d['observations']),'bfcache':{k:v for k,v in d.items() if k.endswith('bfcache')}} for d in report['profiles']],'errors':errors},indent=2))
