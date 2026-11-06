from playwright.sync_api import sync_playwright
from pathlib import Path
import json
out=Path(__file__).parent;report=[];errors=[]
with sync_playwright() as p:
 b=p.chromium.launch(channel='chromium')
 for w,h in [(320,700),(390,844),(768,1024),(1024,768),(1440,900)]:
  page=b.new_page(viewport={'width':w,'height':h},reduced_motion='reduce');page.on('pageerror',lambda e:errors.append(str(e)))
  page.add_init_script('window.layoutShifts=[];new PerformanceObserver(list=>{for(const e of list.getEntries())if(!e.hadRecentInput)layoutShifts.push(e.value)}).observe({type:"layout-shift",buffered:true})');page.goto('http://127.0.0.1:8018/');page.wait_for_function('window.__cosmos?.frames>0');page.evaluate('document.fonts.ready');page.screenshot(path=str(out/f'after-{w}-hero.png'))
  state=page.evaluate('''()=>{const hero=document.querySelector('#hero').getBoundingClientRect(),c=document.querySelector('.hero-conversion').getBoundingClientRect(),bottom=document.querySelector('.hero-bottom').getBoundingClientRect();return {overflow:document.documentElement.scrollWidth-innerWidth,hero:{top:hero.top,bottom:hero.bottom,height:hero.height},conversionBottom:c.bottom,bottomTop:bottom.top,button:document.querySelector('#hero-register').getBoundingClientRect().toJSON(),bad:[...document.querySelectorAll('body *')].filter(e=>e.getBoundingClientRect().right>innerWidth+1&&getComputedStyle(e).display!=='none'&&e.getBoundingClientRect().width>0).slice(0,10).map(e=>[e.tagName,e.className,e.getBoundingClientRect().right])};}''');state['width']=w;state['CLS']=page.evaluate('layoutShifts.reduce((a,b)=>a+b,0)');report.append(state)
  page.locator('#event-flow').screenshot(path=str(out/f'after-{w}-event-information-full.png'))
  for sel in ['#affiliations','#evaluation-schedule','#final-round','#rules','#challenges','#judges','#faq','#registration','#gallery','.site-footer']:
   page.locator(sel).scroll_into_view_if_needed();page.wait_for_timeout(100);page.screenshot(path=str(out/f'after-{w}-{sel.lstrip("#.")}.png'))
  for label,path in [('directory','/problem-statements/'),('brief','/problem-statements/ps-01/'),('credits','/credits.html')]:
   page.goto('http://127.0.0.1:8018'+path,wait_until='networkidle');page.screenshot(path=str(out/f'after-{w}-{label}.png'))
  page.close()
 b.close()
(out/'final-layout-check.json').write_text(json.dumps({'layout':report,'errors':errors},indent=2));print(json.dumps({'profiles':len(report),'CLS':[r['CLS'] for r in report],'errors':errors}))
