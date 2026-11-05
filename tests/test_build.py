"""Protect the authoritative catalogue, full-domain coverage and complete generated collection."""
import copy,json,re,subprocess,tempfile,unittest,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
EXPECTED_DOMAINS=['AI','NLP','HR Tech','Web Development','Automation','Retail Tech','Voice AI','Machine Learning','Cloud Computing','Software Engineering','Networking','Algorithm Transparency','IoT','Agriculture','Cybersecurity','Digital Media','Transportation','Industrial Automation','E-Commerce','Logistics','Energy Management']
class BuildTests(unittest.TestCase):
 def build(self,data):
  temporary=tempfile.TemporaryDirectory();self.addCleanup(temporary.cleanup);root=Path(temporary.name)
  (root/'scripts').mkdir();(root/'problem-statements').mkdir()
  (root/'scripts/build.py').write_text((ROOT/'scripts/build.py').read_text());(root/'content.json').write_text(json.dumps(data))
  subprocess.run(['python3',str(root/'scripts/build.py')],check=True,capture_output=True)
  return root
 def test_exact_seventeen_official_records(self):
  data=json.loads((ROOT/'content.json').read_text())
  official=re.findall(r'### PS (\d{2}) — (.*?)\n\n\*\*Domain:\*\* (.*?)\n\n\*\*Description:\*\* (.*?)\n\n\*\*Challenge:\*\* (.*?)(?=\n\n### PS|\n\n---)',(ROOT/'REFINEMENT_REQUIREMENTS.md').read_text(),re.S)
  self.assertEqual(len(official),17);self.assertEqual(len(data['problems']),21)
  for record,(number,title,domain,description,challenge) in zip(data['problems'],official):
   self.assertEqual(record['id'],f'PS–{number}');self.assertEqual(record['title'],title)
   self.assertEqual(record['domainLabel'],domain);self.assertEqual(record['domains'],domain.split(' / '))
   self.assertEqual(record['description'],description);self.assertEqual(record['challenge'],challenge)
  tags=list(dict.fromkeys(tag for record in data['problems'] for tag in record['domains']))
  self.assertEqual(tags,EXPECTED_DOMAINS)
 def test_all_pages_domains_counts_and_no_company_mapping(self):
  data=json.loads((ROOT/'content.json').read_text());root=self.build(data)
  directory=(root/'problem-statements/index.html').read_text()
  self.assertEqual(directory.count('<article class="problem-card"'),21)
  self.assertIn('Showing 21 of 21 problem statements',directory);self.assertIn('21 Challenges. Endless Possibilities.',directory)
  for domain in EXPECTED_DOMAINS:self.assertIn(f'<option>{domain}</option>',directory)
  self.assertIn('<option value="" selected>All Domains</option>',directory)
  self.assertNotIn('<p class="source">',directory)
  self.assertEqual(len(list((root/'problem-statements').glob('*/index.html'))),21)
  for record in data['problems']:
   detail=(root/'problem-statements'/record['slug']/'index.html').read_text()

   if record.get('format')=='statement':self.assertIn('Problem Statement',detail);self.assertIn(record['subtitle'],detail)
   else:self.assertIn('Problem Description',detail);self.assertIn('Your Challenge',detail)
   self.assertNotIn('SOURCE / CONTRIBUTOR',detail)
  home=(root/'index.html').read_text();self.assertIn('Abhijeet Verma',home);self.assertNotIn('Abhijit Verma',home)
  self.assertIn('https://www.linkedin.com/in/gokarajuabhijit/',home)
 def test_no_hardcoded_total_and_numeric_order(self):
  data=json.loads((ROOT/'content.json').read_text());template=data['problems'][0]
  data['problems']=[]
  # Synthetic regression fixtures exist only in this isolated temporary build.
  for index in range(31,0,-1):
   record=copy.deepcopy(template);record.update(id=f'PS–{index:02}',slug=f'test-only-{index:02}',title=f'Test-only fixture {index}',published=index<=30);data['problems'].append(record)
  root=self.build(data);directory=(root/'problem-statements/index.html').read_text()
  self.assertEqual(directory.count('<article class="problem-card"'),30)
  self.assertIn('Showing 30 of 30 problem statements',directory);self.assertNotIn('test-only-31',directory)
  self.assertLess(directory.index('test-only-01'),directory.index('test-only-30'))
class HackStellarTests(unittest.TestCase):
 def test_original_records_and_finalized_renderer(self):
  data=json.loads((ROOT/'content.json').read_text())
  self.assertEqual(hashlib.sha256(json.dumps(data['problems'][:17],sort_keys=True,ensure_ascii=False).encode()).hexdigest(),'fb47f3040ee5ed7f4ac4bfb61c84fa7b5067e0446b81c77865c0f273b87e5f2e')
  for name,digest in json.loads((ROOT/'tests/finalized_scene_sha256.json').read_text()).items():
   self.assertEqual(hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),digest,name)
 def test_new_briefs_are_exact_and_domains_unconfirmed(self):
  data=json.loads((ROOT/'content.json').read_text())
  official=re.findall(r'^PS (18|19|20|21) — ([^\n]+)\nSubtitle: ([^\n]+)\nProblem Statement:\n(.*?)(?=\nPS (?:18|19|20|21) —|\n6\.)',(ROOT/'HACKSTELLAR_REQUIREMENTS.md').read_text(),re.M|re.S)
  self.assertEqual(len(official),4)
  for record,(number,title,subtitle,statement) in zip(data['problems'][17:],official):
   self.assertEqual(record['id'],'PS–'+number);self.assertEqual(record['title'],title)
   self.assertEqual(record['subtitle'],subtitle);self.assertEqual(record['description'],statement.strip())
   self.assertEqual(record['domains'],[]);self.assertEqual(record['domainLabel'],'')
 def test_all_supplied_photographs_and_current_identity(self):
  data=json.loads((ROOT/'content.json').read_text());self.assertEqual(len(data['gallery']),8)
  self.assertEqual(len(set(p['sourceFilename'] for p in data['gallery'])),8)
  for p in data['gallery']:
   self.assertTrue((ROOT/p['src'].lstrip('/')).is_file());self.assertTrue((ROOT/p['thumbnail'].lstrip('/')).is_file())
  for p in [ROOT/'index.html',ROOT/'credits.html',*(ROOT/'problem-statements').glob('**/index.html')]:
   text=p.read_text();self.assertIn('HackStellar',text);self.assertNotIn('INTERSTELLAR',text)
  self.assertEqual(data['event']['prize'],'₹25,000');self.assertEqual(data['event']['venue'],'ESB Seminar Hall 2')
if __name__=='__main__':unittest.main()
