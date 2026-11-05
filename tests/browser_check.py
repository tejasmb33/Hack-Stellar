"""Run with Playwright against the local server at port 8000."""
from pathlib import Path
import json,re,time
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
ARTIFACTS=ROOT/'tests'/'screenshots';ARTIFACTS.mkdir(exist_ok=True)
checks=[];errors=[]
with sync_playwright() as p:
 browser=p.chromium.launch(args=['--enable-unsafe-swiftshader'])
 def page_at(width=1440,height=900,**options):
  page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1,**options)
  page.on('pageerror',lambda error:errors.append(str(error)))
  page.on('console',lambda message:errors.append(message.text) if message.type=='error' else None)
  return page
 page=page_at()
 page.goto('http://127.0.0.1:8000',wait_until='networkidle')
 page.wait_for_function('window.__cosmos && window.__cosmos.frames > 5')
 before=page.evaluate('({...window.__cosmos})');page.wait_for_timeout(600);after=page.evaluate('({...window.__cosmos})')
 assert after['frames']>before['frames'] and after['earthRotation']>before['earthRotation']
 assert after['cloudRotation']-before['cloudRotation']>after['earthRotation']-before['earthRotation']
 assert after['triangles']>10000 and after['drawCalls']>=4
 checks.append('Actual WebGL geometry, independent Earth/cloud animation and multiple draw calls verified')
 assert page.locator('.site-header').evaluate('(e)=>getComputedStyle(e).position')=='relative'
 assert page.locator('#hero-register').bounding_box()['y']<900
 assert page.locator('.floating-register').is_hidden()
 assert page.locator('#hero-register').get_attribute('href')==page.locator('.floating-register').get_attribute('href')
 page.screenshot(path=str(ARTIFACTS/'desktop-home.png'),full_page=True)
 for image in page.locator('img').all():
  image.scroll_into_view_if_needed();page.wait_for_timeout(40)
  assert image.evaluate('(e)=>e.complete && e.naturalWidth > 0')
 page.locator('#affiliations').scroll_into_view_if_needed();page.wait_for_timeout(900)
 assert page.locator('.site-header').bounding_box()['y']<0
 assert page.evaluate('window.__cosmos.orbitOpacity')>0
 assert page.evaluate('window.__cosmos.cameraZ')>before['cameraZ']
 page.screenshot(path=str(ARTIFACTS/'desktop-orbit.png'))
 checks.append('Header scrolls away; camera and 3D orbital field evolve with scroll; logos load')
 page.evaluate('scrollTo(0, 850)');page.wait_for_timeout(600)
 assert page.locator('.floating-register').is_visible()
 page.locator('#registration').scroll_into_view_if_needed();page.wait_for_timeout(600)
 assert page.locator('.floating-register').is_hidden()
 page.locator('#faq summary').first.click()
 assert page.locator('#faq details').first.get_attribute('open') is not None
 page.locator('#signal').scroll_into_view_if_needed();page.locator('#signal').click()
 assert 'SOS' in page.locator('#signal-message').inner_text()
 page.locator('#time-note').click();assert 'Proper time' in page.locator('#time-message').inner_text()
 checks.append('Floating registration visibility, FAQ and both subtle Easter eggs work')
 page.goto('http://127.0.0.1:8000/problem-statements/',wait_until='networkidle')
 assert page.locator('.problem-card').count()==3
 assert '03' in page.locator('.published-count').inner_text()
 assert page.locator('#source').count()==0
 page.locator('#search').fill('PS-02')
 assert page.locator('.problem-card:visible').count()==1
 assert 'Inventory' in page.locator('.problem-card:visible h2').inner_text()
 page.locator('#search').fill('zz-no-matching-statement')
 assert page.locator('#empty').is_visible()
 page.locator('#empty-reset').click()
 assert page.locator('.problem-card:visible').count()==3
 page.locator('#category').select_option('Voice AI')
 assert page.locator('.problem-card:visible').count()==1
 page.locator('#reset').click()
 assert page.locator('.problem-card:visible').count()==3
 page.evaluate('document.activeElement.blur(); scrollTo({top:0,behavior:"instant"})');page.wait_for_timeout(100)
 page.screenshot(path=str(ARTIFACTS/'desktop-directory.png'),full_page=True)
 for i in range(1,4):
  page.goto(f'http://127.0.0.1:8000/problem-statements/ps-{i:02d}/',wait_until='networkidle')
  assert page.locator('.brief-content h2').count()==4
  assert 'Expected Outcome' in page.locator('.brief-content').inner_text()
  assert 'Note:' in page.locator('.brief-content').inner_text()
  assert 'Contributor to be announced' in page.locator('.brief-meta').inner_text()
  if i==3:assert 'qualified personnel' in page.locator('.brief-content').inner_text()
 page.screenshot(path=str(ARTIFACTS/'desktop-brief.png'),full_page=True)
 page.get_by_role('link',name='← Back to directory').click();assert page.url.endswith('/problem-statements/')
 page.get_by_role('link',name='← Back to Home').first.click();assert page.url.endswith(':8000/')
 checks.append('Dedicated directory, PS-number search, keyword search, categories, counts, reset and all full briefs work')
 for width,height in [(320,700),(390,844),(768,1024),(1280,720),(1440,900)]:
  layout=page_at(width,height,is_mobile=width<600,has_touch=width<600)
  for path in ['/','/problem-statements/','/problem-statements/ps-03/']:
   layout.goto('http://127.0.0.1:8000'+path,wait_until='networkidle')
   assert layout.evaluate('document.documentElement.scrollWidth <= innerWidth'),f'overflow at {width} {path}'
   if path=='/':
    rect=layout.locator('#hero-register').bounding_box();assert rect['y']+rect['height']<height,f'hero CTA below fold at {width}'
   if width==390:
    filename={'/':'mobile-home.png','/problem-statements/':'mobile-directory.png','/problem-statements/ps-03/':'mobile-brief.png'}[path]
    layout.screenshot(path=str(ARTIFACTS/filename),full_page=True)
  layout.close()
 checks.append('All pages fit 320, 390, 768, 1280 and 1440px viewports; hero CTA fits first screen')
 reduced=page_at(reduced_motion='reduce')
 reduced.goto('http://127.0.0.1:8000',wait_until='networkidle');reduced.wait_for_timeout(300)
 a=reduced.evaluate('({...window.__cosmos})');reduced.wait_for_timeout(500);b=reduced.evaluate('({...window.__cosmos})')
 assert a['earthRotation']==b['earthRotation'] and b['paused']
 reduced.evaluate('scrollTo(0,1000)');reduced.wait_for_timeout(200)
 assert reduced.evaluate('window.__cosmos.earthRotation')==a['earthRotation']
 nojs=page_at(java_script_enabled=False)
 nojs.goto('http://127.0.0.1:8000/problem-statements/');assert nojs.locator('.problem-card').count()==3
 nojs.locator('.card-link').first.click();assert nojs.locator('.brief-content').is_visible()
 fallback=browser.new_page(viewport={'width':390,'height':844})
 fallback.add_init_script("const original=HTMLCanvasElement.prototype.getContext;HTMLCanvasElement.prototype.getContext=function(type,...args){if(type.startsWith('webgl'))return null;return original.call(this,type,...args)}")
 fallback.goto('http://127.0.0.1:8000',wait_until='networkidle')
 assert fallback.locator('body').evaluate('(e)=>e.classList.contains("scene-unavailable")')
 assert fallback.locator('#hero-register').is_visible()
 checks.append('Reduced motion pauses animation; no-JavaScript navigation and unavailable-WebGL fallback remain usable')
 assert not errors,errors
 checks.append('No page errors, shader compilation errors, missing images or failed font requests')
 browser.close()
result={'status':'passed','checks':checks};(ROOT/'tests/results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
