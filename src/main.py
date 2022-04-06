"""
Name: Gabriel Engberg, Viggo Rubin
Date: 28-02-2022
Info: Main running file for hotel application. 
This is in theory meant to be used by personal at a given hotel, 
hence the management of seeing SSN easily.
"""

# Pickle or Json dump...
# Tkinter...Imgui? https://github.com/pyimgui/pyimgui/pull/264

from typing import Collection, Any, Iterator
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

        # Extracting or creating required structures
        self.users = self.data["users"] if "users" in self.data else dict()
        self.rooms = self.data["rooms"] if "rooms" in self.data else list()
        # All 'active' bookings are stored in active
        self.active = self.data["active"] if "active" in self.data else dict()
        self.old = self.data["old"] if "old" in self.data else dict()
        # Used when packing or updating data
        self._extracted = {
            "users": self.users,
            "rooms": self.rooms,
            "active": self.active,
            "old": self.old,
        }

        # Type hinting for pylance, only noticeable in IDE with basic or strict type checking...
        self.data: dict[str, Any]
        self.users: dict[str, dict[str, str]]
        self.rooms: list[dict[str, str | list[str]]]
        self.active: dict[str, dict[str, str | bool]]
        self.old: dict[str, int]

    def __str__(self):
        """
        Returns a string representation of the hotel manager.
        """
        # Filter dict to get only vacant rooms
        vacant_room = self.filter_dict(self.rooms, {"state": "vacant"})
        return f"Total bookings: {len(self.active)}\nTotal rooms: {len(self.rooms)}\nVacant rooms: {len(vacant_room)if vacant_room is not None else 0 }"

    def check_in(self, ssn: str) -> bool:
        # Checks if user exists
        if ssn in self.users:
            # Check if already booked
            if ssn in self.active:
                # Check if not checked in
                if not self.users[ssn]["checked_in"]:
                    # Good to check in...
                    self.active[ssn]["checked_in"] = True
                    self._update_data()
                    return True
        # If the controlstructure failed, returns False.
        return False

    def check_out(self, ssn: str) -> bool:
        # Check if user exists and is booked
        if ssn in self.users and ssn in self.active:
            # Check if checked in
            if self.active[ssn]["checked_in"]:
                # Good to check out...
                self.active[ssn]["checked_in"] = False
                # Increment times stayed at the hotel
                self.old[ssn] += 1
                # Remove booking from active dict
                del self.active[ssn]
                # Update data
                self._update_data()
                return True
        return False

    def add_booking(self, ssn: str, room: str) -> bool:
        # Checks if user exists and NOT already booked
        if ssn in self.users and ssn not in self.active:
            # Convert to int and move one step back for correct indexing
            if room.isdigit():
                room_index = int(room) - 1
                # Check if room is in range
                if 0 <= room_index < len(self.rooms):
                    #  Check if room is vacant
                    if self.rooms[room_index]["state"] == "vacant":
                        # Change room state to occupied
                        self.rooms[room_index]["state"] = "occupied"
                        # Add booking to active dict
                        self.active[ssn] = {"room": room, "checked_in": False}
                        # Update data
                        self._update_data()
                        return True
        # If the controlstructure failed, returns False.
        return False

    def remove_booking(self, ssn: str) -> bool:
        # Check if user exists and is booked
        if ssn in self.users and ssn in self.active:
            # Check if not checked in
            if not self.active[ssn]["checked_in"]:
                # Change room state to vacant
                self.rooms[int(self.active[ssn]["room"]) - 1][
                    "state"
                ] = "vacant"
                # Remove booking from active dict
                del self.active[ssn]
                # Update data
                self._update_data()
                return True
        return False

    def edit_booking(self):
        ...

    def add_room(
        self,
        name: str,
        price: str,
        space: str,
        state: str,
        description: str,
        misc: list[str],
    ) -> bool:
        """
        Adds a room to the hotel.

        Args:
            name (str): Name of the room, example: JuniorSuite
            price (str): Price per night, example: 19.99
            space (str): How many can fit? example: 2
            state (str): State of the room, example: vacant or occupied
            description (str): A short description, who its fitted for
            misc (list[str]): list of additional information, example: wifi, type of bed, etc.

        Returns:
            bool: True if operation was successful, False otherwise
        """
        user: str = ""
        message: str = ""
        self.rooms.append(
            {
                "name": name,
                "price": price,
                "space": space,
                "state": state,
                "description": description,
                "misc": misc,
                "user": user,
                "message": message,
            }
        )
        return True

    def remove_room(self):
        ...

    def edit_room(self):
        ...

    def filter_dict(
        self,
        data: Collection[dict],
        filter_: dict | None = None,
        inverted: bool = False,
    ) -> list[dict] | Collection[dict]:
        """Returns a list of all filtered matches depending on given filter

        Args:
            filter_ (dict, optional): A dict of len == 1 where the key is going to be
                                    matched with similar key and also compare value to value.
                                    Defaults to None.
            inverted (bool, optional): Ability to invert results. Defaults to False.

        Returns:
            list[dict] | list: A list of filtered matches or all the matches if no filter is given.
        """
        # Check if filter_ is provided (underscore is to avoid naming conflict)
        if filter_:
            filtered: list = list()
            # Gets first key in dict
            filter_key = list(filter_.keys())[0]
            for value in data:
                if value[filter_key] == filter_[filter_key]:
                    filtered.append(value)
            else:
                if inverted:
                    # Returns the inverted list
                    return [value for value in data if value not in filtered]
                else:
                    return filtered
        else:
            # If no filter was given, return data (all)
            return data

    def _pretty_print(self):
        ...

    def _update_data(self):
        """
        Updates data structure with new data and loads the new data
        """
        # Updates each dict in self.data
        for key, value in self._extracted.items():
            self.data.update({key: value})

        # Same practice as constructor
        self.data_handler.pack_data(self.data)
        self.data = self.data_handler.unpack_data()

        self.users = self.data["users"] if "users" in self.data else dict()
        self.rooms = self.data["rooms"] if "rooms" in self.data else list()
        self.active = self.data["active"] if "active" in self.data else dict()
        self.old = self.data["old"] if "old" in self.data else dict()


class GuiHotel:
    ...


def main():
    test = HotelManager()
    print(test)


if __name__ == "__main__":
    main()
