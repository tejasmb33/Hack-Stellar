"""Official content, keyboard, reflow, floating CTA and live readability checks."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).parent;BASE='http://127.0.0.1:8018';data=json.loads((ROOT/'content.json').read_text());errors=[];report={'layouts':[]}
with sync_playwright() as p:
 browser=p.chromium.launch(channel='chromium')
 for width,height in [(320,700),(390,844),(720,450),(768,1024),(1024,768),(1366,768),(1440,900)]:
  page=browser.new_page(viewport={'width':width,'height':height},reduced_motion='reduce');page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(BASE,wait_until='networkidle');page.evaluate('document.fonts.ready');page.wait_for_function('window.__cosmos?.frames>0')
  cards=page.locator('.evaluation-card');assert cards.count()==2
  for card,record in zip(cards.all(),data['evaluationSchedule']['firstRound']):
   assert card.locator('h3').inner_text()==record['semesters']
   facts=dict(zip(card.locator('dt').all_text_contents(),card.locator('dd').all_text_contents()))
   assert facts['Date']==record['date'] and facts['Time']==record['time'] and facts['Mode']==record['mode']
   assert ('Venue' in facts)==(record['venue'] is not None)
   if record['venue']:assert facts['Venue']==record['venue']
   assert card.locator('a').count()==0
  boxes=[c.bounding_box() for c in cards.all()]
  if width>760:assert abs(boxes[0]['y']-boxes[1]['y'])<1 and abs(boxes[0]['height']-boxes[1]['height'])<1
  else:assert boxes[1]['y']>=boxes[0]['y']+boxes[0]['height']
  assert page.locator('#final-title').inner_text()=='Final Round – External Evaluation'
  final=dict(zip(page.locator('#final-round dt').all_text_contents(),page.locator('#final-round dd').all_text_contents()))
  assert final=={'Date':'13 November 2026','Time':'4:30 PM onwards','Mode':'Offline','Venue':'ESB Seminar Hall','Evaluators':'External Judges'}
  assert page.locator('.eligibility-notice').inner_text()==data['evaluationSchedule']['finalRound']['announcement']
  assert page.locator('#rules').count()==1 and page.locator('.deadline-date').inner_text().replace('\n',' ')==data['event']['deadline'].replace(',','')
  for link in page.locator('[data-register]').all():assert link.get_attribute('href')==data['event']['registrationUrl']
  assert '13 NOV' in page.locator('.hero-meta').inner_text() and 'ESB SEMINAR HALL 2' in page.locator('.hero-meta').inner_text()
  hero=page.locator('#hero').bounding_box();conversion=page.locator('.hero-conversion').bounding_box();bottom=page.locator('.hero-bottom').bounding_box()
  assert conversion['y']+conversion['height']<=bottom['y']-4,(width,conversion,bottom)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  if height>=700:assert page.locator('#hero-register').bounding_box()['y']+page.locator('#hero-register').bounding_box()['height']<height
  page.locator('#signal').click()
  c=page.locator('.hero-conversion').bounding_box();b=page.locator('.hero-bottom').bounding_box()
  assert c['y']+c['height']<=b['y']-4,'Expanded hero control overlaps the conversion panel'
  page.locator('#signal').click();page.evaluate('scrollTo({top:0,behavior:"instant"})');page.evaluate('document.activeElement.blur()');page.goto(BASE,wait_until='networkidle')
  page.keyboard.press('Tab');assert page.locator('.skip-link').evaluate('(e)=>e===document.activeElement')
  assert page.locator('.skip-link').bounding_box()['y']>=0
  for _ in range(4):
   page.keyboard.press('Tab');assert page.evaluate('getComputedStyle(document.activeElement).outlineStyle!=="none"')
  page.locator('.event-shortcut a').click();page.wait_for_url('**/#evaluation-schedule');page.wait_for_timeout(150)
  assert page.locator('#evaluation-schedule').is_visible()
  page.locator('.deadline-callout').evaluate('(e)=>e.scrollIntoView({block:"end",behavior:"instant"})');page.wait_for_timeout(100)
  assert page.locator('.floating-register').is_hidden(),'Floating registration covers the deadline notice'
  report['layouts'].append({'viewport':[width,height],'scheduleCards':'side by side' if width>760 else 'stacked','heroOverlap':False,'keyboardFocus':True,'deadlineProtected':True})
  page.close()
 # Actual compositor zoom plus equivalent desktop 200% CSS reflow above.
 page=browser.new_page(viewport={'width':1440,'height':900},reduced_motion='reduce');page.goto(BASE);cdp=page.context.new_cdp_session(page)
 cdp.send('Emulation.setPageScaleFactor',{'pageScaleFactor':2});assert page.evaluate('visualViewport.scale')==2
 page.screenshot(path=str(OUT/'zoom-200-percent.png'));report['zoom']={'compositorScale':2,'equivalentReflow':[720,450]};page.close()
 # With animation running, inspect live scene phases and scroll without changing it.
 page=browser.new_page(viewport={'width':1440,'height':900});page.on('pageerror',lambda e:errors.append(str(e)));page.goto(BASE);page.wait_for_function('window.__cosmos?.frames>3');first=page.evaluate('({...__cosmos})')
 for selector in ['#hero','#affiliations','#evaluation-schedule','#final-round','#rules','#challenges','#judges','#faq','#registration','#gallery']:
  page.locator(selector).scroll_into_view_if_needed();page.wait_for_timeout(300)
  assert page.evaluate('document.querySelector("canvas").getContext("webgl2").getError()')==0
 last=page.evaluate('({...__cosmos})');assert last['frames']>first['frames'] and last['diskTime']>first['diskTime'] and last['holeVisible']
 report['animation']={'framesAdvanced':last['frames']-first['frames'],'clockAdvanced':last['diskTime']-first['diskTime'],'glError':0};page.close();browser.close()
assert not errors,errors
(OUT/'experience-results.json').write_text(json.dumps({**report,'errors':errors},indent=2));print(json.dumps({**report,'errors':errors},indent=2))
