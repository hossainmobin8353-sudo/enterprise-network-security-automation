import json, tempfile, unittest
from pathlib import Path
from netguard.core import canonical,sha,assess,build_plan,detect,load_repo
from netguard.approval import issue,verify
ROOT=Path(__file__).resolve().parents[1]
class ConfigurationTests(unittest.TestCase):
 def test_inventory(self):
  p,b,o=load_repo(ROOT);self.assertEqual(len(b),3)
 def test_detect_expected_critical(self):
  result=assess(ROOT);self.assertEqual(result['finding_count'],3)
  self.assertEqual(sum(x['severity']=='critical' for x in result['findings']),2)
 def test_clean_baselines(self):
  p,b,o=load_repo(ROOT)
  for name,config in b.items():self.assertEqual(detect(name,config,config,p),[])
 def test_normalization(self):self.assertEqual(canonical('! comment\n hostname A \n'), 'hostname A\n')
 def test_hash_changes(self):self.assertNotEqual(sha('hostname A'),sha('hostname B'))
 def test_plan(self):
  plan=build_plan(ROOT,'CORE-SW1');self.assertIn('+ ip access-group GUEST_FILTER in',plan['diff'])
 def test_unknown_plan(self):
  with self.assertRaises(ValueError):build_plan(ROOT,'UNKNOWN')
 def test_missing_device(self):
  with tempfile.TemporaryDirectory() as t:
   import shutil
   shutil.copytree(ROOT/'configs',Path(t)/'configs');shutil.copytree(ROOT/'data',Path(t)/'data')
   (Path(t)/'configs/observed/EDGE-R1.cfg').unlink()
   with self.assertRaises(ValueError):load_repo(Path(t))
 def test_forbidden_telnet(self):
  p,b,o=load_repo(ROOT)
  f=detect('EDGE-R1',b['EDGE-R1'],b['EDGE-R1']+'transport input telnet\n',p)
  self.assertTrue(any(x.rule=='FORBIDDEN_CONFIG' for x in f))
class ApprovalTests(unittest.TestCase):
 SECRET='long-secret-for-offline-testing-only-123'
 def test_valid(self):
  token=issue(self.SECRET,'CORE','abc',now=100)
  self.assertTrue(verify(self.SECRET,token,'CORE','abc',now=150))
 def test_expired(self):
  token=issue(self.SECRET,'CORE','abc',ttl=5,now=100)
  self.assertFalse(verify(self.SECRET,token,'CORE','abc',now=106))
 def test_wrong_device(self):
  token=issue(self.SECRET,'CORE','abc',now=100)
  self.assertFalse(verify(self.SECRET,token,'EDGE','abc',now=101))
 def test_wrong_hash(self):
  token=issue(self.SECRET,'CORE','abc',now=100)
  self.assertFalse(verify(self.SECRET,token,'CORE','def',now=101))
 def test_tamper(self):
  token=issue(self.SECRET,'CORE','abc',now=100)
  self.assertFalse(verify(self.SECRET,token+'x','CORE','abc',now=101))
 def test_short_secret(self):
  with self.assertRaises(ValueError):issue('short','CORE','abc')
 def test_bad_ttl(self):
  with self.assertRaises(ValueError):issue(self.SECRET,'CORE','abc',ttl=901)
if __name__=='__main__':unittest.main()
