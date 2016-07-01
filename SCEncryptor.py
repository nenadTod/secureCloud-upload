# -*- coding: utf-8 -*-

import ntpath
import shutil
import os

import requests
import json
import bcrypt

from SCCryptoUtil import SCCrypto
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256


class SCEncryptor:

    def __init__(self):

        self.meta1E = 'meta1-en.txt'
        self.meta1D = 'meta1-de.txt'
        self.meta1EEnum = 1
        self.meta1DEnum = 2

        self.meta2E = 'meta2-en.txt'
        self.meta2D = 'meta2-de.txt'
        self.meta2EEnum = 3
        self.meta2DEnum = 4

        self.length_RSA = 2048

        self.storage_folder = "sc_storage"
        self.storage_file_pub = "sc_storage/public.txt"
        self.storage_file_pri = "sc_storage/private.txt"

        self.temp_dir = "sc_temp"


    def encryptLocal(self, file_list, drive, upload_location):

        #  local key storage - if it exists-> take the public key, if not...
        if os.path.exists(self.storage_file_pub):
            with open(self.storage_file_pub, 'r') as fhI:
                pub_key = fhI.read()
                key = RSA.importKey(pub_key)
        else:
            sc = SCCrypto()

            if not os.path.exists(self.storage_folder):
                os.makedirs(self.storage_folder)

            key = RSA.generate(2048)
            xord = sc.splitSK_RSA(key)

            with open(self.storage_file_pub, 'w') as fhO:
                fhO.write(key.publickey().exportKey())

            with open(self.storage_file_pri, 'w') as fhO:
                    fhO.write(xord[0])

            file_id = drive.get_meta_file(upload_location, self.meta1DEnum)
            with open(self.meta1D, 'w') as fhO:
                fhO.write(xord[1])

            drive.update_meta_file(file_id, self.meta1DEnum)
            os.remove(self.meta1D)

        self._do_the_job(self.meta1E, self.meta1EEnum, file_list, key, upload_location, drive)


    def encryptShared(self, file_list, drive, upload_location):

        id = drive.get_user_data()
        hid = SHA256.new(id).hexdigest()

        r = requests.post('http://127.0.0.1:8000/api/exist/', json={"id": hid})  # check if entity with that id exists
        dct = json.loads(r.content)
        ans = dct[0]['Ans']

        if ans == "No":
            recM = SHA256.new("nenadtod@live.com").hexdigest()#оve vrednosti ce se preuzimati sa forme.
            psw = bcrypt.hashpw("hassan", bcrypt.gensalt())#оve vrednosti ce se preuzimati sa forme.
            r = requests.post('http://127.0.0.1:8000/api/newE/', json={"id": hid, "psw": psw, "recM": recM})
            dct = json.loads(r.content)
            ans = dct[0]['Ans']

            if ans == "Duplicate":
                # pop up
                return

            pub_key = dct[0]['PK']
            key = RSA.importKey(pub_key)

            #  implementiraj i cuvanje dela kljuca u secure - folderu, i u folderu pojedinacno.

        else:
            psw = "hassan"#оve vrednosti ce se preuzimati sa forme.

            r = requests.post('http://127.0.0.1:8000/api/getPK/', json={"id": hid, "psw": psw})
            dct = json.loads(r.content)
            ans = dct[0]['Ans']

            if ans == "No permission":
                #  pop up
                return

            if ans == "No such entity":
                #  pop up
                return

            pub_key = dct[0]['PK']
            key = RSA.importKey(pub_key)

            # smestanje dela kljuca za decrypt, malo posle ces odraditi :)
            # file_id = drive.get_meta_file(upload_location, self.meta2DEnum)

            # if os.stat(self.meta2DEnum).st_size == 0:
            # ostaje za sad nedoreceno, jbg.. mozes upload i bez toga, samo se seti da odradis :D

        self._do_the_job(self.meta2E, self.meta2EEnum, file_list, key, upload_location, drive)


    def _do_the_job(self, metaE, metaEEnum, file_list, key, upload_location, drive):

        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)

        sc = SCCrypto()

        ret_val = sc.encrypt_images(self.temp_dir, file_list, key)
        enc_file_list = ret_val[0]  # files for upload in temp folder
        enc_sym_key = ret_val[1]  # encrypted symmetric key
        iv_list = ret_val[2]  # iv for every encrypted file, in the same order

        file_id = drive.get_meta_file(upload_location, metaEEnum)

        with open(metaE, 'a') as fhO:
            fhO.write(enc_sym_key + "\n")
            i = 0
            for f in file_list:
                fhO.write(ntpath.split(f)[1] + " " + str(iv_list[i]) + "\n")
                i += 1

        drive.update_meta_file(file_id, metaEEnum)
        os.remove(metaE)

        drive.upload(enc_file_list, upload_location)

        shutil.rmtree(self.temp_dir)