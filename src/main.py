"""
Name: Gabriel Engberg, Viggo Rubin
Date: 28-02-2022
Info: Main running file for this application
"""

# Pickle or Json dump...
# Tkinter...Imgui? https://github.com/pyimgui/pyimgui/pull/264

import json
import os

# Todo: Be implemented in HotelManager? Or... Extract methods to standalone functions
class DataHandling:
    def __init__(self, filename: str):
        self._filename = self.filename = filename
        self._folder = "json"
        self._path = os.path.dirname(__file__) + "/" + self.folder
        self.full_path = self.path + "/" + self._filename
        # Create self.folder in the current working directory.
        if not os.path.exists(self._path):
            #
            os.makedirs(self._path, exist_ok=True)

        if not self.__file_exists(self.full_path):
            self.__create_file(self.full_path)

    @property
    def path(self) -> str:
        return self._path

    @property
    def folder(self) -> str:
        return self._folder

    @property
    def filename(self) -> str:
        """Property for filename"""
        return self._filename

    @path.setter
    def setter(self, value: str):
        raise ValueError("Path cant be changed")

    @folder.setter
    def folder(self, value: str):
        raise ValueError("Folder cant be changed")

    @filename.setter
    def filename(self, value: str):
        """Setter for filename"""
        # Instead of raising an exception on 'empty filename' a fallback exists.
        self.__fallback = "hotel.json"
        if value:
            if value.endswith(".json"):
                self._filename = value
            else:
                self._filename = value + ".json"
        else:
            self._filename = self.__fallback

    def __file_exists(self, path: str) -> bool:
        return os.path.exists(path)

    def __create_file(self, path: str):
        with open(str(path), "w") as f:
            json.dump({}, f)

    def pack_data(self, data: dict, mode: str = "w") -> bool:
        with open(self.full_path, mode) as f:
            json.dump(data, f)

    def unpack_data(self) -> dict:
        try:
            with open(self.full_path) as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError("Unresolved file error:", self.filename)


class HotelManager:
    """
    Class for managing a hotel database system.
    Used to manipulate data from given file that class DataHandling returns
    when unpacking.

    HotelManager uses methods for checking in, checking out,
    adding bookings, removing bookings, editing bookings, adding rooms,
    removing rooms, editing rooms, and printing data.
    """

    def __init__(self, filename: str = ""):
        # Unpacking and loading data from given path(Default is None)
        self.data_handler = DataHandling(filename)
        self.data = self.data_handler.unpack_data()

        # Creating required structures
        self.users = self.data["users"] if "users" in self.data else dict()
        self.rooms = self.data["rooms"] if "rooms" in self.data else dict()
        self.old = self.data["old"] if "old" in self.data else dict()

    def check_in(self):
        ...

    def check_out(self):
        ...

    def add_booking(self):
        """
        To add a booking, the user must register with SSN and password.
        And then select a room. Via console input.
        """
        userInput = input(">> Press enter to browse through vacant rooms.. ")
        ...

    def remove_booking(self):
        ...

    def edit_booking(self):
        ...

    def filter_rooms(self, filter_:dict = None) -> list:
        # key: What key to check for each room, value is the value of the key
        # Check if filter_ is provided (underscore is to avoid naming conflict)
        filter_ = False if filter_ is None else filter_
        if filter_:
            for room in self.rooms:
                ...
        else:
            # If no filter was given, return self.rooms (all rooms)
            return self.rooms
        

    def add_room(self):
        ...

    def remove_room(self):
        ...

    def edit_room(self):
        ...

    def _pretty_print(self):
        ...


class GuiHotel:
    ...


def main():
    HotelManager()


if __name__ == "__main__":
    main()
