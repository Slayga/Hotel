# Module hotel

Project: Hotel management system

Name: Gabriel Engberg, Viggo Rubin

Date: 28-02-2022

Info: Main running file for hotel application.

This is in theory meant to be used by personal at a given hotel,
hence the management of seeing SSN easily.

## Classes

`ConsoleHotel(hotel: hotel.HotelManager)`
: ConsoleHotel is a console based interface for the hotel.

    Constructor for the ConsoleHotel object. Initializes the hotel object that it will connect to.

    Args:
        hotel (HotelManager): hotel object

    ### Ancestors (in MRO)

    * hotel.HotelInterface

    ### Methods

    `run(self)`
    :   Runs the interface. Prints the menu and waits for user input
        and call respective function, until opted to exit

`GuiHotel()`
: All classes that "connect" to the hotel is derived from HotelInterface.
An abstract class that predefined implementations requirements.

    Initializes the hotel object that it will connect to

    Expected Args:
        hotel (HotelManager): HotelManager object

    ### Ancestors (in MRO)

    * hotel.HotelInterface

`HotelInterface()`
: All classes that "connect" to the hotel is derived from HotelInterface.
An abstract class that predefined implementations requirements.

    Initializes the hotel object that it will connect to

    Expected Args:
        hotel (HotelManager): HotelManager object

    ### Descendants

    * hotel.ConsoleHotel
    * hotel.GuiHotel
    * hotel.WebHotel

    ### Methods

    `run(self)`
    :   Implement the run method to start the interface.
        TL:DR; Talk to the self.hotel object

