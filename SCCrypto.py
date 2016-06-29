from Crypto.PublicKey import RSA
from Crypto.Util import strxor
from Crypto import Random
import base64
import os
import ntpath
from Crypto.Cipher import AES

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

        xord = strxor.strxor(sk, sk2)
        xord = base64.b64encode(xord)
        sk2 = base64.b64decode(sk2)

        return [xord, sk2]


    #merges two string keys into a RSA key that can only encrypt
    def mergeSK_RSA(self, sk1, sk2):

        sk1 = base64.b64decode(sk1)
        sk2 = base64.b64decode(sk2)

        sk = strxor.strxor(sk1, sk2)
        sk = self.key_beginning_RSA + sk + self.key_ending_RSA
        sk = sk[:len(sk)-1]#uvuce se neki \n, moram ovako da ga izbacim.

        key = RSA.importKey(sk)#identicno ce biti za import javnog

        return key

    def bin2b64(self, binStr):
        return base64.b64encode(binStr)


    def b642bin(self, hexStr):
        return base64.b64decode(hexStr)

    def encrypt_images(self,temp_dir, opened_files):

        file_list = []

        for f in opened_files:
            with open(f, 'rb') as fhI:
                file_name = ntpath.split(f)[1]
                file_path = temp_dir + "/" + file_name
                pic_data = fhI.read()


                #encryption - bice zamenjene random vrendostima, naravno :)
                aes = AES.new("askldsjkuierocme", AES.MODE_CFB, 'asdfghjkqwertyui')
                enc_pic_data = aes.encrypt(pic_data)
                enc_pic_data_hex = self.bin2b64(enc_pic_data)#ovo ti mozda i ne treba, zbog cuvanja mesta.. madaa?

                with open(file_path, 'w') as fhO:
                    fhO.write(enc_pic_data_hex)

                abs_file_path = os.path.abspath(file_path)
                file_list.append(abs_file_path)

        return file_list