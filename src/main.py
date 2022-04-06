"""
Name: Gabriel Engberg, Viggo Rubin
Date: 28-02-2022
Info: Main running file for hotel application. 
This is in theory meant to be used by personal at a given hotel, 
hence the management of seeing SSN easily.
"""

# Pickle or Json dump...
# Tkinter...Imgui? https://github.com/pyimgui/pyimgui/pull/264

import json
import os


class DataHandling:
    """
    Class for handling data from json files
    """

    def __init__(self, filename: str = "hotel.json"):
        """
        Constructor for DataHandling

        Args:
            filename (str, optional): Name of the file to be used. Defaults to hotel.json.
        """
        # For a particular reason, this is needed to call the filename setter
        self._filename = self.filename = filename
        self._folder = "json"
        # Gets absolute path to working directory...
        self._path = os.path.dirname(__file__) + "/" + self.folder
        # Absolute path to file (file included)
        self.full_path = self.path + "/" + self._filename
        # Create self.folder in the current working directory.
        if not os.path.exists(self._path):
            # Make a folder called json in directory if not existing
            os.makedirs(self._path, exist_ok=True)

        # Creates the .json file if it doesn't exist.
        if not os.path.exists(self.full_path):
            self.__create_file(self.full_path)

    @property
    def path(self) -> str:
        """Property for path"""
        return self._path

    @property
    def folder(self) -> str:
        """Property for folder"""
        return self._folder

    @property
    def filename(self) -> str:
        """Property for filename"""
        return self._filename

    @path.setter
    def setter(self, _: str):
        """Setter for path, forcing immutable attr...kinda"""
        raise ValueError("Path attr. cant be changed")

    @folder.setter
    def folder(self, _: str):
        """Setter for folder, forcing immutable attr...kinda"""
        raise ValueError("Folder attr. cant be changed")

    @filename.setter
    def filename(self, value: str):
        """Setter for filename"""
        # Instead of raising an exception on no 'filename' a fallback exists.
        self.__fallback = "hotel.json"
        # Evaluate whetever the custom value(if given is a valid file)
        if value:
            if value.endswith(".json"):
                self._filename = value
            else:
                self._filename = value + ".json"
        else:
            self._filename = self.__fallback

    def __create_file(self, path: str):
        """
        Creates an 'empty' json file

        Args:
            path (str): Given path to file
        """
        # Loads an empty dict into the json file, or it will crash on read.
        # See testing.py in 'test' folder for more details.
        with open(str(path), "w") as f:
            json.dump({}, f)

    def pack_data(self, data: dict, mode: str = "w"):
        """
        Writes data to a json file

        Args:
            data (dict): Data structure of data to be stored,
                        #! NOTE that all keys must be of type str
            mode (str, optional): Mode the file will be open in. Defaults to "w".
        """
        with open(self.full_path, mode) as f:
            json.dump(data, f)

    def unpack_data(self) -> dict:
        """
        Opens json file and returns the data structure as a dictionary

        Returns:
            dict: data stored in json file as a dictionary.
        """
        with open(self.full_path) as f:
            return json.load(f)


class HotelManager:
    """
    Class for managing a hotel database system.
    Used to manipulate data from given file that class DataHandling returns
    when unpacking.

    HotelManager uses methods for: checking in, checking out,
    adding bookings, removing bookings, editing bookings, adding rooms,
    removing rooms, editing rooms, and printing raw data.
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

    def filter_rooms(self, filter_: dict = None) -> list[dict] | dict:
        # Check if filter_ is provided (underscore is to avoid naming conflict)
        if filter_:
            # Example of filter check filter_ = {"state": "vacant"}
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
