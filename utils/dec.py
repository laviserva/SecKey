import re
import string
import random
from typing import List
import copy

from Crypto.Cipher import AES

class characters:
    def __init__(self, key) -> None:
        self.__characters = "~@#_^*%.+:;=" + string.ascii_letters + string.digits
        self.__p_sitio = "//s"
        self.__p_user = "//u"
        self.__p_password = "//p"
        self.__p_token = "//t"
        if len(key) != 16:
            raise Exception(ValueError("Incorrect AES key length. It must be 16"))
        self.__key = self.compr_inputs(key)
        self.__div_word = b"xaelko"

    def encript_file(self, file, key=None) -> None:
        if key is None:
            key = self.__key
        with open(file, "r", encoding = 'utf-8') as f:
            for line in f:
                new_line = line.rstrip()
                prefix = new_line[:3]
                sufix = new_line[3:].strip()
                
                if prefix == self.__p_sitio:
                    self.__append_encripted_file(self.__p_sitio + sufix, file)
                elif prefix == self.__p_user:
                    self.__append_encripted_file(self.__p_user + sufix, file)
                elif prefix == self.__p_password:
                    self.__append_encripted_file(self.__p_password + sufix, file)
                elif prefix == self.__p_token:
                    self.__append_encripted_file(self.__p_token + sufix, file)
                    
        with open(file[:-4] + "_encripted.bin", "rb+") as f:
            text = f.read()
            text = text[:-6]
        with open(file[:-4] + "_encripted.bin", "wb+") as f:
            f.write(text)

    def __append_encripted_file(self, string:str, file):
        file = file[:-4]
        out_file = file + "_encripted.bin"
        with open(out_file, "ab") as file_out:
            string = self.__salt_and_encript(string)
            file_out.write(string)
            file_out.write(self.__div_word)
            
    def __salt_and_encript(self, string: str) -> tuple[bytes, bytes, bytes]:
        key = str(self.__key)
        out = key[0] + string[0] + key[1] + string[1:-1] + key[-2] + string[-1] + key[-1]
        return self.__AES_encript(out)
            
    def __AES_encript(self, string) -> tuple[bytes, bytes, bytes]:
        encript_cipher = AES.new(self.__key, AES.MODE_EAX)
        nonce = encript_cipher.nonce
        string = self.compr_inputs(string)
        etxt, tag = encript_cipher.encrypt_and_digest(string)
        return etxt + tag + nonce
    
    def __AES_decript(self, ciphertext: bytes, nonce: bytes, tag:bytes) -> str:
        cipher = AES.new(key, AES.MODE_EAX, nonce)
        data = cipher.decrypt_and_verify(ciphertext, tag)
        return data

    def compr_inputs(self, inputs):
        if isinstance(inputs, bytes):
            inputs = inputs
        elif isinstance(inputs, str):
            inputs = inputs.encode()
        elif isinstance(inputs, (int, float)):
            inputs = str(inputs).encode()
        else:
            raise Exception(TypeError("Input data must be int or str or bytes"))
        return inputs
    
    def decrifrado(self, encript_text):
        return self.__decifr(encript_text)
    
    def __decifr(self, encript_text):
        self.__decript_cipher = AES.new(self.__key, AES.MODE_EAX, nonce=self.__nonce) # fix nonce
        plaintext = self.__decript_cipher.decrypt(encript_text)
        return plaintext.decode()
    
    def random_password(self, size: int = 32) -> str:
        out = "/p"
        for i in range(size):
            out += random.choice(self.__characters)
        return out
                
    def load_data(self, filename: str) -> list[str]:
        sitio = ""
        user = ""
        password = ""
        token = ""
        data_dict = dict()
        with open(filename, "r", encoding = 'utf-8') as f:
            num_users = 0
            sites = []
            for line in f:
                new_line = line.rstrip()
                prefix = new_line[:3]
                sufix = new_line[3:]

                if prefix == self.__p_sitio:
                    sitio = sufix
                    if sitio not in sites:
                        num_users = 0
                    sites.append(sitio)
                    user = ""
                    password = ""
                    token = ""
                    continue

                elif prefix == self.__p_user:
                    user = sufix
                    num_users += 1
                    continue

                elif prefix == self.__p_password:
                    password = sufix

                elif prefix == self.__p_token:
                    token = sufix
                else:
                    continue
                if data_dict.get(sitio) is None and token == "" and user != "" and password != "":
                    data_dict[sitio] = {num_users : {"user": user, "password": password}}

                elif data_dict.get(sitio) and token == "" and user != "" and password != "":
                    data_dict[sitio][num_users] = {"user": user, "password": password}

                elif data_dict.get(sitio) and token != "" and user != "" and password != "":
                    for number in data_dict[sitio]:
                        if user is data_dict[sitio][number]["user"]:
                            data_dict[sitio][number]["token"] = token
                            break
        return data_dict

    def __remove_salt(self, salty_list: list) -> list:
        num_users = 0
        sites = []
        sitio = ""
        user = ""
        password = ""
        token = ""
        data_dict = dict()
        
        for item in salty_list:
            new_line = item.rstrip()
            prefix = new_line[:3]
            sufix = new_line[3:-2] + new_line[-1]
            
            if prefix == self.__p_sitio:
                sitio = sufix
                if sitio not in sites:
                    num_users = 0
                sites.append(sitio)
                user = ""
                password = ""
                token = ""
                continue

            elif prefix == self.__p_user:
                user = sufix
                num_users += 1
                continue

            elif prefix == self.__p_password:
                password = sufix

            elif prefix == self.__p_token:
                token = sufix
            else:
                continue
            
            if data_dict.get(sitio) is None and token == "" and user != "" and password != "":
                data_dict[sitio] = {num_users : {"user": user, "password": password}}

            elif data_dict.get(sitio) and token == "" and user != "" and password != "":
                data_dict[sitio][num_users] = {"user": user, "password": password}

            elif data_dict.get(sitio) and token != "" and user != "" and password != "":
                for number in data_dict[sitio]:
                    if user is data_dict[sitio][number]["user"]:
                        data_dict[sitio][number]["token"] = token
                        break
        return data_dict
    
    def load_and_decript_file(self, file, key=None) -> list:
        out = []
        if key is None:
            key = self.__key
        with open(file, "rb") as f:
            lines = f.read()
            words = lines.split(self.__div_word)
            for word in words:
                etxt = word[:-32]
                tag = word[-32:-16]
                nonce = word[-16:]
                decript = r"/" + self.__AES_decript(etxt, nonce, tag).decode()[3:-1]
                out.append(decript)
        return self.__remove_salt(out)                

key = b'Sixteen byte key'
file = r"file.txt"
file_encripted = r"file_encripted.bin"
ch = characters(key)
#ch.encript_file(file)
file_text = ch.load_data(file)
decripted_text = ch.load_and_decript_file(file_encripted)