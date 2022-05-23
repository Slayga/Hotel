Module hotel
============
Project: Hotel managment system 

Name: Gabriel Engberg, Viggo Rubin 

Date: 28-02-2022 

Info: Main running file for hotel application. 

This is in theory meant to be used by personal at a given hotel, 
hence the management of seeing SSN easily.

Classes
-------

`ConsoleHotel(hotel: hotel.HotelManager)`
:   Normal console (print) implementation
    
    Initializes the hotel object that it will connect to
    
    Expected Args:
        hotel (HotelManager): HotelManager object

    ### Ancestors (in MRO)

    * hotel.HotelInterface

    ### Static methods

    `clear_console()`
    :   Clears the console.

    ### Methods

    `run(self)`
    :   Runs the interface. Prints the menu and waits for user input
        and call respective function, until opted to exit

`GuiHotel()`
:   All classes that "connect" to the hotel is derived from HotelInterface.
    An abstract class that predefines implementations requirements.
    
    Initializes the hotel object that it will connect to
    
    Expected Args:
        hotel (HotelManager): HotelManager object

    ### Ancestors (in MRO)

    * hotel.HotelInterface

`HotelInterface()`
:   All classes that "connect" to the hotel is derived from HotelInterface.
    An abstract class that predefines implementations requirements.
    
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

`HotelManager(filename: str = '')`
:   Class for managing a hotel database system.
    Used to manipulate json data from given file that class JsonHandling returns
    when unpacking.
    
    HotelManager uses methods for: checking in, checking out,
    adding bookings, removing bookings, editing bookings, adding rooms,
    removing rooms, editing rooms, register users, unregister users and printing raw json_data.
    
    Constructor for HotelManager
    
    Args:
        filename (str, optional): Optional argument for the name of the file. Defaults to "".

    ### Methods

    `add_booking(self, ssn: str, room: str) ‑> bool`
    :   Called when user is booking a room. Must be registered to add booking.
        
        Args:
            ssn (str): ssn of user
        
            room (str): room number(digits): "1", "2", "3" etc.
        
        Returns:
            bool: Boolean on success or failure

    `add_room(self, name: str, price: str, capacity: str, state: str, description: str, misc: list) ‑> bool`
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

    `check_in(self, ssn: str) ‑> bool`
    :   Called when user is trying to check in to hotel
        
        Args:
            ssn (str): ssn of user wanting to check in
        
        Returns:
            bool: Boolean on success or failure

    `check_out(self, ssn: str) ‑> bool`
    :   Called when user is trying to check out to hotel
        
        Args:
            ssn (str): ssn of user wanting to check out
        
        Returns:
            bool: Boolean on success or failure

    `edit_booking(self)`
    :

    `edit_room(self)`
    :

    `filter_dict(self, data: Collection[dict], filter_: dict | None = None, inverted: bool = False) ‑> Union[list[dict], Collection[dict]]`
    :   Returns a list of all filtered matches depending on given filter
        
        Args:
            filter_ (dict, optional): A dict of len == 1 where the key is going to be
                                    matched with similar key and also compare value to value.
                                    Defaults to None.
        
            inverted (bool, optional): Ability to invert results. Defaults to False.
        
        Returns:
            list[dict] | list: A list of filtered matches or all the matches if no filter is given.

    `is_registered(self, ssn: str) ‑> bool`
    :   Returns a boolean depending on whether a user is registered or not.
        
        Args:
            ssn (str): SSN of user
        
        Returns:
            bool: True if a user is registered, False otherwise

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
    :   Called when user is removing a booking. Must be registered to remove booking.
        
        Args:
            ssn (str): ssn of user
        
            room (str): room number(digits): "1", "2", "3" etc.
        
        Returns:
            bool: Boolean on success or failure

    `remove_room(self)`
    :

    `unregister_user(self, ssn) ‑> str | bool`
    :   Unregister a user from the HotelManager.
        Will return a string or boolean depending on success.
        (Type check for the str or bool)
        
        Args:
            ssn (str): string of 12 characters representing a user's social security number
        
        Returns:
            str | bool: str on failure, boolean(True) on success

`JsonHandling(filename: str = 'hotel.json')`
:   Class for handling json data from json files
    
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
:   All classes that "connect" to the hotel is derived from HotelInterface.
    An abstract class that predefines implementations requirements.
    
    Initializes the hotel object that it will connect to
    
    Expected Args:
        hotel (HotelManager): HotelManager object

    ### Ancestors (in MRO)

    * hotel.HotelInterface