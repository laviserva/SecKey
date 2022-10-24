import copy
import string
import random
import os

from Crypto.Cipher import AES

class EaD:
    p_sitio = "//s"
    p_description = "//d"
    p_user = "//u"
    p_password = "//p"
    p_token = "//t"
    div_word = b"xaelko"
    def __init__(self) -> None:
        self.__characters = "~@#_^*%.+:;=" + string.ascii_letters + string.digits
        
    def __AES_decript(self, key: bytes, ciphertext: bytes, nonce: bytes, tag:bytes) -> bytes:
        cipher = AES.new(key, AES.MODE_EAX, nonce)
        data = cipher.decrypt_and_verify(ciphertext, tag)
        return data
    
    def __AES_encript(self, string: str, key:bytes) -> tuple[bytes, bytes, bytes]:
        encript_cipher = AES.new(key, AES.MODE_EAX)
        nonce = encript_cipher.nonce
        etxt, tag = encript_cipher.encrypt_and_digest(string.encode())
        return etxt + tag + nonce
    
    def add_data_to_file(self, data:list[str], encripted_file: str, key: bytes) -> None:
        """add a structured data in a encripted file. for adding new sites, users and passwords

        Args:
            data (list[str]): must be a list of strings where you should have the next structure:
            data = ["//ssite", "//uuser", "//ppassword"]
            encripted_file (str): Path of the encripted file

        Raises:
            Exception - FileExistError: Verify if exist encripted file if not, exception will rise.
            Exception - ValueError: If the extension is not .bin then, exception will rise.
            Exception - ValueError: Check if the input data has the correct prefixes.

        Returns:
            None
        """
        if os.path.exists(encripted_file) is not True:
            raise Exception(FileExistsError(f"File {encripted_file} doesn't exist"))
        if encripted_file[-4:] != ".bin":
            raise Exception(ValueError(f"Extension of the file {encripted_file} must be .bin and not '.{encripted_file.rpartition('.')[-1]}'"))
        
        encripted_data = []
        test_data = [dat[:3] for dat in data]
        if self.p_sitio not in test_data or self.p_user not in test_data or self.p_password not in test_data:
            raise Exception(ValueError(f"Input data must have the prefix //s, //u, //p (site, user and passwords) written."))
        del(test_data)
        
        for item in data:
            new_line = item.rstrip()
            prefix = new_line[:3]
            sufix = new_line[3:].strip()
            if prefix == self.p_sitio:
                salt_string = self.__salt_and_encript(self.p_sitio + sufix, key) + self.div_word
                encripted_data.append(salt_string)
            elif prefix == self.p_user:
                salt_string = self.__salt_and_encript(self.p_user + sufix, key) + self.div_word
                encripted_data.append(salt_string)
            elif prefix == self.p_password:
                salt_string = self.__salt_and_encript(self.p_password + sufix, key) + self.div_word
                encripted_data.append(salt_string)
            elif prefix == self.p_token:
                salt_string = self.__salt_and_encript(self.p_token + sufix, key) + self.div_word
                encripted_data.append(salt_string)
        
        with open(encripted_file, "ab") as f:
            f.writelines(encripted_data)
    
    @staticmethod
    def comprobe_duplicates(dicto: dict) -> dict:
        # shift key number if duplicate
        new_dicto = copy.deepcopy(dicto)
        for site in dicto:
            users = []
            for key in dicto[site]:
                user = new_dicto[site][key]["user"]
                if user in users:
                    del(new_dicto[site][key])
                    continue
                users.append(user)
        return new_dicto

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
            raise Exception(FileExistsError(f"Exist an encripted file called {encripted_file}"))
        if os.path.isfile(file) is False:
            raise Exception(FileNotFoundError("File must exist"))
        encripted_data = []
        
        with open(file, "r", encoding = 'utf-8') as f:
            for line in f:
                new_line = line.rstrip()
                prefix = new_line[:3]
                sufix = new_line[3:].strip()
                
                if prefix == self.p_sitio:
                    salt_string = self.__salt_and_encript(self.p_sitio + sufix, key) + self.div_word
                    encripted_data.append(salt_string)
                elif prefix == self.p_user:
                    salt_string = self.__salt_and_encript(self.p_user + sufix, key) + self.div_word
                    encripted_data.append(salt_string)
                elif prefix == self.p_password:
                    salt_string = self.__salt_and_encript(self.p_password + sufix, key) + self.div_word
                    encripted_data.append(salt_string)
                elif prefix == self.p_token:
                    salt_string = self.__salt_and_encript(self.p_token + sufix, key) + self.div_word
                    encripted_data.append(salt_string)
                    
        with open(encripted_file, "wb") as f:
            f.writelines(encripted_data)
    
    def load_and_decript_file(self, encripted_file: str, key: bytes) -> list:
        if os.path.isfile(encripted_file) is False:
            raise Exception(FileNotFoundError("File must exist"))
        
        out = []
        with open(encripted_file, "rb") as f:
            lines = f.read()
            words = lines.split(self.div_word)
            for word in words:
                if word == b"":
                    continue
                etxt = word[:-32]
                tag = word[-32:-16]
                nonce = word[-16:]
                try:
                    decript = self.__AES_decript(key, etxt, nonce, tag).decode()
                except:
                    raise (Exception(ValueError("MAC check failed. The introduced key is incorrect")))
                out.append(decript)
        return self.comprobe_duplicates(self.__remove_salt(out))
            
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

                if prefix == self.p_sitio:
                    sitio = sufix
                    if sitio not in sites:
                        num_users = 0
                    sites.append(sitio)
                    user = ""
                    password = ""
                    token = ""
                    continue

                elif prefix == self.p_user:
                    user = sufix
                    num_users += 1
                    continue

                elif prefix == self.p_password:
                    password = sufix

                elif prefix == self.p_token:
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
        return self.comprobe_duplicates(data_dict)

    def random_password(self, size: int = 16) -> str:
        out = self.p_password
        for _ in range(size):
            out += random.choice(self.__characters)
        return out

    def __remove_salt(self, salty_list: list) -> dict:
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
            
            if prefix == self.p_sitio:
                sitio = sufix
                if sitio not in sites:
                    num_users = 0
                sites.append(sitio)
                user = ""
                password = ""
                token = ""
                continue

            elif prefix == self.p_user:
                user = sufix
                continue

            elif prefix == self.p_password:
                password = sufix

            elif prefix == self.p_token:
                token = sufix
            else:
                continue
            
            if data_dict.get(sitio) is None and token == "" and user != "" and password != "":
                data_dict[sitio] = {1 : {"user": user, "password": password}}

            elif data_dict.get(sitio) and token == "" and user != "" and password != "":
                num_users = len(data_dict[sitio]) + 1
                data_dict[sitio][num_users] = {"user": user, "password": password}

            elif data_dict.get(sitio) and token != "" and user != "" and password != "":
                for number in data_dict[sitio]:
                    if user is data_dict[sitio][number]["user"]:
                        data_dict[sitio][number]["token"] = token
                        break
        return data_dict

    def __salt_and_encript(self, string: str, key) -> tuple[bytes, bytes, bytes]:
        out = key.decode()[0] + string[0] + key.decode()[1] + string[1:-1] + key.decode()[-2] + string[-1] + key.decode()[-1]
        return self.__AES_encript(out, key)