"""Full refinement regression checks. Usage: python tests/browser_check.py [base-url]."""
from pathlib import Path
import json,sys,math
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'tests/screenshots';OUT.mkdir(exist_ok=True)
BASE=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8000'
DATA=json.loads((ROOT/'content.json').read_text());P=DATA['problems'];TOTAL=len(P);DOMAINS=list(dict.fromkeys(tag for record in P for tag in record['domains']));FORM=DATA['event']['registrationUrl']
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
 initial=page.evaluate('({...window.__cosmos})');assert initial['scene']=='black-hole' and initial['raySteps']>=128 and initial['particles']>=1800
 assert initial['cameraZ']<12 and initial['drawCalls']>=3 and initial['pipeline']=='curved-ray-volume/HDR/depth-aware-dust'
 page.wait_for_function('(phase)=>window.__cosmos.diskPhase > phase+.01',arg=initial['diskPhase'])
 moving=page.evaluate('({...window.__cosmos})');assert moving['camera']!=initial['camera'] and moving['diskTime']>initial['diskTime']
 assert ' '.join(page.locator('h1').inner_text().split())=='HackStellar'
 for link in page.locator('[data-register]').all():assert link.get_attribute('href')==FORM
 assert page.locator('.site-header').evaluate('(e)=>getComputedStyle(e).position')=='relative'
 assert page.locator('.problem-providers img').count()==0
 assert page.locator('.provider-name strong').all_text_contents()==DATA['problemProviders']
 assert 'Abhijeet Verma' in page.locator('.judge-card').nth(1).inner_text()
 assert page.locator('.judge-card').nth(1).locator('.profile-link').get_attribute('href')==DATA['judges'][1]['linkedin']
 page.emulate_media(reduced_motion='reduce');page.wait_for_timeout(100)
 page.screenshot(path=str(OUT/'desktop-hero.png'));page.screenshot(path=str(OUT/'desktop-home.png'),full_page=True)
 checks.append('Larger live 3D black hole: rotating disk phase, autonomous camera movement, curved-ray emitting volume and 10500-particle desktop field')
 # Freeze time but sample the full camera path in both directions; visual state may not be hidden or faded.
 route=[0,400,800,1200,1600,1980,1990,2200,2700,3300,2200,1200,400,0]
 recorded={};samples=[]
 for y in route:
  page.evaluate(f'scrollTo({{top:{y},behavior:"instant"}})');page.wait_for_timeout(80)
  page.wait_for_function('(target)=>Math.abs(window.__cosmos.pathProgress-target)<.005',arg=min(y/(page.locator('#hero').evaluate('(e)=>e.offsetTop+e.offsetHeight')*4.8),1))
  state=page.evaluate('({...window.__cosmos})');assert state['holeVisible'] and state['sceneOpacity']==1
  assert page.locator('canvas').evaluate('(e)=>getComputedStyle(e).opacity')=='1'
  if y in recorded:assert math.dist(state['camera'],recorded[y]['camera'])<.001
  recorded[y]=state;samples.append({'scroll':y,'camera':state['camera'],'center':state['center']})
  if y==1200:page.screenshot(path=str(OUT/'desktop-orbit.png'))
 assert recorded[800]['cameraZ']<recorded[0]['cameraZ'] and recorded[3300]['cameraZ']>recorded[800]['cameraZ']
 assert math.dist(recorded[1980]['camera'],recorded[1990]['camera'])<.3
 (ROOT/'tests/scroll-path.json').write_text(json.dumps(samples,indent=2)+'\n')
 checks.append('Approach/pass/recede camera path remains rendered at every sample, has no opacity switch and reverses to matching positions')
 page.evaluate('scrollTo({top:850,behavior:"instant"})');page.locator('.floating-register').wait_for(state='visible')
 page.locator('#registration').scroll_into_view_if_needed();page.locator('.floating-register').wait_for(state='hidden')
 page.locator('#faq summary').first.click();assert page.locator('#faq details').first.get_attribute('open') is not None
 page.locator('#signal').click();assert 'SOS' in page.locator('#signal-message').inner_text()
 checks.append('Non-sticky header, hero/floating registration, confirmed FAQ and subtle Easter egg remain functional')
 page.goto(BASE+'/problem-statements/',wait_until='networkidle')
 assert TOTAL==21 and len(DOMAINS)==21
 assert page.locator('.problem-card:visible').count()==21
 assert page.locator('#domain').input_value()==''
 assert page.locator('#domain option').all_text_contents()==['All Domains']+DOMAINS
 assert page.locator('#result-count').inner_text()=='Showing 21 of 21 problem statements'
 assert '21 Challenges. Endless Possibilities.' in page.locator('.directory-subtitle').inner_text()
 assert page.locator('.problem-card .source').count()==0 and page.locator('.problem-grid img').count()==0
 assert page.locator('.problem-card').evaluate_all('(cards)=>cards.map(card=>card.dataset.number)')==[record['id'] for record in P]
 for domain in DOMAINS:
  page.locator('#domain').select_option(domain)
  expected=[record['id'] for record in P if domain in record['domains']]
  actual=page.locator('.problem-card:visible').evaluate_all('(cards)=>cards.map(card=>card.dataset.number)')
  assert actual==expected,(domain,actual,expected)
  assert page.locator('#result-count').inner_text()==f'Showing {len(expected)} of 21 problem statements'
 page.locator('#domain').select_option('Web Development');assert page.locator('.problem-card:visible').count()==2
 page.locator('#domain').select_option('IoT');assert page.locator('.problem-card:visible').evaluate_all('(cards)=>cards.map(card=>card.dataset.number)')==['PS–11','PS–17']
 page.locator('#search').fill('tariff');assert page.locator('.problem-card:visible').count()==1
 assert 'PS–17' in page.locator('.problem-card:visible .problem-index').inner_text()
 page.locator('#search').fill('zz-no-results');assert page.locator('#empty').is_visible()
 page.locator('#empty-reset').click();assert page.locator('.problem-card:visible').count()==21
 page.locator('#search').fill('PS-02');assert page.locator('.problem-card:visible').count()==1
 page.locator('#reset').click();assert page.locator('#domain').input_value()==''
 page.locator('#domain').select_option('Energy Management');page.reload(wait_until='networkidle')
 assert page.locator('#domain').input_value()=='' and page.locator('.problem-card:visible').count()==21
 page.get_by_role('combobox',name='Domain').focus()
 assert page.evaluate('document.activeElement.id')=='domain'
 assert page.locator('#domain').evaluate('(e)=>e.tagName')=='SELECT'
 page.locator('#domain').select_option('Energy Management')
 assert page.locator('#domain').input_value()=='Energy Management'
 page.locator('#domain').select_option('');assert page.locator('.problem-card:visible').count()==21
 page.evaluate('document.activeElement.blur();scrollTo({top:0,behavior:"instant"})');page.screenshot(path=str(OUT/'desktop-directory.png'),full_page=True)
 checks.append('Exactly 21 ordered statements, all 21 selectable domains, Web Development/IoT examples, combined search, accurate counts, reset and fresh-page defaults')
 for record in P:
  page.goto(BASE+'/problem-statements/'+record['slug']+'/',wait_until='networkidle')
  assert page.locator('.brief-content h2').all_text_contents()==(['Problem Statement'] if record.get('format')=='statement' else ['Problem Description','Your Challenge'])
  assert page.locator('.brief-section').nth(0).locator('p').inner_text()==record['description']
  if record.get('format')!='statement':assert page.locator('.brief-section').nth(1).locator('p').inner_text()==record['challenge']
  assert page.locator('.brief-document h1').inner_text()==record['title']
  if record['domains']:assert page.locator('.brief-meta p').inner_text().replace('DOMAINS\n','')==record['domainLabel']
 page.screenshot(path=str(OUT/'desktop-brief.png'),full_page=True)
 checks.append('All 21 full-statement pages contain the exact official titles and full text, with new subtitles and confirmed domains only without invented sources')
 # Layout and mathematical logo containment checks at desktop, tablet and phone widths.
 for width,height in [(320,700),(390,844),(768,1024),(1280,720),(1440,900)]:
  layout=new_page(width,height,is_mobile=width<600,has_touch=width<600,reduced_motion='reduce')
  for path in ['/','/problem-statements/','/problem-statements/ps-17/']:
   layout.goto(BASE+path,wait_until='networkidle')
   assert layout.evaluate('document.documentElement.scrollWidth<=innerWidth'),f'overflow {width} {path}'
   if path=='/':
    rect=layout.locator('#hero-register').bounding_box();assert rect['y']+rect['height']<height,f'hero action below fold at {width}'
    heights=[]
    for sponsor in layout.locator('.sponsor').all():
     sponsor.scroll_into_view_if_needed();image=sponsor.locator('img');assert image.evaluate('(e)=>e.complete&&e.naturalWidth>0')
     result=sponsor.evaluate('''card=>{const box=card.getBoundingClientRect(),frame=card.querySelector('.logo-safe').getBoundingClientRect(),img=card.querySelector('img').getBoundingClientRect();return {height:box.height,contained:img.left>=frame.left-.5&&img.right<=frame.right+.5&&img.top>=frame.top-.5&&img.bottom<=frame.bottom+.5,cardContained:frame.left>=box.left&&frame.right<=box.right&&frame.top>=box.top&&frame.bottom<=box.bottom,centered:Math.abs((img.left+img.right)/2-(frame.left+frame.right)/2)<1&&Math.abs((img.top+img.bottom)/2-(frame.top+frame.bottom)/2)<1,fit:getComputedStyle(card.querySelector('img')).objectFit}}''')
     assert result['contained'] and result['cardContained'] and result['centered'] and result['fit']=='contain',(width,result)
     heights.append(result['height'])
    assert max(heights)-min(heights)<1
   if width==390:
    layout.evaluate('scrollTo({top:0,behavior:"instant"})');layout.wait_for_timeout(100)
    filename={'/':'mobile-home.png','/problem-statements/':'mobile-directory.png','/problem-statements/ps-17/':'mobile-brief.png'}[path]
    layout.screenshot(path=str(OUT/filename),full_page=True)
  layout.close()
 checks.append('320–1440px layouts pass; every sponsor logo is centered, contained and undistorted within equal-height cards')
 reduced=new_page(reduced_motion='reduce');reduced.goto(BASE,wait_until='networkidle')
 before=reduced.evaluate('window.__cosmos.diskTime');reduced.wait_for_timeout(250);assert reduced.evaluate('window.__cosmos.diskTime')==before
 nojs=new_page(java_script_enabled=False);nojs.goto(BASE+'/problem-statements/');assert nojs.locator('.problem-card').count()==21
 nojs.locator('.card-link').nth(16).click();assert nojs.locator('.brief-content').is_visible()
 fallback=browser.new_page(viewport={'width':390,'height':844})
 fallback.add_init_script("const original=HTMLCanvasElement.prototype.getContext;HTMLCanvasElement.prototype.getContext=function(type,...args){if(type.startsWith('webgl'))return null;return original.call(this,type,...args)}")
 fallback.goto(BASE,wait_until='networkidle');assert fallback.locator('body').evaluate('(e)=>e.classList.contains("scene-unavailable")');assert fallback.locator('#hero-register').is_visible()
 assert not errors,errors
 browser.close()
 checks.append('Reduced motion, accessible native domain control, no-JavaScript full catalogue and unavailable-WebGL fallback remain usable')
result={'status':'passed','publishedStatements':TOTAL,'domainTags':len(DOMAINS),'checks':checks};(ROOT/'tests/results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
