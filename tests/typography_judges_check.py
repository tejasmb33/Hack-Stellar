"""Targeted typography, unified judges, domains and background preservation.
Uses actual platform-font readback, native controls and the saved baseline site.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageChops,ImageStat
import json,sys,time
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'tests/typography-judges';OUT.mkdir(exist_ok=True)
BASE=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8014';OLD=sys.argv[2] if len(sys.argv)>2 else 'http://127.0.0.1:8000'
DATA=json.loads((ROOT/'content.json').read_text());DOMAINS=list(dict.fromkeys(t for r in DATA['problems'] for t in r['domains']));errors=[];report={}
with sync_playwright() as p:
 browser=p.chromium.launch(channel='chromium');context=browser.new_context(viewport={'width':1440,'height':900},reduced_motion='reduce')
 page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
 page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
 # Whole-scene pixel comparisons: only foreground content is hidden in this test.
 parity=[]
 for path in ['/','/problem-statements/']:
  shots={}
  for label,url in [('before',OLD),('after',BASE)]:
   page.goto(url+path,wait_until='networkidle');page.wait_for_function('window.__cosmos?.frames>0')
   page.evaluate("document.querySelectorAll('header,main,footer,.floating-register,.skip-link').forEach(e=>e.style.visibility='hidden')")
   for y in [0,1200,3000]:
    page.evaluate('(y)=>scrollTo({top:y,behavior:"instant"})',y);page.wait_for_timeout(150)
    state=page.evaluate('({...__cosmos})');assert state['diskTime']==0
    name=f'background-{label}-{"home" if path=="/" else "directory"}-{y}.png';page.screenshot(path=str(OUT/name));shots[label,y]=(name,state)
  for y in [0,1200,3000]:
   a,b=shots['before',y],shots['after',y]
   for key in ['camera','center','raySteps','particles','resolution']:assert a[1][key]==b[1][key],(path,y,key)
   difference=ImageChops.difference(Image.open(OUT/a[0]).convert('RGB'),Image.open(OUT/b[0]).convert('RGB'));mean=max(ImageStat.Stat(difference).mean)
   assert mean<.01,(path,y,mean)
   if y==0:assert difference.getbbox() is None
   parity.append(dict(page=path,scroll=y,exact=difference.getbbox() is None,maxMeanChannelDifference=mean))
 report['background']=parity
 for name in json.loads((ROOT/'tests/finalized_scene_sha256.json').read_text()):assert page.request.get(OLD+'/'+name).body()==(ROOT/name).read_bytes(),name
 report['rendererSources']='All renderer bytes match the saved baseline; checksum fixture unchanged.'
 page.goto(BASE,wait_until='networkidle');page.evaluate('document.fonts.ready');assert page.locator('.hero h1').inner_text()=='HACKSTELLAR'
 assert page.locator('link[rel=preload][as=font]').get_attribute('href')=='/assets/josefin-sans-latin-400.woff2'
 cdp=context.new_cdp_session(page);cdp.send('DOM.enable');cdp.send('CSS.enable');doc=cdp.send('DOM.getDocument');node=cdp.send('DOM.querySelector',{'nodeId':doc['root']['nodeId'],'selector':'.title-hackstellar'})
 fonts=cdp.send('CSS.getPlatformFontsForNode',{'nodeId':node['nodeId']})['fonts'];assert any(f['familyName'].startswith('Josefin Sans') and f['isCustomFont'] and f['glyphCount']>0 for f in fonts),fonts
 report['actualTitleFont']=fonts
 assert page.locator('body').evaluate('(e)=>getComputedStyle(e).fontFamily').startswith('Inter')
 assert page.locator('.brand>span').evaluate('(e)=>getComputedStyle(e).fontFamily').startswith('Space')
 assert page.locator('#judges').count()==1 and page.locator('#judges h2').inner_text()=='Meet the Judges'
 assert 'Judges From' not in page.locator('main').inner_text();assert page.locator('.judge-employer,.judge-affiliations,.judge-portrait').count()==0
 assert page.locator('.judge-card').count()==2
 for i,(card,judge) in enumerate(zip(page.locator('.judge-card').all(),DATA['judges']),1):
  assert card.locator('.eyebrow').inner_text()==f'JUDGE {i:02d}'
  assert card.locator('h3').inner_text()==judge['name'];assert card.locator('.judge-company').inner_text()==judge['organization'];assert card.locator('.judge-education').inner_text()==judge['education']
  assert card.locator('.profile-link').get_attribute('href')==judge['linkedin']
  assert card.locator('img').get_attribute('src')==DATA['organizationLogos'][judge['organization']]
 for width,height in [(320,700),(390,844),(768,1024),(1440,900)]:
  page.set_viewport_size({'width':width,'height':height});page.evaluate('scrollTo({top:0,behavior:"instant"})');page.wait_for_timeout(100)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),width
  assert page.locator('.hero h1').evaluate('e=>{const r=e.getBoundingClientRect();const t=document.createRange();t.selectNodeContents(e);const q=t.getBoundingClientRect();return q.left>=r.left-1&&q.right<=r.right+1}'),width
  page.evaluate('document.activeElement?.blur()');page.screenshot(path=str(OUT/f'hero-{width}.png'))
  page.locator('#judges').scroll_into_view_if_needed();page.wait_for_timeout(100)
  cards=page.locator('.judge-card').all();boxes=[c.bounding_box() for c in cards]
  if width>760:
   assert abs(boxes[0]['y']-boxes[1]['y'])<1 and abs(boxes[0]['height']-boxes[1]['height'])<1
  else:assert boxes[1]['y']>=boxes[0]['y']+boxes[0]['height'] and abs(boxes[0]['height']-boxes[1]['height'])<1
  for card in cards:
   image=card.locator('img');image.evaluate('(e)=>e.decode()')
   assert card.evaluate('''e=>{const p=e.querySelector('.company-logo').getBoundingClientRect(),img=e.querySelector('img'),i=img.getBoundingClientRect(),n=e.querySelector('.eyebrow').getBoundingClientRect();return i.left>=p.left&&i.right<=p.right&&i.top>=p.top&&i.bottom<=p.bottom&&i.bottom<n.top&&Math.abs(i.width/i.height-img.naturalWidth/img.naturalHeight)<.01&&Math.abs((i.left+i.right-p.left-p.right)/2)<1}''')
  page.evaluate('document.activeElement?.blur()');page.locator('#judges').screenshot(path=str(OUT/f'judges-{width}.png'),style='.skip-link,.floating-register{visibility:hidden!important}')
  page.goto(BASE+'/problem-statements/',wait_until='networkidle')
  assert page.locator('#domain option').all_text_contents()==['All Domains']+DOMAINS
  assert 'Logistics' not in page.locator('#domain').inner_text();assert page.locator('#domain').input_value()==''
  assert page.locator('.problem-card:visible').count()==21
  for domain in DOMAINS:
   page.locator('#domain').select_option(domain)
   expected=[r['id'] for r in DATA['problems'] if domain in r['domains']]
   actual=page.locator('.problem-card:visible').evaluate_all('(cards)=>cards.map(c=>c.dataset.number)');assert actual==expected,(width,domain)
   assert page.locator('#result-count').inner_text()==f'Showing {len(expected)} of 21 problem statements'
  page.locator('#domain').select_option('E-Commerce');page.locator('#search').fill('Returns That Never Go Home')
  assert page.locator('.problem-card:visible').count()==1 and page.locator('.problem-card:visible').get_attribute('data-number')=='PS–16'
  assert page.locator('.problem-card:visible .domain-tags').inner_text().splitlines()==['AI','E-Commerce']
  page.locator('#search').fill('no matching title');assert page.locator('.problem-card:visible').count()==0
  page.locator('#reset').click();assert page.locator('.problem-card:visible').count()==21
  page.get_by_role('combobox',name='Domain').focus();assert page.evaluate('document.activeElement.id')=='domain'
  page.locator('#domain').select_option(DOMAINS[-1]);assert page.locator('#domain').input_value()==DOMAINS[-1]
  assert page.locator('#domain').evaluate('''e=>{const s=getComputedStyle(e),c=document.createElement('canvas').getContext('2d');c.font=s.font;return Math.max(...Array.from(e.options,o=>c.measureText(o.text).width))<=e.clientWidth-parseFloat(s.paddingLeft)-parseFloat(s.paddingRight)}''')
  page.locator('#domain').select_option('');assert page.locator('.problem-card:visible').count()==21
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),width
  page.screenshot(path=str(OUT/f'directory-{width}.png'))
  page.goto(BASE,wait_until='networkidle')
 report['responsive']='320, 390, 768 and 1440px: title fits, logos retain proportions, balanced desktop cards and stacked mobile cards.'
 report['domains']=dict(valid=len(DOMAINS),default=21,allFilters='passed',combinedSearch='passed',counts='passed',nativeFocusAndLabelFit='passed')
 # Cross-page navigation must land directly on the unified judges section.
 page.goto(BASE+'/problem-statements/',wait_until='networkidle');page.locator('nav a[href="/#judges"]').click();page.wait_for_url(BASE+'/#judges');assert page.locator('#judges').evaluate('(e)=>{const r=e.getBoundingClientRect();return r.top<innerHeight&&r.bottom>0}')
 # All brief content remains accessible, including the corrected PS 16.
 for record in DATA['problems']:
  page.goto(BASE+'/problem-statements/'+record['slug']+'/',wait_until='domcontentloaded')
  assert page.locator('h1').inner_text()==record['title'];assert page.locator('.brief-section p').first.inner_text()==record['description']
  if record['challenge']:assert page.locator('.brief-section p').nth(1).inner_text()==record['challenge']
 report['briefs']='All 21 complete titles/descriptions/challenges verified.'
 # Delayed cold font load: reserve heading/conversion geometry during the block period.
 cold=browser.new_page(viewport={'width':1280,'height':800},reduced_motion='reduce')
 cold.route('**/scene.js',lambda route:route.fulfill(body='// Font-layout-only diagnostic.',content_type='text/javascript'))
 def delayed_font(route):time.sleep(.8);route.continue_()
 cold.route('**/josefin-sans-latin-400.woff2',delayed_font)
 cold.add_init_script('''window.fontTrace=[];addEventListener('DOMContentLoaded',()=>{let n=0;function tick(){const h=document.querySelector('.hero h1'),c=document.querySelector('.hero-conversion');fontTrace.push({loaded:document.fonts.check('400 100px "Josefin Sans"'),h:h.getBoundingClientRect().height,y:c.getBoundingClientRect().top});if(n++<100)requestAnimationFrame(tick)}tick()})''')
 cold.goto(BASE,wait_until='networkidle');cold.evaluate('document.fonts.ready');cold.wait_for_timeout(300);trace=cold.evaluate('fontTrace')
 assert any(t['loaded'] for t in trace)
 assert max(t['h'] for t in trace)-min(t['h'] for t in trace)<.5
 assert max(t['y'] for t in trace)-min(t['y'] for t in trace)<.5
 report['coldFontLoad']=dict(delayMs=800,samples=len(trace),observedPending=any(not t['loaded'] for t in trace),headingShift=max(t['h'] for t in trace)-min(t['h'] for t in trace),conversionShift=max(t['y'] for t in trace)-min(t['y'] for t in trace))
 browser.close()
assert not errors,errors
report.update(status='passed',errors=errors)
(OUT/'results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
