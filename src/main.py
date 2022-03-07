"""
Name: Gabriel Engberg, Viggo Rubin
Date: 28-02-2022
Info: Main running file for this application
"""

# Pickle or Json dump...
# Tkinter...Imgui? https://github.com/pyimgui/pyimgui/pull/264

import json

# Todo: Be implemented in HotelManager? Or... Extarct methods to standalone functions
class DataHandling:
    def __init__(self, path, fallBackName: str = "/hotel", ext: str = ".json"):
        # Check if path is valid and if the json file was given
        # else add fallBackName and .json to path.
        if path is None:
            self.path = fallBackName + ext
        else:
            self.path = path if path.endswith(ext) else self.path + fallBackName + ext

    # Should just be extracted from the class and be standalone function instead of method...
    def create_file(self):
        # Creates a empty file with empty dict
        with open(str(self.path), "w") as f:
            json.dump({}, f)
        return 1

    # Should just be extracted from the class and be standalone function instead of method...
    def pack_data(self, data: dict, mode: str = "w") -> bool:
        with open(self.path, mode) as f:
            json.dump(data, f)

    # Should just be extracted from the class and be standalone function instead of method...
    def unpack_data(self) -> dict:
        # If path is empty or no value
        try:
            with open(self.path) as f:
                return json.load(f)
        except FileNotFoundError:
            return -1


class HotelManager:
    def __init__(self, path):
        self.path = path
        # Tries to unpack data from file
        self.data = DataHandling().unpack_data(self.path)
        # Incase no file was found at path
        if self.data == -1:
            # Create file
            DataHandling().create_file(path)
            # Retry unpacking
            self.data = DataHandling().unpack_data(self.path)
            # If still failing to load raise an exception
            if self.data == -1:
                raise Exception(
                    "Unexpected error in unpacking file: path:'{}'".format(path)
                )
            else:
                # Basically if the json file has saved data already
                # it assigns the values (dicts) to the attribute if
                # the key is in the data... see below:
                # data_a = data["a"] if "a" in data else dict()
                self.users = self.data["users"] if "users" in self.data else dict()
                self.rooms = self.data["rooms"] if "rooms" in self.data else dict()
                self.bookings = (
                    self.data["bookings"] if "bookings" in self.data else dict()
                )
                self.old_books = (
                    self.data["old_books"] if "old_books" in self.data else dict()
                )
        # Should just load data automatically...remove the implementation of
        # auto_load and always load file on init. As it creates file when no file...
        else:
            self.users = dict()
            self.rooms = dict()
            self.bookings = dict()
            self.old_books = dict()  # Breaking GDPR be like...

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

    def _pretty_print(self):
        ...
