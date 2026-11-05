"""Disk-specific sampling regression plus repeated real-page lifecycle tests.
Requires Playwright/Pillow. Usage: python tests/ring_freeze_check.py [base-url].
The harness fixes the camera and excludes particles; texture-only cases also
freeze sky drift and remove analytic light lanes to measure filaments alone.
Accelerated ages are used only in the controlled harness, never on the live page.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageChops,ImageStat,ImageMath
import json,sys,io
ROOT=Path(__file__).resolve().parents[1];FIXTURE=ROOT/'tests/ring-audit';OUT=ROOT/'tests/lifecycle-audit/prior-regression';OUT.mkdir(parents=True,exist_ok=True);BASE=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8000'
errors=[];results={'controlled':[],'live':[]}
def change(a,b):
 r,g,blue=a.split();mask=ImageMath.unsafe_eval('convert((r>100)*(r*100>b*108)*255,"L")',r=r,b=blue)
 difference=ImageChops.difference(a,b)
 changed=ImageChops.multiply(difference.convert('L').point(lambda v:255 if v>2 else 0),mask)
 return {'meanDiskChange':sum(ImageStat.Stat(difference,mask).mean)/3,'changedFraction':changed.histogram()[255]/max(1,mask.histogram()[255])}
with sync_playwright() as p:
 browser=p.chromium.launch(channel='chromium',ignore_default_args=['--disable-back-forward-cache'])
 page=browser.new_page(viewport={'width':1280,'height':800});page.add_init_script(path=str(FIXTURE/'gpu-instrument.js'))
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
 page.goto(BASE+'/tests/ring-audit/harness.html',wait_until='networkidle');page.wait_for_function('window.audit')
 for mode in ['legacy','current']:
  for progress in [0,.5,1]:
   for age in [0,30,300,1800,7200]:
    frames=[]
    for label,offset in [('a',0),('b',2)]:
     page.evaluate('(x)=>audit.render(x)',dict(time=age+offset,progress=progress,filter=mode,textureOnly=True))
     shot=page.screenshot();frames.append(Image.open(io.BytesIO(shot)).convert('RGB'))
     if (progress,age) in [(0,0),(.5,1800),(1,300)]:
      (OUT/f'disk-{mode}-p{progress}-age{age}-{label}.png').write_bytes(shot)
    gpu=page.evaluate('readAnimationUniforms()')
    assert any(abs(g['gpu']-(age+2))<.003 for g in gpu),gpu
    measurement={'mode':mode,'progress':progress,'age':age,**change(*frames),'gpu':gpu}
    results['controlled'].append(measurement)
    if mode=='current':assert measurement['meanDiskChange']>1 and measurement['changedFraction']>.1,measurement
 legacy=next(x for x in results['controlled'] if x['mode']=='legacy' and x['progress']==1 and x['age']==300)
 fixed=next(x for x in results['controlled'] if x['mode']=='current' and x['progress']==1 and x['age']==300)
 assert legacy['meanDiskChange']<.1 and fixed['meanDiskChange']>5,(legacy,fixed)
 results['reproduced']='Moving texture becomes nearly stationary in legacy lookup while GPU time advances; stable-level lookup restores it.'
 # Same-time normal output comparison, without isolating any shader component.
 results['appearance']=[]
 for progress in [0,.5,1]:
  frames=[]
  for mode in ['legacy','current']:
   page.evaluate('(x)=>audit.render(x)',dict(time=0,progress=progress,filter=mode))
   shot=page.screenshot();frames.append(Image.open(io.BytesIO(shot)).convert('RGB'))
   if progress==0:(OUT/f'appearance-{mode}.png').write_bytes(shot)
  difference=sum(ImageStat.Stat(ImageChops.difference(*frames)).mean)/3
  assert difference<2,(progress,difference)
  results['appearance'].append({'progress':progress,'meanChannelDifference':difference})
 page.close()
 context=browser.new_context(viewport={'width':1280,'height':800},record_video_dir=str(OUT),record_video_size={'width':1280,'height':800})
 page=context.new_page();page.add_init_script(path=str(FIXTURE/'gpu-instrument.js'))
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
 def snapshot(label):
  state=page.evaluate('({...window.__cosmos})');gpu=page.evaluate('readAnimationUniforms()')
  disk=[g for g in gpu if g['role']=='disk'];dust=[g for g in gpu if g['role']=='dust']
  assert disk and dust and abs(disk[-1]['gpu']-dust[-1]['gpu'])<.001,(disk,dust)
  results['live'].append({'label':label,'state':state,'gpu':gpu});return state
 def observe(label,ms=1100):
  before=snapshot(label+'-before');page.wait_for_timeout(ms);after=snapshot(label+'-after')
  assert after['diskTime']>before['diskTime']+.3,(label,before,after)
 for run in range(3):
  page.goto(BASE,wait_until='networkidle');page.wait_for_function('window.__cosmos?.frames>3')
  observe(f'fresh-load-{run+1}-top-15s',15000)
  if run==0:
   for y in range(0,1300,60):page.evaluate('(y)=>scrollTo({top:y,behavior:"instant"})',y);page.wait_for_timeout(180)
   observe('slow-scroll-stop')
   for y in [2400,0,1800,600,3000,0,1800,0]:
    page.evaluate('(y)=>scrollTo({top:y,behavior:"instant"})',y);page.wait_for_timeout(100)
   for y in [900,1800,3000,0]:
    page.evaluate('(y)=>scrollTo({top:y,behavior:"smooth"})',y);page.wait_for_timeout(700);observe('rest-at-'+str(y))
   page.set_viewport_size({'width':1440,'height':900});observe('resize')
   page.evaluate('window.__restoreMarker="retained-home"')
   page.goto(BASE+'/problem-statements/',wait_until='networkidle');page.wait_for_function('window.__cosmos?.frames>3');observe('directory')
   page.evaluate('history.back()');page.wait_for_url(BASE+'/',wait_until='commit');page.wait_for_function('window.__cosmos?.frames>3');observe('back-home')
   results['bfcacheRestored']=page.evaluate('window.__restoreMarker==="retained-home"')
   page.emulate_media(reduced_motion='reduce');page.wait_for_timeout(200);paused=snapshot('reduced-motion');page.wait_for_timeout(400)
   assert snapshot('reduced-still')['diskTime']==paused['diskTime']
   page.emulate_media(reduced_motion='no-preference');observe('motion-resumed')
   page.screenshot(path=str(OUT/'live-after-scroll.png'))
 video=page.video;context.close();video.save_as(str(OUT/'repeated-load-scroll-navigation.webm'));video.path().unlink(missing_ok=True)
 browser.close()
assert not errors,errors
results.update(status='passed',errors=errors,limitation='Complete live clock stoppage was not reproduced. Texture-motion loss was reproduced deterministically with accelerated ages; checks cover Chromium/Metal, not every GPU/browser.')
(OUT/'fix-results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps({'status':results['status'],'reproduced':results['reproduced'],'controlledCases':len(results['controlled']),'liveCheckpoints':len(results['live']),'bfcacheRestored':results['bfcacheRestored'],'errors':errors},indent=2))
