"""Protect the corrected organizer schedule, preserved event data and renderer."""
from pathlib import Path
import unittest,json,hashlib,subprocess
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'tests/readability-audit'
class ReadabilityScheduleTests(unittest.TestCase):
 def test_corrected_schedule_and_exact_announcements(self):
  data=json.loads((ROOT/'content.json').read_text());first=data['evaluationSchedule']['firstRound'];final=data['evaluationSchedule']['finalRound']
  self.assertEqual([(x['semesters'],x['date'],x['time'],x['mode'],x['venue']) for x in first],[('3rd Semester','12 November 2026','7:00 PM onwards','Online',None),('1st & 5th Semesters','13 November 2026','11:00 AM onwards','Offline','ESB Seminar Hall')])
  self.assertEqual((final['title'],final['date'],final['time'],final['mode'],final['venue'],final['evaluators'],final['eligibility']),('Final Round – External Evaluation','13 November 2026','4:30 PM onwards','Offline','ESB Seminar Hall','External Judges','Qualified top teams only'))
  self.assertEqual(data['announcements']['prototype'],'Teams can start building their prototypes immediately and directly present their completed prototypes on the evaluation day.')
  self.assertEqual(data['announcements']['communication'],'All further updates and announcements regarding HackStellar will be communicated through the official website and WhatsApp groups.')
  home=(ROOT/'index.html').read_text()
  for text in data['announcements'].values():self.assertIn(text,home)
  self.assertIn(final['announcement'],home);self.assertIn(final['qualification'],home)
  self.assertEqual(home.count('id="rules-title"'),1)
  self.assertLess(home.index('id="evaluation-schedule"'),home.index('id="challenges"'))
  self.assertNotIn('12 November 2026 at 11:59',home);self.assertIn('11 November 2026, 11:59 PM IST',home)
 def test_unrelated_content_and_scene_unchanged(self):
  before=json.loads((OUT/'before-content.json').read_text());after=json.loads((ROOT/'content.json').read_text())
  for key in before:
   if key!='event':self.assertEqual(before[key],after[key],key)
  for key in before['event']:
   if key not in ('deadline','start'):self.assertEqual(before['event'][key],after['event'][key],key)
  self.assertEqual(after['event']['deadline'],'11 November 2026, 11:59 PM IST')
  self.assertEqual(after['event']['start'],'11:00 AM IST')
  hashes=json.loads((OUT/'initial-file-hashes.json').read_text())
  for name,digest in hashes.items():
   if name=='scene.js' or name.startswith(('visuals/','vendor/','assets/')):
    self.assertEqual(hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),digest,name)
  style=(ROOT/'styles.css').read_text();self.assertTrue(style.startswith((OUT/'before-styles.css').read_text()))
  addition=style[len((OUT/'before-styles.css').read_text()):]
  for forbidden in ['.universe','.scene-shade','.scene-fallback','#universe-canvas']:
   self.assertNotIn(forbidden,addition)
if __name__=='__main__':unittest.main()
