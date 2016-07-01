#klasa u kojoj su eksperimenti

from SCCryptoUtil import SCCrypto
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES

sc = SCCrypto()
#igranje sa kljucem, split, merge i encrypt sa RSA
key = RSA.generate(2048)
xord = sc.splitSK_RSA(key)

key2 = sc.mergeSK_RSA(xord[0], xord[1])

keyStr = key.exportKey('PEM')
keyStr2 = key2.exportKey('PEM')



msg = "Warriors dance"
print msg
emsg = key2.encrypt(msg, 'x')[0]
emsgStr = sc.bin2b64(emsg)
print emsgStr
emsg2 = sc.b642bin(emsgStr)
dmsg = key.decrypt(emsg2)
print dmsg

print keyStr == keyStr2
print msg == dmsg

#igranje sa slikama
"""
with open('konji.jpg','rb') as fhI:
    picData = fhI.read()
    picDataStr = sc.bin2hex(picData)
    with open('koji3.jpg', 'w') as fhO:
        fhO.write(picDataStr)
        picData2 = sc.hex2bin(picDataStr)
        print picData == picData2
"""

aes = AES.new("askldsjkuierocme", AES.MODE_CFB, 'asdfghjkqwertyui')
with open('images/icon.ico', 'rb') as fhI:

    picData = fhI.read()
    picDataStr = sc.bin2b64(picData)
    aes_emsg = aes.encrypt(picDataStr)
    with open('images/koji2.jpg', 'w') as fhO:
        fhO.write(aes_emsg)


    #print emsg
    aes = AES.new("askldsjkuierocme", AES.MODE_CFB, 'asdfghjkqwertyui')
    aes_dmsg = aes.decrypt(aes_emsg)
    picData2 = sc.b642bin(aes_dmsg)

    print len(picData)
    print len(picData2)
    print picData2 == picData
    with open('images/koji3.jpg', 'wb') as fhO2:
        fhO2.write(picData2)
    #print aes_dmsg