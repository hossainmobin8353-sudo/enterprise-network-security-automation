import argparse, json, os, sys
from pathlib import Path
from .core import assess,build_plan,load_repo,sha
from .approval import issue,verify

def main(argv=None):
    ap=argparse.ArgumentParser(description='Offline network drift and approval lab')
    ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[2])
    sub=ap.add_subparsers(dest='command',required=True)
    sub.add_parser('scan')
    plan=sub.add_parser('plan');plan.add_argument('--device',required=True)
    approve=sub.add_parser('approve');approve.add_argument('--device',required=True)
    simulate=sub.add_parser('simulate');simulate.add_argument('--device',required=True);simulate.add_argument('--token',required=True)
    a=ap.parse_args(argv);root=a.root
    try:
        if a.command=='scan': result=assess(root)
        elif a.command=='plan':result=build_plan(root,a.device)
        elif a.command=='approve':
            policy,base,obs=load_repo(root)
            if a.device not in obs: raise ValueError('Unknown device')
            secret=os.environ.get('NETGUARD_APPROVAL_SECRET','')
            result={'device':a.device,'token':issue(secret,a.device,sha(obs[a.device])),'scope':'simulation-only'}
        else:
            policy,base,obs=load_repo(root)
            if a.device not in obs: raise ValueError('Unknown device')
            secret=os.environ.get('NETGUARD_APPROVAL_SECRET','')
            if not verify(secret,a.token,a.device,sha(obs[a.device])):raise ValueError('Invalid, expired, or mismatched approval')
            # Deliberately NO write to configs/observed or any device.
            result={'device':a.device,'simulated':True,'would_change':sha(base[a.device])!=sha(obs[a.device]),
                    'note':'Approval validated. No configuration changes performed.'}
        print(json.dumps(result,indent=2));return 0
    except (OSError,ValueError) as e:
        print('ERROR: '+str(e),file=sys.stderr);return 2
if __name__=='__main__':sys.exit(main())
