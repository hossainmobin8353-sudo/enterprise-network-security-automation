"""Scoped HMAC-signed short-lived tokens for offline simulated remediation."""
import base64, hashlib, hmac, json, time

def _b64(data:bytes)->str: return base64.urlsafe_b64encode(data).decode().rstrip('=')
def _unb64(data:str)->bytes: return base64.urlsafe_b64decode(data+'='*(-len(data)%4))
def issue(secret:str,device:str,expected_hash:str,ttl:int=300,now:int|None=None)->str:
    if not secret or len(secret)<24: raise ValueError('Approval signing secret must be at least 24 characters')
    if not 1<=ttl<=900: raise ValueError('TTL must be 1-900 seconds')
    ts=int(time.time()) if now is None else now
    payload={'device':device,'expected_hash':expected_hash,'expires':ts+ttl,'issued':ts,'purpose':'simulation-only'}
    body=_b64(json.dumps(payload,sort_keys=True,separators=(',',':')).encode())
    sig=_b64(hmac.new(secret.encode(),body.encode(),hashlib.sha256).digest())
    return body+'.'+sig

def verify(secret:str,token:str,device:str,expected_hash:str,now:int|None=None)->bool:
    try:
        body,sig=token.split('.')
        actual=_b64(hmac.new(secret.encode(),body.encode(),hashlib.sha256).digest())
        payload=json.loads(_unb64(body))
        ts=int(time.time()) if now is None else now
        return (hmac.compare_digest(actual,sig) and payload['device']==device
          and payload['expected_hash']==expected_hash and payload['purpose']=='simulation-only'
          and payload['issued']<=ts<payload['expires'])
    except (ValueError,KeyError,TypeError,UnicodeError):return False
