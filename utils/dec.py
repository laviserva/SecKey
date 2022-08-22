import string
import random
from typing import List
from cryptography.fernet import Fernet

class characters:
    def __init__(self) -> None:
        self.__characters = "~@#_^*%.+:;=" + string.ascii_letters + string.digits
        self.__p_sitio = "/*s"
        self.__p_user = "/*u"
        self.__p_password = "/*p"
        self.__p_token = "/*t"
    
    def cifrado(self):
        pass
    
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
            
ch = characters()
password = ch.random_password()
lst = ["sitio", "usuario", str(password)]
#ch.save_data(lst, "filename.txt")
lst2 = ch.load_data("filename.txt")
print(lst2)
A = {"B": {1, 2}, "C": 2}
