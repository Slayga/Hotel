"""
Project: Hotel management system \n
Name: Gabriel Engberg, Viggo Rubin \n
Date: 28-02-2022 \n
Info: Main running file for hotel application. \n
This is in theory meant to be used by personal at a given hotel, 
hence the management of seeing SSN easily.
"""

from abc import ABCMeta, abstractmethod
import json
import os
# Typing is used for type-hinting
from typing import Collection, Any


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
        # Evaluate whatever the custom value(if given is a valid file)
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
        """
        Constructor for HotelManager

        Args:
            filename (str, optional): Optional argument for the name of the file. Defaults to "".
        """
        # Unpacking and loading json_data from given path(Default is None)
        self.json_handler: JsonHandling = JsonHandling(filename)
        self.json_data = self.json_handler.unpack_data()

        # Extracting or creating required structures
        self.users = (self.json_data["users"]
                      if "users" in self.json_data else dict())
        self.rooms = (self.json_data["rooms"]
                      if "rooms" in self.json_data else list())
        # All 'active' bookings are stored in active
        self.active = (self.json_data["active"]
                       if "active" in self.json_data else dict())
        self.old = self.json_data["old"] if "old" in self.json_data else dict()

        # Updates the file incase one of the values wasn't in the file
        self._update_json()

        # Type hinting for pylance, only noticeable in IDE with basic or strict type checking... Ignore
        self.json_data: dict[str, Any]
        self.users: dict[str, dict[str, str]]
        self.rooms: list[dict[str, str | list[str]]]
        self.active: dict[str, dict[str, str | bool]]
        self.old: dict[str, dict[str, str]]

    def __str__(self):
        """
        Returns a string representation of the class HotelManager.
        Will ultimately return a string of amount of bookings, total room and vacant rooms.
        """
        # Filter dict to get only vacant rooms
        vacant_room = self.filter_dict(self.rooms, {"state": "vacant"})
        return f"Total bookings: {len(self.active)}\nTotal rooms: {len(self.rooms)}\nVacant rooms: {len(vacant_room)if vacant_room is not None else 0 } \nRegistered users: {len(self.users)}"

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
        if self.is_registered(ssn):
            return "User with given ssn already exists"

        # Check if age is a number
        if not age.isdigit():
            return "Age must be a number"
        # Else add user to self.users with ssn as the key
        self.users[ssn] = {"name": name, "age": age}
        self._update_json()
        return True

    def been_registered(self, ssn: str) -> bool:
        """
        Checks if a user has been registered.

        Args:
            ssn (str): string of 12 characters representing a user's social security number

        Returns:
            bool: True if user is registered, False if not
        """
        return ssn in self.old

    def is_registered(self, ssn: str) -> bool:
        """
        Returns a boolean depending on whether a user is registered or not.

        Args:
            ssn (str): SSN of user

        Returns:
            bool: True if a user is registered, False otherwise
        """
        return ssn in self.users

    def is_ssn_valid(self, ssn: str) -> bool:
        """Evaluate if ssn is valid

        Args:
            ssn (str): Social security number.

        Returns:
            bool: True on success, False otherwise
        """
        # Removes all dashes and spaces
        ssn = ssn.replace("-", "").replace(" ", "")
        if ssn.isdigit():
            if len(ssn) == 12:
                return True
        return False

    def edit_user(self,
                  ssn: str,
                  name: str = "",
                  age: str = "",
                  new_ssn: str = "") -> bool:
        """
        Edits a user's information.

        Args:
            ssn (str): SSN of the CURRENTLY registered user, provide new_ssn to edit this
            name (str, optional): New name. Defaults to "".
            age (str, optional): New age. Defaults to "".
            new_ssn (str, optional): New ssn. Defaults to "".

        Returns:
            bool: True on success, False otherwise
        """
        if not self.is_ssn_valid(ssn):
            return False

        if self.is_registered(ssn):
            # If new ssn is provided, the key must be updated.
            if new_ssn:
                # Changes key in self.users to new_ssn(pop returns the value hence the assignment below)
                self.users[new_ssn] = self.users.pop(ssn)
                # Edit booking ssn
                if self.is_booked(ssn):
                    self.active[new_ssn] = self.active.pop(ssn)
                    booked_room_index = int(self.active[new_ssn]["room"]) - 1
                    self.rooms[booked_room_index]["user"] = new_ssn

                # Edit old ssn
                if ssn in self.old:
                    self.old[new_ssn] = self.old.pop(ssn)
                # To not interfere with multiple changes
                ssn = new_ssn
            if name:
                self.users[ssn]["name"] = name
            if age:
                self.users[ssn]["age"] = age
            self._update_json()
            return True
        # User is not registered
        return False

    def unregister_user(self, ssn: str) -> bool | str:
        """
        Unregister a user from the HotelManager.
        Will return a string or boolean depending on success.

        Args:
            ssn (str): string of 12 characters representing a user's social security number

        Returns:
            str | bool: str on failure, boolean(True) on success
        """
        if not self.is_ssn_valid(ssn):
            return "Invalid ssn"

        # Check if a user is already registered
        if not self.is_registered(ssn):
            return "User with given ssn does not exist"

        if self.is_booked(ssn):
            # Removes current booking, but does not unregister the user(yet)
            self.remove_booking(ssn, False)
        # Total registration count
        if "total registrations" in self.old[ssn]:
            total_reg = int(self.old[ssn]["total registrations"])
        else:
            total_reg = 0

        total_reg += 1
        self.old[ssn]["total registrations"] = str(total_reg)
        self.old[ssn]["name"] = self.users[ssn]["name"]
        self.old[ssn]["age"] = self.users[ssn]["age"]

        del self.users[ssn]

        self._update_json()
        return True

    def check_in(self, ssn: str) -> bool:
        """
        Called when user is trying to check in to hotel

        Args:
            ssn (str): ssn of user wanting to check in

        Returns:
            bool: Boolean on success or failure
        """
        if not self.is_ssn_valid(ssn):
            return False

        # Checks if user exists
        if self.is_registered(ssn):
            # Check if already booked
            if self.is_booked(ssn):
                # Check if not checked in
                if not self.active[ssn]["checked_in"]:
                    # Good to check in...
                    self.active[ssn]["checked_in"] = True
                    self._update_json()
                    return True
        # If the controlstructure failed, returns False.
        return False

    def check_out(self, ssn: str, unregister: bool) -> bool:
        """
        Called when user is trying to check out to hotel

        Args:
            ssn (str): ssn of user wanting to check out
            unregister (bool): Boolean on whether to unregister user or not

        Returns:
            bool: Boolean on success or failure
        """
        if not self.is_ssn_valid(ssn):
            return False

        # Check if user exists and is booked
        if self.is_registered(ssn) and self.is_booked(ssn):
            # Check if checked in
            if self.active[ssn]["checked_in"]:
                # Good to check out...
                booked_room_index = int(self.active[ssn]["room"]) - 1
                self.rooms[booked_room_index]["user"] = ""
                self.rooms[booked_room_index]["message"] = ""
                self.rooms[booked_room_index]["state"] = "vacant"

                self.active[ssn]["checked_in"] = False

                # Remove booking from active dict
                del self.active[ssn]
                if unregister:
                    self.unregister_user(ssn)
                # Update json_data
                self._update_json()
                return True
        # If the controlstructure failed, returns False.
        return False

    def add_booking(self,
                    ssn: str,
                    room: str,
                    message: str = "",
                    _override_is_booked=False) -> bool:
        """
        Called when user is booking a room. Must be registered to add booking.

        Args:
            ssn (str): ssn of user\n
            room (str): room number(digits): "1", "2", "3" etc.
            message (str, optional): message from user. Defaults to "".
            _override_is_booked (bool, optional): Overrides the check for already book 
            (use with precaution). Defaults to False.

        Returns:
            bool: Boolean on success or failure
        """

        if not self.is_ssn_valid(ssn):
            return False

        # Checks if user exists and NOT already booked

        if self.is_registered(ssn):
            if not self.is_booked(ssn) or _override_is_booked:
                if room.isdigit():
                    # Convert to int and move one step back for correct indexing
                    room_index = int(room) - 1
                    # Check if room is in range
                    if 0 <= room_index < len(self.rooms):
                        #  Check if room is vacant
                        if self.rooms[room_index]["state"] == "vacant":
                            # Change room state to occupied
                            self.rooms[room_index]["state"] = "occupied"
                            self.rooms[room_index]["user"] = ssn
                            self.rooms[room_index]["message"] = message
                            # Add booking to active dict
                            self.active[ssn] = {
                                "room": room,
                                "checked_in": False
                            }
                            # Update json_data
                            self._update_json()
                            return True
        # If the controlstructure failed, returns False.
        return False

    def is_booked(self, ssn: str) -> bool:
        """
        Returns a boolean depending on whether a user is booked or not.

        Args:
            ssn (str): SSN of user

        Returns:
            bool: True if a user is booked, False otherwise
        """
        return ssn in self.active

    def remove_booking(self, ssn: str, unregister: bool) -> bool:
        """
        Called when user is trying to remove a booking. Must be registered to remove booking.

        Args:
            ssn (str): _description_
            unregister (bool): unregister the user when removing booking

        Returns:
            bool: _description_
        """
        if not self.is_ssn_valid(ssn):
            return False

        # Check if user exists and is booked
        if self.is_registered(ssn) and self.is_booked(ssn):
            # Check if not checked in
            if not self.active[ssn]["checked_in"]:
                # Change room state to vacant
                booked_room_index = int(self.active[ssn]["room"]) - 1
                # Remove rooms user and message
                self.rooms[booked_room_index]["state"] = "vacant"
                self.rooms[booked_room_index]["user"] = ""
                self.rooms[booked_room_index]["message"] = ""

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

    def _change_room_state(self,
                           room_number: str,
                           state: str = "vacant") -> tuple[str, str] | bool:
        """
        Manually change rooms state, private method as it is supposed to only 
        be called when editing a booking.

        Args:
            room_number (str): Room number, (not index)
            state (str, optional): What state (optional incase further implementation). Defaults to "vacant".

        Returns:
            bool: True on success, else False
        """

        if room_number.isdigit():
            # Convert to int and move one step back for correct indexing
            room_index = int(room_number) - 1
            # Check if room is in range
            if 0 <= room_index < len(self.rooms):
                # Manually change state (note it does not care about user or message):
                self.rooms[room_index]["state"] = state
                message = str(self.rooms[room_index]["message"])
                ssn = str(self.rooms[room_index]["user"])

                # Unset message and user
                self.rooms[room_index]["message"] = ""
                self.rooms[room_index]["user"] = ""

                # Update json_data
                self._update_json()
                return (message, ssn)
        return False

    def edit_booking(self, ssn: str, new_room: str = "", message: str = ""):
        """
        Called when user is trying to edit a booking. Must be registered to edit booking.

        Args:
            ssn (str): SSN of user
            new_room (str, optional): If wished to swap room. Defaults to "".
            message (str, optional): Messages, can be passed alone or with new_room. Defaults to "".

        Returns:
            bool: True if successful, False otherwise
        """
        if not self.is_ssn_valid(ssn):
            return False

        if self.is_registered(ssn) and self.is_booked(ssn):
            if new_room:
                if new_room.isdigit():
                    old_room = str(self.active[ssn]["room"])
                    # Change room state to vacant, returns message and ssn
                    if type(result := self._change_room_state(
                            old_room)) == tuple:
                        old_message, old_ssn = result  # type: ignore
                        if (self.add_booking(old_ssn,
                                             new_room,
                                             old_message,
                                             _override_is_booked=True)):

                            self._update_json()
                            return True
            elif message:
                booked_room = int(self.active[ssn]["room"]) - 1
                self.rooms[booked_room]["message"] = message
                self._update_json()
                return True
        return False

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
        self.rooms.append({
            "name": name,
            "price": price,
            "capacity": capacity,
            "state": state,
            "description": description,
            "misc": misc,
            "user": user,
            "message": message,
        })
        self._update_json()
        return True

    def remove_room(self, room_nr: str) -> bool:
        """
        Removes a room from the hotel.

        Args:
            room_nr (str): Room nr (index in room list + 1)

        Returns:
            bool: True if operation was successful, False otherwise
        """
        if room_nr.isdigit():
            room_index = int(room_nr) - 1
            if 0 <= room_index < len(self.rooms):
                del self.rooms[room_index]
                self._update_json()
                return True
        return False

    def edit_room(
        self,
        room_id: str,
        name: str = "",
        price: str = "",
        capacity: str = "",
        state: str = "",
        description: str = "",
        misc: list[str] = [],
    ):
        """
        Edits a room in the hotel. Only the fields that are not empty will change.

        Args:
            room_id (_type_): Room ID (index in room list + 1)
            name (str): Name of the room, example: JuniorSuite\n
            price (str): Price per night, example: 19.99\n
            capacity (str): How many can fit? example: 2\n
            state (str): State of the room, example: vacant or occupied\n
            description (str): A short description, who its fitted for\n
            misc (list[str]): list of additional information, example: wifi, type of bed, etc.\n
        """
        if room_id.isdigit():
            room_index = int(room_id) - 1
            if 0 <= room_index < len(self.rooms):
                if name:
                    self.rooms[room_index]["name"] = name
                if price:
                    self.rooms[room_index]["price"] = price
                if capacity:
                    self.rooms[room_index]["capacity"] = capacity
                if state:
                    self.rooms[room_index]["state"] = state
                if description:
                    self.rooms[room_index]["description"] = description
                if misc:
                    self.rooms[room_index]["misc"] = misc
                self._update_json()
                return True
        return False

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
        # Unimplemented, intended for debugging only...
        raise NotImplementedError

    def _update_json(self):
        """
        Updates data structure with new json_data and loads the new json_data
        """
        self.json_data["rooms"] = self.rooms
        self.json_data["active"] = self.active
        self.json_data["users"] = self.users
        self.json_data["old"] = self.old

        # Same practice as constructor
        self.json_handler.pack_data(self.json_data)
        self.json_data = self.json_handler.unpack_data()

        self.users = (self.json_data["users"]
                      if "users" in self.json_data else dict())
        self.rooms = (self.json_data["rooms"]
                      if "rooms" in self.json_data else list())
        self.active = (self.json_data["active"]
                       if "active" in self.json_data else dict())
        self.old = self.json_data["old"] if "old" in self.json_data else dict()


