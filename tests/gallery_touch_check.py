"""Mobile background parity, touch controls, swipe events and modal focus containment."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageChops
import sys,json
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'tests/hackstellar'
BASE=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8012'
OLD=sys.argv[2] if len(sys.argv)>2 else 'http://127.0.0.1:8000'
with sync_playwright() as p:
 browser=p.chromium.launch(channel='chromium')
 page=browser.new_page(viewport={'width':390,'height':844},has_touch=True,is_mobile=True,reduced_motion='reduce')
 for label,url in [('before',OLD),('after',BASE),('directory',BASE+'/problem-statements/')]:
  page.goto(url,wait_until='networkidle');page.wait_for_function('window.__cosmos?.frames>0')
  page.evaluate("document.querySelectorAll('header,main,footer,.floating-register,.skip-link').forEach(e=>e.style.visibility='hidden')")
  page.screenshot(path=str(OUT/f'mobile-background-{label}.png'))
 before=Image.open(OUT/'mobile-background-before.png').convert('RGB')
 for label in ['after','directory']:
  assert ImageChops.difference(before,Image.open(OUT/f'mobile-background-{label}.png').convert('RGB')).getbbox() is None
 page.goto(BASE,wait_until='networkidle');page.locator('.gallery-item').first.tap()
 dialog=page.locator('dialog');assert dialog.is_visible()
 dialog.locator('.lightbox-next').tap();assert dialog.locator('.lightbox-count').inner_text()=='2 / 8'
 dialog.locator('.lightbox-prev').tap();assert dialog.locator('.lightbox-count').inner_text()=='1 / 8'
 dialog.locator('figure').evaluate('''f=>{const a=new Touch({identifier:1,target:f,clientX:300,clientY:300}),b=new Touch({identifier:1,target:f,clientX:100,clientY:310});f.dispatchEvent(new TouchEvent('touchstart',{touches:[a],changedTouches:[a],bubbles:true}));f.dispatchEvent(new TouchEvent('touchend',{touches:[],changedTouches:[b],bubbles:true}));}''')
 assert dialog.locator('.lightbox-count').inner_text()=='2 / 8'
 for _ in range(8):
  page.keyboard.press('Tab');assert page.evaluate('!!document.activeElement.closest("dialog")')
 dialog.locator('.lightbox-close').tap();assert not dialog.is_visible()
 browser.close()
report={'mobileBackground':'Pixel-identical approved home, updated home and reused directory at fixed time.','touch':'Tap, next/previous, horizontal swipe event, close and native modal focus containment passed.','limitation':'Chromium mobile viewport and touch emulation; not a physical phone.'}
(OUT/'touch-results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
