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
file = r"file.txt" # must be organized -> //u, //s, //p, //d
"""
Warning - avoid using .txt files
"""
file_encripted = file[:-4] + r"_encripted.bin" # Where the encripted data will be

ch = EaD()
ch.encript_file(file, key)

# Loading normal file organized -> //u, //s, //p, //d
file_text = ch.load_data(file)
 
"""
# Encript and add this information to the file encripted.
# If the file doesn't have .bin extension, will arise an exception
# If the list doesn't have at least this 3 elements, it won't be added
# If an item from the list doesn't have this format, it will be ignored.
"""
ch.add_data_to_file(["//ssite4", "//uuser4", "//ppass4"], file_encripted, key) 
ch.add_data_to_file(["//ssite1", "//uuser5", "//ppass5", "ignored"], file_encripted, key)

key =     b'Sixteen byte key'
decripted_text = ch.load_and_decript_file(file_encripted, key)