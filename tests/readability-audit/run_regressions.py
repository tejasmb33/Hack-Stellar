"""Use the existing website and gallery regressions on the native local GPU."""
from pathlib import Path
from playwright.sync_api import BrowserType
import runpy,sys,json,shutil
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).parent;original=BrowserType.launch
BrowserType.launch=lambda self,*args,**kwargs:original(self,*args,**{**kwargs,'channel':'chromium','args':[a for a in kwargs.get('args',[]) if a!='--enable-unsafe-swiftshader']})
for script,args,result in [('browser_check.py',['http://127.0.0.1:8018'],'tests/results.json'),('hackstellar_check.py',['http://127.0.0.1:8018','http://127.0.0.1:8000'],'tests/hackstellar/results.json')]:
 print('RUN',script,flush=True);sys.argv=[script]+args;runpy.run_path(str(ROOT/'tests'/script),run_name='__main__')
 shutil.copyfile(ROOT/result,OUT/(script.removesuffix('.py')+'-results.json'))
