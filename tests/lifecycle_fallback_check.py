"""Reproduce UNORM8's false empty-space shadow and verify the precision-aware fix."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageChops,ImageStat
import io,json,sys
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'tests/lifecycle-audit'
BASE=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8000'
results=[];errors=[]
with sync_playwright() as p:
 browser=p.chromium.launch(channel='chromium')
 for mode,query in [('hdr',''),('unorm8','?ldr=1')]:
  page=browser.new_page(viewport={'width':874,'height':418});page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(BASE+'/tests/lifecycle-audit/harness.html'+query);page.wait_for_function('window.audit')
  for progress in [i/8 for i in range(9)]:
   frames=[];counts=[]
   for old in [True,False]:
    page.evaluate('(o)=>audit.render(o)',dict(time=30,progress=progress,onlyDust=True,baselineDust=old))
    shot=page.screenshot();frame=Image.open(io.BytesIO(shot)).convert('RGB');frames.append(frame)
    counts.append(frame.convert('L').point(lambda v:255 if v>10 else 0).histogram()[255])
    if mode=='unorm8' and progress in [0,.5,1]:(OUT/f'fallback-{"before" if old else "after"}-p{progress}.png').write_bytes(shot)
   difference=sum(ImageStat.Stat(ImageChops.difference(*frames)).mean)/3
   entry=dict(mode=mode,progress=progress,beforeVisiblePixels=counts[0],afterVisiblePixels=counts[1],difference=difference);results.append(entry)
   if mode=='hdr':assert difference==0,entry
   else:
    assert counts[1]>counts[0],entry
    if progress==1:assert counts[1]>counts[0]*2,entry
  page.close()
 browser.close()
assert not errors,errors
(OUT/'fallback-results.json').write_text(json.dumps(dict(status='passed',results=results,errors=errors),indent=2)+'\n')
print(json.dumps(dict(status='passed',cases=len(results),receded=results[-1],errors=errors),indent=2))
