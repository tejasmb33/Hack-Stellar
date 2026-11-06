"""Existing content/gallery checks with intentional rendering changes assessed separately."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageChops
import json,sys
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'tests/sharpness-audit/ui';OUT.mkdir(exist_ok=True)
BASE=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8012'
OLD=sys.argv[2] if len(sys.argv)>2 else 'http://127.0.0.1:8000'
DATA=json.loads((ROOT/'content.json').read_text());errors=[];report={}
with sync_playwright() as p:
 browser=p.chromium.launch(channel='chromium')
 page=browser.new_page(viewport={'width':1440,'height':900},reduced_motion='reduce')
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
 report['background']='Intentional quality changes: reference captures are in sharpness-audit/comparison-results.json.'
 page.goto(BASE,wait_until='networkidle')
 assert page.locator('.hero h1').inner_text()=='HACKSTELLAR'
 assert page.locator('.hero-prize strong').inner_text()=='₹25,000'
 assert 'ESB SEMINAR HALL 2' in page.locator('.hero-meta').inner_text()
 assert 'HackStellar' in page.title() and 'ESB Seminar Hall 2' in page.locator('meta[name=description]').get_attribute('content')
 page.screenshot(path=str(OUT/'desktop-hero.png'))
 for card,record in zip(page.locator('.sponsor').all(),DATA['sponsors']):
  assert card.get_attribute('href')==record['url']
  assert card.get_attribute('target')=='_blank'
  assert set(card.get_attribute('rel').split()) >= {'noopener','noreferrer'}
 for card,record in zip(page.locator('.judge-card').all(),DATA['judges']):
  assert card.locator('img').get_attribute('src')==DATA['organizationLogos'][record['organization']]
  card.scroll_into_view_if_needed()
  card.locator('img').evaluate('(e)=>e.decode()')
  assert card.locator('img').evaluate('(e)=>e.complete&&e.naturalWidth>0')
  assert card.evaluate('e=>e.querySelector("img").getBoundingClientRect().bottom<e.querySelector(".judge-body .eyebrow").getBoundingClientRect().top')
 page.locator('.judge-grid').screenshot(path=str(OUT/'company-logos.png'))
 assert page.locator('#gallery-title').inner_text()=='A glimpse into what we have accomplished together.'
 assert page.locator('.gallery-item').count()==8
 page.locator('#gallery').scroll_into_view_if_needed()
 page.locator('.gallery-item').last.scroll_into_view_if_needed();page.wait_for_timeout(500)
 page.locator('#gallery').screenshot(path=str(OUT/'desktop-gallery.png'))
 for item in page.locator('.gallery-item').all():assert item.locator('img').evaluate('(e)=>e.complete&&e.naturalWidth>0')
 page.locator('.gallery-item').first.click()
 dialog=page.locator('.gallery-lightbox');assert dialog.is_visible()
 assert dialog.locator('.lightbox-count').inner_text()=='1 / 8'
 for index in range(8):
  assert dialog.locator('img').get_attribute('src')==page.locator('.gallery-item').nth(index).get_attribute('href') or dialog.locator('img').get_attribute('src')==BASE+page.locator('.gallery-item').nth(index).get_attribute('href')
  page.keyboard.press('ArrowRight')
 assert dialog.locator('.lightbox-count').inner_text()=='1 / 8'
 page.keyboard.press('ArrowLeft');assert dialog.locator('.lightbox-count').inner_text()=='8 / 8'
 dialog.locator('img').evaluate('(e)=>e.decode()')
 assert dialog.locator('img').evaluate('(e)=>getComputedStyle(e).objectFit')=='contain'
 page.screenshot(path=str(OUT/'lightbox.png'))
 page.keyboard.press('Escape');assert not dialog.is_visible()
 assert page.locator('.gallery-item').first.evaluate('(e)=>document.activeElement===e')
 page.locator('.gallery-item').nth(1).click();dialog.locator('.lightbox-next').click();assert dialog.locator('.lightbox-count').inner_text()=='3 / 8'
 dialog.locator('.lightbox-prev').click();dialog.locator('.lightbox-close').click();assert not dialog.is_visible()
 report['gallery']='All 8 supplied photographs; full images, next/previous, wraparound, Escape, close and focus restoration passed.'
 page.goto(BASE+'/problem-statements/',wait_until='networkidle')
 assert page.locator('.problem-card:visible').count()==21
 for record in DATA['problems'][17:]:
  page.locator('#search').fill(record['subtitle']);assert page.locator('.problem-card:visible').count()==1
  page.locator('.card-link:visible').click()
  assert page.locator('.brief-subtitle').inner_text()==record['subtitle']
  assert page.locator('.brief-section p').inner_text()==record['description']
  assert page.locator('.brief-meta').count()==0
  page.goto(BASE+'/problem-statements/',wait_until='networkidle')
 page.emulate_media(reduced_motion='no-preference');page.wait_for_timeout(500)
 a=page.evaluate('window.__cosmos.diskTime');page.wait_for_timeout(500);assert page.evaluate('window.__cosmos.diskTime')>a
 report['directory']='All 21 visible by default; new subtitles searchable; exact full briefs without invented domains; shared background animates.'
 for width,height in [(320,700),(390,844),(768,1024),(1440,900)]:
  page.emulate_media(reduced_motion='reduce');page.set_viewport_size({'width':width,'height':height})
  for path in ['/','/problem-statements/','/problem-statements/ps-21/']:
   page.goto(BASE+path,wait_until='networkidle');assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,path)
   if path=='/':
    if width==390:page.screenshot(path=str(OUT/'mobile-hero.png'))
    for card in page.locator('.judge-card').all():
     card.scroll_into_view_if_needed()
     assert card.evaluate('e=>{const p=e.querySelector(".company-logo").getBoundingClientRect(),i=e.querySelector("img").getBoundingClientRect();return i.left>=p.left&&i.right<=p.right&&i.top>=p.top&&i.bottom<=p.bottom&&Math.abs((i.left+i.right-p.left-p.right)/2)<1}')
    page.locator('#gallery').scroll_into_view_if_needed()
    if width==390:page.locator('#gallery').screenshot(path=str(OUT/'mobile-gallery.png'))
    page.locator('.gallery-item').last.click();assert dialog.is_visible();assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    page.keyboard.press('Escape')
 report['responsive']='320, 390, 768 and 1440px layouts, logo containment and mobile lightbox passed.'
 assert not errors,errors
 browser.close()
report['status']='passed';(OUT/'results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
