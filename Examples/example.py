import os
import sys

file_dir = __file__
current_dir = os.path.dirname(file_dir)
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from utils.dec import EaD

# Creating a Key
key = b'Sixteen byte key'

# Files from we import the data
file = r"file.txt" # must be organized -> //u, //s, //p
file_encripted = file[:-4] + r"_encripted.bin" # Where the encripted data will go

ch = EaD()
ch.encript_file(file, key)

 
"""
# Encript and add this information to the file encripted.
# If the file doesn't have .bin extension, will arise an exception
# If the list doesn't have at least this 3 elements, it won't be added
# If an item from the list doesn't have this format, it will be ignored.
"""
ch.add_data_to_file(["//ssite4", "//uuser4", "//ppass4"], file_encripted, key) 
ch.add_data_to_file(["//ssite1", "//uuser5", "//ppass5", "ignored"], file_encripted, key)
file_text = ch.load_data(file)

# There are 2 differents forms to load and decript a file.
key =     b'Sixteen byte key'
new_key = b'A new key to use'
diferent_encripted_file = "different.bin"
#decripted_text = ch.load_and_decript_file(file_encripted, b'Sixteen byte ke1') # Exception - not right key.
#decripted_text = ch.load_and_decript_file(diferent_encripted_file, new_key) # Ok (uses a diferent key from where you initialize the class)
decripted_text = ch.load_and_decript_file(file_encripted, key) # Ok uses the previous one key. (new_key, if it was uncommented)
print(decripted_text)
# Recomended if you will uses diferents files and keys
#decripted_text = ch.load_and_decript_file(file_encripted, key) # Ok (uses a diferent key from where you initialize the class)