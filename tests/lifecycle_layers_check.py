"""Actual-pipeline layer isolation; accelerated ages are diagnostic, not real visits.
Camera/sky/dust cannot inflate disk motion. Dust groups use the real depth target.
Usage: python tests/lifecycle_layers_check.py [base-url].
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageChops,ImageStat,ImageMath,ImageFilter,ImageDraw
import io,json,sys
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'tests/lifecycle-audit'
BASE=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8000'
report={'disk':[],'dust':[],'appearance':[],'handoffs':[]};errors=[]
def rgb(shot):return Image.open(io.BytesIO(shot)).convert('RGB')
def mask_for(image):
 r,g,b=image.split();return ImageMath.unsafe_eval('convert((r>80)*(r*100>b*108)*255,"L")',r=r,b=b)
def motion(a,b):
 mask=mask_for(a)
 return {str(radius):sum(ImageStat.Stat(ImageChops.difference(a.filter(ImageFilter.GaussianBlur(radius)),b.filter(ImageFilter.GaussianBlur(radius))),mask).mean)/3 for radius in [0,4,8]}
with sync_playwright() as p:
 browser=p.chromium.launch(channel='chromium')
 for profile,width,height,normal in [('desktop',874,418,.85),('mobile',390,844,.72)]:
  page=browser.new_page(viewport={'width':width,'height':height},is_mobile=profile=='mobile',has_touch=profile=='mobile')
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  page.goto(BASE+'/tests/lifecycle-audit/harness.html');page.wait_for_function('window.audit')
  def render(**options):
   page.evaluate('(o)=>audit.render(o)',options);return rgb(page.screenshot())
  for progress in [i/8 for i in range(9)]:
   for age in [0,30,300,7200]:
    for scale in [normal,.4]:
     frames=[render(time=age+dt,progress=progress,scale=scale,noDust=True,noSky=True) for dt in [0,2]]
     entry=dict(profile=profile,progress=progress,age=age,scale=scale,motion=motion(*frames));report['disk'].append(entry)
     assert entry['motion']['4']>.5,entry
   for group in ['orbital','world']:
    frames=[render(time=300+dt,progress=progress,scale=normal,onlyDust=True,group=group) for dt in [0,2]]
    lit=frames[0].convert('L').point(lambda v:255 if v>10 else 0).histogram()[255]
    changed=ImageChops.difference(*frames).convert('L').point(lambda v:255 if v>5 else 0).histogram()[255]
    entry=dict(profile=profile,progress=progress,group=group,visiblePixels=lit,movingPixels=changed);report['dust'].append(entry)
    assert lit>10 and changed>5,entry
    if progress in [0,.5,1]:
     for dt,frame in zip([0,2],frames):frame.save(OUT/f'{profile}-{group}-p{progress}-{dt}s.png')
  # First fourteen seconds retain the exact original field (compiler rounding allowed).
  for age in [0,3,7.9,13.9]:
   for progress in [0,.5,1]:
    frames=[render(time=age,progress=progress,baseline=old,scale=normal) for old in [True,False]]
    difference=sum(ImageStat.Stat(ImageChops.difference(*frames)).mean)/3
    report['appearance'].append(dict(profile=profile,age=age,progress=progress,difference=difference));assert difference<.01
  for age in [8,16,24,32,300,7200]:
   frames=[render(time=age+dt,progress=.5,scale=normal,noDust=True,noSky=True) for dt in [-.001,0,.001]]
   left=motion(frames[0],frames[1])['0'];right=motion(frames[1],frames[2])['0']
   entry=dict(profile=profile,age=age,left=left,right=right);report['handoffs'].append(entry)
   assert max(left,right)<1,entry
  # Reproduce loss of coherent flow: raw pixel noise must not count as recovery.
  comparison=[]
  for old in [True,False]:
   frames=[render(time=300+dt,progress=.5,scale=normal,noDust=True,noSky=True,baseline=old) for dt in [0,2]]
   comparison.append(motion(*frames))
   for dt,frame in zip([0,2],frames):frame.save(OUT/f'{profile}-disk-{"before" if old else "after"}-{dt}s.png')
  assert comparison[1]['8']>comparison[0]['8']*2,(profile,comparison)
  report[profile+'CoherenceComparison']=comparison
  page.close()
 browser.close()
assert not errors,errors
report.update(errors=errors,status='passed',note='Accelerated ages, fixed camera and diagnostic layer isolation; not elapsed wall-clock endurance.')
(OUT/'layer-results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':report['status'],'diskCases':len(report['disk']),'dustCases':len(report['dust']),'appearanceCases':len(report['appearance']),'handoffs':len(report['handoffs']),'desktopCoherence':report['desktopCoherenceComparison'],'mobileCoherence':report['mobileCoherenceComparison'],'errors':errors},indent=2))
