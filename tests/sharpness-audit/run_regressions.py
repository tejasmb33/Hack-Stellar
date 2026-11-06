"""Run existing site regressions on the native GPU, then the gallery checks.
Software fallback and GPU context recovery use their existing dedicated fixtures.
"""
from pathlib import Path
import runpy,sys,json,shutil
from playwright.sync_api import BrowserType
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).parent
launch=BrowserType.launch
def native(self,*args,**kwargs):
 kwargs['args']=[arg for arg in kwargs.get('args',[]) if arg!='--enable-unsafe-swiftshader'];kwargs['channel']='chromium'
 return launch(self,*args,**kwargs)
BrowserType.launch=native
summary=[]
for script,result in [('browser_check.py','tests/results.json'),('sharpness_ui_check.py','tests/sharpness-audit/ui/results.json'),('lifecycle_fallback_check.py','tests/lifecycle-audit/fallback-results.json'),('lifecycle_context_check.py','tests/lifecycle-audit/context-results.json')]:
 print('RUN',script,flush=True);sys.argv=[script,'http://127.0.0.1:8017'];runpy.run_path(str(ROOT/'tests'/script),run_name='__main__')
 target=OUT/(script.removesuffix('.py')+'-results.json');shutil.copyfile(ROOT/result,target);summary.append({'test':script,'status':'passed','result':target.name})
(OUT/'regression-results.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary),flush=True)
