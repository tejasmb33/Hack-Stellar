"""Software mobile-viewport profile, reduced motion and WebGL recovery.
This is not a physical phone benchmark. Usage: python tests/mobile_scene_check.py [base-url].
"""
from playwright.sync_api import sync_playwright
from pathlib import Path
import json
import sys
ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'tests/visual-evidence'
BASE=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8000'
with sync_playwright() as p:
 browser=p.chromium.launch(args=['--enable-unsafe-swiftshader'])
 page=browser.new_page(viewport={'width':390,'height':844},device_scale_factor=1,is_mobile=True,has_touch=True)
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(BASE,wait_until='networkidle');page.wait_for_function('window.__cosmos.frames>3');page.wait_for_timeout(9000)
 a=page.evaluate('({wall:performance.now(),...window.__cosmos})');page.wait_for_timeout(5000);b=page.evaluate('({wall:performance.now(),...window.__cosmos})')
 report={'viewport':[390,844],'emulation':'Mobile viewport, desktop CPU/SwiftShader; not a physical phone','fps':(b['frames']-a['frames'])*1000/(b['wall']-a['wall']),'clockRatio':(b['diskTime']-a['diskTime'])*1000/(b['wall']-a['wall']),'state':b}
 page.emulate_media(reduced_motion='reduce');page.wait_for_timeout(200)
 t=page.evaluate('window.__cosmos.diskTime');page.wait_for_timeout(300);assert page.evaluate('window.__cosmos.diskTime')==t
 page.evaluate("window.testLoss=document.querySelector('canvas').getContext('webgl2').getExtension('WEBGL_lose_context');window.testLoss.loseContext()")
 page.wait_for_function('document.body.classList.contains("scene-unavailable")');page.evaluate('window.testLoss.restoreContext()')
 page.wait_for_function('document.body.classList.contains("scene-ready")');page.wait_for_timeout(400)
 assert page.locator('#hero-register').is_visible()
 report.update({'reducedMotion':'passed','contextRecovery':'passed','errors':errors});assert not errors,errors
 (out/'mobile-performance.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
 browser.close()
