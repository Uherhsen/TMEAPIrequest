# TME API - example usage with Python
# More info and create application at: https://developers.tme.eu
# Пример хеширования на Python3: https://stackoverflow.com/questions/37763235/unicode-objects-must-be-encoded-before-hashing-error
# hmac - Keyed-Hashing for Message Authentication
import collections, urllib, base64, hmac, hashlib, json # urllib2

token = 'TOKEN'
app_secret = 'SECRET'
action = 'Products/GetPrices'
params = {
        'SymbolList[0]' : 'GSM90A12-P1M',
        'SymbolList[1]' : 'IPP50R199CPXKSA1',
        'Country': 'PL',
        'Currency': 'PLN',
        'Language': 'PL',
    }

def product_import_tme(token, app_secret,action,params):
    # /product/product_import_tme/

    token = token.encode() # TOKEN
    app_secret = app_secret.encode() #bytes('0b748f6e5d340d693703', encoding='utf8') #App secret

    response = api_call( action, params, token, app_secret, True)
    response = json.loads(response)
    return response

def api_call(action, params, token, app_secret, show_header=False):
    api_url = 'https://api.tme.eu/' + action + '.json'
    params['Token'] = token

    params = collections.OrderedDict(sorted(params.items()))

    encoded_params = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    signature_base = 'POST' + '&' + urllib.parse.quote(api_url, '') + '&' + urllib.parse.quote(encoded_params, '')

    #api_signature = base64.encodestring(hmac.new(app_secret, signature_base, hashlib.sha1).digest()).rstrip()
    api_signature = base64.b64encode(hmac.new(app_secret, signature_base.encode(), hashlib.sha1).digest()) 
    params['ApiSignature'] = api_signature
    
    #opts = {'http': {'method' : 'POST','header' : 'Content-type: application/x-www-form-urlencoded','content' : urllib.parse.urlencode(params)}}

    http_header = {"Content-type": "application/x-www-form-urlencoded",} 

    # create your HTTP request
    req = urllib.request.Request(api_url, urllib.parse.urlencode(params).encode('utf-8'), http_header) # OK 
    
    # submit your request
    res = urllib.request.urlopen(req)
    html = res.read()

    return html

if __name__ == "__main__":
    print(product_import_tme(token, app_secret,action,params))