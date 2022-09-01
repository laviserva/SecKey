from calendar import day_abbr
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
        self.__saltkey = self.__key[0:2] + self.__key[-2:]
    
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
    
    def cipher(self, data):
        #data = self.compr_inputs(data)
        #data = self.__salt(data)
        return self.__cifr(data)
    
    def __cifr(self, data: dict) -> tuple:
        key = self.__saltkey.decode()
        # a_dict[new_key] = a_dict.pop(old_key) # change key name
        new_dict = copy.deepcopy(data)
        for old_key in new_dict.keys():
            new_key = key[0] + old_key[0] + key[1] + old_key[1:-1] + key[-2] + old_key[-1] + key[-1]
            #new_key = self.__AES_string(new_key) # encrypt
            data[new_key] = data.pop(old_key)

            for number_user in new_dict[old_key].keys():
                new_number_user = key[2] + str(number_user) # Salt
                new_number_user = self.__AES_string(new_number_user) # encrypt
                data[new_key][new_number_user] = data[new_key].pop(number_user)

                for us_pw_t in new_dict[old_key][number_user]:
                    new_us_pw_t = key[0] + us_pw_t[0] + key[1] + us_pw_t[1:-1] + key[-2] + us_pw_t[-1] + key[-1] # Salt
                    new_us_pw_t = self.__AES_string(new_us_pw_t) # encrypt
                    old_data_info = data[new_key][new_number_user][us_pw_t]
                    #print(old_data_info)
                    data[new_key][new_number_user][new_us_pw_t] = data[new_key][new_number_user].pop(us_pw_t)

                    if data[new_key][new_number_user][new_us_pw_t] != "":
                        aux = key[0] + old_data_info[0] + key[1] + old_data_info[1:-1] + key[-2] + old_data_info[-1] + key[-1] # Salt
                        data[new_key][new_number_user][new_us_pw_t] = self.__AES_string(aux) # encrypt
        return data

    def __AES_string(self, string):
        encript_cipher = AES.new(self.__key, AES.MODE_EAX)
        nonce = encript_cipher.nonce
        string = self.compr_inputs(string)
        etxt, tag = encript_cipher.encrypt_and_digest(string)
        return etxt, tag, nonce
    
    def decrifrado(self, encript_text):
        return self.__decifr(encript_text)
    
    def __decifr(self, encript_text):
        ...
        """
        self.__decript_cipher = AES.new(self.__key, AES.MODE_EAX, nonce=self.__nonce) # fix nonce
        plaintext = self.__decript_cipher.decrypt(encript_text)
        return plaintext
        """

    def comprobe(self, decript_text):
        return self.__compr(decript_text)
    
    def __compr(self, decript_text):
        try:
            self.__decript_cipher.verify(self.__tag)
            print("The message is authentic:", decript_text)
        except ValueError:
            print("Key incorrect or message corrupted")
            
        return decript_text == self.__tag
    
    def random_password(self, size: int = 32) -> str:
        out = "/p"
        for i in range(size):
            out += random.choice(self.__characters)
        return out

    def save_data(self, encripted_dict: dict, filename: str) -> None:
        with open(filename, "wb") as f:
            pass
                
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

key = b'Sixteen byte key'
ch = characters(key)
file_text = ch.load_data(r"file.txt")
encoded_text = ch.cipher(file_text)
print(encoded_text)
#ch.save_data(encoded_text)