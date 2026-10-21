import os, subprocess, sys, json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class IntegrationTests(unittest.TestCase):
 def run_cli(self,*args,secret='test-secret-1234567890-abcdef'):
  env=os.environ.copy();env['PYTHONPATH']=str(ROOT/'src');env['NETGUARD_APPROVAL_SECRET']=secret
  return subprocess.run([sys.executable,'-m','netguard.cli',*args],env=env,capture_output=True,text=True,cwd=ROOT)
 def test_scan_cli(self):
  r=self.run_cli('scan');self.assertEqual(r.returncode,0,r.stderr)
  self.assertEqual(json.loads(r.stdout)['finding_count'],3)
 def test_plan_cli(self):
  r=self.run_cli('plan','--device','CORE-SW1');self.assertEqual(r.returncode,0)
  self.assertIn('GUEST_FILTER',json.loads(r.stdout)['diff'])
 def test_approved_simulation(self):
  r=self.run_cli('approve','--device','CORE-SW1');self.assertEqual(r.returncode,0,r.stderr)
  token=json.loads(r.stdout)['token']
  x=self.run_cli('simulate','--device','CORE-SW1','--token',token)
  self.assertEqual(x.returncode,0,x.stderr)
  self.assertTrue(json.loads(x.stdout)['simulated'])
 def test_reject_fake_approval(self):
  r=self.run_cli('simulate','--device','CORE-SW1','--token','invalid')
  self.assertNotEqual(r.returncode,0)
if __name__=='__main__':unittest.main()
