from Crypto.PublicKey import RSA
from Crypto.Util import strxor
from Crypto import Random
import  binascii

class SCCrypto:

    def __init__(self):
        self.length_RSA = 2048
        self.key_beginning_RSA = "-----BEGIN RSA PRIVATE KEY-----\n"
        self.key_ending_RSA = "\n-----END RSA PRIVATE KEY-----\n"


    #splits secret key (using new key and string xor)
    def splitSK_RSA(self, key):
        sk = key.exportKey("PEM")

        key2 = RSA.generate(self.length_RSA);
        sk2 = key2.exportKey("PEM")


        sk = sk[len(self.key_beginning_RSA):-len(self.key_ending_RSA)+1]
        sk2 = sk2[len(self.key_beginning_RSA):-len(self.key_ending_RSA)+1]

        if len(sk)>len(sk2):
            needed = len(sk)-len(sk2)
            sk2 = sk2 + Random.new().read(needed);

        if len(sk) < len(sk2):
            sk2 = sk2[:len(sk)]

        xord = strxor.strxor(sk,sk2)
        xord = binascii.hexlify(xord)
        sk2 = binascii.hexlify(sk2)

        return [xord, sk2]


    #merges two string keys into a RSA key that can only encrypt
    def mergeSK_RSA(self, sk1, sk2):

        sk1 = binascii.unhexlify(sk1)
        sk2 = binascii.unhexlify(sk2)

        sk = strxor.strxor(sk1, sk2)
        sk = self.key_beginning_RSA + sk + self.key_ending_RSA
        sk = sk[:len(sk)-1]#uvuce se neki \n, moram ovako da ga izbacim.

        key = RSA.importKey(sk)#identicno ce biti za import javnog

        return key

    def bin2hex(self, binStr):
        return binascii.hexlify(binStr)


    def hex2bin(self, hexStr):
        return binascii.unhexlify(hexStr)