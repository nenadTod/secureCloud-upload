# -*- coding: utf-8 -*-

import os
import shutil

from Crypto.Cipher import AES
from SCCrytpo_API.SCCryptoUtil import SCCrypto

from cloud_API.google_drive_API import GoogleDriveAPI
from cloud_API.one_drive_API import OneDriveAPI
from cloud_API.dropbox_API import DropboxAPI

class SCDecryptor:

    def __init__(self):
        self.temp_dir = "sc_temp_down"
        self.temp_meta1D = self.temp_dir + "/meta1-de.txt"
        self.temp_meta1E = self.temp_dir + "/meta1-en.txt"

        self.storage_folder = "sc_storage"
        self.storage_GD_folder = "google_drive"
        self.storage_OD_folder = "one_drive"
        self.storage_DB_folder = "drop_box"
        self.storage_file_pri = "private.txt"

    # bice izmena posle, zbog nacina downloada.
    def decryptLocal(self, location_folder_value, download_path, drive):
        user_id = drive.get_user_data()

        file_pri = None

        if isinstance(drive,  GoogleDriveAPI):
            file_pri = self.storage_folder + "/" + self.storage_GD_folder + "/" + user_id + "/" + self.storage_file_pri

        if isinstance(drive,  OneDriveAPI):
            file_pri = self.storage_folder + "/" + self.storage_OD_folder + "/" + user_id + "/" + self.storage_file_pri

        if isinstance(drive,  DropboxAPI):
            file_pri = self.storage_folder + "/" + self.storage_DB_folder + "/" + user_id + "/" + self.storage_file_pri

        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)

        drive.download_files(location_folder_value, self.temp_dir)

        private1_exists = False
        if os.path.exists(file_pri) and os.stat(file_pri).st_size != 0:
            private1_exists = True

        private2_exists = False
        if os.path.exists(self.temp_meta1D) and os.stat(self.temp_meta1D).st_size != 0:
            private2_exists = True

        list_file_exists = False
        if os.path.exists(self.temp_meta1E):
            list_file_exists = True

        if not(private1_exists and private2_exists and list_file_exists):
            # ovde neka forma
            return

        if os.stat(self.temp_meta1E).st_size == 0:
            # ovde neka forma
            return

        with open(self.temp_meta1D, 'r') as fhI:
            key_part_1 = fhI.read()

        with open(file_pri, 'r') as fhI:
            key_part_2 = fhI.read()

        sc = SCCrypto()
        key = sc.mergeSK_RSA(key_part_1, key_part_2)

        dsk = None
        with open(self.temp_meta1E, 'r') as fhI:

            for line in fhI:
                line_content = str.split(line)
                if len(line_content) == 1:
                    dsk = key.decrypt(sc.b642bin(line_content[0]))
                else:

                    with open(self.temp_dir + "/" + line_content[0], 'r') as fhI2:
                        enc_pic_data_hex = fhI2.read()
                        enc_pic_data_bin = sc.b642bin(enc_pic_data_hex)

                        aes = AES.new(dsk, AES.MODE_CFB, sc.b642bin(line_content[1]))
                        dec_pic_data_bin = aes.decrypt(enc_pic_data_bin)

                        location = download_path + "/" + line_content[0] # da li treba ovde taj slash?
                        with open(location, 'wb') as fhO:
                            fhO.write(dec_pic_data_bin)

        shutil.rmtree(self.temp_dir)

        return True
