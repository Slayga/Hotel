"""
Name: Gabriel Engberg
Date: 02-03-2022
Info:
Keep track of how to handle certain issues and 
example solutions//general direction to the solution.

Quick TL:DR:
        1. Use context manager to write and read json.
        2. Always have the keys in the dict being of type string.
        3. Always make sure to have at least an empty dict in the json file.
            (If you read an empty json file the program will crash...)

"""
import json
import imgui
import os

# Note: That path is just to get the exact path to the working directory.
path = os.path.dirname(__file__)
# Create folder "json" in the current working directory.
if not os.path.exists(path + "\\json"):
    os.makedirs(path + "\\json", exist_ok=True)


def test_basic_json():
    """
    Basics for writing and reading json files.

    Returns:
        None: None
    """
    import json  # required...

    # Data to store
    dict_data = {"name": "bob", "misc": {"1": [1, 2, 3, 4]}}

    # ? Writing data with context manager // will automatically close file... f.close(), '(__exit__)'
    with open(path + "/json/test_example.json", "w") as f:
        # Always have keys as strings ({"1": 1}) and avoid int ({1: 1}):
        json.dump(dict_data, f)  # dumps the data into the file...
        # ! note the mode in open("...", "w") -> "w" will overwrite the file. Not append to it

    # ? Reading data with context manager...
    # No need to pass mode in open() as default is "r" (read)
    with open(path + "/json/test_example.json") as f:
        json_content = json.load(f)  # json.load(<file>) will return the dict

    # Fact check the results from the read (json.load(f))...
    print(json_content, type(json_content))


def test_empty_json():
    import json

    # Write an empty dict to not crash when reading json...
    with open(path + "/json/test_empty.json", "w") as f:
        json.dump({}, f)

    with open(path + "/json/test_empty.json") as f:
        empty_json = json.load(f)

    print(empty_json)


def test_writing_json():
    # Below is acceptable way to store & write json
    dict_str_key = {str(): int()}
    # While this will be converted by json.dump(...) to dict_str_key
    dict_int_key = {int(): int()}

    with open(path + "/json/test_write_str_key.json", "w") as f:
        json.dump(dict_str_key, f)

    with open(path + "/json/test_write_int_key.json", "w") as f:
        json.dump(dict_int_key, f)


if __name__ == "__main__":
    # 1
    test_basic_json()
    # 2
    test_writing_json()
    # 3
    test_empty_json()
    ...
