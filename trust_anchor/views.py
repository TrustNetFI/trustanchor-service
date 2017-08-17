import asyncio
import json

from django.shortcuts import render
from django.http import HttpResponse

from trust_anchor.trustanchor import TrustAnchor

ta = None

def index(request):
    error = {}
    reg_result = None
    reg_error = None
    did = ''
    verkey = ''
    captcha = ''
    
    if request.method == 'POST':
        did = request.POST['did'].strip()
        verkey = request.POST['verkey'].strip()
        captcha = request.POST['captcha'].strip()
        if not did:
            error["did"] = "Please supply a proper DID"
            print("error did")
        if not verkey:
            error["verkey"] = "Please supply a proper verification key"
        if captcha != "CAPTCHA":
            error["captcha"] = "CAPTCHA check failed"

        if not error:
            loop = asyncio.new_event_loop()
            res = loop.run_until_complete(register(did, verkey))
            loop.close()
            if 'error' in res:
                reg_error = res['error']
            if 'result' in res:
                reg_result = res['result']
                reg_result['data'] = json.loads(reg_result['data'])
                did = ""
                verkey = ""
                captcha = ""
    elif request.method == 'GET':
        if 'did' in request.GET:
            did = request.GET['did']
        if 'verkey' in request.GET:
            verkey = request.GET['verkey']
    
    return render(request, 'trust_anchor/index.html', {
        'error': error,
        'did': did,
        'verkey': verkey,
        'captcha': captcha,
        'reg_result': reg_result,
        'reg_error': reg_error
    })


async def register(did, verkey):
    global ta
    
    if not ta:
        ta = await TrustAnchor.create()
    return await ta.register_did(did, verkey)
