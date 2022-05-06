"""
Project: Hotel managment system \n
Name: Gabriel Engberg, Viggo Rubin \n
Date: 28-02-2022 \n
Info: Main running file for hotel application. \n
This is in theory meant to be used by personal at a given hotel, 
hence the management of seeing SSN easily.
"""

# Pickle or Json dump...
# Tkinter...Imgui? https://github.com/pyimgui/pyimgui/pull/264

from typing import Collection, Any, Iterator
import json
import os
from abc import ABCMeta, abstractmethod


class JsonHandling:
    """
    Class for handling json data from json files
    """

    def __init__(self, filename: str = "hotel.json"):
        """
        Constructor for JsonHandling

        Args:
            filename (str, optional): Name of the file to be used. Defaults to hotel.json.
        """
        self.filename = filename
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
        """Setter for path"""
        raise ValueError("Path attr. cant be changed")

    @folder.setter
    def folder(self, _: str):
        """Setter for folder"""
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

    def pack_data(self, json_data: dict, mode: str = "w"):
        """
        Writes json data to a json file

        Args:
            json_data (dict): data to be stored in json file,
                        #! NOTE that all keys must be of type str
            mode (str, optional): Mode the file will be open in. Defaults to "w".
        """
        with open(self.full_path, mode) as f:
            json.dump(json_data, f)

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
    Used to manipulate json data from given file that class JsonHandling returns
    when unpacking.

    HotelManager uses methods for: checking in, checking out,
    adding bookings, removing bookings, editing bookings, adding rooms,
    removing rooms, editing rooms, register users, unregister users and printing raw json_data.
    """

    def __init__(self, filename: str = ""):
        """Constructor for HotelManager

        Args:
            filename (str, optional): Optional argument for the name of the file. Defaults to "".
        """
        # Unpacking and loading json_data from given path(Default is None)
        self.json_handler = JsonHandling(filename)
        self.json_data = self.json_handler.unpack_data()

        # Extracting or creating required structures
        self.users = self.json_data["users"] if "users" in self.json_data else dict()
        self.rooms = self.json_data["rooms"] if "rooms" in self.json_data else list()
        # All 'active' bookings are stored in active
        self.active = self.json_data["active"] if "active" in self.json_data else dict()
        self.old = self.json_data["old"] if "old" in self.json_data else dict()
        # Used when packing or updating json_data
        self._extracted = {
            "users": self.users,
            "rooms": self.rooms,
            "active": self.active,
            "old": self.old,
        }

        # Type hinting for pylance, only noticeable in IDE with basic or strict type checking...
        self.json_data: dict[str, Any]
        self.users: dict[str, dict[str, str]]
        self.rooms: list[dict[str, str | list[str]]]
        self.active: dict[str, dict[str, str | bool]]
        self.old: dict[str, int]

    def __str__(self):
        """
        Returns a string representation of the class HotelManager.
        Will ultimately return a string of amount of bookings, total room and vacant rooms.
        """
        # Filter dict to get only vacant rooms
        vacant_room = self.filter_dict(self.rooms, {"state": "vacant"})
        return f"Total bookings: {len(self.active)}\nTotal rooms: {len(self.rooms)}\nVacant rooms: {len(vacant_room)if vacant_room is not None else 0 }"

    def register_user(self, ssn: str, name: str, age: str) -> str | bool:
        """
        Registers a user to the HotelManager.
        Will return a string or boolean depending on success.
        (Type check for the str or bool)

        Args:
            ssn (str): string of 12 characters representing a user's social security number
            name (str): name of given user
            age (str): age of given user

        Returns:
            str | bool: str on failure, boolean(True) on success
        """
        # Check if a user is already registered
        if ssn in self.users:
            return "User with given ssn already exists"
        # Check if age is a number
        if not age.isdigit():
            return "Age must be a number"
        # Else add user to self.users with ssn as the key
        self.users[ssn] = {"name": name, "age": age}
        return True

    def is_registered(self, ssn: str) -> bool:
        """
        Returns a boolean depending on whether a user is registered or not.

        Args:
            ssn (str): SSN of user

        Returns:
            bool: True if a user is registered, False otherwise
        """
        return ssn in self.users

    def unregister_user(self, ssn) -> bool | str:
        """
        Unregister a user from the HotelManager.
        Will return a string or boolean depending on success.
        (Type check for the str or bool)

        Args:
            ssn (str): string of 12 characters representing a user's social security number

        Returns:
            str | bool: str on failure, boolean(True) on success
        """
        # Check if a user is already registered
        if ssn not in self.users:
            return "User with given ssn does not exist"
        # Else add user to self.old and remove user from self.users with ssn as the key
        self.old[ssn] += 1
        del self.users[ssn]
        return True

    def check_in(self, ssn: str) -> bool:
        """
        Called when user is trying to check in to hotel

        Args:
            ssn (str): ssn of user wanting to check in

        Returns:
            bool: Boolean on success or failure
        """
        # Checks if user exists
        if ssn in self.users:
            # Check if already booked
            if ssn in self.active:
                # Check if not checked in
                if not self.users[ssn]["checked_in"]:
                    # Good to check in...
                    self.active[ssn]["checked_in"] = True
                    self._update_json()
                    return True
        # If the controlstructure failed, returns False.
        return False

    def check_out(self, ssn: str) -> bool:
        """
        Called when user is trying to check out to hotel

        Args:
            ssn (str): ssn of user wanting to check out

        Returns:
            bool: Boolean on success or failure
        """
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
                # Update json_data
                self._update_json()
                return True
        # If the controlstructure failed, returns False.
        return False

    def add_booking(self, ssn: str, room: str) -> bool:
        """
        Called when user is booking a room. Must be registered to add booking.

        Args:
            ssn (str): ssn of user\n
            room (str): room number(digits): "1", "2", "3" etc.

        Returns:
            bool: Boolean on success or failure
        """
        # Checks if user exists and NOT already booked
        if ssn in self.users and ssn not in self.active:
            if room.isdigit():
                # Convert to int and move one step back for correct indexing
                room_index = int(room) - 1
                # Check if room is in range
                if 0 <= room_index < len(self.rooms):
                    #  Check if room is vacant
                    if self.rooms[room_index]["state"] == "vacant":
                        # Change room state to occupied
                        self.rooms[room_index]["state"] = "occupied"
                        # Add booking to active dict
                        self.active[ssn] = {"room": room, "checked_in": False}
                        # Update json_data
                        self._update_json()
                        return True
        # If the controlstructure failed, returns False.
        return False

    def remove_booking(self, ssn: str, unregister: bool) -> bool:
        """
        Called when user is removing a booking. Must be registered to remove booking.

        Args:
            ssn (str): ssn of user\n
            room (str): room number(digits): "1", "2", "3" etc.

        Returns:
            bool: Boolean on success or failure
        """
        # Check if user exists and is booked
        if ssn in self.users and ssn in self.active:
            # Check if not checked in
            if not self.active[ssn]["checked_in"]:
                # Change room state to vacant
                self.rooms[int(self.active[ssn]["room"]) - 1]["state"] = "vacant"
                # Remove booking from active dict
                del self.active[ssn]
                if unregister:
                    # Unregister user
                    if not self.unregister_user(ssn):
                        # Failed un-registration
                        return False
                # Update json_data
                self._update_json()
                return True
        # If the controlstructure failed, returns False.
        return False

    def edit_booking(self):
        ...

    def add_room(
        self,
        name: str,
        price: str,
        capacity: str,
        state: str,
        description: str,
        misc: list[str],
    ) -> bool:
        """
        Adds a room to the hotel.

        Args:
            name (str): Name of the room, example: JuniorSuite\n
            price (str): Price per night, example: 19.99\n
            capacity (str): How many can fit? example: 2\n
            state (str): State of the room, example: vacant or occupied\n
            description (str): A short description, who its fitted for\n
            misc (list[str]): list of additional information, example: wifi, type of bed, etc.\n

        Returns:
            bool: True if operation was successful, False otherwise
        """
        user: str = ""
        message: str = ""
        self.rooms.append(
            {
                "name": name,
                "price": price,
                "capacity": capacity,
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
                                    Defaults to None.\n
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

    def _update_json(self):
        """
        Updates data structure with new json_data and loads the new json_data
        """
        # Updates each dict in self.json_data
        for key, value in self._extracted.items():
            self.json_data.update({key: value})

        # Same practice as constructor
        self.json_handler.pack_data(self.json_data)
        self.json_data = self.json_handler.unpack_data()

        self.users = self.json_data["users"] if "users" in self.json_data else dict()
        self.rooms = self.json_data["rooms"] if "rooms" in self.json_data else list()
        self.active = self.json_data["active"] if "active" in self.json_data else dict()
        self.old = self.json_data["old"] if "old" in self.json_data else dict()


class HotelInterface(metaclass=ABCMeta):
    """
    All classes that "connect" to the hotel is derived from HotelInterface.
    An abstract class that predefines implementations requirements.
    """

    @abstractmethod
    def __init__(self):
        """
        Initializes the hotel object that it will connect to

        Expected Args:
            hotel (HotelManager): HotelManager object
        """

    @abstractmethod
    def run(self):
        """
        Implement the run method to start the interface.
        TL:DR; Talk to the self.hotel object
        """
        ...


class WebHotel(HotelInterface):
    # Django or Flask implementation
    ...


class GuiHotel(HotelInterface):
    # PyImgui implementation
    ...


class ConsoleHotel(HotelInterface):
    """Normal console (print) implementation"""

    def __init__(self, hotel: HotelManager):
        # Object instance of HotelManager class
        self.hotel = hotel

        # Console related attributes
        self._menu_option = {
            "header": "Nimbus Hotel",
            "description": "Welcome to Nimbus Hotel's Navigation Menu.\nPlease select an option.",
            "options": {
                "Hotel Info": self._print_hotel_info,
                "View all vacant rooms": self._print_all_vacant,
                "Add Booking": self._add_booking,
                "Register": self._register_user,
                "Book": self._add_booking,
                "Check-in": self._check_in,
                "Check-out": self._check_out,
            },
            "exit": "#",
        }

    def run(self):
        """
        Runs the interface. Prints the menu and waits for user input
        and call respective function, until opted to exit
        """
        # Main loop
        while True:
            # Prints the menu and gets input
            user_input = self._print_menu()

            if user_input.isdigit():  # type: ignore
                if int(user_input) in range(0, len(self._menu_option["options"])):
                    # If input is a number, execute the corresponding function
                    self._menu_option["options"][
                        list(self._menu_option["options"].keys())[int(user_input)]
                    ]()

            elif user_input == self._menu_option["exit"]:
                # Update json_data before exiting
                self.hotel._update_json()
                # Exits the loop & program
                break

    @staticmethod
    def _userPrint(*args, **kwargs):
        """
        Override to print ">>" before message that is directed to a user.
        For visibility purposes.
        Used exactly like print().
        """
        print(">> ", end="")
        print(*args, **kwargs)

    @staticmethod
    def _userInput(*args, **kwargs):
        """
        Override to print ">>" before message that is directed to a user.
        For visibility purposes.
        """
        print(">> ", end="")
        return input(*args, **kwargs)

    @staticmethod
    def clear_console():
        """
        Clears the console.
        """
        os.system("cls" if os.name == "nt" else "clear")

    def _print_menu(self, noInput=False, noClear=False) -> str:
        """
        Prints the predefined menu options

        Args:
            noInput (bool, optional): Option to not prompt the user for input. Defaults to False.

        Returns:
            str | None: str if user input is expected else None
        """
        # Clear console window if user hasn't disabled the option
        self.clear_console() if not noClear else ...

        print(self._menu_option["header"])
        print("=" * len(self._menu_option["header"]))
        print(self._menu_option["description"])
        # Prints the menu options
        print("-" * max(len(opt) for opt in self._menu_option["options"]))
        for index, option in enumerate(self._menu_option["options"]):
            self._userPrint(f"[{index}] {option}")

        # Print exit option
        self._userPrint(
            f"[{self._menu_option['exit']}] Exit or return to top level menu"
        )
        print("")
        # If no input is required, return None else return user input
        if not noInput:
            return self._userInput("Please select an option: ")

        # If noInput is true, returns an empty string
        return ""

    def _print_hotel_info(self):
        self.clear_console()
        print(self._menu_option["header"])
        print("=" * len(self._menu_option["header"]))
        print(self.hotel)
        self._userInput("Press enter to continue...")

    def _print_all_vacant(self):
        self.vacant_rooms = self.hotel.filter_dict(
            self.hotel.rooms, {"state": "vacant"}
        )
        self.clear_console()
        print(self._menu_option["header"])
        print("=" * len(self._menu_option["header"]))
        print(f"There are {len(self.vacant_rooms)} vacant rooms")
        print("-" * 15)
        # Print out all room information here
        for room in self.vacant_rooms:
            print(f"Type: {room['name']}")
            print(f"State: {room['state']}")
            print(f"Price: {room['price']}c")
            print(f"Capacity: {room['capacity']}")
            print(f"Description: {room['description']}")
            print(f"Features:", ", ".join(room["misc"]))
            print("-" * 15)
        self._userInput("Press enter to continue...")

    def _add_booking(self):
        while not self.hotel.is_registered(
            (userSsn := self._userInput("Please enter your SSN: "))
        ):
            self._userInput("Invalid SSN. Press enter to try again or # to exit")
        userRoom = self._userInput("Please enter the room number: ")

        if self.hotel.add_booking(userSsn, userRoom):
            self._userPrint("Booking successful!")
        else:
            self._userPrint("Booking failed!")
        self._userInput("Press enter to continue...")
        ...

    def _remove_booking(self):
        ...

    def _edit_booking(self):
        ...

    def _add_room(self):
        ...

    def _remove_room(self):
        ...

    def _register_user(self):
        ...

    def _unregister_user(self):
        ...

    def _check_in(self):
        ...

    def _check_out(self):
        ...


def _main():
    test = HotelManager()
    # print(test)

    ConsoleHotel(test).run()


if __name__ == "__main__":
    _main()
    # ConsoleHotel(HotelManager())._print_menu()
    # ConsoleHotel(HotelManager())._userInput("Enter your choice: "))
