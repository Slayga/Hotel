"""
Name: Gabriel Engberg, Viggo Rubin
Date: 28-02-2022
Info: Main running file for this application
"""

# Pickle or Json dump...
# Tkinter...imgui? https://github.com/pyimgui/pyimgui/pull/264

import json
from typing import Iterable

# Todo: Be implemented in HotelManager?
class DataHandling:
    # Should just be extracted from the class and be standalone function instead of method...
    @staticmethod
    def create_file(path: str, ext: str = "json"):
        json.dump(open(str(path + ext), "w")).close()
        return 1

    # Should just be extracted from the class and be standalone function instead of method...
    @staticmethod
    def pack_data(data: Iterable, path: str, mode: str = "w") -> bool:
        ...

    # Should just be extracted from the class and be standalone function instead of method...
    @staticmethod
    def unpack_data(path: str) -> dict:
        # If path is empty or no value
        if not path:
            return -1
        try:
            with open(path) as f:
                return json.load(f)
        except FileNotFoundError:
            return -1


class HotelManager:
    def __init__(self, path, auto_load: bool = True):
        # Will automatically load data from given json file...
        if auto_load:
            # Tries to unpack data from file
            self.data = DataHandling().unpack_data()
            # Incase no file was found at path
            if self.data == -1:
                # Create file
                DataHandling().create_file(path)
                # Retry unpacking
                self.data = DataHandling().unpack_data()
                # If still failing to load raise an exception
                if self.data == -1:
                    raise Exception(
                        "Unexpected error in unpacking file: path:%s".format(
                            path
                        )
                    )
                else:
                    self.users = (
                        self.data["users"] if "users" in self.data else dict()
                    )
                    self.rooms = (
                        self.data["rooms"] if "rooms" in self.data else dict()
                    )
                    self.bookings = (
                        self.data["bookings"]
                        if "bookings" in self.data
                        else dict()
                    )
                    self.old_books = (
                        self.data["old_books"]
                        if "old_books" in self.data
                        else dict()
                    )
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
