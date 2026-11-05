"""Five-second hands-off motion review. No scrolling, mouse movement or time overrides.
The saved frames/recording must be visually reviewed; image differences alone
are not evidence that motion looks convincing to a visitor.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageChops,ImageStat
import json,sys,math
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'tests/visual-evidence'
BASE=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8000'
with sync_playwright() as p:
 browser=p.chromium.launch(channel='chromium')
 context=browser.new_context(viewport={'width':1440,'height':900},record_video_dir=str(OUT),record_video_size={'width':1440,'height':900})
 page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
 page.goto(BASE,wait_until='networkidle');page.wait_for_function('window.__cosmos.frames>2')
 # The video includes page entry, but frame comparisons begin only after its
 # existing canvas fade has settled. Entry opacity must not inflate the signal.
 page.wait_for_function('Number(getComputedStyle(document.querySelector("canvas")).opacity)>.999')
 snapshots=[]
 for label,wait in [('0s',0),('2s',2000),('5s',3000)]:
  if wait:page.wait_for_timeout(wait)
  page.screenshot(path=str(OUT/f'motion-{label}.png'))
  snapshots.append(page.evaluate('({wall:performance.now(),scroll:scrollY,...window.__cosmos})'))
 assert all(s['scroll']==0 for s in snapshots)
 assert not errors,errors
 before=snapshots[0];after=snapshots[-1]
 report={'review':'Hands-off first five seconds; no mouse, scroll, reduced-motion emulation or time override','snapshots':snapshots,'measuredFPS':(after['frames']-before['frames'])*1000/(after['wall']-before['wall']),'cameraDistanceMoved':math.dist(before['camera'],after['camera']),'errors':errors}
 initial=Image.open(OUT/'motion-0s.png').convert('RGB')
 for label in ['2s','5s']:
  later=Image.open(OUT/f'motion-{label}.png').convert('RGB')
  difference=ImageChops.difference(initial.crop((700,220,1440,850)),later.crop((700,220,1440,850)))
  report[f'diskRegionChange{label}']=sum(ImageStat.Stat(difference).mean)/3
 # A bounded orbit can return near its initial position. Check the sampled
 # excursion, not just endpoint distance; the capture still needs visual review.
 assert max(math.dist(a['camera'],b['camera']) for a in snapshots for b in snapshots)>.2,report
 assert report['diskRegionChange2s']>3,report
 assert report['diskRegionChange5s']>3,report
 video=page.video;context.close();video.save_as(str(OUT/'five-seconds-hands-off.webm'));video.path().unlink(missing_ok=True)
 browser.close()
(OUT/'motion-review.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='snapshots'},indent=2))
