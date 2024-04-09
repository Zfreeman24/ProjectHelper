import requests

apikey='..................'# the web api key

idToken='eyJh1pVjuYvfX72ewSqUxRNUNoGKgdhsaYdeOjs9OsQ......'#token

def VerifyEmail(idToken):
    headers = {
        'Content-Type': 'application/json',
    }
    data='{"requestType":"VERIFY_EMAIL","idToken":"'+idToken+'"}'
    r = requests.post('https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={}'.format(apikey), headers=headers, data=data)
    if 'error' in r.json().keys():
        return {'status':'error','message':r.json()['error']['message']}
    if 'email' in r.json().keys():
        return {'status':'success','email':r.json()['email']}