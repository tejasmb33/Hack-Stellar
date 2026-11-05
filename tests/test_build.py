"""Regression checks: totals must reflect the complete published collection, never a hard-coded three."""
import copy,json,subprocess,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class BuildTests(unittest.TestCase):
 def build(self,content):
  directory=tempfile.TemporaryDirectory();self.addCleanup(directory.cleanup)
  root=Path(directory.name);(root/'scripts').mkdir();(root/'problem-statements').mkdir()
  (root/'scripts/build.py').write_text((ROOT/'scripts/build.py').read_text())
  (root/'content.json').write_text(json.dumps(content))
  subprocess.run(['python3',str(root/'scripts/build.py')],check=True,capture_output=True)
  return root
 def test_complete_published_collection_and_no_default_filter(self):
  content=json.loads((ROOT/'content.json').read_text());template=content['problems'][0]
  # Isolated, explicitly synthetic test fixtures; never written to the real content collection.
  content['problems']=[]
  for index in range(1,32):
   fixture=copy.deepcopy(template);fixture.update(id=f'PS–{index:02}',slug=f'test-only-{index:02}',title=f'Test-only fixture {index}',published=index<=30);content['problems'].append(fixture)
  root=self.build(content);html=(root/'problem-statements/index.html').read_text()
  self.assertEqual(html.count('<article class="problem-card"'),30)
  self.assertIn('Showing all 30 problem statements',html)
  self.assertIn('All Domains',html)
  self.assertIn('<option value="" selected>All Domains</option>',html)
  self.assertNotIn('test-only-31',html)
  self.assertEqual(len(list((root/'problem-statements').glob('*/index.html'))),30)
 def test_real_content_branding_and_private_attribution(self):
  data=json.loads((ROOT/'content.json').read_text());root=self.build(data)
  home=(root/'index.html').read_text();directory=(root/'problem-statements/index.html').read_text()
  self.assertIn('INTERSTELLAR : THE BUILDATHON',home)
  self.assertIn('Showing all 3 problem statements',directory)
  self.assertNotIn('<p class="source">',directory)
  self.assertIn('Gokaraju Abhijit',home);self.assertIn('Ribbon Communications',home);self.assertIn('BITS Pilani',home)
  self.assertNotIn('Abhijit Verma',home)
  for p in data['problems']:
   detail=(root/'problem-statements'/p['slug']/'index.html').read_text()
   self.assertNotIn('SOURCE / CONTRIBUTOR',detail)
  self.assertEqual(json.loads((ROOT/'content.json').read_text()),data)
if __name__=='__main__':unittest.main()
