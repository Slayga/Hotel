"""
Name: Gabriel Engberg, Viggo Rubin
Date: 28-02-2022
Info: Main running file for this application
"""

# Pickle or Json dump...
# Tkinter...imgui? https://github.com/pyimgui/pyimgui/pull/264
"""
import json

# dict to save into a file and the load into memory again...
dict_data = {"name": "bob"}

# path and write mode
a_file = open("src/bobdumb.json", "w")

# dump the data to the file
json.dump(dict_data, a_file)

# !IMPORTANT: closing file...
a_file.close()

# path and read mode...
a_file = open("src/bobdumb.json", "r")

# json.load loads the dict into var output
output = json.load(a_file)

# Just to print output and check type
print(output, type(output))

# !IMPORTANT: close file when finished...
a_file.close()

"""

import json

# Writing data with context manager...
dict_data = {"name": "bob"}
with open("src/bobdump.json", "w") as f:
    json.dump(dict_data, f)

# Reading data with context manager...
with open("src/bobdump.json") as f:
    json_content = json.load(f)

print(json_content, type(json_content))

# Pack & unpack data?
import json
from typing import Iterable


class DataHandling:
    def __init__(self):
        ...

    def pack_data(self, data: Iterable, path: str, mode: str = "w") -> bool:
        ...

    def unpack_data(self) -> Iterable:
        ...


class HotelManager:
    def __init__(self):
        ...

    def check_in(self):
        ...

    def check_out(self):
        ...

    def add_booking(self):
        ...

    def remove_booking(self):
        ...

    def edit_booking(self):
        ...

    def show_bookings(self):
        ...

    def add_room(self):
        ...

    def remove_room(self):
        ...

    def edit_room(self):
        ...
