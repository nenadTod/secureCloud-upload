# -*- coding: utf-8 -*-

import os
import shutil

from Crypto.Cipher import AES
from SCCrytpo.SCCryptoUtil import SCCrypto
import tkMessageBox

class SCDecryptor:

    def __init__(self):
        self.temp_dir = "sc_temp_down"
        self.storage_folder = "sc_storage"
        self.storage_file_pri = "private.txt"

        self.meta1E = 'meta1-en.txt'
        self.meta1D = 'meta1-de.txt'
        self.meta1EEnum = 1
        self.meta1DEnum = 2

    # bice izmena posle, zbog nacina downloada.
    def decryptLocal(self, location_folder_value, location_folder_name, download_path, drive):
        user_id, bl = drive.get_user_data()

        meta_pri = self.temp_dir + "/" + self.meta1D
        meta_pub = self.temp_dir + "/" + self.meta1E

        drive_class_name = drive.__class__.__name__

        stored_file_pri = self.storage_folder + "/" + drive_class_name + "/" + user_id + "/" + self.storage_file_pri

        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)

        drive.get_meta_file(location_folder_name, self.temp_dir, self.meta1DEnum)
        drive.get_meta_file(location_folder_name, self.temp_dir, self.meta1EEnum)

        private1_exists = False
        if os.path.exists(stored_file_pri) and os.stat(stored_file_pri).st_size != 0:
            private1_exists = True

        private2_exists = False
        if os.path.exists(meta_pri) and os.stat(meta_pri).st_size != 0:
            private2_exists = True

        list_file_exists = False
        if os.path.exists(meta_pub):
            list_file_exists = True

        if not(private1_exists and private2_exists and list_file_exists):
            tkMessageBox.showinfo("There's nothing to decrypt.")
            return

        if os.stat(meta_pub).st_size == 0:
            tkMessageBox.showinfo("There's nothing to decrypt.")
            return

        with open(meta_pri, 'r') as fhI:
            key_part_1 = fhI.read()

        with open(stored_file_pri, 'r') as fhI:
            key_part_2 = fhI.read()

        sc = SCCrypto()
        key = sc.mergeSK_RSA(key_part_1, key_part_2)

        dsk = None
        with open(meta_pub, 'r') as fhI:

            for line in fhI:
                line_content = line.split(",")
                if len(line_content) == 1:
                    dsk = key.decrypt(sc.b642bin(line_content[0]))
                else:

                    drive.download_file(location_folder_value, line_content[0], self.temp_dir)

                    with open(self.temp_dir + "/" + line_content[0], 'r') as fhI2:
                        enc_pic_data_hex = fhI2.read()
                        enc_pic_data_bin = sc.b642bin(enc_pic_data_hex)

                        aes = AES.new(dsk, AES.MODE_CFB, sc.b642bin(line_content[1]))
                        dec_pic_data_bin = aes.decrypt(enc_pic_data_bin)

                        location = download_path + "/" + line_content[0]
                        with open(location, 'wb') as fhO:
                            fhO.write(dec_pic_data_bin)

        shutil.rmtree(self.temp_dir)

        return True
