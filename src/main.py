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
    def __init__(self, path: str):
        # This should stay constant(private) throughout the lifetime of the program.
        # I dunno rly setter doesn't get called otherwise...
        self._path = self.path = path
        print(self.path)
        if not self.__file_exists():
            # TODO Check if folder exist or not /json/hotel.json
            self.__create_file()

    @property
    def path(self) -> str:
        """Property for path"""
        return self._path

    @path.setter
    def path(self, value: str):
        """Setter for path"""
        # Instead of raising an exception on 'empty path' a fallback exists.
        self.__fallback = "hotel.json"
        if value:
            if value.endswith(".json"):
                self._path = value
            else:
                self._path = value + "/" + self.__fallback
        else:
            self._path = self.__fallback

    def __file_exists(self) -> bool:
        return os.path.exists(self._path)

    def __create_file(self):
        with open(str(self.path), "w") as f:
            json.dump({}, f)

    def pack_data(self, data: dict, mode: str = "w") -> bool:
        with open(self.path, mode) as f:
            json.dump(data, f)

    def unpack_data(self) -> dict:
        try:
            with open(self.path) as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError("Unresolved file error:", self.path)


class HotelManager:
    def __init__(self, path: str = "/json"):
        self.data_handler = DataHandling(path)
        self.data = self.data_handler.unpack_data()

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


class GuiHotel:
    ...


if __name__ == "__main__":
    HotelManager()
