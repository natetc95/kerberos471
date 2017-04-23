import json
from pycrypto.Cipher import DES as eAlgorithm
from pycrypto.Hash import SHA as hAlgorithm
import random
import string

print "JSON: "
msg = '{"un": "wew"}'
print '  ', json.loads(msg)["un"]


print "HASHING: "
key = hAlgorithm.new('mywickedsickpassword').digest()[:8]
print '  ', key
print "ENCRYPTION:"
test = eAlgorithm.new(key);
phrase2encrypt = 'nate is great'
l = 8 - (len(phrase2encrypt) % 8)
phrase2encrypt = phrase2encrypt + (l*'\0')
phrase2decrypt = test.encrypt(phrase2encrypt)
print '  ', phrase2decrypt, '/', test.decrypt(phrase2decrypt).replace('\0','')

def generateSK_TGS():
    from pycrypto.Hash import SHA as hAlgorithm
    import os
    key = hAlgorithm.new(os.urandom(8)).digest()[:8]
    return key

print generateSK_TGS()
