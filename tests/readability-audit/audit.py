"""Scan every public page at phone, tablet and desktop sizes.
Contrast uses computed colors over both white and black scene extremes; foreground
surfaces are composited through ancestors. This is not a full WCAG certification.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).parent;BASE='http://127.0.0.1:8018';contrast=(OUT/'contrast.js').read_text();errors=[];results=[]
paths=['/','/problem-statements/','/credits.html']+['/problem-statements/'+p['slug']+'/' for p in json.loads((ROOT/'content.json').read_text())['problems']]
with sync_playwright() as p:
 browser=p.chromium.launch(channel='chromium')
 for w,h in [(320,700),(768,1024),(1440,900)]:
  page=browser.new_page(viewport={'width':w,'height':h},reduced_motion='reduce');page.on('pageerror',lambda e:errors.append(str(e)))
  for path in paths:
   page.goto(BASE+path,wait_until='networkidle');page.evaluate('document.fonts.ready')
   if path=='/':page.locator('#faq details').evaluate_all('(nodes)=>nodes.forEach(e=>e.open=true)')
   c=page.evaluate(contrast)
   layout=page.evaluate('''()=>({overflow:document.documentElement.scrollWidth-innerWidth,bad:[...document.querySelectorAll('main *,header *,footer *')].filter(e=>{const s=getComputedStyle(e),r=e.getBoundingClientRect();return !e.closest('.sr-only,[hidden],.gallery-lightbox')&&s.display!=='none'&&r.width>0&&(r.right>innerWidth+1||r.left< -1)}).slice(0,8).map(e=>[e.tagName,e.className,e.textContent.trim().slice(0,60)])})''')
   results.append(dict(width=w,path=path,contrast=c,layout=layout))
   if path in ['/problem-statements/ps-17/','/problem-statements/ps-18/','/problem-statements/ps-21/']:
    page.screenshot(path=str(OUT/f'after-{w}-{path.strip("/").replace("/","-")}.png'),full_page=True)
  page.close()
 browser.close()
report={'pages':len(paths),'cases':len(results),'textChecks':sum(x['contrast']['count'] for x in results),'errors':errors,'results':results};(OUT/'audit-results.json').write_text(json.dumps(report,indent=2))
failed=[{'width':r['width'],'path':r['path'],'contrast':r['contrast']['failures'],'small':r['contrast']['small'],'layout':r['layout']} for r in results if r['contrast']['failures'] or r['contrast']['small'] or r['layout']['overflow'] or r['layout']['bad']]
print(json.dumps({'cases':len(results),'textChecks':report['textChecks'],'failedCases':len(failed),'examples':failed[:3],'errors':errors},indent=2))
assert not failed and not errors,(failed[:3],errors)
