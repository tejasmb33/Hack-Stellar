"""Browser regressions. Usage: python tests/browser_check.py [base-url]."""
from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'tests/screenshots';OUT.mkdir(exist_ok=True)
BASE=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8000'
DATA=json.loads((ROOT/'content.json').read_text());TOTAL=sum(p.get('published',True) for p in DATA['problems']);FORM=DATA['event']['registrationUrl']
checks=[];errors=[]
with sync_playwright() as p:
 browser=p.chromium.launch(args=['--enable-unsafe-swiftshader'])
 def new_page(w=1440,h=900,**options):
  page=browser.new_page(viewport={'width':w,'height':h},device_scale_factor=1,**options)
  page.on('pageerror',lambda error:errors.append(str(error)))
  page.on('console',lambda message:errors.append(message.text) if message.type=='error' else None)
  return page
 page=new_page();page.goto(BASE,wait_until='networkidle')
 page.wait_for_function('window.__cosmos && window.__cosmos.frames > 2')
 state=page.evaluate('({...window.__cosmos})');assert state['scene']=='black-hole' and state['raySteps']>=100 and state['particles']>=1000
 assert state['drawCalls']>=3 and state['triangles']>1000
 page.wait_for_function('(before)=>window.__cosmos.diskTime > before',arg=state['diskTime'])
 assert 'earthRotation' not in page.evaluate('window.__cosmos')
 assert ' '.join(page.locator('h1').inner_text().split())=='INTERSTELLAR : THE BUILDATHON'
 assert 'INTERSTELLAR : THE BUILDATHON' in page.title()
 assert page.locator('.site-header').evaluate('(e)=>getComputedStyle(e).position')=='relative'
 assert page.locator('#hero-register').bounding_box()['y']<900
 assert page.locator('.floating-register').is_hidden()
 for button in page.locator('[data-register]').all():assert button.get_attribute('href')==FORM
 assert page.locator('.problem-providers img').count()==0
 assert page.locator('.provider-name strong').all_text_contents()==['Amazon','TCS','HP','Blackhawk Networks','Cisco']
 assert page.locator('.sponsor img').count()==3
 assert 'Microsoft' in page.locator('.judge-card').nth(0).inner_text();assert 'IITian' in page.locator('.judge-card').nth(0).inner_text()
 assert 'Gokaraju Abhijit' in page.locator('.judge-card').nth(1).inner_text();assert 'Ribbon Communications' in page.locator('.judge-card').nth(1).inner_text();assert 'BITS Pilani' in page.locator('.judge-card').nth(1).inner_text()
 assert page.locator('.judge-card').nth(1).locator('.profile-link').get_attribute('href')=='https://www.linkedin.com/in/gokarajuabhijit/'
 page.emulate_media(reduced_motion='reduce');page.wait_for_timeout(150)
 page.screenshot(path=str(OUT/'desktop-hero.png'));page.screenshot(path=str(OUT/'desktop-home.png'),full_page=True)
 checks.append('Live 3D ray-traced black hole, lensed disk, animated dust, new branding, verified judges and direct registration links')
 for image in page.locator('img').all():
  image.scroll_into_view_if_needed();assert image.evaluate('(e)=>e.complete && e.naturalWidth>0')
 page.locator('#affiliations').scroll_into_view_if_needed();page.wait_for_timeout(150)
 assert page.locator('.site-header').bounding_box()['y']<0
 assert page.evaluate('window.__cosmos.cameraZ')>state['cameraZ']
 page.screenshot(path=str(OUT/'desktop-orbit.png'))
 page.evaluate('scrollTo({top:850,behavior:"instant"})');page.wait_for_timeout(150)
 assert page.locator('.floating-register').is_visible()
 page.locator('#registration').scroll_into_view_if_needed();page.locator('.floating-register').wait_for(state='hidden')
 page.locator('#faq summary').first.click();assert page.locator('#faq details').first.get_attribute('open') is not None
 page.locator('#signal').scroll_into_view_if_needed();page.locator('#signal').click();assert 'SOS' in page.locator('#signal-message').inner_text()
 page.locator('#time-note').click();assert 'Proper time' in page.locator('#time-message').inner_text()
 checks.append('Scroll camera transitions, non-sticky header, floating registration visibility, FAQ, Easter eggs and sponsor assets')
 page.goto(BASE+'/problem-statements/',wait_until='networkidle')
 assert page.locator('.problem-card:visible').count()==TOTAL
 assert page.locator('#domain').input_value()=='' and page.locator('#domain option:checked').inner_text()=='All Domains'
 assert page.locator('#result-count').inner_text()==f'Showing all {TOTAL} problem statements'
 assert page.locator('.problem-card .source').count()==0 and page.locator('.problem-grid img').count()==0
 assert page.locator('#source').count()==0
 page.locator('#domain').select_option('Automation');assert page.locator('.problem-card:visible').count()==2
 assert page.locator('#result-count').inner_text()==f'Showing 2 of {TOTAL} problem statements'
 page.locator('#domain').select_option('');assert page.locator('.problem-card:visible').count()==TOTAL
 assert page.locator('#result-count').inner_text()==f'Showing all {TOTAL} problem statements'
 page.locator('#search').fill('PS-02');assert page.locator('.problem-card:visible').count()==1
 page.locator('#search').fill('zzz-no-match');assert page.locator('#empty').is_visible()
 page.locator('#empty-reset').click();assert page.locator('.problem-card:visible').count()==TOTAL
 page.locator('#domain').select_option('Voice AI');page.reload(wait_until='networkidle')
 assert page.locator('#domain').input_value()=='' and page.locator('.problem-card:visible').count()==TOTAL
 page.evaluate('document.activeElement.blur();scrollTo({top:0,behavior:"instant"})');page.screenshot(path=str(OUT/'desktop-directory.png'),full_page=True)
 for problem in DATA['problems']:
  page.goto(BASE+'/problem-statements/'+problem['slug']+'/',wait_until='networkidle')
  assert page.locator('.brief-content h2').count()==4
  assert 'Note:' in page.locator('.brief-content').inner_text()
  assert 'SOURCE / CONTRIBUTOR' not in page.locator('.brief-meta').inner_text()
 page.screenshot(path=str(OUT/'desktop-brief.png'),full_page=True)
 page.get_by_role('link',name='← Back to directory').click();assert page.url.endswith('/problem-statements/')
 page.get_by_role('link',name='← Back to Home').first.click();assert page.url.rstrip('/')==BASE
 checks.append('All records initially visible; All Domains restoration, explicit filtering, count wording, search, reset, reload defaults and all full briefs')
 for width,height in [(320,700),(390,844),(768,1024),(1280,720),(1440,900)]:
  layout=new_page(width,height,is_mobile=width<600,has_touch=width<600,reduced_motion='reduce')
  for path in ['/','/problem-statements/','/problem-statements/ps-03/']:
   layout.goto(BASE+path,wait_until='networkidle')
   assert layout.evaluate('document.documentElement.scrollWidth <= innerWidth'),f'overflow at {width} {path}'
   if path=='/':
    r=layout.locator('#hero-register').bounding_box();assert r['y']+r['height']<height,f'hero action below fold at {width}'
   if width==390:
    filename={'/':'mobile-home.png','/problem-statements/':'mobile-directory.png','/problem-statements/ps-03/':'mobile-brief.png'}[path]
    layout.screenshot(path=str(OUT/filename),full_page=True)
  layout.close()
 checks.append('Homepage, directory and full brief fit 320,390,768,1280,1440px widths; initial registration action remains visible')
 reduced=new_page(reduced_motion='reduce');reduced.goto(BASE,wait_until='networkidle')
 a=reduced.evaluate('({...window.__cosmos})');reduced.wait_for_timeout(250);b=reduced.evaluate('({...window.__cosmos})')
 assert a['diskTime']==b['diskTime'] and b['paused']
 nojs=new_page(java_script_enabled=False);nojs.goto(BASE+'/problem-statements/')
 assert nojs.locator('.problem-card').count()==TOTAL;nojs.locator('.card-link').first.click();assert nojs.locator('.brief-content').is_visible()
 fallback=browser.new_page(viewport={'width':390,'height':844})
 fallback.add_init_script("const original=HTMLCanvasElement.prototype.getContext;HTMLCanvasElement.prototype.getContext=function(type,...args){if(type.startsWith('webgl'))return null;return original.call(this,type,...args)}")
 fallback.goto(BASE,wait_until='networkidle');assert fallback.locator('body').evaluate('(e)=>e.classList.contains("scene-unavailable")');assert fallback.locator('#hero-register').is_visible()
 checks.append('Reduced-motion pause, all content without JavaScript and usable unavailable-WebGL fallback')
 assert not errors,errors
 browser.close()
result={'status':'passed','publishedStatements':TOTAL,'checks':checks};(ROOT/'tests/results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