class HotelInterface(metaclass=ABCMeta):
    """
    All classes that "connect" to the hotel is derived from HotelInterface.
    An abstract class that predefined implementations requirements.
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

    #! NOT IMPLEMENTED
    ...


class GuiHotel(HotelInterface):
    # PyImgui implementation
    # Specific branch (context manager integration by mcoding):
    # https://github.com/pyimgui/pyimgui/pull/264

    #! NOT IMPLEMENTED
    ...


class ConsoleHotel(HotelInterface):
    """
    ConsoleHotel is a console based interface for the hotel.
    """

    def __init__(self, hotel: HotelManager):
        """
        Constructor for the ConsoleHotel object. Initializes the hotel object that it will connect to.

        Args:
            hotel (HotelManager): hotel object
        """
        # Object instance of HotelManager class
        self.hotel = hotel

        # Console related attributes, avoid having exit value as a number(interferes with options menu
        self._menu_option = {
            "header": "Nimbus Hotel",
            "description":
            "Welcome to Nimbus Hotel's Navigation Menu.\nPlease select an option.",
            "options": {
                "Hotel Info": self._print_hotel_info,
                "User Menu": self._menu_user,
                "Booking Menu": self._menu_booking,
                "Room Menu": self._menu_room,
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
            # Updates the hotels internal information
            self.hotel._update_json()
            # Prints the menu and gets input
            user_input = self._print_menu(self._menu_option)

            if user_input.isdigit():
                # Checks if the user input is within the range of allowed options
                if int(user_input) in range(
                        1,
                        len(self._menu_option["options"]) + 1):
                    # Calls the corresponding method to call.
                    # For example user_input = 1 will call self._print_all_vacant()
                    self._menu_option["options"][list(
                        self._menu_option["options"].keys())[int(user_input) -
                                                             1]]()

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
    def _clear_console():
        """
        Clears the console.
        """
        os.system("cls" if os.name == "nt" else "clear")

    def _menu_user(self):
        """Menu for user related actions"""
        # Menu options
        self._menu_user_option = {
            "header": "User Menu",
            "description": "User correlated actions",
            "options": {
                "View all users": self._print_all_users,
                "Register new user": self._register_user,
                "Edit user": self._edit_user,
                "Unregister user": self._unregister_user,
            },
            "exit": self._menu_option["exit"],
        }
        while True:
            self.hotel._update_json()
            # Print menu and get input
            user_input = self._print_menu(self._menu_user_option)
            # Check if user wants to exit
            if user_input == self._menu_option["exit"]:
                break
            # Check if user input is valid
            if user_input.isdigit() and int(user_input) in range(
                    1,
                    len(self._menu_user_option) + 1):
                # Call the function associated with the option
                self._menu_user_option["options"][list(
                    self._menu_user_option["options"].keys())[int(user_input) -
                                                              1]]()
            else:
                print("Invalid input, try again.")

    def _menu_booking(self):
        """Menu for booking related actions"""
        # Menu options
        self._menu_booking_option = {
            "header": "Booking Menu",
            "description": "Booking correlated actions",
            "options": {
                "Add booking": self._add_booking,
                "Edit booking": self._edit_booking,
                "Remove booking": self._remove_booking,
                "View all bookings": self._print_all_bookings,
            },
            "exit": self._menu_option["exit"],
        }
        while True:
            self.hotel._update_json()
            # Print menu and get input
            user_input = self._print_menu(self._menu_booking_option)
            # Check if user wants to exit
            if user_input == self._menu_option["exit"]:
                break
            # Check if user input is valid
            if user_input.isdigit() and int(user_input) in range(
                    1,
                    len(self._menu_booking_option) + 1):
                # Call the function associated with the option
                self._menu_booking_option["options"][list(
                    self._menu_booking_option["options"].keys())[
                        int(user_input) - 1]]()
            else:
                print("Invalid input, try again.")

    def _menu_room(self):
        """Menu for room related actions"""
        # Menu options
        self._menu_room_option = {
            "header": "Room Menu",
            "description": "Room correlated actions",
            "options": {
                "Add room": self._add_room,
                "Edit room": self._edit_room,
                "Remove room": self._remove_room,
                "View all rooms": self._print_all_rooms,
            },
            "exit": self._menu_option["exit"],
        }
        while True:
            self.hotel._update_json()
            # Print menu and get input
            user_input = self._print_menu(self._menu_room_option)
            # Check if user wants to exit
            if user_input == self._menu_option["exit"]:
                break
            # Check if user input is valid
            if user_input.isdigit() and int(user_input) in range(
                    1,
                    len(self._menu_room_option) + 1):
                # Call the function associated with the option
                self._menu_room_option["options"][list(
                    self._menu_room_option["options"].keys())[int(user_input) -
                                                              1]]()
            else:
                print("Invalid input, try again.")

    def _print_menu(self,
                    menu: dict[str, Any],
                    noInput=False,
                    noClear=False) -> str:
        """Prints the menu and returns the user input"""
        # Print menu
        if not noClear:
            self._clear_console()
        print(menu["header"])
        print("=" * len(menu["header"]))
        print(menu["description"])
        print("-" * 15)
        for index, option in enumerate(menu["options"]):
            print(f"[{index+1}]: {option}")
        print(f"[{menu['exit']}]: Exit or return to top level menu")
        print()
        # Get user input
        if noInput:
            return ""
        return self._userInput("Please select an option: ")

    def _print_hotel_info(self):
        """
        Prints the hotel information.
        """
        self._clear_console()

        # Print menu header; hotel name
        print(self._menu_option["header"])
        print("=" * len(self._menu_option["header"]))
        # Prints the instance of the hotel, returns hotel information...
        print(self.hotel)
        self._userInput("Press enter to continue...")

    def _print_all_vacant(self):
        """
        Prints all vacant rooms.
        """
        # Gets all rooms that are vacant.
        self.vacant_rooms = self.hotel.filter_dict(self.hotel.rooms,
                                                   {"state": "vacant"})
        self._clear_console()
        print(self._menu_option["header"])
        print("=" * len(self._menu_option["header"]))
        print(f"There are {len(self.vacant_rooms)} vacant rooms")
        print("-" * 15)
        # Print out all room information here
        for room in self.vacant_rooms:
            print(f"Room Number:  {self.hotel.rooms.index(room)+1}")
            print(f"Type: {room['name']}")
            print(f"State: {room['state']}")
            print(f"Price: {room['price']}c")
            print(f"Capacity: {room['capacity']}")
            print(f"Description: {room['description']}")
            print(f"Features:", ", ".join(room["misc"]))
            print("-" * 15)
        self._userInput("Press enter to continue...")

    def _register_user(self):
        """
        Registers a new user.
        """
        self._clear_console()
        print(self._menu_option["header"])
        print("=" * len(self._menu_option["header"]))
        print("Register a new user")
        print("-" * 15)
        # Prompt user for input
        while True:
            while (userSSN :=
                   self._userInput("Enter your SSN (12 characters): ")
                   ) != self._menu_option["exit"]:
                if self.hotel.is_ssn_valid(userSSN):
                    break
                else:
                    self._userPrint(
                        "SSN is invalid, make sure its following format: YYYYMMDDXXXX"
                    )

            if userSSN == self._menu_option["exit"]:
                return

            if self.hotel.is_registered(userSSN):
                self._userPrint("User already registered")
                break
            elif self.hotel.been_registered(userSSN):
                self._userPrint(
                    "You have been registered before! Do you want to autofill the following information?"
                )
                name = self.hotel.old[userSSN]["name"]
                age = self.hotel.old[userSSN]["age"]

                autofill_msg = str("-" * 7 + "AUTOFILL INFORMATION" + "-" * 7)
                print(autofill_msg)
                self._userPrint(f"Name: {name}")
                self._userPrint(f"Age: {age}")
                print("-" * len(autofill_msg))

                while True:
                    userInput = self._userInput("(y/n): ")
                    if userInput == "y":
                        if type(result := self.hotel.register_user(
                                userSSN, name, age)) == bool:
                            return
                        else:
                            self._userPrint("Something went wrong:", result)
                            self._userInput(
                                "Press enter to enter name and age manually..."
                            )
                            break

                    elif userInput == "n":
                        break
                    else:
                        self._userPrint("Invalid input")

            while (userName := self._userInput("Enter your name: ")
                   ) != self._menu_option["exit"]:
                if userName:
                    break
                else:
                    self._userPrint(
                        "Name is invalid, make sure its following format: Firstname Lastname"
                    )

            if userName == self._menu_option["exit"]:
                return

            while (userAge := self._userInput("Enter your age: ")
                   ) != self._menu_option["exit"]:

                if userAge.isdigit():
                    break
                else:
                    self._userPrint(
                        "Age is invalid, make sure its a number only")

            if userAge == self._menu_option["exit"]:
                return

            if type(result := self.hotel.register_user(userSSN, userName,
                                                       userAge)) == bool:
                # Registered user if the result is a bool
                self._userPrint("User registered")
                self._userInput("Press enter to continue")
                return
            else:
                # Prints the error message
                self._userPrint(result)
                self._userInput("Press enter to continue...")
                return

        self._userInput("Press enter to continue...")

    def _edit_user(self):
        self._clear_console()
        print(self._menu_option["header"])
        print("=" * len(self._menu_option["header"]))
        print("Edit user")
        print("-" * 15)
        # Prompt user for input
        while not self.hotel.is_registered(
            (userSsn := self._userInput("Please enter your SSN: "))):
            if userSsn == self._menu_option["exit"]:
                return
            self._userInput(
                f"Invalid SSN (Make sure its 12 numbers and registered). Press enter to try again or {self._menu_option['exit']} to exit"
            )

        while True:
            name = self.hotel.users[userSsn]["name"]
            age = self.hotel.users[userSsn]["age"]
            self._clear_console()

            print("What to edit?")
            print("-" * 15)

            self._userPrint(f"SSN: {userSsn}")
            self._userPrint(f"Name: {name}")
            self._userPrint(f"Age: {age}")
            self._userPrint("-" * 15)
            self._userPrint("[1]: Change SSN")
            self._userPrint("[2]: Change name")
            self._userPrint("[3]: Change age")
            self._userPrint(f"[{self._menu_option['exit']}]: Exit")
            print()
            userInput = self._userInput("Please select an option: ")

            if userInput == self._menu_option["exit"]:
                return

            elif userInput == "1":
                while True:
                    newSsn = self._userInput("Enter new SSN: ")
                    if self.hotel.is_ssn_valid(newSsn):
                        break
                    else:
                        self._userPrint(
                            "SSN is invalid, make sure its following format: YYYYMMDDXXXX"
                        )
                if type(result := self.hotel.edit_user(
                        userSsn, new_ssn=newSsn)) == bool:
                    self._userPrint("SSN changed")
                    self._userInput("Press enter to continue...")
                    return
                else:
                    self._userPrint(result)
                    self._userInput("Press enter to continue...")
                    return

            elif userInput == "2":
                while True:
                    newName = self._userInput("Enter new name: ")
                    if newName:
                        break
                    else:
                        self._userPrint(
                            "Name is invalid, make sure its following format: Firstname Lastname OR Firstname"
                        )
                if self.hotel.edit_user(userSsn, name=newName):
                    self._userPrint("Name changed")
                else:
                    self._userPrint("Name change failed")

                self._userInput("Press enter to continue...")

            elif userInput == "3":
                while True:
                    newAge = self._userInput("Enter new age: ")
                    if newAge.isdigit():
                        break
                    else:
                        self._userPrint(
                            "Age is invalid, make sure its a number")
                if self.hotel.edit_user(userSsn, age=newAge):
                    self._userPrint("Age changed")
                else:
                    self._userPrint("Age change failed")

                self._userInput("Press enter to continue...")
        ...

    def _unregister_user(self):
        self._clear_console()
        print(self._menu_option["header"])
        print("=" * len(self._menu_option["header"]))
        print("Unregister a user")
        print("-" * 15)
        # Prompt user for input
        while True:
            while (userSSN :=
                   self._userInput("Enter your SSN (12 characters): ")
                   ) != self._menu_option["exit"]:
                if self.hotel.is_ssn_valid(userSSN):
                    # Checks if the SSN is valid
                    self._userPrint("SSN is valid")
                    break
                else:
                    self._userPrint(
                        "SSN is invalid, make sure its following format: YYYYMMDDXXXX"
                    )

            if userSSN == self._menu_option["exit"]:
                break

            if type(result := self.hotel.unregister_user(userSSN)) == bool:
                # Unregistered user if the result is a bool
                self._userPrint("User unregistered")
            else:
                # Prints the error message
                self._userPrint(result)
            self._userInput("Press enter to continue")
            break

    def _print_all_users(self):
        self._clear_console()
        print(self._menu_option["header"])
        print("=" * len(self._menu_option["header"]))
        print("All users")
        print("-" * 15)
        # Print out all user information here
        for index, (k, v) in enumerate(self.hotel.users.items()):
            print(f"User {index+1}:")
            print("SSN:", k)
            print("Name:", v["name"])
            print("Age:", v["age"])
            print("-" * 15)

        self._userInput("Press enter to continue...")

    def _add_booking(self):
        self._clear_console()
        print(self._menu_option["header"])
        print("=" * len(self._menu_option["header"]))
        print("Add a new booking")
        print("-" * 15)

        # Prompt user for input until valid input is registered.
        while not self.hotel.is_registered(
            (userSsn := self._userInput("Please enter your SSN: "))):
            if userSsn == self._menu_option["exit"]:
                return
            self._userInput(
                f"Invalid SSN (Make sure its 12 numbers and registered). Press enter to try again or {self._menu_option['exit']} to exit"
            )

        # Check if already booked:
        if self.hotel.is_booked(userSsn):
            self._userInput(
                f"You already have a booking. Press enter to continue")
            return

        while True:
            self._userPrint(
                "Enter a room number or 'rooms' to see all vacant rooms")
            userRoom = self._userInput("Enter your choice: ")
            if userRoom == self._menu_option["exit"]:
                return

            if userRoom == "rooms":
                self._print_all_vacant()

            elif userRoom.isdigit() and int(userRoom) in range(
                    1,
                    len(self.hotel.rooms) + 1):
                # Lowers the number by one step (index starts at 0)
                break
            else:
                self._userInput(
                    f"Invalid room number. Press enter to try again or {self._menu_option['exit']} to exit"
                )

        while True:
            # Prompt user if they want to add message to staff.
            userMessage = self._userInput(
                "Do you want to add a message to the staff? (y/n): ")
            if userMessage == self._menu_option["exit"]:
                return
            if userMessage.lower() in ["y", "n"]:
                break
            else:
                self._userInput(
                    f"Invalid input. Press enter to try again or {self._menu_option['exit']} to exit"
                )

        # If user wants to add message to staff, prompt for message.
        if userMessage.lower() == "y":
            while True:
                userMessage = self._userInput("Please enter your message: ")
                if userMessage == self._menu_option["exit"]:
                    return
                if userMessage:
                    break
                else:
                    self._userInput(
                        f"Invalid message. Press enter to try again or {self._menu_option['exit']} to exit"
                    )
        else:
            userMessage = ""

        if self.hotel.add_booking(userSsn, userRoom, userMessage):
            self._userPrint("Booking successful!")
        else:
            self._userPrint(
                "Booking failed! (Make sure room is vacant and its the right number)"
            )
        self._userInput("Press enter to continue...")

    def _remove_booking(self):
        self._clear_console()
        print(self._menu_option["header"])
        print("=" * len(self._menu_option["header"]))
        print("Remove a booking")
        print("-" * 15)

        # Prompt user for input until valid input is registered.
        while not self.hotel.is_registered(
            (userSsn := self._userInput("Please enter your SSN: "))):
            if userSsn == self._menu_option["exit"]:
                return
            self._userInput(
                f"Invalid SSN (Make sure its 12 numbers and registered). Press enter to try again or {self._menu_option['exit']} to exit"
            )

        while True:
            userUnregister = self._userInput(
                "Do you want to unregister the user? (y/n): ")
            if userUnregister == self._menu_option["exit"]:
                return
            if userUnregister.lower() in ["y", "n"]:
                break
            else:
                self._userInput(
                    f"Invalid input. Press enter to try again or {self._menu_option['exit']} to exit"
                )

        if userUnregister.lower() == "y":
            userUnregister = True
        else:
            userUnregister = False

        if self.hotel.remove_booking(userSsn, userUnregister):
            self._userPrint("Booking removed!")
        else:
            self._userPrint("Un-booking failed!, contact an admin")

        self._userInput("Press enter to continue...")
        return

    def _edit_booking(self):
        self._clear_console()
        print(self._menu_option["header"])
        print("=" * len(self._menu_option["header"]))
        print("Edit a booking")
        print("-" * 15)

        # Prompt user for input until valid input is registered.
        while not self.hotel.is_registered(
            (userSsn := self._userInput("Please enter your SSN: "))):
            if userSsn == self._menu_option["exit"]:
                return
            self._userInput(
                f"Invalid SSN (Make sure its 12 numbers and registered). Press enter to try again or {self._menu_option['exit']} to exit"
            )

        while True:
            booked_room = self.hotel.active[userSsn]["room"]
            message = self.hotel.rooms[int(booked_room) - 1]["message"]
            self._clear_console()

            print("What to edit?")
            print("-" * 15)
            self._userPrint(f"You are currently booked in room {booked_room}")
            self._userPrint(f"You provided the following message: {message}")
            print("-" * 15)
            self._userPrint("[1]: Change message")
            self._userPrint("[2]: Change room")
            self._userPrint(f"[{self._menu_option['exit']}]: Exit")

            userChoice = self._userInput("Enter your choice: ")
            if userChoice == self._menu_option["exit"]:
                return

            if userChoice == "1":
                print("-" * 15)
                self._userPrint("Current message:", message)
                print("-" * 15)
                userMessage = self._userInput("New message: ")
                if userMessage == self._menu_option["exit"]:
                    return
                if self.hotel.edit_booking(userSsn, message=userMessage):
                    self._userPrint("Message changed!")
                else:
                    self._userPrint("Message change failed!")
                    self._userInput("Press enter to continue...")

            elif userChoice == "2":
                while True:
                    print("-" * 15)
                    self._userPrint("Current room:", booked_room)
                    self._userPrint(
                        "Enter [rooms] to see all vacant rooms to book")
                    print("-" * 15)
                    userRoom = self._userInput("New room: ")
                    if userRoom == self._menu_option["exit"]:
                        return

                    if userRoom == "rooms":
                        self._print_all_vacant()
                        continue

                    elif self.hotel.edit_booking(userSsn, new_room=userRoom):
                        self._userPrint("Room changed!")
                        break
                    else:
                        self._userPrint("Room change failed!")
                        self._userInput("Press enter to continue...")

    def _print_all_bookings(self):
        self._clear_console()
        print(self._menu_option["header"])
        print("=" * len(self._menu_option["header"]))
        print("All bookings")
        print("-" * 15)
        # Print out all user information here
        for index, (k, v) in enumerate(self.hotel.active.items()):
            print(f"Booking {index+1}:")
            print("SSN:", k)
            print("Room:", v["room"])
            print("Message:", self.hotel.rooms[int(v["room"]) - 1]["message"])
            print("-" * 15)

        self._userInput("Press enter to continue...")

    def _add_room(self):
        self._clear_console()
        print(self._menu_option["header"])
        print("=" * len(self._menu_option["header"]))
        print("Add a room")
        print("-" * 15)

        # Prompt the user to enter following required information
        # name: str, price: str, capacity: str, state: str, description: str, misc: list[str]
        while True:
            userName = self._userInput("Please enter the name of the room: ")
            if userName == self._menu_option["exit"]:
                return
            if userName:
                break
            else:
                self._userInput(
                    f"Invalid name. Press enter to try again or {self._menu_option['exit']} to exit"
                )

        while True:
            userPrice = self._userInput("Please enter the price of the room: ")
            if userPrice == self._menu_option["exit"]:
                return

            if userPrice:
                # Test if float (199.99 is allowed pricing, but isdigit() returns false)):
                try:
                    float(userPrice)
                except ValueError:
                    self._userInput(
                        f"Invalid price. Press enter to try again or {self._menu_option['exit']} to exit"
                    )
                else:
                    # On no exception

                    # Checks if the price is of digits (NaN is float and etc.)
                    if userPrice.replace(".", "").isdigit():
                        break
                    else:
                        self._userInput(
                            f"Invalid price. Press enter to try again or {self._menu_option['exit']} to exit"
                        )

            else:
                self._userInput(
                    f"Invalid price. Press enter to try again or {self._menu_option['exit']} to exit"
                )

        while True:
            userCapacity = self._userInput(
                "Please enter the capacity of the room: ")
            if userCapacity == self._menu_option["exit"]:
                return
            if userCapacity.isdigit():
                break
            else:
                self._userInput(
                    f"Invalid capacity. Press enter to try again or {self._menu_option['exit']} to exit"
                )

        while True:
            userState = self._userInput("Please enter the state of the room: ")
            if userState == self._menu_option["exit"]:
                return
            if userState:
                break
            else:
                self._userInput(
                    f"Invalid state. Press enter to try again or {self._menu_option['exit']} to exit"
                )

        while True:
            userDescription = self._userInput(
                "Please enter the description of the room: ")
            if userDescription == self._menu_option["exit"]:
                return
            if userDescription:
                break
            else:
                self._userInput(
                    f"Invalid description. Press enter to try again or {self._menu_option['exit']} to exit"
                )

        userMisc = []
        while True:
            userInput = self._userInput(
                "Enter miscellaneous information (leave empty to continue): ")
            if userInput == self._menu_option["exit"]:
                return
            if userInput:
                userMisc.append(userInput)
            else:
                break

        if self.hotel.add_room(userName, userPrice, userCapacity, userState,
                               userDescription, userMisc):
            self._userPrint("Room added!")
        else:
            self._userPrint("Room addition failed!")

        self._userInput("Press enter to continue...")

    def _remove_room(self):
        self._clear_console()
        print(self._menu_option["header"])
        print("=" * len(self._menu_option["header"]))
        print("Remove a room")
        print("-" * 15)

        # Print all rooms, and prompt user to enter room number, confirm with room name
        self._userPrint(
            "All rooms will first be displayed, please note which room number for removal."
        )
        self._userInput("Press enter to continue...")
        self._print_all_rooms()

        while True:
            userNumber = self._userInput("Chose room number: ")
            if userNumber == self._menu_option["exit"]:
                return
            if userNumber.isdigit():
                break
            else:
                self._userInput(
                    f"Invalid room number. Press enter to try again or {self._menu_option['exit']} to exit"
                )

        room = self.hotel.rooms[int(userNumber) - 1]
        roomName = room["name"]

        while True:
            userName = self._userInput(f"Enter [{roomName}] to confirm: ")
            if userName == self._menu_option["exit"]:
                return
            if userName == roomName:
                break
            else:
                self._userInput(
                    f"Invalid room name. Press enter to try again or {self._menu_option['exit']} to exit"
                )

        if self.hotel.remove_room(userNumber):
            self._userPrint("Room removed!")
        else:
            self._userPrint("Room removal failed!")

        self._userInput("Press enter to continue...")

    def _edit_room(self):
        self._clear_console()
        print(self._menu_option["header"])
        print("=" * len(self._menu_option["header"]))
        print("Edit a room")
        print("-" * 15)

        self._userPrint(
            "All rooms will first be displayed, please note which room number for edit."
        )
        self._userInput("Press enter to continue...")
        self._print_all_rooms()

        while True:
            userNumber = self._userInput("Chose room number: ")
            if userNumber == self._menu_option["exit"]:
                return
            if userNumber.isdigit():
                break
            else:
                self._userInput(
                    f"Invalid room number. Press enter to try again or {self._menu_option['exit']} to exit"
                )

        room = self.hotel.rooms[int(userNumber) - 1]
        roomName = room["name"]

        while True:
            userName = self._userInput(f"Enter [{roomName}] to confirm: ")
            if userName == self._menu_option["exit"]:
                return
            if userName == roomName:
                break
            else:
                self._userInput(
                    f"Invalid room name. Press enter to try again or {self._menu_option['exit']} to exit"
                )

        while True:
            self._clear_console()
            print(self._menu_option["header"])
            print("=" * len(self._menu_option["header"]))
            print("Edit a room")
            print("-" * 15)
            print(f"Editing room: {userNumber} - {room['name']}")
            print("With following current Information:")
            print("-" * 15)
            for index, info in enumerate(room):
                # Exclude keys, user and message
                if info not in ["user", "message", "state"]:
                    self._userPrint(f"[{index+1}] {info}: {room[info]}")
            self._userPrint(f"[{self._menu_option['exit']}]: Exit")
            print("-" * 15)
            print()

            userChoice = self._userInput("Enter your choice: ")
            if userChoice == self._menu_option["exit"]:
                return

            if userChoice.isdigit():
                userChoice = int(userChoice) - 1
                if userChoice in range(len(room)):
                    userInput = self._userInput(
                        f"Enter new {list(room.keys())[userChoice]}: ")
                    # userInput = self._userInput(
                    #     f"Enter new {room[list(room.keys())[userChoice]]}: ")
                    if userInput == self._menu_option["exit"]:
                        pass
                    else:
                        room[list(room.keys())[userChoice]] = userInput
                else:
                    self._userInput(
                        f"Invalid choice. Press enter to try again or {self._menu_option['exit']} to exit"
                    )

            else:
                self._userInput(
                    f"Invalid choice. Press enter to try again or {self._menu_option['exit']} to exit"
                )

    def _print_all_rooms(self):
        self._clear_console()
        print(self._menu_option["header"])
        print("=" * len(self._menu_option["header"]))
        print("All Rooms")
        print("-" * 15)

        for index, room in enumerate(self.hotel.rooms):
            print(f"Room: {index+1}:")
            print(f"Name: {room['name']}")
            print(f"Price: {room['price']}")
            print(f"Capacity: {room['capacity']}")
            print(f"State: {room['state']}")
            print(f"Description: {room['description']}")
            print(f"Miscellaneous: {', '.join(room['misc'])}")
            print(f"User: {room['user']}")
            print(f"Message: {room['message']}")
            print("-" * 15)

        self._userInput("Press enter to continue...")

    def _check_in(self):
        self._clear_console()
        print(self._menu_option["header"])
        print("=" * len(self._menu_option["header"]))
        print("Check in")
        print("-" * 15)

        # Prompt user for input until valid input is registered.
        while not self.hotel.is_registered(
            (userSsn := self._userInput("Please enter your SSN: "))):
            if userSsn == self._menu_option["exit"]:
                return
            self._userInput(
                f"Invalid SSN (Make sure its 12 numbers and registered). Press enter to try again or {self._menu_option['exit']} to exit"
            )

        if self.hotel.check_in(userSsn):
            self._userPrint("Check in successful!")

        else:
            self._userPrint("Check in failed!")

        self._userInput("Press enter to continue...")

    def _check_out(self):
        self._clear_console()
        print(self._menu_option["header"])
        print("=" * len(self._menu_option["header"]))
        print("Check out")
        print("-" * 15)

        # Prompt user for input until valid input is registered.
        while not self.hotel.is_registered(
            (userSsn := self._userInput("Please enter your SSN: "))):
            if userSsn == self._menu_option["exit"]:
                return
            self._userInput(
                f"Invalid SSN (Make sure its 12 numbers and registered). Press enter to try again or {self._menu_option['exit']} to exit"
            )

        # Prompt user about un-registration on checkout.
        while True:
            userUnregister = self._userInput(
                "Do you want to unregister the user? (y/n): ")
            if userUnregister == self._menu_option["exit"]:
                return
            if userUnregister.lower() in ["y", "n"]:
                break
            else:
                self._userInput(
                    f"Invalid input. Press enter to try again or {self._menu_option['exit']} to exit"
                )

        if userUnregister.lower() == "y":
            userUnregister = True
        else:
            userUnregister = False

        if self.hotel.check_out(userSsn, userUnregister):
            self._userPrint("Check out successful!")

        else:
            self._userPrint("Check out failed!")

        self._userInput("Press enter to continue...")


def _main():
    """
    Main function. Used for testing and running the application
    """
    # Initialize an object of the class
    while True:
        while True:
            userChoice = input("Do you want to start the hotel? (y/n): ")
            if userChoice.lower() in ["y", "n"]:
                break
            else:
                print("Invalid input!")

        # Start the hotel
        if "y" == userChoice.lower():
            test_hotel = HotelManager()

            # Initialize an object of the class
            test_console = ConsoleHotel(test_hotel)

            # Runs the interface
            test_console.run()

        else:
            return


if __name__ == "__main__":
    _main()
