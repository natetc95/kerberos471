import json
from pycrypto.Cipher import DES as eAlgorithm
from pycrypto.Hash import SHA as hAlgorithm
import random
import string


msg = '{"un": "wew"}'
print json.loads(msg)["un"]


key = hAlgorithm.new('mywickedsickpassword').digest()[:8]
print key
testRC4 = eAlgorithm.new(key);
phrase2encrypt = 'nate is great'
l = 8 - (len(phrase2encrypt) % 8)
phrase2encrypt = phrase2encrypt + (l*'\0')
phrase2decrypt = testRC4.encrypt(phrase2encrypt)
print phrase2decrypt, '/', testRC4.decrypt(phrase2decrypt).replace('\0','')
