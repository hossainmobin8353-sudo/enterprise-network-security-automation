"""Offline network configuration policy engine. No network connections are made."""
from dataclasses import dataclass, asdict
from pathlib import Path
import hashlib, json, re, difflib

@dataclass(frozen=True)
class Finding:
    device: str
    rule: str
    severity: str
    detail: str

def canonical(config: str) -> str:
    return '\n'.join(line.strip() for line in config.splitlines()
                     if line.strip() and not line.lstrip().startswith('!')) + '\n'

def sha(text: str) -> str:
    return hashlib.sha256(canonical(text).encode()).hexdigest()

def detect(device: str, baseline: str, observed: str, policy: dict) -> list[Finding]:
    results = []
    lines = canonical(observed).splitlines()
    actual = '\n'.join(lines)
    if sha(baseline) != sha(observed):
        results.append(Finding(device,'CONFIG_DRIFT','medium','Observed config differs from approved baseline'))
    for forbidden in policy['forbidden_patterns']:
        if re.search(forbidden,actual,re.I|re.M):
            results.append(Finding(device,'FORBIDDEN_CONFIG','high',f'Forbidden pattern detected: {forbidden}'))
    for required in policy['required_lines'].get(device,[]):
        if required not in lines:
            results.append(Finding(device,'REQUIRED_MISSING','high',f'Missing baseline control: {required}'))
    # Policy: guest VLAN 30 may not access management segment 10.99.0.0/24
    if device == 'CORE-SW1':
        if 'deny ip 10.30.0.0 0.0.0.255 10.99.0.0 0.0.0.255' not in lines:
            results.append(Finding(device,'GUEST_MGMT_ISOLATION','critical','Guest-to-management deny ACL not present'))
        if 'ip access-group GUEST_FILTER in' not in lines:
            results.append(Finding(device,'GUEST_ACL_BINDING','critical','Guest ACL not applied inbound'))
    return results

def load_repo(root: Path) -> tuple[dict,dict,dict]:
    policy=json.loads((root/'data/policy.json').read_text())
    base={q.stem:q.read_text() for q in sorted((root/'configs/baseline').glob('*.cfg'))}
    obs={q.stem:q.read_text() for q in sorted((root/'configs/observed').glob('*.cfg'))}
    if set(base)!=set(obs):
        raise ValueError('Baseline and observed device sets must match')
    if set(base)!=set(policy['devices']):
        raise ValueError('Device inventory and configuration files must match')
    return policy,base,obs

def assess(root: Path) -> dict:
    policy,base,obs=load_repo(root)
    findings=[asdict(item) for device in sorted(base) for item in detect(device,base[device],obs[device],policy)]
    return {'devices':len(base),'findings':findings,'finding_count':len(findings),
            'baseline_hashes':{k:sha(v) for k,v in base.items()},
            'observed_hashes':{k:sha(v) for k,v in obs.items()}}

def build_plan(root:Path,device:str)->dict:
    policy,base,obs=load_repo(root)
    if device not in base: raise ValueError('Device not in approved inventory')
    diff=''.join(difflib.unified_diff(obs[device].splitlines(True),base[device].splitlines(True),
                 fromfile='observed',tofile='baseline'))
    return {'device':device,'action':'REPLACE_SIMULATED_CONFIG',
            'baseline_sha256':sha(base[device]),'observed_sha256':sha(obs[device]),
            'diff':diff,'warning':'Simulation only. Never applies configurations to physical devices.'}
