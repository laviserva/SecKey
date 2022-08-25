import string
import random
from typing import List

from Crypto.Cipher import AES

class characters:
    def __init__(self, key) -> None:
        self.__characters = "~@#_^*%.+:;=" + string.ascii_letters + string.digits
        self.__p_sitio = "/*s"
        self.__p_user = "/*u"
        self.__p_password = "/*p"
        self.__p_token = "/*t"

        self.__key = self.compr_inputs(key)
    
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
    
    def cifrado(self, data):
        data = self.compr_inputs(data)
        return self.__cifr(data)
    
    def __cifr(self, data):
        encript_cipher = AES.new(self.__key, AES.MODE_EAX)
        self.__nonce = encript_cipher.nonce
        self.__encript_ciphertext, self.__tag = encript_cipher.encrypt_and_digest(data)
        return self.__encript_ciphertext
    
    def decrifrado(self, encript_text):
        if isinstance(encript_text, bytes):
            return self.__decifr(encript_text).decode()
        raise Exception(TypeError("Input data must be bytes"))
    
    def __decifr(self, encript_text):
        self.__decript_cipher = AES.new(self.__key, AES.MODE_EAX, nonce=self.__nonce)
        plaintext = self.__decript_cipher.decrypt(encript_text)
        return plaintext

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

    def save_data(self, lst: list[str], filename: str) -> None:
        if len(lst) != 3:
            raise Exception("list must be length of 3")
        with open(filename, "ab") as f:
            for l in lst:
                f.write(l.encode())
                f.write(b"\n")
                
    def load_data(self, filename: str) -> list[str]:
        p_sitio = "/s"
        p_user = "/u"
        p_password = "/p"
        p_token = "/t"

        sitio = ""
        user = ""
        password = ""
        token = ""

        data_dict = dict()
        with open(filename, "r", encoding = 'utf-8') as f:
            
            for line in f:
                new_line = line.rstrip()
                prefix = new_line[:2]
                sufix = new_line[2:]
                
                if prefix == p_sitio:
                    sitio = sufix
                    
                elif prefix == p_user:
                    user = sufix
                    
                elif prefix == p_password:
                    password = sufix
                    
                elif prefix == p_token:
                    token = sufix
                    
                if sitio == "" or user == "" or password == "":
                    continue
                
                if data_dict.get(sitio):
                    int_dict = len(data_dict[sitio].keys())
                    temp_dict = {int_dict + 1 : {"user": user, "password": password, "token": token}}
                    data_dict[sitio].update(temp_dict)
                    sitio = ""
                    user = ""
                    password = ""
                    token = ""
                    
                else:
                    data_dict[sitio] = {1 : {"user": user, "password": password, "token": token}}
                    sitio = ""
                    user = ""
                    password = ""
                    token = ""
                    
        return data_dict

"""
ch = characters()
password = ch.random_password()
lst = ["sitio", "usuario", str(password)]
#ch.save_data(lst, "filename.txt")
lst2 = ch.load_data("filename.txt")
print(lst2)
A = {"B": {1, 2}, "C": 2}
"""

key = b'Sixteen byte key'
ch = characters(key)
texto = ch.cifrado("oliaru")
print(texto)
print(ch.decrifrado(texto))