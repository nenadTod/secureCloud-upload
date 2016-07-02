from Crypto.PublicKey import RSA
from Crypto.Util import strxor
from Crypto import Random
import binascii
import base64
import os
import ntpath
from Crypto.Cipher import AES

class SCCrypto:

    def __init__(self):
        self.length_RSA = 2048
        self.key_beginning_RSA = "-----BEGIN RSA PRIVATE KEY-----\n"
        self.key_ending_RSA = "\n-----END RSA PRIVATE KEY-----\n"
        self.length_AES = 24

    # splits secret key (using new key and string xor)
    def splitSK_RSA(self, key):
        sk = key.exportKey("PEM")

        key2 = RSA.generate(self.length_RSA);
        sk2 = key2.exportKey("PEM")


        sk = sk[len(self.key_beginning_RSA):-len(self.key_ending_RSA)+1]
        sk2 = sk2[len(self.key_beginning_RSA):-len(self.key_ending_RSA)+1]

        if len(sk)>len(sk2):
            needed = len(sk)-len(sk2)
            sk2 = sk2 + Random.new().read(needed)

        if len(sk) < len(sk2):
            sk2 = sk2[:len(sk)]

        xord = strxor.strxor(sk, sk2)
        xord = binascii.hexlify(xord)
        sk2 = binascii.hexlify(sk2)

        return [xord, sk2]  # 2. vraca onaj koji je vec bio string tipa

    # merges two string keys into a RSA key that can only encrypt
    def mergeSK_RSA(self, sk1, sk2):

        sk1 = binascii.unhexlify(sk1)
        sk2 = binascii.unhexlify(sk2)

        sk = strxor.strxor(sk1, sk2)
        sk = self.key_beginning_RSA + sk + self.key_ending_RSA
        sk = sk[:len(sk)-1]  # uvuce se neki \n, moram ovako da ga izbacim.

        key = RSA.importKey(sk)  # identicno izgleda import javnog

        return key

    def bin2b64(self, binStr):
        return base64.b64encode(binStr)


    def b642bin(self, b64Str):
        return base64.b64decode(b64Str)

    def encrypt_images(self, temp_dir, opened_files, sec_key):

        file_list = []
        iv_list = []

        sim_key = Random.new().read(self.length_AES)

        for f in opened_files:
            with open(f, 'rb') as fhI:
                file_name = ntpath.split(f)[1]
                file_path = temp_dir + "/" + file_name
                pic_data = fhI.read()

                iv = Random.new().read(16)
                iv_list.append(self.bin2b64(iv))

                aes = AES.new(sim_key, AES.MODE_CFB, iv)
                enc_pic_data = aes.encrypt(pic_data)
                enc_pic_data_hex = self.bin2b64(enc_pic_data)  # ovo ti i ne treba, zbog cuvanja mesta.. madaa? Izbacices, valja radit brze:D

                with open(file_path, 'w') as fhO:
                    fhO.write(enc_pic_data_hex)

                abs_file_path = os.path.abspath(file_path)
                file_list.append(abs_file_path)

        esk = sec_key.encrypt(sim_key, 'x')[0]
        esk = self.bin2b64(esk)



        return [file_list, esk, iv_list]