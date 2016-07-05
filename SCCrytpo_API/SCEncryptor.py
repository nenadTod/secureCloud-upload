# -*- coding: utf-8 -*-

import ntpath
import shutil
import os
import json
import tkSimpleDialog

import requests
import bcrypt

from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from SCCrytpo_API.SCCryptoUtil import SCCrypto

from gui_uc_register import UCRegister
import tkMessageBox


class SCEncryptor:

    def __init__(self, controller):

        self.controller = controller
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

        self.storage_file_pub = "public.txt"
        self.storage_file_pri = "private.txt"

        self.temp_dir = "sc_temp"

        self.email = ""
        self.password = ""

    def encryptLocal(self, file_list, drive, upload_location):

        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)

        user_id, bl = drive.get_user_data()

        meta_pub = self.temp_dir + "/" + self.meta1E
        meta_pri = self.temp_dir + "/" + self.meta1D

        file_pub = None  # stored
        file_pri = None  # stored
        folder_cloud = None  # stored

        drive_class_name = drive.__class__.__name__

        file_pub = self.storage_folder + "/" + drive_class_name + "/" + user_id + "/" + self.storage_file_pub
        file_pri = self.storage_folder + "/" + drive_class_name + "/" + user_id + "/" + self.storage_file_pri
        folder_cloud = self.storage_folder + "/" + drive_class_name + "/" + user_id


        #  local key storage - if it exists-> take the public key, if not...
        if os.path.exists(file_pub):
            with open(file_pub, 'r') as fhI:
                pub_key = fhI.read()
                key = RSA.importKey(pub_key)

            file_id = drive.get_meta_file(upload_location, self.temp_dir, self.meta1DEnum)

            if os.stat(meta_pri).st_size == 0:

                drive.get_meta_file("root", self.temp_dir, self.meta1DEnum)
                if os.stat(meta_pri).st_size == 0:
                    tkMessageBox.showerror("Error", "Application has encountered an error.")
                    return False

                drive.update_meta_file(file_id, self.temp_dir, self.meta1DEnum)

        else:
            sc = SCCrypto()

            if not os.path.exists(folder_cloud):
                os.makedirs(folder_cloud)

            key = RSA.generate(self.length_RSA)
            xord = sc.splitSK_RSA(key)

            with open(file_pub, 'w') as fhO:
                fhO.write(key.publickey().exportKey())

            with open(file_pri, 'w') as fhO:
                    fhO.write(xord[0])

            file_id = drive.get_meta_file(upload_location, self.temp_dir, self.meta1DEnum)
            with open(meta_pri, 'w') as fhO:
                fhO.write(xord[1])

            drive.update_meta_file(file_id, self.temp_dir, self.meta1DEnum)
            os.remove(meta_pri)

            file_id = drive.get_meta_file("root", self.temp_dir, self.meta1DEnum)
            with open(meta_pri, 'w') as fhO:
                fhO.write(xord[1])

            drive.update_meta_file(file_id, self.temp_dir, self.meta1DEnum)

        self._do_the_job(meta_pub, self.meta1EEnum, file_list, key, upload_location, drive)
        return True


    def encryptShared(self, file_list, drive, upload_location):

        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)

        meta_pri = self.temp_dir + "/" + self.meta2D
        meta_pub = self.temp_dir + "/" + self.meta2E

        uid, bl = drive.get_user_data()
        hid = SHA256.new(uid).hexdigest()

        r = requests.post('https://127.0.0.1:8000/api/exist/', json={"id": hid}, verify=False)
        dct = json.loads(r.content)
        ans = dct[0]['Ans']

        if ans == "No":
            UCRegister(self.controller.view.root, self)

            if self.email == "" and self.password == "":
                return False

            recM = SHA256.new(self.email).hexdigest()
            psw = bcrypt.hashpw(self.password, bcrypt.gensalt())

            self.email = ""
            self.password = ""
            r = requests.post('https://127.0.0.1:8000/api/newE/', json={"id": hid, "psw": psw, "recM": recM}, verify=False)
            dct = json.loads(r.content)
            ans = dct[0]['Ans']

            if ans == "Duplicate":
                # pop up
                return False

            pub_key = dct[0]['PK']
            key = RSA.importKey(pub_key)

            prKPart = dct[0]['PrKPart']

            # save key part in a file located in the root folder
            file_id = drive.get_meta_file("root", self.temp_dir, self.meta2DEnum)
            with open(meta_pri, 'w') as fhO:
                fhO.write(prKPart)

            drive.update_meta_file(file_id, self.temp_dir, self.meta2DEnum)
            os.remove(meta_pri)

            # save key part in a file located in the upload folder
            file_id = drive.get_meta_file(upload_location, self.temp_dir, self.meta2DEnum)
            with open(meta_pri, 'w') as fhO:
                fhO.write(prKPart)

            drive.update_meta_file(file_id, self.temp_dir, self.meta2DEnum)
            os.remove(meta_pri)

        else:
            psw = tkSimpleDialog.askstring("Password", "Enter password", show=u"\u25CF")

            r = requests.post('https://127.0.0.1:8000/api/getPK/', json={"id": hid, "psw": psw}, verify=False)
            dct = json.loads(r.content)
            ans = dct[0]['Ans']

            if ans == "No permission":
                tkMessageBox.showerror("Error", "Wrong password.")
                return False

            if ans == "No such entity":
                tkMessageBox.showerror("Error", "Application has encountered an error.")
                return False

            pub_key = dct[0]['PK']
            key = RSA.importKey(pub_key)

            # get a file with part of the private key located in the root folder
            drive.get_meta_file("root", self.temp_dir, self.meta2DEnum)
            if os.stat(meta_pri).st_size == 0:
                tkMessageBox.showerror("Error", "Application has encountered an error, some data is missing.")
                return False

            with open(meta_pri, 'r') as fhO:
                prKPart = fhO.read()

            os.remove(meta_pri)

            # save that part of the private key in a meta file located in the upload folder
            file_id = drive.get_meta_file(upload_location, self.temp_dir, self.meta2DEnum)

            if os.stat(meta_pri).st_size == 0:
                with open(meta_pri, 'w') as fhO:
                    fhO.write(prKPart)

                drive.update_meta_file(file_id, self.temp_dir, self.meta2DEnum)

        self._do_the_job(meta_pub, self.meta2EEnum, file_list, key, upload_location, drive)
        return True

    def _do_the_job(self, metaE, metaEEnum, file_list, key, upload_location, drive):

        sc = SCCrypto()

        ret_val = sc.encrypt_images(self.temp_dir, file_list, key)
        enc_file_list = ret_val[0]  # files for upload in temp folder
        enc_sym_key = ret_val[1]  # encrypted symmetric key
        iv_list = ret_val[2]  # iv for every encrypted file, in the same order

        file_id = drive.get_meta_file(upload_location, self.temp_dir, metaEEnum)

        with open(metaE, 'a') as fhO:
            fhO.write(enc_sym_key + "\n")
            i = 0
            for f in file_list:
                fhO.write(ntpath.split(f)[1] + "," + str(iv_list[i]) + "\n")
                i += 1

        drive.update_meta_file(file_id, self.temp_dir, metaEEnum)

        drive.upload(enc_file_list, upload_location)

        shutil.rmtree(self.temp_dir)

    def register_user(self, email, password):
        self.email = email
        self.password = password