`HotelManager(filename: str = '')`
: Class for managing a hotel database system.
Used to manipulate json data from given file that class JsonHandling returns
when unpacking.

    HotelManager uses methods for: checking in, checking out,
    adding bookings, removing bookings, editing bookings, adding rooms,
    removing rooms, editing rooms, register users, unregister users and printing raw json_data.

    Constructor for HotelManager

    Args:
        filename (str, optional): Optional argument for the name of the file. Defaults to "".

    ### Methods

    `add_booking(self, ssn: str, room: str, message: str = '') ‑> bool`
    :   Called when user is booking a room. Must be registered to add booking.

        Args:
            ssn (str): ssn of user

            room (str): room number(digits): "1", "2", "3" etc.
            message (str, optional): message from user. Defaults to "".
            _override_is_booked (bool, optional): Overrides the check for already book
            (use with precaution). Defaults to False.

        Returns:
            bool: Boolean on success or failure

    `add_room(self, name: str, price: str, capacity: str, state: str, description: str, misc: list[str]) ‑> bool`
    :   Adds a room to the hotel.

        Args:
            name (str): Name of the room, example: JuniorSuite

            price (str): Price per night, example: 19.99

            capacity (str): How many can fit? example: 2

            state (str): State of the room, example: vacant or occupied

            description (str): A short description, who its fitted for

            misc (list[str]): list of additional information, example: wifi, type of bed, etc.


        Returns:
            bool: True if operation was successful, False otherwise

    `been_registered(self, ssn: str) ‑> bool`
    :   Checks if a user has been registered.

        Args:
            ssn (str): string of 12 characters representing a user's social security number

        Returns:
            bool: True if user is registered, False if not

    `check_in(self, ssn: str) ‑> bool`
    :   Called when user is trying to check in to hotel

        Args:
            ssn (str): ssn of user wanting to check in

        Returns:
            bool: Boolean on success or failure

    `check_out(self, ssn: str, unregister: bool) ‑> bool`
    :   Called when user is trying to check out to hotel

        Args:
            ssn (str): ssn of user wanting to check out
            unregister (bool): Boolean on whether to unregister user or not

        Returns:
            bool: Boolean on success or failure

    `edit_booking(self, ssn: str, new_room: str = '', message: str = '')`
    :   Called when user is trying to edit a booking. Must be registered to edit booking.

        Args:
            ssn (str): SSN of user
            new_room (str, optional): If wished to swap room. Defaults to "".
            message (str, optional): Messages, can be passed alone or with new_room. Defaults to "".

        Returns:
            bool: True if successful, False otherwise

    `edit_room(self, room_id: str, name: str = '', price: str = '', capacity: str = '', state: str = '', description: str = '', misc: list[str] = [])`
    :   Edits a room in the hotel. Only the fields that are not empty will change.

        Args:
            room_id (_type_): Room ID (index in room list + 1)
            name (str): Name of the room, example: JuniorSuite

            price (str): Price per night, example: 19.99

            capacity (str): How many can fit? example: 2

            state (str): State of the room, example: vacant or occupied

            description (str): A short description, who its fitted for

            misc (list[str]): list of additional information, example: wifi, type of bed, etc.

    `edit_user(self, ssn: str, name: str = '', age: str = '', new_ssn: str = '') ‑> bool`
    :   Edits a user's information.

        Args:
            ssn (str): SSN of the CURRENTLY registered user, provide new_ssn to edit this
            name (str, optional): New name. Defaults to "".
            age (str, optional): New age. Defaults to "".
            new_ssn (str, optional): New ssn. Defaults to "".

        Returns:
            bool: True on success, False otherwise

    `filter_dict(self, data: Collection[dict], filter_: dict | None = None, inverted: bool = False) ‑> Union[list[dict], Collection[dict]]`
    :   Returns a list of all filtered matches depending on given filter

        Args:
            filter_ (dict, optional): A dict of len == 1 where the key is going to be
                                    matched with similar key and also compare value to value.
                                    Defaults to None.

            inverted (bool, optional): Ability to invert results. Defaults to False.

        Returns:
            list[dict] | list: A list of filtered matches or all the matches if no filter is given.

    `is_booked(self, ssn: str) ‑> bool`
    :   Returns a boolean depending on whether a user is booked or not.

        Args:
            ssn (str): SSN of user

        Returns:
            bool: True if a user is booked, False otherwise

    `is_registered(self, ssn: str) ‑> bool`
    :   Returns a boolean depending on whether a user is registered or not.

        Args:
            ssn (str): SSN of user

        Returns:
            bool: True if a user is registered, False otherwise

    `is_ssn_valid(self, ssn: str) ‑> bool`
    :   Evaluate if ssn is valid

        Args:
            ssn (str): Social security number.

        Returns:
            bool: True on success, False otherwise

    `register_user(self, ssn: str, name: str, age: str) ‑> str | bool`
    :   Registers a user to the HotelManager.
        Will return a string or boolean depending on success.
        (Type check for the str or bool)

        Args:
            ssn (str): string of 12 characters representing a user's social security number
            name (str): name of given user
            age (str): age of given user

        Returns:
            str | bool: str on failure, boolean(True) on success

    `remove_booking(self, ssn: str, unregister: bool) ‑> bool`
    :   Called when user is trying to remove a booking. Must be registered to remove booking.

        Args:
            ssn (str): _description_
            unregister (bool): unregister the user when removing booking

        Returns:
            bool: _description_

    `remove_room(self, room_nr: str) ‑> bool`
    :   Removes a room from the hotel.

        Args:
            room_nr (str): Room nr (index in room list + 1)

        Returns:
            bool: True if operation was successful, False otherwise

    `unregister_user(self, ssn: str) ‑> str | bool`
    :   Unregister a user from the HotelManager.
        Will return a string or boolean depending on success.

        Args:
            ssn (str): string of 12 characters representing a user's social security number

        Returns:
            str | bool: str on failure, boolean(True) on success

`JsonHandling(filename: str = 'hotel.json')`
: Class for handling json data from json files

    Constructor for JsonHandling

    Args:
        filename (str, optional): Name of the file to be used. Defaults to hotel.json.

    ### Instance variables

    `filename: str`
    :   Property for filename

    `folder: str`
    :   Property for folder

    `path: str`
    :   Property for path

    `setter: str`
    :   Property for path

    ### Methods

    `pack_data(self, json_data: dict, mode: str = 'w')`
    :   Writes json data to a json file

        Args:
            json_data (dict): data to be stored in json file,
                        #! NOTE that all keys must be of type str
            mode (str, optional): Mode the file will be open in. Defaults to "w".

    `unpack_data(self) ‑> dict`
    :   Opens json file and returns the data structure as a dictionary

        Returns:
            dict: data stored in json file as a dictionary.

`WebHotel()`
: All classes that "connect" to the hotel is derived from HotelInterface.
An abstract class that predefined implementations requirements.

    Initializes the hotel object that it will connect to

    Expected Args:
        hotel (HotelManager): HotelManager object

    ### Ancestors (in MRO)

    * hotel.HotelInterface
