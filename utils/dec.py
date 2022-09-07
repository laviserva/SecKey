import string
import random
import os

from Crypto.Cipher import AES

class SecKeys:
    def __init__(self, key) -> None:
        self.__characters = "~@#_^*%.+:;=" + string.ascii_letters + string.digits
        self.__p_sitio = "//s"
        self.__p_description = "//d"
        self.__p_user = "//u"
        self.__p_password = "//p"
        self.__p_token = "//t"
        if len(key) != 16:
            raise Exception(ValueError("Incorrect AES key length. It must be 16"))
        self.__key = self.compr_inputs(key)
        self.__div_word = b"xaelko"

    def encript_file(self, file: str, key:bytes=None) -> None:
        """encript_file encripts and organize a file.txt using AES algorithm.
        Args:
            Input:
                file (str): Encoding = utf-8, the content must be organized in this way.
                
                //s www.site_example.com -> Must     - website (it doesn't matter if you put spaces after //s or not)
                //u User 1         -> Must     - user for the previous website (can store countless users for the same site)
                //p Password       -> Must     - for User 1
                //d App/Website    -> Optional - description if you have something important to say
                //t Token          -> Optional - if you 
                
                key (bytes, optional): if you introduce a key, the previous one (The key that was used when initialize the class is replaced)
                                    if you don't introduce a new key, the previus one will be used.
            
            Output:
                None

        Example:
            The file "file.txt" has inside this information:
            //s site
            //u user
            //p password
            
            old_key = b'1234567890123456' # 16 bytes key
            new_key = b'6543210987654321' # 16 bytes key
            seck = secKeys(old_key)
            SecKeys.encript_file("file.txt", new_key)
            
            or
            
            key = b'1234567890123456' # 16 bytes key
            seck = SecKeys(key)
            seck.encript_file("file.txt")
            
        Warning:
            Be careful with the size of the files, you could run out of memory.
        """
        
        encripted_file = file[:-4] + "_encripted.bin"
        if os.path.isfile(encripted_file):
            os.remove(encripted_file)
        if os.path.isfile(file) is False:
            raise Exception(FileNotFoundError("File must exist"))
        
        if key is None:
            key = self.__key
        encripted_data = []
        
        with open(file, "r", encoding = 'utf-8') as f:
            for line in f:
                new_line = line.rstrip()
                prefix = new_line[:3]
                sufix = new_line[3:].strip()
                
                if prefix == self.__p_sitio:
                    salt_string = self.__salt_and_encript(self.__p_sitio + sufix) + self.__div_word
                    encripted_data.append(salt_string)
                elif prefix == self.__p_user:
                    salt_string = self.__salt_and_encript(self.__p_user + sufix) + self.__div_word
                    encripted_data.append(salt_string)
                elif prefix == self.__p_password:
                    salt_string = self.__salt_and_encript(self.__p_password + sufix) + self.__div_word
                    encripted_data.append(salt_string)
                elif prefix == self.__p_token:
                    salt_string = self.__salt_and_encript(self.__p_token + sufix) + self.__div_word
                    encripted_data.append(salt_string)
                    
        encripted_data[-1] = encripted_data[-1][:-len(self.__div_word)]

        with open(encripted_file, "wb+") as f:
            f.writelines(encripted_data)

    def __append_to_encripted_file(self, string:str, file):
        pass
        """
        with open(out_file, "r+") as file_out:
            ...
        """
            
    def __salt_and_encript(self, string: str) -> tuple[bytes, bytes, bytes]:
        key = self.__key.decode()
        out = key[0] + string[0] + key[1] + string[1:-1] + key[-2] + string[-1] + key[-1]
        return self.__AES_encript(out)
            
    def __AES_encript(self, string) -> tuple[bytes, bytes, bytes]:
        encript_cipher = AES.new(self.__key, AES.MODE_EAX)
        nonce = encript_cipher.nonce
        string = self.compr_inputs(string)
        etxt, tag = encript_cipher.encrypt_and_digest(string)
        return etxt + tag + nonce
    
    def __AES_decript(self, key: bytes, ciphertext: bytes, nonce: bytes, tag:bytes) -> str:
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
        out = self.__p_password
        for _ in range(size):
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

    def __remove_salt(self, salty_list: list) -> dict:
        num_users = 0
        sites = []
        sitio = ""
        user = ""
        password = ""
        token = ""
        data_dict = dict()
        
        for item in salty_list:
            new_line = item.rstrip()
            prefix = new_line[1] + new_line[3:5]
            sufix = new_line[5:-3] + new_line[-2]
            
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
    
    def load_and_decript_file(self, encripted_file: str, key: bytes = None) -> list:
        if os.path.isfile(encripted_file) is False:
            raise Exception(FileNotFoundError("File must exist"))
        
        if key is None:
            print("Key has not introduced. Using the previous key")
            key = self.__key
            
        out = []
        with open(encripted_file, "rb") as f:
            lines = f.read()
            words = lines.split(self.__div_word)
            for word in words:
                etxt = word[:-32]
                tag = word[-32:-16]
                nonce = word[-16:]
                try:
                    decript = self.__AES_decript(key, etxt, nonce, tag).decode()
                except:
                    raise (Exception(ValueError("MAC chekc failed. The introduced key is incorrect")))
                out.append(decript)
        return self.__remove_salt(out)

key = b'Sixteen byte key'
file = r"file.txt"
file_encripted = file[:-4] + r"_encripted.bin"
ch = SecKeys(key)
ch.encript_file(file)
file_text = ch.load_data(file)
#decripted_text = ch.load_and_decript_file(file_encripted, b'Sixteen byte ke1') # Error
decripted_text = ch.load_and_decript_file(file_encripted, key) # ok
#decripted_text = ch.load_and_decript_file(file_encripted) # Ok